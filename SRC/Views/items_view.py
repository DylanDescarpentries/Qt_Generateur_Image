from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QMessageBox, QMenu
from PySide6.QtCore import Qt, Signal
from Models.text_item import TextColonneItem


class ItemWidget(QWidget):
    itemSelected = Signal(TextColonneItem)

    def __init__(self,  proprietesWidget, parent=None):
        super().__init__(parent)

        self.proprietesWidget = proprietesWidget
        
        # Création du QListWidget pour les éléments
        self.layout = QVBoxLayout(self)
        self.itemsList = QListWidget(self)
        self.layout.addWidget(self.itemsList)

        self.itemsList.itemSelectionChanged.connect(self.onItemSelected)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.ouvrirContextMenu)

    def ajouterItemVersListe(self, item):
        listItem = QListWidgetItem(str(item))
        listItem.setData(Qt.UserRole, item)
        self.itemsList.addItem(listItem)
        self.itemsList.setCurrentItem(listItem)
        self.itemsList.setDragDropMode(QListWidget.InternalMove)


    def ouvrirContextMenu(self, position):
        contextMenu = QMenu(self)
        supprimerAction = contextMenu.addAction("Supprimer")
        supprimerAction.triggered.connect(self.supprimerSelectedItem)
        contextMenu.exec_(self.mapToGlobal(position))
        
    def supprimerSelectedItem(self):
        selectedItem = self.itemsList.currentItem()
        if selectedItem:
            reply = QMessageBox.question(self, 'Confirmation',
                                        "Êtes-vous sûr de vouloir supprimer cet élément?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                row = self.itemsList.row(selectedItem)
                itemAEffacer = self.itemsList.takeItem(row).data(Qt.UserRole)

                self.mainWindow.imageViewActif.supprimerItem(itemAEffacer)

    def onItemSelected(self):
        selectedItem = self.itemsList.currentItem()
        if selectedItem:
            textItem = self.getItemFor(selectedItem)
            self.itemSelected.emit(textItem)

    def getItemFor(self, listItem):
        '''Retourne le TextItem correspondant à l'élément de la liste donné.'''
        textItem = listItem.data(Qt.UserRole)
        return textItem