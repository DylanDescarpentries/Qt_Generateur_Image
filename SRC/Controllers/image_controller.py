from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QInputDialog, QFileDialog
from Models.text_item import TextUniqueItem, ImageUniqueItem

class ImageController:
    def __init__(self, mainWindow, itemWidget):
        self.mainWindow = mainWindow
        self.itemWidget = itemWidget        

    def onXChanged(self, x):
        if self.mainWindow.imageViewActif:
            textItem = self.getSelectedTextItem()
            if textItem:
                textItem.x = x
                self.mainWindow.imageViewActif.mettreAJourImage()

    def onYChanged(self, y):
        textItem = self.getSelectedTextItem()
        if textItem:
            textItem.y = y
            self.mainWindow.imageViewActif.mettreAJourImage()

    def onFontStyleChanged(self, font):
        textItem = self.getSelectedTextItem()
        if textItem:
            textItem.font = font
            self.mainWindow.imageViewActif.mettreAJourImage()
    
    def onFontSizeChanged(self, fontSize):
        textItem = self.getSelectedTextItem()
        if textItem:
            textItem.fontSize = fontSize
            self.mainWindow.imageViewActif.mettreAJourImage()

    def getSelectedTextItem(self):
        selectedItem = self.itemWidget.itemsList.currentItem()
        if selectedItem:
            textItem = selectedItem.data(Qt.UserRole)
            return textItem
        else:
            QMessageBox.warning(None, 'Attention !', 'Aucun item selectionné !')
                
    def applyChanges(self):
        selectedItem = self.mainWindow.itemWidget.itemsList.currentItem()
        if selectedItem:
            textItem = selectedItem.data(Qt.UserRole)
            if textItem:
                textItem.x = self.mainWindow.proprietesWidget.xpositionsEdit.value()
                textItem.y = self.mainWindow.proprietesWidget.ypositionsEdit.value()
                self.mainWindow.imageViewActif.mettreAJourImage()

    def onTextAjout(self):
       if self.mainWindow.imageViewActif:
            texte, ok = QInputDialog.getText(None, 'Ajouter Texte', 'Entrer votre texte :')
            if ok:
                textItem = TextUniqueItem(texte, 20, 20)
                self.mainWindow.imageViewActif.ajouterItem(textItem)
                self.mainWindow.itemWidget.ajouterItemVersListe(textItem) 
    
    def onImageAjout(self):
        if self.mainWindow.imageViewActif:
            imagePath = QFileDialog.getOpenFileName(None, 'Sélectionner une image', '', 'Images (*.png *.jpg *.jpeg)')[0]
            if imagePath:
                x, y, width, height = 20, 20, 100, 100  # Valeurs fixes pour l'instant
                imageItem = ImageUniqueItem(imagePath, x, y, width, height)
                self.mainWindow.imageViewActif.ajouterItem(imageItem)
                self.mainWindow.itemWidget.ajouterItemVersListe(imageItem)
