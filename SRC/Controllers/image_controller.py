from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox

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