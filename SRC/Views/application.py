from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout,  QDockWidget, QTabWidget, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from Views.barreMenu import MenuBarre
from Views.data_view import DataView
from Views.proprietesBox import ProprietesWidget
from Views.items_view import ItemWidget
from Views.boitesOutils import BoiteOutils
from Controllers.data_controller import DataController
from Controllers.projet_controller import ProjetController
from Controllers.projet_controller import EditableTabBar
from Controllers.ui_controller import UiController
from Controllers.image_controller import ImageController
from Models.text_item import TextColonneteItem

class MainWindow(QMainWindow):
    '''
    Fenêtre principale de l'application Générateur de fiches.

    Intègre une interface utilisateur permettant de créer, afficher et exporter
    des images générées à partir de données pandas DataFrame.
    '''

    def __init__(self):
        '''
        Initialise la fenêtre principale et ses composants.
        '''
        super().__init__()
        self.setWindowTitle('Générateur de fiches')
        self.setGeometry(0, 0, 1200, 720)  # Définit la taille initiale de la fenêtre
        self.imageViewActif = None  # Référence à l'ImageView actuellement actif
        self._setupUI()  # Configuration de l'interface utilisateur
        self.itemWidget = ItemWidget(self.proprietesWidget)

    def _setupUI(self):
        self._setupCentralWidget()
        self._setupControllers()
        self._setupDockWidgets()
        self._setupMenuBar()
        self._connectSignals()
        
    def _setupCentralWidget(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.tabWidget = QTabWidget(self)
        layout.addWidget(self.tabWidget)        

    def _setupControllers(self):
        self.dataController = DataController()
        self.projetController = ProjetController(self, self.tabWidget)
        self.itemWidget = ItemWidget(self)
        self.imageController = ImageController(self, self.itemWidget)
        self.proprietesWidget = ProprietesWidget(imageController=self.imageController, parent=self)
        self.tabWidget.setTabBar(EditableTabBar())
        self.tabWidget.setTabsClosable(True)

    def _setupDockWidgets(self):
        self.boiteOutils = BoiteOutils(self, self.dataController, self.imageController)
        self.boiteOutilsDockWidget = self._createLeftDockWidget('Boîte à outils', self.boiteOutils)
        self.dataView = DataView(self)
        self.dataDockWidget = self._createLeftDockWidget('Tableau', self.dataView)
        self.proprietesDockWidget = self._createRightDockWidget('Propriétés', self.proprietesWidget)
        self.itemDockWidget = self._createRightDockWidget('Items', self.itemWidget)
        self.uiController = UiController(self.tabWidget, self.dataDockWidget, self.proprietesDockWidget, self.itemWidget, self.itemDockWidget, self.boiteOutilsDockWidget)

    def _setupMenuBar(self):
        self.menuBarre = MenuBarre(self, self.tabWidget, self.dataController, self.projetController)
        self.setMenuBar(self.menuBarre)

    def _connectSignals(self):
        self.dataView.colonneAjoutee.connect(self.onColonneAjoutee)
        self.dataController.fileImported.connect(self.dataView.load_data)
        self.tabWidget.currentChanged.connect(self.uiController.ongletChange)
        self.tabWidget.tabCloseRequested.connect(self.uiController.fermerOnglet)
        self.itemWidget.itemSelected.connect(self.onItemSelected)     
        self.proprietesWidget.xChanged.connect(self.imageController.onXChanged)
        self.proprietesWidget.yChanged.connect(self.imageController.onYChanged) 
        self.proprietesWidget.fontStyleChanged.connect(self.imageController.onFontStyleChanged)  
        self.proprietesWidget.fontSizeChanged.connect(self.imageController.onFontSizeChanged)
        self.proprietesWidget.fontColorChanged.connect(self.imageController.onFontColorChanged)
        self.proprietesWidget.largeurChanged.connect(self.imageController.onLargeurChanged)
        self.proprietesWidget.hauteurChanged.connect(self.imageController.onHauteurChanged)
    
    def _createRightDockWidget(self, title, widget):
        dockWidget = QDockWidget(title, self)
        dockWidget.setWidget(widget)
        self.addDockWidget(Qt.RightDockWidgetArea, dockWidget)
        return dockWidget
    
    def _createLeftDockWidget(self, title, widget):
        dockWidget = QDockWidget(title, self)
        dockWidget.setWidget(widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)
        return dockWidget

    def _createTabWidget(self):
        tabWidget = QTabWidget(self)
        tabWidget.setTabsClosable(True)
        return tabWidget

    def onColonneAjoutee(self, textItem):
        if self.imageViewActif:
            self.imageViewActif.ajouterItem(textItem)

    def onItemSelected(self, item):
        if isinstance(item, TextColonneteItem):
            try:
                self.proprietesWidget.setXandY(item.x, item.y)
            except ValueError:
                QMessageBox.critical(None, 'Erreur Valeur', f'Erreur : les valeurs \'x\' et \'y\' doivent être des nombres entiers. \n x :{item.x} y :{item.y}')
                print('Erreur : les valeurs x et y doivent être des nombres entiers.')
            