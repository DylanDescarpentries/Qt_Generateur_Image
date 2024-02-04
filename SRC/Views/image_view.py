"""///////////////////////////////////////////////////////////////////////////
    Widget pour afficher et manipuler des images dans le Générateur de fiches.

    Permet d'afficher une image vide ou chargée, d'ajouter des annotations
    textuelles et d'exporter l'image résultante.
////////////////////////////////////////////////////////////////////////////"""

import logging
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtGui import QPixmap, QPainter, QFont, QBrush, QColor, QPen
from PySide6.QtCore import Qt, Signal, QRect
from Models.itemsModels import *


class ImageView(QWidget):
    itemAdded = Signal(TextColonneItem)

    def __init__(self, parent=None, largeur: int = 800, hauteur: int = 600) -> None:
        """
        Initialise ImageView avec une image vide de dimensions spécifiées.

        :param parent: Widget parent de cet ImageView.
        :param imageLargeur: Largeur de l'image vide initiale.
        :param imageHauteur: Hauteur de l'image vide initiale.
        """
        super().__init__(parent)
        self.largeur = largeur
        self.hauteur = hauteur
        self.layout = QVBoxLayout(self)
        self.imageLabel = QLabel()
        self.layout.addWidget(self.imageLabel)
        self.creerImageVide(largeur, hauteur)
        self.items = []  # Stocke les informations sur les colonnes ajoutées

    def creerImageVide(self, largeur, hauteur) -> None:
        """
        Crée et affiche une image vide de dimensions spécifiées.

        :param largeur: Largeur de l'image vide.
        :param hauteur: Hauteur de l'image vide.
        """
        videPixmap = QPixmap(largeur, hauteur)
        videPixmap.fill(Qt.white)
        self.imageLabel.setPixmap(videPixmap)

    def afficherNomColonne(self, nomColonne, donnees) -> None:
        """
        Ajoute une annotation textuelle pour une colonne de données sur l'image.

        :param nomColonne: Le nom de la colonne à annoter.
        :param donnees: Les données de la colonne à utiliser pour l'annotation.
        """
        self.colonnes.append({"nom": nomColonne, "donnees": donnees})
        self.mettreAJourImage()

    def ajouterItem(self, item) -> None:
        item.index = len(self.items)
        self.items.append(item)
        self.itemAdded.emit(item)
        self.mettreAJourImage()

    def supprimerItem(self, itemToDelete) -> None:
        if itemToDelete in self.items:
            self.items.remove(itemToDelete)
        self.mettreAJourLesIndex()
        self.mettreAJourImage()

    def reordonnerItems(self, nouveauxItems) -> None:
        # Met à jour l'ordre des items graphiques selon `nouveauxItems`
        self.items = nouveauxItems
        self.mettreAJourLesIndex()
        self.mettreAJourImage()

    def mettreAJourLesIndex(self):
        # Met à jout l'ordre des items aprèes une suppression
        for i, item in enumerate(self.items):
            item.index = i

    def mettreAJourImage(self) -> None:
        try:
            pixmap = QPixmap(self.imageLabel.pixmap().size())
            pixmap.fill(Qt.white)
            painter = QPainter(pixmap)

            sortedItems = sorted(self.items, key=lambda item: item.index)

            for item in sortedItems:
                if isinstance(item, TextUniqueItem) or isinstance(
                    item, TextColonneItem
                ):
                    # réinitialise le brush
                    painter.setBrush(Qt.NoBrush)
                    rect = QRect(item.x, item.y, item.largeur, item.hauteur)
                    painter.drawRect(rect)
                    painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))

                    painter.setFont(QFont(item.font, item.fontSize))
                    painter.setPen(QPen(QColor(item.fontColor)))
                    painter.drawText(
                        rect,
                        Qt.AlignLeft | Qt.AlignVCenter | Qt.TextWordWrap,
                        str(item.nom),
                    )
                elif isinstance(item, ImageUniqueItem):
                    imageToDraw = QPixmap(item.imagePath)
                    painter.drawPixmap(
                        item.x, item.y, item.largeur, item.hauteur, imageToDraw
                    )
                elif isinstance(item, ImageColonneItem):
                    imageToDraw = QPixmap(item.nom)
                    painter.drawPixmap(
                        item.x, item.y, item.largeur, item.hauteur, imageToDraw
                    )
                elif isinstance(item, FormeGeometriqueItem):
                    # Configurer la brosse pour le remplissage
                    brush = QBrush(Qt.SolidPattern)
                    brush.setColor(QColor(item.color))
                    painter.setBrush(brush)  # Appliquer le brush pour le remplissage
                    # Dessiner la forme géométrique avec remplissage
                    painter.drawRoundedRect(
                        item.x,
                        item.y,
                        item.largeur,
                        item.hauteur,
                        item.radius,
                        item.radius,
                    )

            painter.end()
            self.imageLabel.setPixmap(pixmap)
        except Exception as e:
            logging.error(f"Rafraichissement Image \n {e}", exc_info=True)
            QMessageBox.critical(
                None,
                "Rafraichissement Image ",
                f"Problème lors du Rafraichissement de l'image: \n{e}.",
            )

    def afficherElementLePlusGrand(self, text_colonne_items):
        for item in text_colonne_items:
            longest_element = max(item.text, key=lambda x: len(str(x)))
            item.nom = longest_element
        self.mettreAJourImage()
