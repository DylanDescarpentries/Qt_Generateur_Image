import os
import time
from PySide6.QtWidgets import QFileDialog, QApplication, QMessageBox
from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QImage, QPainter, QFont
from Views.image_view import ImageView
from Views.dialogbox.progressbar import ProgressBar

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
        if imageView is None or not imageView.textItems:
            return

        dossier = QFileDialog.getExistingDirectory(None, "Sélectionner un dossier d'export")
        if not dossier:
            return
        
        # Déterminer le nombre maximal de lignes parmi tous les TextItems
        nombreLignes = max(len(textItem.text) for textItem in imageView.textItems)

        tailleImage = imageView.imageLabel.pixmap().size()
        progressBar = ProgressBar(nombreLignes)
        progressBar.show()

        current_image = 0
        for numLigne in range(nombreLignes):
            image = QImage(tailleImage, QImage.Format_RGB32)
            image.fill(Qt.white)
            painter = QPainter(image)

            for textItem in imageView.textItems:
                if numLigne < len(textItem.text):
                    ligne = textItem.text[numLigne]
                    painter.setFont(QFont(textItem.font, textItem.fontSize))
                    painter.drawText(textItem.x, textItem.y, ligne)

            painter.end()

            nomFichier = os.path.join(dossier, f"{ligne}.png")
            image.save(nomFichier)
            current_image += 1
            progressBar.update_progress(current_image, f'Exportation en cours : {ligne}.png')
            QApplication.processEvents()
            time.sleep(0.1)

        progressBar.close()
        QMessageBox.information(None, 'Exportation Status', 'Exportation Terminée !')