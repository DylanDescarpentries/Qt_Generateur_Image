from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
    QLabel,
    QComboBox,
    QColorDialog,
    QFileDialog,
)
from PySide6.QtGui import QFontDatabase, QColor, QFont
from PySide6.QtCore import Signal
from utils.SpinBox import SpinBox


class ProprietesWidget(QWidget):
    xChanged = Signal(int)
    yChanged = Signal(int)
    fontStyleChanged = Signal(str)
    fontSizeChanged = Signal(int)
    largeurChanged = Signal(int)
    hauteurChanged = Signal(int)
    radiusChanged = Signal(int)
    fontColorChanged = Signal(str)
    formColorChanged = Signal(str)

    def __init__(self, imageController, parent=None) -> None:
        super().__init__(parent)
        self.imageController = imageController
        self.layout = QVBoxLayout(self)

        self.setupParametreGroup()
        self.setupTexteGroup()

        # Ajout des groupes au layout principal
        self.layout.addWidget(
            self.creerPliableGroupe(self.parametreContainer, "Parametres")
        )
        self.layout.addWidget(self.creerPliableGroupe(self.texteContainer, "Texte"))

    def setupParametreGroup(self) -> None:
        self.parametreContainer = QGroupBox()
        self.parametreLayout = QVBoxLayout(self.parametreContainer)

        self.setupDimensionsWidget()
        self.setupPositionsWidget()

        self.parametreContainer.setLayout(self.parametreLayout)

    def setupDimensionsWidget(self) -> None:
        self.dimensionsWidget = QWidget()
        self.dimensionsLayout = QHBoxLayout(self.dimensionsWidget)
        self.largeurEdit = SpinBox(self.dimensionsWidget)
        self.hauteurEdit = SpinBox(self.dimensionsWidget)
        self.radiusEdit = SpinBox(self.dimensionsWidget)
        self.dimensionsLayout.addWidget(QLabel("Largeur:"))
        self.dimensionsLayout.addWidget(self.largeurEdit)
        self.dimensionsLayout.addWidget(QLabel("Hauteur:"))
        self.dimensionsLayout.addWidget(self.hauteurEdit)
        self.dimensionsLayout.addWidget(QLabel("Radius:"))
        self.dimensionsLayout.addWidget(self.radiusEdit)
        self.parametreLayout.addWidget(self.dimensionsWidget)

        maxValues = 999999
        self.largeurEdit.setMaximum(maxValues)
        self.hauteurEdit.setMaximum(maxValues)
        self.radiusEdit.setMaximum(maxValues)

        # Connexions des SpinBox
        self.radiusEdit.valueChanged.connect(self.radiusChanged.emit)
        self.largeurEdit.valueChanged.connect(self.largeurChanged.emit)
        self.hauteurEdit.valueChanged.connect(self.hauteurChanged.emit)

    def setupPositionsWidget(self) -> None:
        self.positionsWidget = QWidget()
        self.positionsLayout = QHBoxLayout(self.positionsWidget)
        self.xpositionsEdit = SpinBox(self.positionsWidget)
        self.ypositionsEdit = SpinBox(self.positionsWidget)

        maxValues = 999999
        minValues = -999999
        self.xpositionsEdit.setMaximum(maxValues)
        self.ypositionsEdit.setMaximum(maxValues)
        self.xpositionsEdit.setMinimum(minValues)
        self.ypositionsEdit.setMinimum(minValues)

        self.positionsLayout.addWidget(QLabel("Position X :"))
        self.positionsLayout.addWidget(self.xpositionsEdit)
        self.positionsLayout.addWidget(QLabel("Position Y :"))
        self.positionsLayout.addWidget(self.ypositionsEdit)
        self.parametreLayout.addWidget(self.positionsWidget)

        # Connexions des SpinBox
        self.xpositionsEdit.valueChanged.connect(self.xChanged.emit)
        self.ypositionsEdit.valueChanged.connect(self.yChanged.emit)

    def setupTexteGroup(self) -> None:
        self.texteContainer = QGroupBox()
        self.texteLayout = QVBoxLayout(self.texteContainer)

        self.setupFontComboBox()
        self.setupFontSizeSpinBox()
        self.setupFontColor()
        self.setupFormColor()

        # Définir le layout pour texteContainer
        self.texteContainer.setLayout(self.texteLayout)

    def setupFontComboBox(self) -> None:
        self.fontEdit = QComboBox(self)
        self.fontEdit.addItems(QFontDatabase().families())
        self.fontEdit.addItem("Charger une police...")
        self.texteLayout.addWidget(QLabel("Changer la police :"))
        self.texteLayout.addWidget(self.fontEdit)
        self.fontEdit.currentIndexChanged.connect(self.onFontComboBoxChanged)
        self.fontEdit.currentTextChanged.connect(self.fontStyleChanged.emit)

    def setupFontSizeSpinBox(self) -> None:
        self.fontSizeEdit = SpinBox(self)
        self.texteLayout.addWidget(QLabel("Taille Police :"))
        self.texteLayout.addWidget(self.fontSizeEdit)
        self.fontSizeEdit.valueChanged.connect(self.fontSizeChanged.emit)

    def setupFontColor(self) -> None:
        self.fontColorEdit = QPushButton("Choisir une couleur", self)
        self.texteLayout.addWidget(self.fontColorEdit)
        self.fontColorEdit.clicked.connect(lambda: self.openColorDialog("font"))

    def setupFormColor(self) -> None:
        self.formColorEdit = QPushButton("Choisir une couleur", self)
        self.positionsLayout.addWidget(self.formColorEdit)
        self.formColorEdit.clicked.connect(lambda: self.openColorDialog("form"))

    def openColorDialog(self, source: str) -> None:
        # Définir une couleur initiale
        initialColor = QColor(255, 0, 0)

        # Ouvrir le dialogue de sélection de couleur
        color = QColorDialog.getColor(initialColor, self)

        if color.isValid():
            if source == "font":
                self.fontColorChanged.emit(color.name())
            elif source == "form":
                self.formColorChanged.emit(color.name())

    def creerPliableGroupe(self, groupBox, title: str) -> QWidget:
        container = QWidget()
        containerLayout = QVBoxLayout(container)
        toggleButton = QPushButton(title)
        toggleButton.setStyleSheet("text-align: left;")
        toggleButton.setCheckable(True)
        toggleButton.setChecked(True)
        toggleButton.clicked.connect(lambda checked: groupBox.setVisible(checked))
        containerLayout.addWidget(toggleButton)
        containerLayout.addWidget(groupBox)

        return container

    def setProprietesItemOnButton(
        self,
        x: int,
        y: int,
        largeur: int = None,
        hauteur: int = None,
        couleur: QColor = None,
        police: QFont = None,
        taillePolice: int = None,
    ) -> None:
        self.xpositionsEdit.setValue(x)
        self.ypositionsEdit.setValue(y)
        if largeur is not None:
            self.largeurEdit.setValue(largeur)
        if hauteur is not None:
            self.hauteurEdit.setValue(hauteur)
        if police is not None and taillePolice is not None:
            self.policeEdit.setCurrentFont(police)
            self.taillePoliceEdit.setValue(taillePolice)

    def onFontComboBoxChanged(self) -> None:
        if self.fontEdit.currentText() == "Charger une police...":
            self.loadCustomFont()
        else:
            self.fontStyleChanged.emit(self.fontEdit.currentText())

    def loadCustomFont(self) -> None:
        fontFilePath, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner une police", "", "Font Files (*.ttf *.otf)"
        )
        if fontFilePath:
            fontId = QFontDatabase.addApplicationFont(fontFilePath)
            if fontId != -1:
                fontFamilies = QFontDatabase.applicationFontFamilies(fontId)
                if fontFamilies:
                    customFontFamily = fontFamilies[0]
                    self.fontEdit.addItem(customFontFamily)
                    self.fontEdit.setCurrentText(customFontFamily)
                    self.fontStyleChanged.emit(customFontFamily)
