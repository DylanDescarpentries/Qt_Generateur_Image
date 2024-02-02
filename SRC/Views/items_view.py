from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidgetItem,
    QMessageBox,
    QMenu,
    QInputDialog,
    QApplication,
    QStyle,
)
from Views.Widgets.customListWidget import CustomListWidget
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from Models.text_item import TextColonneItem, TextUniqueItem
from copy import deepcopy


class ItemWidget(QWidget):
    itemSelected = Signal(TextColonneItem)

    def __init__(self, mainWindow, parent=None) -> None:
        super().__init__(parent)
        self.mainWindow = mainWindow

        # Création du QListWidget pour les éléments
        self.layout = QVBoxLayout(self)
        self.itemsList = CustomListWidget(self)
        self.layout.addWidget(self.itemsList)

        self.itemsList.itemSelectionChanged.connect(self.onItemSelected)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.ouvrirContextMenu)
        self.itemsList.itemsReordered.connect(self.onItemsReordonnes)

    def ajouterItemVersListe(self, item) -> None:
        self.listItem = QListWidgetItem(str(item))
        self.listItem.setData(Qt.UserRole, item)
        self.itemsList.addItem(self.listItem)
        self.itemsList.setCurrentItem(self.listItem)
        self.itemsList.setDragDropMode(CustomListWidget.InternalMove)

    def ouvrirContextMenu(self, position) -> None:
        contextMenu = QMenu(self)

        modifierAction = contextMenu.addAction("Modifier")
        modifierAction.triggered.connect(self.modifierItem)

        supprimerAction = contextMenu.addAction("Supprimer")
        supprimerAction.triggered.connect(self.onSupprimerAction)
        supprimerAction.setIcon(QIcon(r"RESSOURCES\ASSETS\images\logo\supprimer.png"))

        copierAction = contextMenu.addAction("Copier")
        copierAction.triggered.connect(self.copierItem)
        copierAction.setIcon(QIcon(r"RESSOURCES\ASSETS\images\logo\copie.png"))

        couperAction = contextMenu.addAction("Couper")
        couperAction.triggered.connect(self.couperItem)
        couperAction.setIcon(QIcon(r"RESSOURCES\ASSETS\images\logo\couper.png"))

        collerAction = contextMenu.addAction("Coller")
        collerAction.triggered.connect(self.collerItem)
        collerAction.setIcon(QIcon(r"RESSOURCES\ASSETS\images\logo\coller.png"))

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
            if isinstance(itemCopie, (TextUniqueItem, TextColonneItem)):
                itemCopie.nom += " - copie -"
                self.mainWindow.imageViewActif.ajouterItem(itemCopie)

    def modifierItem(self) -> None:
        selectedItem = self.itemsList.currentItem()
        if selectedItem:
            itemAModifier = selectedItem.data(Qt.UserRole)

            if isinstance(itemAModifier, TextUniqueItem) or isinstance(
                itemAModifier, TextColonneItem
            ):
                nouveauTexte, ok = QInputDialog.getText(
                    self.mainWindow,
                    "Modifier Texte",
                    "Entrer votre nouveau texte :",
                    text=itemAModifier.nom,
                )

                if ok:
                    if nouveauTexte.strip() == "":
                        QMessageBox.warning(
                            self.mainWindow,
                            "Attention !",
                            "Vous n'avez pas entré de texte",
                        )
                    else:
                        itemAModifier.nom = nouveauTexte
                        self.mainWindow.imageViewActif.mettreAJourImage()
                        selectedItem.setText(nouveauTexte)
            else:
                QMessageBox.warning(
                    self.mainWindow,
                    "Attention !",
                    "L'élément sélectionné n'est pas modifiable.",
                )

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

    def onItemsReordonnes(self):
        nouveauxItems = []
        for index in range(self.itemsList.count()):
            listItem = self.itemsList.item(index)
            item = listItem.data(Qt.UserRole)
            nouveauxItems.append(item)
        if self.mainWindow.imageViewActif:
            self.mainWindow.imageViewActif.reordonnerItems(nouveauxItems)
