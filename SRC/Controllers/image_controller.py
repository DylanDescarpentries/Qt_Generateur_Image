"""""" """""" """""" """""" """""" """""" """""" """""" """""" """
Module de contrôle pour la gestion des images dans l'application.
Principalement le controle de la vue contenant le projet
""" """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QInputDialog, QFileDialog
from Models.itemsModels import TextUniqueItem, ImageUniqueItem, FormeGeometriqueItem
from Views.Widgets.dialogFormeGeometriqueAjout import DialogFormeGeometriqueAjout


class ImageController:
    """
    Contrôleur pour la gestion des actions liées aux images et aux éléments textuels dans l'application.
    Permet de manipuler les propriétés des items et d'ajouter de nouveaux éléments au projet actif.
    """

    def __init__(self, mainWindow, itemWidget) -> None:
        """
        Initialise le contrôleur avec des références à la fenêtre principale et au widget d'items.

        :param mainWindow: La fenêtre principale de l'application.
        :param itemWidget: Le widget qui liste les items du projet actuel.
        """
        self.mainWindow = mainWindow
        self.itemWidget = itemWidget

    def onXChanged(self, x: int) -> None:
        if self.mainWindow.imageViewActif:
            textItem = self.getSelectedTextItem()
            if textItem:
                textItem.x = x
                self.mainWindow.imageViewActif.mettreAJourImage()

    def onYChanged(self, y: int) -> None:
        textItem = self.getSelectedTextItem()
        if textItem:
            textItem.y = y
            self.mainWindow.imageViewActif.mettreAJourImage()

    def onLargeurChanged(self, largeur: int) -> None:
        item = self.getSelectedTextItem()
        if item:
            item.largeur = largeur
            self.mainWindow.imageViewActif.mettreAJourImage()

    def onHauteurChanged(self, hauteur: int) -> None:
        item = self.getSelectedTextItem()
        if item:
            item.hauteur = hauteur
            self.mainWindow.imageViewActif.mettreAJourImage()

    def onRadiusChanged(self, radius: int) -> None:
        item = self.getSelectedTextItem()
        if item:
            item.radius = radius
            self.mainWindow.imageViewActif.mettreAJourImage()

    def onFontStyleChanged(self, font: str) -> None:
        textItem = self.getSelectedTextItem()
        if textItem:
            textItem.font = font
            self.mainWindow.imageViewActif.mettreAJourImage()

    def onFontSizeChanged(self, fontSize: int) -> None:
        textItem = self.getSelectedTextItem()
        if textItem:
            textItem.fontSize = fontSize
            self.mainWindow.imageViewActif.mettreAJourImage()

    def onFontColorChanged(self, fontColor: str) -> None:
        textItem = self.getSelectedTextItem()
        if textItem:
            textItem.fontColor = fontColor
            self.mainWindow.imageViewActif.mettreAJourImage()

    def onFormColorChanged(self, Color: str) -> None:
        item = self.getSelectedTextItem()
        if item:
            item.color = Color
            self.mainWindow.imageViewActif.mettreAJourImage()

    def getSelectedTextItem(self) -> None:
        selectedItem = self.itemWidget.itemsList.currentItem()
        if selectedItem:
            textItem = selectedItem.data(Qt.UserRole)  # type: ignore
            return textItem
        else:
            QMessageBox.warning(
                self.mainWindow, "Attention !", "Aucun item selectionné !"
            )

    def applyChanges(self) -> None:
        selectedItem = self.mainWindow.itemWidget.itemsList.currentItem()
        if selectedItem:
            textItem = selectedItem.data(Qt.UserRole)  # type: ignore
            if textItem:
                textItem.x = self.mainWindow.proprietesWidget.xpositionsEdit.value()
                textItem.y = self.mainWindow.proprietesWidget.ypositionsEdit.value()
                self.mainWindow.imageViewActif.mettreAJourImage()

    def onTextAjout(self) -> None:
        if self.mainWindow.imageViewActif:
            texte, ok = QInputDialog.getText(
                self.mainWindow, "Ajouter Texte", "Entrer votre texte :"
            )
            if ok:
                if texte == "":
                    QMessageBox.warning(
                        self.mainWindow, "Attention !", "Vous n'avez pas entré de texte"
                    )
                else:
                    textItem = TextUniqueItem(texte, 20, 20)
                    self.mainWindow.imageViewActif.ajouterItem(textItem)
                    self.mainWindow.itemWidget.ajouterItemVersListe(textItem)
        else:
            self.afficherMessageErreur()

    def onImageAjout(self) -> None:
        if self.mainWindow.imageViewActif:
            imagePath = QFileDialog.getOpenFileName(
                None, "Sélectionner une image", "", "Images (*.png *.jpg *.jpeg)"
            )[0]
            if imagePath:
                x, y, width, height = 20, 20, 100, 100
                imageItem = ImageUniqueItem(imagePath, x, y, width, height)
                self.mainWindow.imageViewActif.ajouterItem(imageItem)
                self.mainWindow.itemWidget.ajouterItemVersListe(imageItem)
        else:
            self.afficherMessageErreur()

    def onFormeGeometriqueAjout(self) -> None:
        if self.mainWindow.imageViewActif:
            dialog = DialogFormeGeometriqueAjout()
            if dialog.exec():
                largeur, hauteur, radius = dialog.getDimensions()
                try:
                    largeur = int(largeur)
                    hauteur = int(hauteur)
                    radius = int(radius)
                    formeGeometriqueItem = FormeGeometriqueItem(
                        "test", 20, 20, largeur, hauteur, radius, "black"
                    )
                    self.mainWindow.imageViewActif.ajouterItem(formeGeometriqueItem)
                    self.mainWindow.itemWidget.ajouterItemVersListe(
                        formeGeometriqueItem
                    )
                except ValueError:
                    pass
        else:
            self.afficherMessageErreur()

    def afficherMessageErreur(self):
        QMessageBox.warning(
            self.mainWindow,
            "Action impossible",
            "Veuillez créer ou ouvrir un projet avant d'ajouter un item.",
        )
