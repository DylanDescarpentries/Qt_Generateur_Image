"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"
Ce module contient la classe ProjetController et EditableTabBar, responsable du controle des projet,
notamment l'exportations des projets et la sauvegarde de ceux-ci.
""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

import os, logging, json
import pandas as pd
from pandas import isna
from typing import Optional, Any, Dict
from PySide6.QtWidgets import (
    QFileDialog,
    QApplication,
    QTabBar,
    QMessageBox,
    QLineEdit,
    QScrollArea,
)
from PySide6.QtCore import Qt, QObject, QRect
from PySide6.QtGui import QImage, QPainter, QFont, QPixmap, QPen, QColor, QBrush
from Views.image_view import ImageView
from Views.Widgets.progressbar import ProgressBar
from Models.itemsModels import *


class ProjetController(QObject):
    """Contrôleur principal gérant les actions sur les projets dans l'application."""

    def __init__(self, mainWindow, tabWidget):
        """Initialise le contrôleur avec la fenêtre principale et le widget d'onglets.

        :param mainWindow: Référence à la fenêtre principale de l'application.
        :param tabWidget: Widget d'onglets pour afficher les différentes vues du projet.
        """
        self.mainWindow = mainWindow
        self.tabWidget = tabWidget

    def creerNouveauProjet(
        self, largeur: int, hauteur: int, tabTitle: str = "Sans Titre"
    ) -> None:
        """Crée un nouveau projet avec une image vide et l'ajoute à l'interface utilisateur.

        :param largeur: Largeur de la nouvelle image du projet.
        :param hauteur: Hauteur de la nouvelle image du projet.
        :param tabTitle: Titre de l'onglet pour le nouveau projet. Par défaut, "Sans Titre".
        """
        imageView = ImageView(self.mainWindow, largeur, hauteur)
        imageView.creerImageVide(largeur, hauteur)
        scrollArea = self.creerScroll(imageView)

        indexNouvelOnglet = self.tabWidget.addTab(scrollArea, tabTitle)
        self.tabWidget.setCurrentIndex(indexNouvelOnglet)
        self.mainWindow.imageViewActif = imageView

    def preparerLaSauvegarde(self) -> None:
        """Prépare les données du projet actif pour la sauvegarde."""
        imageView = self.mainWindow.getActiveImageView()
        if imageView is None or not self.validerImageView(imageView):
            QMessageBox.warning(
                self.mainWindow,
                "Attention",
                "Aucun projet actif ou contenu à sauvegarder.",
            )
            return

        dossierSauvegarde = r"RESSOURCES\sauvegarde"
        itemsClassifies = self.classifierItems(imageView)
        self.sauvegarderProjet(dossierSauvegarde, itemsClassifies)

    def sauvegarderProjet(self, dossierSauvegarde: str, itemsClassifies: list) -> None:
        """
        Sauvegarde le projet actif dans un fichier JSON spécifié.

        :param dossierSauvegarde: Chemin du dossier où le fichier de sauvegarde sera créé.
        :param itemsClassifies: Liste des items classifiés à sauvegarder, organisés par type.
        """
        # Définition de la structure de base pour le fichier de sauvegarde
        sauvegarde = {
            "titre": self.mainWindow.tabWidget.tabText(
                self.mainWindow.tabWidget.currentIndex()
            ),
            "dimensions": {
                "largeur": self.mainWindow.imageViewActif.largeur,
                "hauteur": self.mainWindow.imageViewActif.hauteur,
            },
            "items": [],
        }

        # Ajout des items au dictionnaire de sauvegarde
        for categorie, items in zip(
            [
                "TextColonneItem",
                "TextUniqueItem",
                "ImageUniqueItem",
                "ImageColonneItem",
                "FormeGeometriqueItem",
            ],
            itemsClassifies,
        ):
            for item in items:
                itemDict = self.convertirItemEnDictionnaire(item, categorie)
                sauvegarde["items"].append(itemDict)

        # Construction du chemin de fichier complet
        cheminFichier = os.path.join(
            dossierSauvegarde, f'{sauvegarde["titre"].replace(" ", "_")}.json'
        )
        if os.path.exists(cheminFichier):
            reponse = QMessageBox.warning(
                self.mainWindow,
                "Fichier de sauvegarde existant",
                f'Un fichier de sauvegarde {sauvegarde["titre"].replace(" ", "_")}.json',
                QMessageBox.Save | QMessageBox.Cancel,
            )
            if reponse == QMessageBox.Save:
                with open(cheminFichier, "w") as fichier:
                    json.dump(sauvegarde, fichier, indent=4)
        else:
            with open(cheminFichier, "w") as fichier:
                json.dump(sauvegarde, fichier, indent=4)

    def convertirItemEnDictionnaire(self, item, categorie):
        """
        Convertit un item en dictionnaire pour la sauvegarde.

        :param item: L'item à convertir.
        :param categorie: La catégorie de l'item.
        :return: Un dictionnaire représentant l'item.
        """
        # Exemple de conversion pour TextUniqueItem, à adapter selon vos besoins
        if categorie == "TextUniqueItem":
            return {
                "type": categorie,
                "nom": item.nom,
                "position": {"x": item.x, "y": item.y},
                "dimensions": {"largeur": item.largeur, "hauteur": item.hauteur},
                "font": item.font,
                "fontSize": item.fontSize,
                "fontColor": item.fontColor,
                "index": item.index,
            }
        if categorie == "TextColonneItem":
            return {
                "type": categorie,
                "id": item.id,
                "nom": item.nom,
                "texte": item.text,
                "positions": {"x": item.x, "y": item.y},
                "dimensions": {"largeur": item.largeur, "hauteur": item.hauteur},
                "font": item.font,
                "fontSize": item.fontSize,
                "fontColor": item.fontColor,
                "index": item.index,
            }
        if categorie == "ImageUniqueItem":
            return {
                "type": categorie,
                "Chemin Image": item.imagePath,
                "position": {"x": item.x, "y": item.y},
                "dimensions": {"largeur": item.largeur, "hauteur": item.hauteur},
                "index": item.index,
            }

        if categorie == "ImageColonneItem":
            return {
                "type": categorie,
                "nom": item.nom,
                "Chemin Image": item.imagePath,
                "positions": {"x": item.x, "y": item.y},
                "dimensions": {"largeur": item.largeur, "hauteur": item.hauteur},
                "index": item.index,
            }
        if categorie == "FormeGeometriqueItem":
            return {
                "type": categorie,
                "nom": item.nom,
                "position": {"x": item.x, "y": item.y},
                "dimensions": {"largeur": item.largeur, "hauteur": item.hauteur},
                "radius": item.radius,
                "couleur": item.color,
                "index": item.index,
            }

    def chargerProjet(self, nomSauvegarde: str) -> None:
        """
        Charge un projet à partir d'un fichier JSON sauvegardé.

        :param cheminFichier: Chemin complet vers le fichier de projet JSON à charger.
        """
        with open(f"RESSOURCES\sauvegarde\{nomSauvegarde}", "r") as fichierSauvegarde:
            donneesProjet = json.load(fichierSauvegarde)

        itemsRecrees = [
            self.recreerItem(itemData) for itemData in donneesProjet.get("items", [])
        ]
        itemsTries = sorted(itemsRecrees, key=lambda item: item.index)

        # récupère les dimensions du projet et le titre
        largeur = donneesProjet["dimensions"]["largeur"]
        hauteur = donneesProjet["dimensions"]["hauteur"]
        tabTitle = donneesProjet.get("titre", "Sans Titre")
        self.creerNouveauProjet(largeur, hauteur, tabTitle)

        # Itére sur les items sauvegardés et les recréer
        for item in itemsTries:
            self.mainWindow.imageViewActif.ajouterItem(item)

        # Mettre à jour l'affichage de l'image
        self.mainWindow.imageViewActif.mettreAJourImage()

    def recreerItem(self, itemData: Dict[str, Any]) -> Any:
        ...
        """
        Recrée un item à partir des données spécifiées. Cette méthode devra être adaptée
        pour gérer différents types d'items en fonction de leur structure de données.

        :param itemData: Un dictionnaire contenant les données de l'item.
        :return: L'instance de l'item recréé.
        """

        if itemData["type"] == "FormeGeometriqueItem":
            item = FormeGeometriqueItem(
                nom=itemData["nom"],
                x=itemData["position"]["x"],
                y=itemData["position"]["y"],
                largeur=itemData["dimensions"]["largeur"],
                hauteur=itemData["dimensions"]["hauteur"],
                radius=itemData["radius"],
                color=itemData["couleur"],
            )
            item.index = itemData["index"]
            return item

        if itemData["type"] == "ImageColonneItem":
            item = ImageColonneItem(
                nom=itemData["nom"],
                imagePath=itemData["Chemin Image"],
                x=itemData["positions"]["x"],
                y=itemData["positions"]["y"],
                largeur=itemData["dimensions"]["largeur"],
                hauteur=itemData["dimensions"]["hauteur"],
            )
            item.index = itemData["index"]
            return item

        if itemData["type"] == "TextColonneItem":
            item = TextColonneItem(
                id=str(itemData["id"]),
                nom=str(itemData["nom"]),
                text=itemData["texte"],
                x=itemData["positions"]["x"],
                y=itemData["positions"]["y"],
                largeur=itemData["dimensions"]["largeur"],
                hauteur=itemData["dimensions"]["hauteur"],
                font=itemData["font"],
                fontSize=itemData["fontSize"],
                fontColor=itemData["fontColor"],
            )
            item.index = itemData["index"]
            return item

        if itemData["type"] == "TextUniqueItem":
            item = TextUniqueItem(
                nom=str(itemData["nom"]),
                x=itemData["position"]["x"],
                y=itemData["position"]["y"],
                largeur=itemData["dimensions"]["largeur"],
                hauteur=itemData["dimensions"]["hauteur"],
                font=itemData["font"],
                fontSize=itemData["fontSize"],
                fontColor=itemData["fontColor"],
            )
            item.index = itemData["index"]
            return item

        if itemData["type"] == "ImageUniqueItem":
            item = ImageUniqueItem(
                imagePath=itemData["Chemin Image"],
                x=itemData["position"]["x"],
                y=itemData["position"]["y"],
                largeur=itemData["dimensions"]["largeur"],
                hauteur=itemData["dimensions"]["hauteur"],
            )
            item.index = itemData["index"]
            return item

    def creerScroll(self, widget: ImageView) -> QScrollArea:
        """Crée et retourne une zone de défilement pour l'ImageView donné.

        :param widget: L'ImageView à encapsuler dans une zone de défilement.
        :return: Un QScrollArea contenant l'ImageView donné.
        """
        scrollArea = QScrollArea()
        scrollArea.setWidget(widget)
        scrollArea.setWidgetResizable(True)
        return scrollArea

    def exporterProjet(self, imageView: ImageView) -> None:
        """Exporte le projet actif vers un dossier spécifié par l'utilisateur.

        :param imageView: Vue de l'image à exporter.
        """

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
        """Vérifie si l'ImageView donné est valide pour l'exportation.

        :param imageView: L'ImageView à valider.
        :return: True si l'ImageView est valide, False sinon.
        """

        if imageView is None or not imageView.items:
            QMessageBox.warning(
                None,
                "Attention",
                "Aucune image à exporter ou aucun élément de texte ajouté.",
            )
            return False
        return True

    def selectionnerDossierExport(self) -> Optional[str]:
        """Ouvre une boîte de dialogue permettant à l'utilisateur de sélectionner un dossier d'exportation.

        :return: Le chemin du dossier sélectionné pour l'exportation, ou None si aucun dossier n'est sélectionné.
        """
        titreProjet = self.mainWindow.tabWidget.tabText(
            self.mainWindow.tabWidget.currentIndex()
        )  # récupère le titre du la vue active
        dossier = QFileDialog.getExistingDirectory(
            None, "Sélectionner un dossier d'export"
        )
        if not dossier:
            return None
        dossierFinal = os.path.join(dossier, titreProjet)
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
        """Prépare les éléments nécessaires pour l'exportation de l'ImageView.

        :param imageView: L'ImageView contenant les éléments à exporter.
        :param dossierExport: Le chemin du dossier où les éléments seront exportés.
        """
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
        """Classifie les items de l'ImageView en différentes catégories.

        :param imageView: L'ImageView contenant les items à classifier.
        :return: Une liste de listes, chaque sous-liste contenant des items d'une certaine catégorie.
        """
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
        """Détermine le nombre de lignes pour les items de texte en colonnes.

        :param textColonneteItems: Liste des items de texte en colonnes.
        :return: Le nombre maximal de lignes parmi tous les items de texte en colonnes.
        """
        return (
            max(len(item.text) for item in textColonneteItems)
            if textColonneteItems
            else 1
        )

    def creerProgressBar(self, nombreLignes: int) -> ProgressBar:
        """Crée une barre de progression pour l'exportation.

        :param nombreLignes: Le nombre total de lignes à exporter, déterminant la longueur de la progression.
        :return: Une instance de ProgressBar initialisée.
        """
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
        """Effectue l'exportation des items du projet vers des images.

        :param textColonneteItems: Items de texte en colonnes à exporter.
        :param textUniqueItems: Items de texte uniques à exporter.
        :param imageUniqueItems: Items d'image uniques à exporter.
        :param imageColonneItem: Items d'image en colonnes à exporter.
        :param formeGemotriqueItem: Items de formes géométriques à exporter.
        :param nombreLignes: Nombre total de lignes à exporter.
        :param tailleImage: Taille de l'image à exporter.
        :param dossierExport: Chemin du dossier où les images seront sauvegardées.
        :param progressBar: Barre de progression à mettre à jour pendant l'exportation.
        """
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
        # Créer une liste unique de tous les éléments
        tousLesItems = (
            imageUniqueItems
            + imageColonneItem
            + textColonneteItems
            + textUniqueItems
            + formeGemotriqueItem
        )
        tousLesItemsTries = sorted(tousLesItems, key=lambda item: item.index)
        """Dessine les items sur une image en utilisant QPainter.

        :param painter: QPainter utilisé pour dessiner les items.
        :param imageUniqueItems: Liste des items d'image uniques à dessiner.
        :param imageColonneItem: Liste des items d'image en colonnes à dessiner.
        :param textColonneteItems: Liste des items de texte en colonnes à dessiner.
        :param textUniqueItems: Liste des items de texte uniques à dessiner.
        :param formeGemotriqueItem: Liste des items de formes géométriques à dessiner.
        :param numLigne: Numéro de la ligne actuelle, utilisé pour les items en colonnes.
        """
        try:
            # Dessiner les éléments triés
            for item in tousLesItemsTries:
                if isinstance(item, ImageUniqueItem):
                    imageToDraw = QPixmap(item.imagePath)
                    painter.drawPixmap(
                        item.x, item.y, item.largeur, item.hauteur, imageToDraw
                    )

                elif isinstance(item, FormeGeometriqueItem):
                    brush = QBrush(Qt.SolidPattern)
                    brush.setColor(QColor(item.color))
                    painter.setBrush(brush)

                    painter.drawRoundedRect(
                        item.x,
                        item.y,
                        item.largeur,
                        item.hauteur,
                        item.radius,
                        item.radius,
                    )
                elif isinstance(item, ImageColonneItem) and numLigne < len(
                    item.imagePath
                ):
                    cheminImage = item.imagePath[numLigne]
                    if (
                        isinstance(cheminImage, str)
                        and not pd.isna(cheminImage)
                        and cheminImage.strip() != ""
                    ):
                        self.configurerImageColonne(painter, item, str(cheminImage))

                elif isinstance(item, TextColonneItem) and numLigne < len(item.text):
                    ligne = item.text[numLigne]
                    self.configurerStyloEtTexte(painter, item, str(ligne))

                elif isinstance(item, TextUniqueItem):
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
        """Configure et dessine une image en colonne sur le QPainter.

        :param painter: QPainter utilisé pour le dessin.
        :param item: L'item d'image en colonne à dessiner.
        :param cheminImage: Le chemin de l'image à dessiner.
        """
        imageToDraw = QPixmap(cheminImage)
        if not imageToDraw.isNull():
            painter.drawPixmap(item.x, item.y, item.largeur, item.hauteur, imageToDraw)

    def configurerStyloEtTexte(self, painter, item: TextUniqueItem, texte: str) -> None:
        """Configure le stylo et le texte pour le dessin sur QPainter.

        :param painter: QPainter utilisé pour le dessin.
        :param item: L'item de texte à dessiner.
        :param texte: Le texte à dessiner.
        """
        rect = QRect(item.x, item.y, item.largeur, item.hauteur)
        painter.setFont(QFont(item.font, item.fontSize))
        painter.setPen(QPen(QColor(item.fontColor)))
        painter.drawText(
            rect, Qt.AlignLeft | Qt.AlignVCenter | Qt.TextWordWrap, str(texte)
        )

    def sauvegarderImage(self, image: QImage, dossierExport: str, numLigne: int):
        """Sauvegarde une image dans le dossier spécifié.

        :param image: L'image à sauvegarder.
        :param dossierExport: Chemin du dossier où l'image sera sauvegardée.
        :param numLigne: Numéro de la ligne, utilisé pour nommer l'image.
        """
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
        """Met à jour la barre de progression pendant l'exportation.

        :param progressBar: La barre de progression à mettre à jour.
        :param current_image: Index de l'image actuelle dans le processus d'exportation.
        :param numLigne: Numéro de la ligne actuelle, utilisé pour l'affichage dans la barre de progression.
        """
        progressBar.update_progress(
            current_image + 1, f"Exportation en cours : image_{numLigne}.png"
        )
        QApplication.processEvents()


