from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableView, QMenu
from PySide6.QtCore import Qt, Signal
from Models.data import PandasTableModel
from Models.text_item import TextColonneItem
import pandas as pd

class DataView(QWidget):
    '''
    DataView est un widget personnalisé qui affiche un DataFrame pandas dans un QTableView.
    Permet l'interaction utilisateur pour sélectionner des données à inclure dans le projet d'image.
    '''
    colonneAjoutee = Signal(TextColonneItem)

    def __init__(self, mainWindow, dataController):
        '''
        Initialisation de DataView.

        :param mainWindow: Référence à la fenêtre principale de l'application pour accéder à d'autres composants.
        '''
        super().__init__()
        self.mainWindow = mainWindow
        self.dataController = dataController
        self.setupUI()

    def setupUI(self):
        '''
        Configure les éléments de l'interface utilisateur pour DataView.
        '''
        self.layout = QVBoxLayout(self)
        self.tableView = self.createTableView()
        self.layout.addWidget(self.tableView)

    def createTableView(self):
        '''
        Crée et configure le QTableView pour afficher les données pandas DataFrame.

        :return: Une instance configurée de QTableView.
        '''
        tableView = QTableView(self)
        tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        tableView.customContextMenuRequested.connect(self.ouvrirContextMenu)
        tableView.setModel(PandasTableModel(pd.DataFrame()))
        return tableView

    def load_data(self, dataFrame):
        '''
        Charge les données pandas DataFrame dans le modèle du QTableView.

        :param dataFrame: Les données pandas DataFrame à afficher.
        '''
        self.tableView.model().set_data(dataFrame)


    def ouvrirContextMenu(self, position):
        '''
        Ouvre un menu contextuel à la position spécifiée, offrant des options pour manipuler les données.

        :param position: La position dans le widget où le menu contextuel doit être ouvert.
        '''
        contextMenu = QMenu(self)
        ajouterColonneAction = contextMenu.addAction('Ajouter la colonne au projet')
        importTableauAction = contextMenu.addAction('Importer un tableau')
        action = contextMenu.exec(self.tableView.mapToGlobal(position))
        if action == ajouterColonneAction:
            self.ajouterColonneAuProjet()
        if action == importTableauAction:
            self.dataController.importFichier()

    def ajouterColonneAuProjet(self):
        currentIndex = self.tableView.currentIndex()
        if currentIndex.isValid():
            nomColonne = self.tableView.model().headerData(currentIndex.column(), Qt.Horizontal)
            donnees = self.tableView.model().columnData(currentIndex.column())

            # Assurez-vous que 'donnees' est une liste de chaînes de caractères
            if not isinstance(donnees, list):
                print('Les données ne sont pas une liste.')
                return

            # Créer un TextItem avec la liste des données
            textItem = TextColonneItem(nomColonne, donnees) 

            # Émettre le signal avec l'objet TextItem
            self.colonneAjoutee.emit(textItem)

