"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"
Ce module contient la classe DataController, responsable de la gestion des données,
notamment l'importation des fichiers et la manipulation des DataFrames pandas.
""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
import os, logging
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

        ouvrirProjetMenu = QMenu("Ouvrir un projet", self)

        # création des sous-menu d'ouvrir projet
        projetExistants = (
            self.listeProjetExistant()
        )  # récupère la liste des projets existant
        for sauvegarde in projetExistants:
            actionProjet = QAction(sauvegarde, self)
            actionProjet.triggered.connect(
                lambda checked: self.projetController.chargerProjet(sauvegarde)
            )
            ouvrirProjetMenu.addAction(actionProjet)

        # importer un fichier
        importFileAction = QAction("Importer un fichier", self)
        importFileAction.setShortcut("Ctrl+O")
        ouvrirFichierIcon = QApplication.style().standardIcon(QStyle.SP_FileIcon)
        importFileAction.setIcon(ouvrirFichierIcon)
        importFileAction.triggered.connect(self.dataController.importFichier)

        # Sauvegarder le projet
        sauvegarderProjetAction = QAction("Sauvegarder", self)
        sauvegarderProjetAction.setShortcut("Ctrl+S")
        sauvegarderProjetAction.triggered.connect(
            self.projetController.preparerLaSauvegarde
        )

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
        fileMenu.addMenu(ouvrirProjetMenu)
        fileMenu.addAction(creerProjetAction)
        fileMenu.addAction(importFileAction)
        fileMenu.addSeparator()
        fileMenu.addAction(sauvegarderProjetAction)
        fileMenu.addAction(exporterProjetAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        return fileMenu

    # Création du menu Edition
    def creerEditMenu(self) -> None:
        editMenu = self.addMenu("Edition")

    # Création du menu Affichage
    def creerAffichageMenu(self):

        # création menu
        affichageMenu = self.addMenu("Affichage")
        vuesSubMenu = QMenu("Vues", self)
        themesSubMenu = QMenu("Themes", self)
        afficherElementSetup = QAction("Afficher l'élément le plus long", self, checkable=True)
        raffraichirImageAction = QAction("Rafraichir image", self)

        affichageMenu.addAction(raffraichirImageAction)
        affichageMenu.addMenu(vuesSubMenu)
        affichageMenu.addMenu(themesSubMenu)
        affichageMenu.addAction(afficherElementSetup)

        afficherItemAction = QAction("Afficher Items", self)
        afficherProprieteAction = QAction("Propriétés", self)
        afficherDataViewAction = QAction("Tableau", self)
        afficherBoitOutilsAction = QAction("Boite Outils", self)

        themeWindows = QAction("Windows", self)
        themeWindowsVista = QAction("Windows Vista", self)
        themeFusion = QAction("Fusion", self)

        # raccourcis clavier
        afficherElementSetup.setShortcut("Ctrl+I")
        afficherItemAction.setShortcut("I")
        afficherDataViewAction.setShortcut("T")
        afficherProprieteAction.setShortcut("P")
        afficherBoitOutilsAction.setShortcut("B")

        # connexion des menus avec leur methode associées
        raffraichirImageAction.triggered.connect(self.mainWindow.imageViewActif.mettreAJourImage)
        afficherElementSetup.triggered.connect(self.dataController.switchAffichageElementSetup)
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

        # Ajouter les sous_menus
        vuesSubMenu.addAction(afficherBoitOutilsAction)
        vuesSubMenu.addAction(afficherItemAction)
        vuesSubMenu.addAction(afficherProprieteAction)
        vuesSubMenu.addAction(afficherDataViewAction)


        afficherElementSetup
        themesSubMenu.addAction(themeWindows)
        themesSubMenu.addAction(themeWindowsVista)
        themesSubMenu.addAction(themeFusion)

    def nouveauProjet(self) -> None:
        """
        Lance un dialogue pour créer un nouveau projet avec des dimensions spécifiées par l'utilisateur.
        Crée le projet si l'utilisateur confirme avec des dimensions valides.
        """
        dialog = DialogNouveauProjet(self)
        if dialog.exec():
            largeur, hauteur = dialog.getDimensions()
            try:
                largeur = int(largeur)
                hauteur = int(hauteur)
                self.projetController.creerNouveauProjet(largeur, hauteur)
            except ValueError:
                pass

    def listeProjetExistant(self) -> list:
        dossierSauvegarde = "RESSOURCES/sauvegarde"
        projetsExistants = []
        try:
            fichiers = os.listdir(dossierSauvegarde)
            for fichier in fichiers:
                if fichier.endswith(".json"):
                    projetsExistants.append(fichier)
        except Exception as e:
            logging.error(
                f"Erreur lors de la construction de la liste des fichiers de sauvegarde (MenuBarre): \n{e}",
                exc_info=True,
            )
            QMessageBox.critical(
                None,
                "Erreur d'Exportation",
                f"Erreur lors de la construction de la liste des fichiers de sauvegarde (MenuBarre): \n{e}",
            )

        return projetsExistants

    def exporterProjet(self) -> None:
        reply = QMessageBox.question(
            None,
            "Exporter le projet",
            "Voulez-vous Exporter le projet ?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.projetController.exporterProjet(self.mainWindow.imageViewActif)
