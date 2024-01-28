from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton, QSpinBox, QLabel)

class ProprietesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Création du groupe Paramètres
        self.parametreContainer = QGroupBox()
        self.parametreLayout = QVBoxLayout(self.parametreContainer)

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
        self.positionsLayout.addWidget(QLabel("Position X:"))
        self.positionsLayout.addWidget(self.xpositionsEdit)
        self.positionsLayout.addWidget(QLabel("Position Y:"))
        self.positionsLayout.addWidget(self.ypositionsEdit)
        self.parametreLayout.addWidget(self.positionsWidget)

        # Ajout du groupe Paramètres au layout principal
        self.layout.addWidget(self.createCollapsibleGroup(self.parametreContainer, "Parametres"))

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

    def applyChanges(self):
        # Appliquez les changements à l'élément sélectionné dans la liste
        selectedItem = self.parent().itemWidget.itemsList.currentItem()
        if selectedItem:
            textItem = self.parent().itemWidget.getTextItemFor(selectedItem)
            textItem.x = self.xpositionsEdit.value()
            textItem.y = self.ypositionsEdit.value()
            self.parent().imageViewActif.mettreAJourImage()
