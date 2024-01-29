import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QPainter, QFont
from PySide6.QtCore import Qt, Signal
from Models.text_item import TextColonneteItem, ImageUniqueItem

'''///////////////////////////////////////////////////////////////////////////
    Widget pour afficher et manipuler des images dans le Générateur de fiches.

    Permet d'afficher une image vide ou chargée, d'ajouter des annotations
    textuelles et d'exporter l'image résultante.
////////////////////////////////////////////////////////////////////////////'''
class ImageView(QWidget):
    itemAdded = Signal(TextColonneteItem)

    def __init__(self, parent=None, imageWidth=800, imageHeight=600):
        '''
        Initialise ImageView avec une image vide de dimensions spécifiées.

        :param parent: Widget parent de cet ImageView.
        :param imageWidth: Largeur de l'image vide initiale.
        :param imageHeight: Hauteur de l'image vide initiale.
        '''
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.imageLabel = QLabel()
        self.layout.addWidget(self.imageLabel)
        self.createEmptyImage(imageWidth, imageHeight)
        self.textItems = []  # Stocke les informations sur les colonnes ajoutées

    def createEmptyImage(self, width, height):
        '''
        Crée et affiche une image vide de dimensions spécifiées.

        :param width: Largeur de l'image vide.
        :param height: Hauteur de l'image vide.
        '''
        emptyPixmap = QPixmap(width, height)
        emptyPixmap.fill(Qt.white)
        self.imageLabel.setPixmap(emptyPixmap)

    def afficherNomColonne(self, nomColonne, donnees):
        '''
        Ajoute une annotation textuelle pour une colonne de données sur l'image.

        :param nomColonne: Le nom de la colonne à annoter.
        :param donnees: Les données de la colonne à utiliser pour l'annotation.
        '''
        self.colonnes.append({'nom': nomColonne, 'donnees': donnees})
        self.mettreAJourImage()

    def ajouterTextItem(self, textItem):
        self.textItems.append(textItem)
        self.itemAdded.emit(textItem)
        self.mettreAJourImage() 

    def mettreAJourImage(self):
        pixmap = QPixmap(self.imageLabel.pixmap().size())
        pixmap.fill(Qt.white)
        painter = QPainter(pixmap)

        for item in self.textItems:
            if hasattr(item, 'font') and hasattr(item, 'fontSize'):
                painter.setFont(QFont(item.font, item.fontSize))
                painter.drawText(item.x, item.y, item.nom)
            elif isinstance(item, ImageUniqueItem):
                imageToDraw = QPixmap(item.imagePath)
                painter.drawPixmap(item.x, item.y, item.width, item.height, imageToDraw)

        painter.end()
        self.imageLabel.setPixmap(pixmap)
