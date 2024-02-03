from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget


class BoiteOutils(QWidget):
    """
    Vue pour afficher le Widgets contenant les outils pour la création de projet
    """

    def __init__(self, mainWindow, dataController, imageController) -> None:
        super().__init__()
        self.mainWindow = mainWindow
        self.dataController = dataController
        self.imageController = imageController
        self.layout = QGridLayout(self)

        # Création des boutons
        self.tableauImport = QPushButton("Importer Tableau")
        self.textAjout = QPushButton("Ajouter un texte")
        self.formeGemotriqueAjout = QPushButton("Ajouter une Forme")
        self.ImageAjout = QPushButton("Ajouter Image")

        # Ajout des boutons au layout en spécifiant la ligne et la colonne
        self.layout.addWidget(self.tableauImport, 0, 0)
        self.layout.addWidget(self.textAjout, 0, 1)
        self.layout.addWidget(self.formeGemotriqueAjout, 1, 0)
        self.layout.addWidget(self.ImageAjout, 1, 1)

        # Connexion du signal clicked au slot importFile
        self.tableauImport.clicked.connect(self.dataController.importFichier)
        self.textAjout.clicked.connect(self.imageController.onTextAjout)
        self.ImageAjout.clicked.connect(self.imageController.onImageAjout)
        self.formeGemotriqueAjout.clicked.connect(
            self.imageController.onFormeGeometriqueAjout
        )
