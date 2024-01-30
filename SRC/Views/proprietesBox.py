from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton, QSpinBox, QLabel, QComboBox, QColorDialog, QFileDialog
from PySide6.QtGui import QFontDatabase, QColor
from PySide6.QtCore import Signal

class ProprietesWidget(QWidget):
    xChanged = Signal(int)
    yChanged = Signal(int)
    fontStyleChanged = Signal(str)
    fontSizeChanged = Signal(int)
    largeurChanged = Signal(int)
    hauteurChanged = Signal(int)
    fontColorChanged = Signal(str)

    def __init__(self, imageController, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.imageController = imageController

        self.setupParametreGroup()
        self.setupTexteGroup()

        # Ajout des groupes au layout principal
        self.layout.addWidget(self.createCollapsibleGroup(self.parametreContainer, 'Parametres'))
        self.layout.addWidget(self.createCollapsibleGroup(self.texteContainer, 'Texte'))

    def setupParametreGroup(self):
        self.parametreContainer = QGroupBox()
        self.parametreLayout = QVBoxLayout(self.parametreContainer)

        self.setupDimensionsWidget()
        self.setupPositionsWidget()

        self.parametreContainer.setLayout(self.parametreLayout)

    def setupDimensionsWidget(self):
        self.dimensionsWidget = QWidget()
        self.dimensionsLayout = QHBoxLayout(self.dimensionsWidget)
        self.largeurEdit = QSpinBox(self.dimensionsWidget)
        self.hauteurEdit = QSpinBox(self.dimensionsWidget)
        self.dimensionsLayout.addWidget(QLabel('Largeur:'))
        self.dimensionsLayout.addWidget(self.largeurEdit)
        self.dimensionsLayout.addWidget(QLabel('Hauteur:'))
        self.dimensionsLayout.addWidget(self.hauteurEdit)
        self.parametreLayout.addWidget(self.dimensionsWidget)

        maxValues = 999999
        self.largeurEdit.setMaximum(maxValues)
        self.hauteurEdit.setMaximum(maxValues)
        # Connexions des SpinBox
        self.largeurEdit.valueChanged.connect(self.largeurChanged.emit)
        self.hauteurEdit.valueChanged.connect(self.hauteurChanged.emit)

    def setupPositionsWidget(self):
        self.positionsWidget = QWidget()
        self.positionsLayout = QHBoxLayout(self.positionsWidget)
        self.xpositionsEdit = QSpinBox(self.positionsWidget)
        self.ypositionsEdit = QSpinBox(self.positionsWidget)

        maxValues = 999999
        self.xpositionsEdit.setMaximum(maxValues)
        self.ypositionsEdit.setMaximum(maxValues)

        self.positionsLayout.addWidget(QLabel('Position X :'))
        self.positionsLayout.addWidget(self.xpositionsEdit)
        self.positionsLayout.addWidget(QLabel('Position Y :'))
        self.positionsLayout.addWidget(self.ypositionsEdit)
        self.parametreLayout.addWidget(self.positionsWidget)

        # Connexions des SpinBox
        self.xpositionsEdit.valueChanged.connect(self.xChanged.emit)
        self.ypositionsEdit.valueChanged.connect(self.yChanged.emit)

    def setupTexteGroup(self):
        self.texteContainer = QGroupBox("Texte")
        self.texteLayout = QVBoxLayout(self.texteContainer)

        self.setupFontComboBox()
        self.setupFontSizeSpinBox()
        self.setupFontColor()

        # Définir le layout pour texteContainer
        self.texteContainer.setLayout(self.texteLayout)

    def setupFontComboBox(self):
        self.fontEdit = QComboBox(self)
        self.fontEdit.addItems(QFontDatabase().families())
        self.fontEdit.addItem('Charger une police...')
        self.texteLayout.addWidget(QLabel('Changer la police :'))
        self.texteLayout.addWidget(self.fontEdit)
        self.fontEdit.currentIndexChanged.connect(self.onFontComboBoxChanged)
        self.fontEdit.currentTextChanged.connect(self.fontStyleChanged.emit)

    def setupFontSizeSpinBox(self):
        self.fontSizeEdit = QSpinBox(self)
        self.texteLayout.addWidget(QLabel('Taille Police :'))
        self.texteLayout.addWidget(self.fontSizeEdit)
        self.fontSizeEdit.valueChanged.connect(self.fontSizeChanged.emit)
    
    def setupFontColor(self):
        self.fontColorEdit = QPushButton('Choisir une couleur', self)
        self.texteLayout.addWidget(self.fontColorEdit)
        self.fontColorEdit.clicked.connect(self.openColorDialog)

    def openColorDialog(self):
        # Définir une couleur initiale
        initialColor = QColor(255, 0, 0)

        # Ouvrir le dialogue de sélection de couleur
        color = QColorDialog.getColor(initialColor, self)

        if color.isValid():
            # Utilisez la couleur sélectionnée ici
            self.fontColorChanged.emit(color.name())

    def createCollapsibleGroup(self, groupBox, title):
        container = QWidget()
        containerLayout = QVBoxLayout(container)
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
    
    def onFontComboBoxChanged(self, index):
        if self.fontEdit.currentText() == "Charger une police...":
            self.loadCustomFont()
        else:
            self.fontStyleChanged.emit(self.fontEdit.currentText())

    def loadCustomFont(self):
        fontFilePath, _ = QFileDialog.getOpenFileName(self, "Sélectionner une police", "", "Font Files (*.ttf *.otf)")
        if fontFilePath:
            fontId = QFontDatabase.addApplicationFont(fontFilePath)
            if fontId != -1:
                fontFamilies = QFontDatabase.applicationFontFamilies(fontId)
                if fontFamilies:
                    customFontFamily = fontFamilies[0]
                    self.fontEdit.addItem(customFontFamily)
                    self.fontEdit.setCurrentText(customFontFamily)
                    self.fontStyleChanged.emit(customFontFamily)
