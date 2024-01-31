from PySide6.QtWidgets import QScrollArea, QApplication
from Views.image_view import ImageView
class UiController:
    def __init__(self,tabWidget, dataViewDockWidget, proprieteDockWidget, itemWidget, itemDockWidget, boiteOutilsDockWidget):
        self.dataViewDockWidget = dataViewDockWidget
        self.proprieteDockWidget = proprieteDockWidget
        self.itemDockWidget = itemDockWidget
        self.tabWidget = tabWidget
        self.itemWidget = itemWidget
        self.boiteOutilsDockWidget = boiteOutilsDockWidget

    ''' //////////////////////////////////////////
    S'occupe de basculer la visibilité des widget. 
    C'est methode sont appelé par la barre de menu 
    //////////////////////////////////////////'''
    def toggleDataView(self):
        # Basculer la visibilité de DataView DockWidget
        self.dataViewDockWidget.setVisible(not self.dataViewDockWidget.isVisible())

    def toggleProprietes(self):
        # Basculer la visibilité de Proprietes DockWidget
        self.proprieteDockWidget.setVisible(not self.proprieteDockWidget.isVisible())

    def toggleItem(self):
        # Basculer la visibilité de Item DockWidget
        self.itemDockWidget.setVisible(not self.itemDockWidget.isVisible())

    def toggleBoiteOutils(self):
        # Basculer la visibilité de BoiteOutils DockWidget
        self.boiteOutilsDockWidget.setVisible(not self.boiteOutilsDockWidget.isVisible())

    def fermerOnglet(self, index):
        '''
        Ferme l'onglet spécifié dans le QTabWidget.
        :param index: L'index de l'onglet à fermer.
        '''
        self.tabWidget.removeTab(index)

    def changeThemeVersWindows(self):
        QApplication.setStyle('Windows')

    def changeThemeVersFusion(self):
        QApplication.setStyle('Fusion')

    def changeThemeVersWindowsVista(self):
        QApplication.setStyle('windowsvista')

    def ongletChange(self, index):
    # Obtient le widget actuel dans l'onglet, qui est maintenant un QScrollArea
        scrollArea = self.tabWidget.widget(index)
        if isinstance(scrollArea, QScrollArea):
            # Accéder à ImageView à partir de QScrollArea
            imageView = scrollArea.widget()
            if isinstance(imageView, ImageView):
                self.imageViewActif = imageView
                # Connecter les signaux comme avant
                imageView.itemAdded.connect(self.itemWidget.ajouterItemVersListe)
            else:
                self.imageViewActif = None

