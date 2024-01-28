from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class DialogNouveauProjet(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nouveau Projet")
        layout = QVBoxLayout(self)

        # Ajouter des champs pour la largeur et la hauteur
        self.largeurEdit = QLineEdit(self)
        self.hauteurEdit = QLineEdit(self)
        layout.addWidget(QLabel("Largeur:"))
        layout.addWidget(self.largeurEdit)
        layout.addWidget(QLabel("Hauteur:"))
        layout.addWidget(self.hauteurEdit)

        # Ajouter un bouton pour valider
        btnValider = QPushButton("Créer", self)
        btnValider.clicked.connect(self.accept)
        layout.addWidget(btnValider)

    def getDimensions(self):
        """Retourne les dimensions saisies par l'utilisateur."""
        return self.largeurEdit.text(), self.hauteurEdit.text()
