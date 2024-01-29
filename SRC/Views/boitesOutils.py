from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget, QListWidgetItem

class BoiteOutils(QWidget):
    def __init__(self, mainWindow, dataController, imageController):
        super().__init__()
        self.mainWindow = mainWindow
        self.dataController = dataController
        self.imageController = imageController
        self.layout = QGridLayout(self)

        # Création des boutons
        self.tableauImport = QPushButton('Importer Tableau')
        self.textAjout = QPushButton('Ajouter un texte')
        self.ImageAjout = QPushButton('Ajouter Image')
        # Ajout des boutons au layout en spécifiant la ligne et la colonne
        self.layout.addWidget(self.tableauImport, 0, 0)
        self.layout.addWidget(self.textAjout, 1, 0)
        self.layout.addWidget(self.ImageAjout, 1, 1)

        # Connexion du signal clicked au slot importFile
        self.tableauImport.clicked.connect(self.dataController.importFile)
        self.textAjout.clicked.connect(self.imageController.onTextAjout)
        self.ImageAjout.clicked.connect(self.imageController.onImageAjout)