class EditableTabBar(QTabBar):
    """Une barre d'onglets personnalisée permettant le renommage des onglets par double-clic."""

    def __init__(self, parent=None) -> None:
        """Initialise la barre d'onglets éditable.

        :param parent: Le widget parent de la barre d'onglets.
        """
        super().__init__(parent)

    def mouseDoubleClickEvent(self, event) -> None:
        """Gère l'événement de double-clic de la souris sur un onglet pour activer le renommage.

        :param event: L'objet d'événement contenant les détails du double-clic.
        """
        index = self.tabAt(event.position().toPoint())
        if index >= 0:
            self.renameTab(index)

    def renameTab(self, index: int) -> None:
        """Active l'édition du titre de l'onglet spécifié.

        Crée un QLineEdit pour permettre à l'utilisateur de saisir un nouveau titre pour l'onglet.

        :param index: L'indice de l'onglet à renommer.
        """
        editor = QLineEdit(self)
        editor.setText(self.tabText(index))
        editor.editingFinished.connect(lambda: self.changeTabTitle(editor, index))
        self.setTabText(index, "")
        self.setTabButton(index, QTabBar.LeftSide, editor)
        editor.selectAll()
        editor.setFocus()

    def changeTabTitle(self, editor, index: int) -> None:
        """Met à jour le titre de l'onglet après l'édition.

        :param editor: Le QLineEdit utilisé pour l'édition du titre de l'onglet.
        :param index: L'indice de l'onglet dont le titre est mis à jour.
        """
        self.setTabText(index, editor.text())
        self.setTabButton(index, QTabBar.LeftSide, None)
        editor.deleteLater()
