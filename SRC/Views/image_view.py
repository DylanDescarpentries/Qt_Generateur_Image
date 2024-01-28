import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QPainter, QFont
from PySide6.QtCore import Qt, Signal
from Models.text_item import TextItem

class ImageView(QWidget):
    """
    Widget pour afficher et manipuler des images dans le Générateur de fiches.

    Permet d'afficher une image vide ou chargée, d'ajouter des annotations
    textuelles et d'exporter l'image résultante.
    """
    itemAdded = Signal(TextItem)

    def __init__(self, parent=None, imageWidth=800, imageHeight=600):
        """
        Initialise ImageView avec une image vide de dimensions spécifiées.

        :param parent: Widget parent de cet ImageView.
        :param imageWidth: Largeur de l'image vide initiale.
        :param imageHeight: Hauteur de l'image vide initiale.
        """
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.imageLabel = QLabel()
        self.layout.addWidget(self.imageLabel)
        self.createEmptyImage(imageWidth, imageHeight)
        self.textItems = []  # Stocke les informations sur les colonnes ajoutées

    def createEmptyImage(self, width, height):
        """
        Crée et affiche une image vide de dimensions spécifiées.

        :param width: Largeur de l'image vide.
        :param height: Hauteur de l'image vide.
        """
        emptyPixmap = QPixmap(width, height)
        emptyPixmap.fill(Qt.white)
        self.imageLabel.setPixmap(emptyPixmap)

    def afficherNomColonne(self, nomColonne, donnees):
        """
        Ajoute une annotation textuelle pour une colonne de données sur l'image.

        :param nomColonne: Le nom de la colonne à annoter.
        :param donnees: Les données de la colonne à utiliser pour l'annotation.
        """
        self.colonnes.append({"nom": nomColonne, "donnees": donnees})
        self.mettreAJourImage()

    def ajouterTextItem(self, textItem):
        self.textItems.append(textItem)  # Ajouter le TextItem à la liste
        self.itemAdded.emit(textItem.nom)
        self.mettreAJourImage()  # Mettre à jour l'image

    def mettreAJourImage(self):
        pixmap = QPixmap(self.imageLabel.pixmap().size())
        pixmap.fill(Qt.white)
        painter = QPainter(pixmap)
        painter.setFont(QFont('Arial', 12))
        
        for item in self.textItems:
            painter.drawText(item.x, item.y, item.text)  # Utiliser les propriétés de TextItem
        painter.end()
        self.imageLabel.setPixmap(pixmap)