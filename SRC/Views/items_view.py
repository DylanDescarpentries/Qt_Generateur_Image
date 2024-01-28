from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QMessageBox
from PySide6.QtCore import Qt, Signal
from Models.text_item import TextItem

class ItemWidget(QWidget):
    itemSelected = Signal(TextItem)
    def __init__(self, proprietesWidget, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.proprietesWidget = proprietesWidget
        
        # Création du QListWidget pour les éléments
        self.itemsList = QListWidget(self)
        self.layout.addWidget(self.itemsList)

        self.itemsList.itemSelectionChanged.connect(self.onItemSelected)

    def addItem(self, textItem):
        """Ajoute un nouvel item à la liste."""
        item = QListWidgetItem(str(textItem))
        item.setData(Qt.UserRole, textItem)
        self.itemsList.addItem(item)
        self.itemsList.setCurrentItem(item)

    def onItemSelected(self):
        selectedItem = self.itemsList.currentItem()
        if selectedItem:
            textItem = self.getTextItemFor(selectedItem)
            self.itemSelected.emit(textItem)

    def getTextItemFor(self, listItem):
        """Retourne le TextItem correspondant à l'élément de la liste donné."""
        textItem = listItem.data(Qt.UserRole)
        return textItem