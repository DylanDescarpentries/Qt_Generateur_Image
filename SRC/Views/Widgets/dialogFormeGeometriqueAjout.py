from typing import Tuple, Optional
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QSpinBox
)

"""////////////////////////////////////////////
Ouvre une boîte de dialogue lorsque l'utilisateur
souhaite ajouter une forme Geometrique
et retourne les info saisies
////////////////////////////////////////////"""


class DialogFormeGeometriqueAjout(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Ajouter une forme")
        
        mainLayout = QVBoxLayout(self)
        
        # Zone de choix de la forme
        choixFormeLayout = QHBoxLayout()
        self.carreChoix = QPushButton("Carré", self)
        self.rondChoix = QPushButton("Rond", self)
        choixFormeLayout.addWidget(self.carreChoix)
        choixFormeLayout.addWidget(self.rondChoix)
        
        # Zone de paramètres de la forme
        parametresFormeLayout = QHBoxLayout()
        
        # Largeur
        largeurLayout = QVBoxLayout()
        largeurLabel = QLabel("Largeur :", self)
        self.largeurEdit = QSpinBox(self)
        largeurLayout.addWidget(largeurLabel)
        largeurLayout.addWidget(self.largeurEdit)
        
        # Hauteur
        hauteurLayout = QVBoxLayout()
        hauteurLabel = QLabel("Hauteur :", self)
        self.hauteurEdit = QSpinBox(self)
        hauteurLayout.addWidget(hauteurLabel)
        hauteurLayout.addWidget(self.hauteurEdit)
        
        # Rayon (pour le rond)
        radiusLayout = QVBoxLayout()
        radiusLabel = QLabel("Rayon :", self)
        self.radiusEdit = QSpinBox(self)
        radiusLayout.addWidget(radiusLabel)
        radiusLayout.addWidget(self.radiusEdit)

        # Ajouter un bouton pour valider
        validationLayout = QHBoxLayout()
        btnValider = QPushButton("Créer", self)
        btnAnnuler = QPushButton("Annuler", self)
        btnValider.clicked.connect(self.accept)
        validationLayout.addWidget(btnValider)
        validationLayout.addWidget(btnAnnuler)

        btnValider.clicked.connect(self.accept)

        # Ajouter les layouts de paramètres au layout horizontal
        parametresFormeLayout.addLayout(largeurLayout)
        parametresFormeLayout.addLayout(hauteurLayout)
        parametresFormeLayout.addLayout(radiusLayout)
        
        # Ajouter les sous-layouts au layout principal
        mainLayout.addLayout(choixFormeLayout)
        mainLayout.addLayout(parametresFormeLayout)
        mainLayout.addLayout(validationLayout)

    def getDimensions(self) -> Optional[Tuple[int, int, int]]:
        """Retourne les dimensions saisies par l'utilisateur."""
        largeur = self.largeurEdit.text()
        hauteur = self.hauteurEdit.text()
        radius = self.radiusEdit.text()

        # Vérifie si les champs sont vides
        if not largeur or not hauteur:
            QMessageBox.warning(
                None,
                "Attention !",
                "Veuillez entrer des valeurs pour la largeur et la hauteur.",
            )
            return None, None
        else:
            return largeur, hauteur, radius