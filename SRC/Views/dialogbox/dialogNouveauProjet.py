from typing import Tuple, Optional
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)

"""////////////////////////////////////////////
Ouvre une boîte de dialogue lorsque l'utilisateur
créé unnouveau projet et retourne les info saisies
////////////////////////////////////////////"""


class DialogNouveauProjet(QDialog):
    def __init__(self, parent=None) -> None:
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

    def getDimensions(self) -> Optional[Tuple[int, int]]:
        """Retourne les dimensions saisies par l'utilisateur."""
        largeur = self.largeurEdit.text()
        hauteur = self.hauteurEdit.text()

        # Vérifie si les champs sont vides
        if not largeur or not hauteur:
            QMessageBox.warning(
                None,
                "Attention !",
                "Veuillez entrer des valeurs pour la largeur et la hauteur.",
            )
            return None, None
        else:
            return largeur, hauteur
