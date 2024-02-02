import os, logging
from pandas import isna
from typing import Optional
from PySide6.QtWidgets import (
    QFileDialog,
    QApplication,
    QTabBar,
    QMessageBox,
    QLineEdit,
    QScrollArea,
)
from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QImage, QPainter, QFont, QPixmap, QPen, QColor, QBrush
from Views.image_view import ImageView
from Views.Widgets.progressbar import ProgressBar
from Models.text_item import *


class ProjetController(QObject):
    def __init__(self, mainWindow, tabWidget):
        self.mainWindow = mainWindow
        self.tabWidget = tabWidget

    def creerNouveauProjet(
        self, largeur: int, hauteur: int, tabTitle: str = "Sans Titre"
    ) -> None:
        imageView = ImageView(self.mainWindow, largeur, hauteur)
        imageView.creerImageVide(largeur, hauteur)
        scrollArea = self.creerScroll(imageView)

        indexNouvelOnglet = self.tabWidget.addTab(scrollArea, tabTitle)
        self.tabWidget.setCurrentIndex(indexNouvelOnglet)
        self.mainWindow.imageViewActif = imageView

    def creerScroll(self, widget: ImageView) -> QScrollArea:
        scrollArea = QScrollArea()
        scrollArea.setWidget(widget)
        scrollArea.setWidgetResizable(True)
        return scrollArea

    def exporterProjet(self, imageView: ImageView) -> None:
        try:
            imageView = self.mainWindow.getActiveImageView()
            if imageView is None:
                if imageView is None:
                    QMessageBox.warning(
                        self.mainWindow,
                        "Avertissement",
                        "Aucun projet actif pour l'exportation.",
                    )
                    return

                if not self.validerImageView(imageView):
                    return

            dossierExport = self.selectionnerDossierExport()
            if not dossierExport:
                return

            self.preparerExport(imageView, dossierExport)
        except Exception as e:
            logging.error(
                f"Erreur lors de l'exportation du projet \n {e}", exc_info=True
            )
            QMessageBox.critical(
                None,
                "Erreur d'Exportation",
                f"Une erreur inattendue est survenue lors de l'exportation : \n {e}.",
            )

    def validerImageView(self, imageView: ImageView) -> bool:
        if imageView is None or not imageView.items:
            QMessageBox.warning(
                None,
                "Attention",
                "Aucune image à exporter ou aucun élément de texte ajouté.",
            )
            return False
        return True

    def selectionnerDossierExport(self) -> Optional[str]:
        dossier = QFileDialog.getExistingDirectory(
            None, "Sélectionner un dossier d'export"
        )
        if not dossier:
            return None
        dossierFinal = os.path.join(dossier, "ProjetExport")
        if not os.path.exists(dossierFinal):
            os.makedirs(dossierFinal)
        return dossierFinal

    def définirNombresLignes(self, textColonneteItems, imageColonneItem) -> int:
        """
        Détermine le nombre total de lignes basé sur les éléments de texte et d'image.

        :param textColonneteItems: Liste des éléments de texte.
        :param imageColonneItem: Liste des éléments d'image.
        :return: Le nombre total de lignes nécessaire pour afficher tous les éléments.
        """
        if textColonneteItems:
            nombreLignesTexte = self.determinerNombreLignes(textColonneteItems)
        else:
            nombreLignesTexte = 0
        if imageColonneItem:
            nombreLignesImage = max(
                len(item.imagePath)
                for item in imageColonneItem
                if isinstance(item, ImageColonneItem)
            )
        else:
            nombreLignesImage = 0

        nombreLignesTotal = max(nombreLignesTexte, nombreLignesImage)
        return nombreLignesTotal

    def preparerExport(self, imageView: ImageView, dossierExport: str) -> None:
        (
            textColonneteItems,
            textUniqueItems,
            imageUniqueItems,
            imageColonneItem,
            formeGeometriqueItem,
        ) = self.classifierItems(imageView)
        nombreLignes = nombreLignes = self.définirNombresLignes(
            textColonneteItems, imageColonneItem
        )

        tailleImage = imageView.imageLabel.pixmap().size()
        progressBar = self.creerProgressBar(nombreLignes)

        self.effectuerExport(
            textColonneteItems,
            textUniqueItems,
            imageUniqueItems,
            imageColonneItem,
            formeGeometriqueItem,
            nombreLignes,
            tailleImage,
            dossierExport,
            progressBar,
        )

    def classifierItems(self, imageView: ImageView) -> list[str]:
        imageUniqueItems = [
            item for item in imageView.items if isinstance(item, ImageUniqueItem)
        ]
        imageColonneItem = [
            item for item in imageView.items if isinstance(item, ImageColonneItem)
        ]
        textColonneteItems = [
            item for item in imageView.items if isinstance(item, TextColonneItem)
        ]
        textUniqueItems = [
            item for item in imageView.items if isinstance(item, TextUniqueItem)
        ]

        formeGeometriqueItem = [
            item for item in imageView.items if isinstance(item, FormeGeometriqueItem)
        ]

        return (
            textColonneteItems,
            textUniqueItems,
            imageUniqueItems,
            imageColonneItem,
            formeGeometriqueItem,
        )

    def determinerNombreLignes(self, textColonneteItems) -> None:
        return (
            max(len(item.text) for item in textColonneteItems)
            if textColonneteItems
            else 1
        )

    def creerProgressBar(self, nombreLignes: int) -> ProgressBar:
        progressBar = ProgressBar(nombreLignes)
        progressBar.show()
        return progressBar

    def effectuerExport(
        self,
        textColonneteItems,
        textUniqueItems,
        imageUniqueItems,
        imageColonneItem,
        formeGemotriqueItem,
        nombreLignes,
        tailleImage,
        dossierExport,
        progressBar,
    ) -> None:
        current_image = 0
        for numLigne in range(nombreLignes):
            image = QImage(tailleImage, QImage.Format_ARGB32)
            image.fill(Qt.white)
            painter = QPainter(image)
            self.dessinerItems(
                painter,
                imageUniqueItems,
                imageColonneItem,
                textColonneteItems,
                textUniqueItems,
                formeGemotriqueItem,
                numLigne,
            )
            painter.end()

            self.sauvegarderImage(image, dossierExport, numLigne)
            self.mettreAJourProgressBar(progressBar, current_image, numLigne)
            current_image += 1

        progressBar.close()

    def dessinerItems(
        self,
        painter,
        imageUniqueItems,
        imageColonneItem,
        textColonneteItems,
        textUniqueItems,
        formeGemotriqueItem,
        numLigne,
    ) -> None:
        try:
            # Dessiner les ImageUniqueItem
            for item in imageUniqueItems:
                imageToDraw = QPixmap(item.imagePath)
                painter.drawPixmap(
                    item.x, item.y, item.largeur, item.hauteur, imageToDraw
                )

            # Dessiner Les ImageColonneItem
            for item in imageColonneItem:
                if isinstance(item, ImageColonneItem) and numLigne < len(
                    item.imagePath
                ):
                    cheminImage = item.imagePath[numLigne]
                    if (
                        isinstance(cheminImage, str)
                        and not isna(cheminImage)
                        and cheminImage.strip() != ""
                    ):
                        self.configurerImageColonne(painter, item, str(cheminImage))

            # dessiner les FormeGemotriqueItem
            for item in formeGemotriqueItem:
                brush = QBrush(Qt.SolidPattern)
                brush.setColor(QColor(item.color))
                painter.setBrush(brush)
                painter.drawRoundedRect(
                    item.x, item.y, item.largeur, item.hauteur, item.radius, item.radius
                )

            # Dessiner les TextColonneteItem
            for item in textColonneteItems:
                if numLigne < len(item.text):
                    ligne = item.text[numLigne]
                    self.configurerStyloEtTexte(painter, item, str(ligne))

            # Dessiner les TextUniqueItem
            for item in textUniqueItems:
                self.configurerStyloEtTexte(painter, item, item.nom)
        except Exception as e:
            logging.error(f"Erreur lors du dessin des items {e}", exc_info=True)
            QMessageBox.critical(
                None,
                "Erreur d'Exportation",
                f"Une erreur inattendue est survenue lors de l'écriture des images : \n {e}.",
            )

    def configurerImageColonne(
        self, painter, item: ImageColonneItem, cheminImage: str
    ) -> None:
        # Charger l'image à partir du chemin fourni
        imageToDraw = QPixmap(cheminImage)
        if not imageToDraw.isNull():
            painter.drawPixmap(item.x, item.y, item.largeur, item.hauteur, imageToDraw)

    def configurerStyloEtTexte(self, painter, item: TextUniqueItem, texte: str) -> None:
        painter.setFont(QFont(item.font, item.fontSize))
        color = QColor(item.fontColor)
        pen = QPen(color)
        painter.setPen(pen)
        painter.drawText(item.x, item.y, texte)

    def sauvegarderImage(self, image: QImage, dossierExport: str, numLigne: int):
        try:
            nomFichier = os.path.join(dossierExport, f"ligne_{numLigne}.png")
            if not image.save(nomFichier):
                raise Exception(f"Impossible de sauvegarder l'image {nomFichier}")
        except Exception as e:
            logging.error("Erreur lors de la sauvegarde de l'image", exc_info=True)
            QMessageBox.critical(
                None,
                "Erreur de Sauvegarde",
                f"Impossible de sauvegarder l'image {nomFichier}.",
            )

    def mettreAJourProgressBar(self, progressBar, current_image, numLigne):
        progressBar.update_progress(
            current_image + 1, f"Exportation en cours : image_{numLigne}.png"
        )
        QApplication.processEvents()


class EditableTabBar(QTabBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

    def mouseDoubleClickEvent(self, event) -> None:
        index = self.tabAt(event.position().toPoint())
        if index >= 0:
            self.renameTab(index)

    def renameTab(self, index: int) -> None:
        editor = QLineEdit(self)
        editor.setText(self.tabText(index))
        editor.editingFinished.connect(lambda: self.changeTabTitle(editor, index))
        self.setTabText(index, "")
        self.setTabButton(index, QTabBar.LeftSide, editor)
        editor.selectAll()
        editor.setFocus()

    def changeTabTitle(self, editor, index: int) -> None:
        self.setTabText(index, editor.text())
        self.setTabButton(index, QTabBar.LeftSide, None)
        editor.deleteLater()
