import os
import time
from PySide6.QtWidgets import QFileDialog, QApplication, QTabBar, QMessageBox, QLineEdit
from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QImage, QPainter, QFont, QPixmap
from Views.image_view import ImageView
from Views.dialogbox.progressbar import ProgressBar
from Models.text_item import TextColonneteItem, TextUniqueItem, ImageUniqueItem

class ProjetController(QObject):
    def __init__(self, mainWindow, tabWidget):
        self.mainWindow = mainWindow
        self.tabWidget = tabWidget

    def creerNouveauProjet(self, largeur, hauteur, tabTitle='Sans Titre'):
        imageView = ImageView(self.mainWindow, imageWidth=largeur, imageHeight=hauteur)
        imageView.createEmptyImage(largeur, hauteur)
        indexNouvelOnglet = self.tabWidget.addTab(imageView, tabTitle)
        self.tabWidget.setCurrentIndex(indexNouvelOnglet)
        self.mainWindow.imageViewActif = imageView

    def exporterProjet(self, imageView):
        if imageView is None or not imageView.items:
            return

        dossier = QFileDialog.getExistingDirectory(None, 'Sélectionner un dossier d\'export')
        if not dossier:
            return
        
        # Séparer les TextColonneteItem et les TextUniqueItem
        imageUniqueItems = [item for item in imageView.items if isinstance(item, ImageUniqueItem)]
        textColonneteItems = [item for item in imageView.items if isinstance(item, TextColonneteItem)]
        textUniqueItems = [item for item in imageView.items if isinstance(item, TextUniqueItem)]

        # Déterminer le nombre maximal de lignes parmi les TextColonneteItem
        nombreLignes = max(len(item.text) for item in textColonneteItems) if textColonneteItems else 1

        tailleImage = imageView.imageLabel.pixmap().size()
        progressBar = ProgressBar(nombreLignes)
        progressBar.show()
        current_image = 0

        dossierExport = 'ProjetExport'
        dossierFinal = os.path.join(dossier, dossierExport)
        if not os.path.exists(dossierFinal):
            os.makedirs(dossierFinal)

        for numLigne in range(nombreLignes):
            image = QImage(tailleImage, QImage.Format_ARGB32)
            image.fill(Qt.white)
            painter = QPainter(image)

            # Dessiner les TextColonneteItem
            for item in textColonneteItems:
                if numLigne < len(item.text):
                    ligne = item.text[numLigne]
                    painter.setFont(QFont(item.font, item.fontSize))
                    painter.drawText(item.x, item.y, ligne)

            # Dessiner les TextUniqueItem sur chaque image
            for item in textUniqueItems:
                painter.setFont(QFont(item.font, item.fontSize))
                painter.drawText(item.x, item.y, item.nom)

            for item in imageUniqueItems:
                imageToDraw = QPixmap(item.imagePath)  # Créer un QPixmap à partir du chemin
                painter.drawPixmap(item.x, item.y, item.height, item.width, imageToDraw)

            painter.end()

            nomFichier = os.path.join(dossierFinal, f'ligne_{numLigne}.png')
            image.save(nomFichier)
            current_image += 1
            time.sleep(0.3)
            progressBar.update_progress(current_image, f'Exportation en cours : ligne_{numLigne}.png')
            QApplication.processEvents()

        progressBar.close()
        QMessageBox.information(None, 'Exportation Status', 'Exportation Terminée !')

class EditableTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mouseDoubleClickEvent(self, event):
        index = self.tabAt(event.position().toPoint())
        if index >= 0:
            self.renameTab(index)

    def renameTab(self, index):
        editor = QLineEdit(self)
        editor.setText(self.tabText(index))
        editor.editingFinished.connect(lambda: self.changeTabTitle(editor, index))
        self.setTabText(index, '')
        self.setTabButton(index, QTabBar.LeftSide, editor)
        editor.selectAll()
        editor.setFocus()

    def changeTabTitle(self, editor, index):
        self.setTabText(index, editor.text())
        self.setTabButton(index, QTabBar.LeftSide, None)
        editor.deleteLater()