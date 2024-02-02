from PySide6.QtWidgets import QMenuBar, QApplication, QMessageBox, QMenu, QStyle
from PySide6.QtGui import QAction, QIcon
from Views.Widgets.dialogNouveauProjet import DialogNouveauProjet


class MenuBarre(QMenuBar):
    def __init__(
        self, mainWindow, tabWidget=None, dataController=None, projetController=None
    ) -> None:
        super().__init__()
        self.tabWidget = tabWidget
        self.mainWindow = mainWindow
        self.dataController = dataController
        self.projetController = projetController
        self.creerMenus()

    # Ajouter les menus creer
    def creerMenus(self) -> None:
        self.creerFileMenu()
        self.creerEditMenu()
        self.creerAffichageMenu()

    # Création du menu Fichier
    def creerFileMenu(self) -> None:
        # Ajouter le menu
        fileMenu = self.addMenu("Fichier")

        # Creer un nouveau projet
        creerProjetAction = QAction("Nouveau projet", self)
        creerProjetAction.setShortcut("Ctrl+N")
        creerProjetAction.triggered.connect(self.nouveauProjet)

        # importer un fichier
        importFileAction = QAction("Importer un fichier", self)
        importFileAction.setShortcut("Ctrl+O")
        ouvrirFichierIcon = QApplication.style().standardIcon(QStyle.SP_FileIcon)
        importFileAction.setIcon(ouvrirFichierIcon)
        importFileAction.triggered.connect(self.dataController.importFichier)

        # Exporter projet
        exporterProjetAction = QAction("Exporter projet", self)
        exporterProjetAction.setIcon(
            QIcon("RESSOURCES\ASSETS\images\logo\exportation.png")
        )
        exporterProjetAction.triggered.connect(self.exporterProjet)

        # Quitter l'application
        exitAction = QAction("Quitter", self)
        exitAction.setIcon(QIcon("RESSOURCES\ASSETS\images\logo\quitter.png"))
        exitAction.setShortcut("alt+f4")
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
    def creerEditMenu(self) -> None:
        editMenu = self.addMenu("Edition")

    def creerAffichageMenu(self):
        affichageMenu = self.addMenu("Affichage")
        vuesSubMenu = QMenu("Vues", self)
        themesSubMenu = QMenu("Themes", self)

        affichageMenu.addMenu(vuesSubMenu)
        affichageMenu.addMenu(themesSubMenu)

        afficherItemAction = QAction("Afficher Items", self)
        afficherProprieteAction = QAction("Propriétés", self)
        afficherDataViewAction = QAction("Tableau", self)
        afficherBoitOutilsAction = QAction("Boite Outils", self)

        themeWindows = QAction("Windows", self)
        themeWindowsVista = QAction("Windows Vista", self)
        themeFusion = QAction("Fusion", self)

        afficherItemAction.setShortcut("I")
        afficherDataViewAction.setShortcut("T")
        afficherProprieteAction.setShortcut("P")
        afficherBoitOutilsAction.setShortcut("B")

        afficherBoitOutilsAction.triggered.connect(
            self.mainWindow.uiController.toggleBoiteOutils
        )
        afficherItemAction.triggered.connect(self.mainWindow.uiController.toggleItem)
        afficherProprieteAction.triggered.connect(
            self.mainWindow.uiController.toggleProprietes
        )
        afficherDataViewAction.triggered.connect(
            self.mainWindow.uiController.toggleDataView
        )

        themeWindows.triggered.connect(
            self.mainWindow.uiController.changeThemeVersWindows
        )
        themeWindowsVista.triggered.connect(
            self.mainWindow.uiController.changeThemeVersWindowsVista
        )
        themeFusion.triggered.connect(
            self.mainWindow.uiController.changeThemeVersFusion
        )

        vuesSubMenu.addAction(afficherBoitOutilsAction)
        vuesSubMenu.addAction(afficherItemAction)
        vuesSubMenu.addAction(afficherProprieteAction)
        vuesSubMenu.addAction(afficherDataViewAction)

        themesSubMenu.addAction(themeWindows)
        themesSubMenu.addAction(themeWindowsVista)
        themesSubMenu.addAction(themeFusion)

        # Ajouter les actions
        affichageMenu.addAction

    def nouveauProjet(self) -> None:
        dialog = DialogNouveauProjet(self)
        if dialog.exec():
            largeur, hauteur = dialog.getDimensions()
            try:
                largeur = int(largeur)
                hauteur = int(hauteur)
                self.projetController.creerNouveauProjet(largeur, hauteur)
            except ValueError:
                pass

    def exporterProjet(self) -> None:
        reply = QMessageBox.question(
            None,
            "Exporter le projet",
            "Voulez-vous Exporter le projet ?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.projetController.exporterProjet(self.mainWindow.imageViewActif)
