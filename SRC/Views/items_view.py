from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QMenu,
)
from PySide6.QtCore import Qt, Signal
from Models.text_item import TextColonneItem
from copy import deepcopy


class ItemWidget(QWidget):
    itemSelected = Signal(TextColonneItem)

    def __init__(self, mainWindow, parent=None) -> None:
        super().__init__(parent)
        self.mainWindow = mainWindow

        # Création du QListWidget pour les éléments
        self.layout = QVBoxLayout(self)
        self.itemsList = QListWidget(self)
        self.layout.addWidget(self.itemsList)

        self.itemsList.itemSelectionChanged.connect(self.onItemSelected)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.ouvrirContextMenu)

    def ajouterItemVersListe(self, item) -> None:
        self.listItem = QListWidgetItem(str(item))
        self.listItem.setData(Qt.UserRole, item)
        self.itemsList.addItem(self.listItem)
        self.itemsList.setCurrentItem(self.listItem)
        self.itemsList.setDragDropMode(QListWidget.InternalMove)

    def ouvrirContextMenu(self, position) -> None:
        contextMenu = QMenu(self)

        supprimerAction = contextMenu.addAction("Supprimer")
        supprimerAction.triggered.connect(self.onSupprimerAction)

        copierAction = contextMenu.addAction("Copier")
        copierAction.triggered.connect(self.copierItem)

        couperAction = contextMenu.addAction("Couper")
        couperAction.triggered.connect(self.couperItem)

        collerAction = contextMenu.addAction("Coller")
        collerAction.triggered.connect(self.collerItem)

        contextMenu.exec_(self.mapToGlobal(position))

    def onSupprimerAction(self) -> None:
        selectedItem = self.itemsList.currentItem()
        if selectedItem:
            reply = QMessageBox.question(
                self,
                "Confirmation",
                "Êtes-vous sûr de vouloir supprimer cet élément?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply == QMessageBox.Yes:
                itemAEffacer = self.getItemFor(selectedItem)
                self.supprimerItem(itemAEffacer)

    def supprimerItem(self, itemASupprimer) -> None:
        row = self.itemsList.row(self.itemsList.currentItem())
        self.itemsList.takeItem(row)
        if itemASupprimer in self.mainWindow.imageViewActif.items:
            self.mainWindow.imageViewActif.items.remove(itemASupprimer)

        self.mainWindow.imageViewActif.mettreAJourImage()

    def copierItem(self) -> None:
        selectedItem = self.itemsList.currentItem()
        if selectedItem:
            self.elementCopie = selectedItem.data(Qt.UserRole)

    def collerItem(self) -> None:
        if self.elementCopie:
            itemCopie = deepcopy(self.elementCopie)
            self.mainWindow.imageViewActif.ajouterItem(itemCopie)

    def couperItem(self) -> None:
        selectedItem = self.itemsList.currentItem()
        if selectedItem:
            itemASupprimer = selectedItem.data(Qt.UserRole)
            self.elementCopie = deepcopy(itemASupprimer)
            row = self.itemsList.row(selectedItem)
            self.itemsList.takeItem(row)
            if itemASupprimer in self.mainWindow.imageViewActif.items:
                self.mainWindow.imageViewActif.items.remove(itemASupprimer)

            self.mainWindow.imageViewActif.mettreAJourImage()

    def onItemSelected(self) -> None:
        selectedItem = self.itemsList.currentItem()
        if selectedItem:
            textItem = self.getItemFor(selectedItem)
            self.itemSelected.emit(textItem)

    def getItemFor(self, listItem) -> None:
        Item = listItem.data(Qt.UserRole)
        return Item

    def updateList(self, items) -> None:
        self.itemsList.clear()
        for item in items:
            self.ajouterItemVersListe(item)
