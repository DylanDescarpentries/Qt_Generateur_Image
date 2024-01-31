import os
import time
from PySide6.QtWidgets import QFileDialog, QApplication, QTabBar, QMessageBox, QLineEdit, QScrollArea
from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QImage, QPainter, QFont, QPixmap, QPen, QColor
from Views.image_view import ImageView
from Views.dialogbox.progressbar import ProgressBar
from Models.text_item import TextColonneItem, TextUniqueItem, ImageUniqueItem

class ProjetController(QObject):
    def __init__(self, mainWindow, tabWidget):
        self.mainWindow = mainWindow
        self.tabWidget = tabWidget

    def creerNouveauProjet(self, largeur, hauteur, tabTitle='Sans Titre'):
        imageView = ImageView(self.mainWindow, largeur, imageHeight=hauteur)
        imageView.creerImageVide(largeur, hauteur)

        scrollArea = self.creerScroll(imageView)

        indexNouvelOnglet = self.tabWidget.addTab(scrollArea, tabTitle)
        self.tabWidget.setCurrentIndex(indexNouvelOnglet)
        self.mainWindow.imageViewActif = imageView
    
    def creerScroll(self, widget):
        scrollArea = QScrollArea()
        scrollArea.setWidget(widget)
        scrollArea.setWidgetResizable(True)
        return scrollArea

    def exporterProjet(self, imageView):
        if not self.validerImageView(imageView):
            return

        dossierExport = self.selectionnerDossierExport()
        if not dossierExport:
            return

        self.preparerExport(imageView, dossierExport)

    def validerImageView(self, imageView):
        if imageView is None or not imageView.items:
            QMessageBox.warning(None, 'Attention', 'Aucune image à exporter ou aucun élément de texte ajouté.')
            return False
        return True

    def selectionnerDossierExport(self):
        dossier = QFileDialog.getExistingDirectory(None, 'Sélectionner un dossier d\'export')
        if not dossier:
            return None
        dossierFinal = os.path.join(dossier, 'ProjetExport')
        if not os.path.exists(dossierFinal):
            os.makedirs(dossierFinal)
        return dossierFinal

    def preparerExport(self, imageView, dossierExport):
        textColonneteItems, textUniqueItems, imageUniqueItems = self.classifierItems(imageView)
        nombreLignes = self.determinerNombreLignes(textColonneteItems)
        tailleImage = imageView.imageLabel.pixmap().size()
        progressBar = self.creerProgressBar(nombreLignes)
        
        self.effectuerExport(textColonneteItems, textUniqueItems, imageUniqueItems, nombreLignes, tailleImage, dossierExport, progressBar)

    def classifierItems(self, imageView):
        imageUniqueItems = [item for item in imageView.items if isinstance(item, ImageUniqueItem)]
        textColonneteItems = [item for item in imageView.items if isinstance(item, TextColonneItem)]
        textUniqueItems = [item for item in imageView.items if isinstance(item, TextUniqueItem)]
        return textColonneteItems, textUniqueItems, imageUniqueItems

    def determinerNombreLignes(self, textColonneteItems):
        return max(len(item.text) for item in textColonneteItems) if textColonneteItems else 1

    def creerProgressBar(self, nombreLignes):
        progressBar = ProgressBar(nombreLignes)
        progressBar.show()
        return progressBar

    def effectuerExport(self, textColonneteItems, textUniqueItems, imageUniqueItems, nombreLignes, tailleImage, dossierExport, progressBar):
        current_image = 0
        for numLigne in range(nombreLignes):
            image = QImage(tailleImage, QImage.Format_ARGB32)
            image.fill(Qt.white)
            painter = QPainter(image)
            self.dessinerItems(painter, imageUniqueItems, textColonneteItems, textUniqueItems, numLigne)
            painter.end()

            self.sauvegarderImage(image, dossierExport, numLigne)
            self.mettreAJourProgressBar(progressBar, current_image, numLigne)
            current_image += 1

        progressBar.close()

    def dessinerItems(self, painter, imageUniqueItems, textColonneteItems, textUniqueItems, numLigne):
        # Dessiner les ImageUniqueItem
        for item in imageUniqueItems:
            imageToDraw = QPixmap(item.imagePath)
            painter.drawPixmap(item.x, item.y, item.largeur, item.hauteur, imageToDraw)

        # Dessiner les TextColonneteItem
        for item in textColonneteItems:
            if numLigne < len(item.text):
                ligne = item.text[numLigne]
                self.configurerStyloEtTexte(painter, item, ligne)

        # Dessiner les TextUniqueItem
        for item in textUniqueItems:
            self.configurerStyloEtTexte(painter, item, item.nom)

    def configurerStyloEtTexte(self, painter, item, texte):
        painter.setFont(QFont(item.font, item.fontSize))
        color = QColor(item.fontColor)
        pen = QPen(color)
        painter.setPen(pen)
        painter.drawText(item.x, item.y, texte)

    def sauvegarderImage(self, image, dossierExport, numLigne):
        nomFichier = os.path.join(dossierExport, f'ligne_{numLigne}.png')
        image.save(nomFichier)

    def mettreAJourProgressBar(self, progressBar, current_image, numLigne):
        progressBar.update_progress(current_image + 1, f'Exportation en cours : image_{numLigne}.png')
        QApplication.processEvents()
        time.sleep(0.1)

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