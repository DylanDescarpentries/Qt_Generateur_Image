import os
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QImage, QPainter, QFont
from Views.image_view import ImageView
from Models.text_item import TextItem

class ProjetController(QObject):
    def __init__(self, mainWindow, tabWidget):
        self.mainWindow = mainWindow
        self.tabWidget = tabWidget

    def creerNouveauProjet(self, largeur, hauteur):
        imageView = ImageView(self.mainWindow, imageWidth=largeur, imageHeight=hauteur)
        imageView.createEmptyImage(largeur, hauteur)
        indexNouvelOnglet = self.tabWidget.addTab(imageView, "Sans titre")
        self.tabWidget.setCurrentIndex(indexNouvelOnglet)
        self.mainWindow.imageViewActif = imageView


    def exporterProjet(self, imageView):
        """
        Exporte l'image de l'ImageView en respectant les paramètres et annotations.
        :param imageView: L'instance d'ImageView à exporter.
        """
        if imageView is None or not imageView.colonnes:
            print("Aucune image à exporter ou aucune colonne annotée.")
            return

        dossier = QFileDialog.getExistingDirectory(None, "Sélectionner un dossier d'export")
        if not dossier:
            return

        # Déterminer le nombre maximal de lignes parmi toutes les colonnes
        nombreLignes = max(len(colonne['donnees']) for colonne in imageView.colonnes)

        for i in range(nombreLignes):
            image = QImage(imageView.imageLabel.pixmap().size(), QImage.Format_RGB32)
            image.fill(Qt.white)
            painter = QPainter(image)
            painter.setFont(QFont('Arial', 12))
            
            y_offset = 50
            for colonne in imageView.colonnes:
                valeur = colonne['donnees'][i] if i < len(colonne['donnees']) else ""
                painter.drawText(10, y_offset, f"{colonne['nom']}: {valeur}")
                y_offset += 20
            
            painter.end()
            
            nomFichier = os.path.join(dossier, f"ligne_{i}.png")
            image.save(nomFichier)

        print("Exportation terminée.")