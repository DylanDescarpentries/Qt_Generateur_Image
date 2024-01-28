from PySide6.QtWidgets import QMenuBar, QApplication, QMessageBox
from PySide6.QtGui import QAction
from Views.dialogbox.dialogNouveauProjet import DialogNouveauProjet
from Views.dialogbox.progressbar import ProgressBar


class MenuBarre(QMenuBar):
    def __init__(self, mainWindow, tabWidget=None, dataController=None, projetController=None):
        super().__init__()
        self.tabWidget = tabWidget
        self.mainWindow = mainWindow
        self.dataController = dataController
        self.projetController = projetController
        self.creerMenus()

    # Ajouter les menus creer 
    def creerMenus(self):
        self.creerFileMenu()
        self.creerEditMenu()
        self.creerAffichageMenu()

    # Création du menu Fichier
    def creerFileMenu(self):
        #Ajouter le menu
        fileMenu = self.addMenu('Fichier')

        # Creer un nouveau projet
        creerProjetAction = QAction('Nouveau projet', self)
        creerProjetAction.setShortcut('Ctrl+N')
        creerProjetAction.triggered.connect(self.nouveauProjet)

        #importer un fichier
        importFileAction = QAction('Importer un fichier', self)
        importFileAction.setShortcut('Ctrl+O')
        importFileAction.triggered.connect(self.dataController.importFile)

        # Exporter projet
        exporterProjetAction = QAction('Exporter projet', self)
        exporterProjetAction.triggered.connect(self.exporterProjet)

        # Quitter l'application
        exitAction = QAction('Quitter', self)
        exitAction.setShortcut('alt+f4')
        exitAction.triggered.connect(QApplication.quit)

        # Ajouter les actions
        fileMenu.addAction(creerProjetAction)
        fileMenu.addAction(importFileAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exporterProjetAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        return fileMenu
    
    # Création du menu Edition
    def creerEditMenu(self):
        editMenu = self.addMenu('Edition')
        testChargementAction = QAction('TestChargement', self)
        testChargementAction.triggered.connect(self.test)

        editMenu.addAction(testChargementAction)

    def creerAffichageMenu(self):
        affichageMenu = self.addMenu('Affichage')
        afficherItemAction = QAction('Afficher Items', self)
        afficherProprieteAction = QAction('Propriétés', self)
        afficherDataViewAction = QAction('Tableau', self)

        afficherItemAction.setShortcut('I')
        afficherDataViewAction.setShortcut('T')
        afficherProprieteAction.setShortcut('P')

        afficherItemAction.triggered.connect(self.mainWindow.uiController.toggleProprietes)
        afficherProprieteAction.triggered.connect(self.mainWindow.uiController.toggleProprietes)
        afficherDataViewAction.triggered.connect(self.mainWindow.uiController.toggleDataView)

        affichageMenu.addAction(afficherItemAction)
        affichageMenu.addAction(afficherProprieteAction)
        affichageMenu.addAction(afficherDataViewAction)

        #Ajouter les actions
        affichageMenu.addAction

    def nouveauProjet(self):
        dialog = DialogNouveauProjet(self)
        if dialog.exec():
            largeur, hauteur = dialog.getDimensions()
            try:
                largeur = int(largeur)
                hauteur = int(hauteur)
                self.projetController.creerNouveauProjet(largeur, hauteur)
            except ValueError:
                pass
    
    def exporterProjet(self):
        reply = QMessageBox.question(None, "Exporter le projet", "Voulez-vous Exporter le projet ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if hasattr(self.mainWindow, 'imageViewActif') and self.mainWindow.imageViewActif is not None:
                self.projetController.exporterProjet(self.mainWindow.imageViewActif)
            else:
                QMessageBox.information(None, 'Évènement Inattendu !', 'Aucun projet à exporter !')

    def test(self):
        # Créez une instance de la classe ProgressBar
        progress_dialog = ProgressBar(self)
        progress_dialog.exec_()