import logging
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableView,
    QMenu,
    QComboBox,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from Models.data import PandasTableModel
from Models.itemsModels import TextColonneItem, ImageColonneItem
import pandas as pd


class DataView(QWidget):
    """
    DataView est un widget personnalisé qui affiche un DataFrame pandas dans un QTableView.
    Permet l'interaction utilisateur pour sélectionner des données à inclure dans le projet d'image.
    """

    colonneAjoutee = Signal(TextColonneItem)

    def __init__(self, mainWindow, dataController) -> None:
        """
        Initialise DataView, connecte les signaux et prépare l'UI.

        :param mainWindow: La fenêtre principale pour l'accès global.
        :param dataController: Le contrôleur pour la gestion des données.
        """
        super().__init__()
        self.mainWindow = mainWindow
        self.dataController = dataController
        self.setupUI()
        self.dataController.fichierImporte.connect(self.majSheetSelecteur)
        self.dataFrames = {}

    def setupUI(self) -> None:
        """
        Configure l'interface utilisateur de DataView, y compris la création de la vue de table et du sélecteur de feuille.
        """

        self.layout = QVBoxLayout(self)
        self.tableView = self.createTableView()
        self.sheetSelecteur = QComboBox(self)
        self.layout.addWidget(self.sheetSelecteur)
        self.layout.addWidget(self.tableView)
        self.sheetSelecteur.currentIndexChanged.connect(self.onSheetSelectionne)

    def createTableView(self) -> QTableView:
        """
        Crée le QTableView pour l'affichage des données DataFrame.

        :return: Une instance configurée de QTableView.
        """
        tableView = QTableView(self)
        tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        tableView.customContextMenuRequested.connect(self.ouvrirContextMenu)
        tableView.setModel(PandasTableModel(pd.DataFrame()))
        return tableView

    def load_data(self, dataFrame: pd.DataFrame) -> None:
        """
        Charge un DataFrame dans le modèle du QTableView.

        :param dataFrame: Le DataFrame pandas à charger dans la vue.
        """
        try:
            model = self.tableView.model()
            if isinstance(model, PandasTableModel):
                model.set_data(dataFrame)
            else:
                nouveauModel = PandasTableModel(dataFrame)
                self.tableView.setModel(nouveauModel)
        except Exception as e:
            logging.error(f"Erreur Chargement\n {e}", exc_info=True)
            QMessageBox.critical(
                None,
                "Erreur fichier Data",
                f"Problème lors du chargement les données : \n{e}.",
            )

    def projetEstOuvert(self) -> bool:
        """
        Vérifie si un projet est actuellement ouvert dans l'application.

        :return: Booléen indiquant si un projet est ouvert.
        """
        return self.mainWindow.imageViewActif is not None

    def afficherMessageErreurAbsenceProjet(self) -> None:
        QMessageBox.warning(
            self,
            "Action impossible",
            "Veuillez créer ou ouvrir un projet avant d'ajouter un item.",
        )

    def afficherMessageErreurAbsenceTableau(self) -> None:
        QMessageBox.warning(
            self, "Action impossible", "Veuillez initialiser un tableau"
        )

    def ouvrirContextMenu(self, position) -> None:
        """
        Ouvre un menu contextuel à la position spécifiée, offrant des options pour manipuler les données.

        :param position: La position dans le widget où le menu contextuel doit être ouvert.
        """
        contextMenu = QMenu(self)
        importTableauAction = contextMenu.addAction("Importer un tableau")
        importTableauAction.setIcon(QIcon("RESSOURCES\ASSETS\images\logo\data.png"))
        ajouterColonneAction = contextMenu.addAction(
            "Ajouter la colonne comme un texte"
        )
        ajouterColonneAction.setIcon(
            QIcon(r"RESSOURCES\ASSETS\images\logo\ajouter.png")
        )
        ajouterImagesAction = contextMenu.addAction(
            "Ajouter la colonne Comme une image"
        )
        ajouterImagesAction.setIcon(QIcon(r"RESSOURCES\ASSETS\images\logo\ajouter.png"))
        action = contextMenu.exec(self.tableView.mapToGlobal(position))

        if action == ajouterColonneAction:
            if self.projetEstOuvert():
                self.ajouterColonneAuProjet()
            else:
                self.afficherMessageErreurAbsenceProjet()
        elif action == importTableauAction:
            self.dataController.importFichier()
        elif action == ajouterImagesAction:
            if self.projetEstOuvert():
                self.AjouterColonneImageAuProjet()
            else:
                self.afficherMessageErreurAbsenceTableau()

    def ajouterColonneAuProjet(self) -> None:
        try:
            currentIndex = self.tableView.currentIndex()
            if currentIndex.isValid():
                nomColonne = self.tableView.model().headerData(
                    currentIndex.column(), Qt.Horizontal
                )
                donnees = self.tableView.model().columnData(currentIndex.column())

                if not isinstance(donnees, list):
                    return

                # Créer un TextItem avec la liste des données
                textItem = TextColonneItem(nomColonne, donnees)

                # Émettre le signal avec l'objet TextItem
                self.colonneAjoutee.emit(textItem)
            else:
                self.afficherMessageErreurAbsenceTableau()
        except Exception as e:
            logging.error(
                f"Erreur lors de la sauvegarde de l'image \n {e}", exc_info=True
            )
            QMessageBox.critical(
                None,
                "Erreur Ajout Colonne",
                f"Problème lors de l'ajout de la Colonne : \n{e}.",
            )

    def AjouterColonneImageAuProjet(self) -> None:
        try:
            currentIndex = self.tableView.currentIndex()
            if currentIndex.isValid():
                cheminsImages = self.tableView.model().columnData(currentIndex.column())

                if not isinstance(cheminsImages, list):
                    return
                imageItem = ImageColonneItem(cheminsImages)

                self.colonneAjoutee.emit(imageItem)
            else:
                self.afficherMessageErreurAbsenceTableau()
        except Exception as e:
            logging.error(
                f"Erreur lors de la sauvegarde de l'image \n {e}", exc_info=True
            )
            QMessageBox.critical(
                None,
                "Erreur Ajout Colonne",
                f"Problème lors de l'ajout de la Colonne : \n{e}.",
            )

    def majSheetSelecteur(self, dataFrames) -> None:
        self.dataFrames = dataFrames
        self.sheetSelecteur.clear()
        self.sheetSelecteur.addItems(list(dataFrames.keys()))

    def onSheetSelectionne(self) -> None:
        selected_sheet_name = self.sheetSelecteur.currentText()
        if selected_sheet_name in self.dataFrames:
            dataFrame = self.dataFrames[selected_sheet_name]
            self.load_data(dataFrame)
