from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton, QSpinBox, QLabel, QComboBox)
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import Signal

class ProprietesWidget(QWidget):
    xChanged = Signal(int)
    yChanged = Signal(int)
    def __init__(self, imageController, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        # Controller
        self.imageController = imageController

        """Création des Groupe (section) des Propriétés"""
        # Création du groupe Paramètres
        self.parametreContainer = QGroupBox()
        self.parametreLayout = QVBoxLayout(self.parametreContainer)

        # Création du groupe Texte
        self.texteContainer = QGroupBox()
        self.texteLayout = QVBoxLayout(self.texteContainer)



        # Ajout des éléments de dimensions
        self.dimensionsWidget = QWidget()
        self.dimensionsLayout = QHBoxLayout(self.dimensionsWidget)
        self.largeurEdit = QSpinBox(self.dimensionsWidget)
        self.hauteurEdit = QSpinBox(self.dimensionsWidget)
        self.dimensionsLayout.addWidget(QLabel("Largeur:"))
        self.dimensionsLayout.addWidget(self.largeurEdit)
        self.dimensionsLayout.addWidget(QLabel("Hauteur:"))
        self.dimensionsLayout.addWidget(self.hauteurEdit)
        self.parametreLayout.addWidget(self.dimensionsWidget)

        # Ajout des éléments de positions
        self.positionsWidget = QWidget()
        self.positionsLayout = QHBoxLayout(self.positionsWidget)
        self.xpositionsEdit = QSpinBox(self.positionsWidget)
        self.ypositionsEdit = QSpinBox(self.positionsWidget)
        self.positionsLayout.addWidget(QLabel("Position X :"))
        self.positionsLayout.addWidget(self.xpositionsEdit)
        self.positionsLayout.addWidget(QLabel("Position Y :"))
        self.positionsLayout.addWidget(self.ypositionsEdit)
        self.parametreLayout.addWidget(self.positionsWidget)

        maxValues = 999999
        self.xpositionsEdit.setMaximum(maxValues)
        self.ypositionsEdit.setMaximum(maxValues)


        self.textWidget = QWidget()
        self.texteContainer = QGroupBox()
        self.texteLayout = QVBoxLayout(self.textWidget)

        # Configuration de la ComboBox pour la police
        self.fontSizeChange = QSpinBox(self.textWidget)
        self.fontComboBox = QComboBox(self.textWidget)
        self.fontComboBox.addItems(QFontDatabase().families())
        self.texteLayout.addWidget(QLabel('Taille Police :'))
        self.texteLayout.addWidget(self.fontSizeChange)
        self.fontComboBox.addItem("Charger une police...")
        self.texteLayout.addWidget(QLabel('Changer la police :'))
        
        # Ajout de la ComboBox au layout du groupe de texte
        self.texteLayout.addWidget(self.fontComboBox)

        self.texteContainer.setLayout(self.texteLayout)

        # Ajout du groupe Paramètres au layout principal
        self.layout.addWidget(self.createCollapsibleGroup(self.parametreContainer, "Parametres"))
        self.layout.addWidget(self.createCollapsibleGroup(self.texteContainer, "Texte"))

        #Connexions des SpinBox aux methodes
        self.fontComboBox.currentIndexChanged.connect(self.fontChanged)
        self.xpositionsEdit.valueChanged.connect(self.xChanged.emit)
        self.ypositionsEdit.valueChanged.connect(self.yChanged.emit)

    def createCollapsibleGroup(self, groupBox, title):
        """
        Crée un groupe rétractable avec un en-tête cliquable.

        :param groupBox: Le QGroupBox à rendre rétractable.
        :param title: Le titre de la section.
        :return: QWidget contenant le groupBox et le bouton pour le rétracter.
        """
        container = QWidget()
        containerLayout = QVBoxLayout(container)
        
        # Bouton pour basculer la visibilité
        toggleButton = QPushButton(title)
        toggleButton.setCheckable(True)
        toggleButton.setChecked(True)
        toggleButton.clicked.connect(lambda checked: groupBox.setVisible(checked))
        
        containerLayout.addWidget(toggleButton)
        containerLayout.addWidget(groupBox)
        
        return container
    
    def setXandY(self, x, y):
        self.xpositionsEdit.setValue(x)
        self.ypositionsEdit.setValue(y)
    
    def fontChanged(self, index):
        QComboBox.information(None, 'Information', 'Cette fonctionnalité n\'existe pas encore')