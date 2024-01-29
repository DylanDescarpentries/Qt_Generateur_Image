from Views.image_view import ImageView

class UiController:
    def __init__(self,tabWidget, dataViewDockWidget, proprieteDockWidget, itemWidget, itemDockWidget):
        self.dataViewDockWidget = dataViewDockWidget
        self.proprieteDockWidget = proprieteDockWidget
        self.itemDockWidget = itemDockWidget
        self.tabWidget = tabWidget
        self.itemWidget = itemWidget

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

    def fermerOnglet(self, index):
        '''
        Ferme l'onglet spécifié dans le QTabWidget.
        :param index: L'index de l'onglet à fermer.
        '''
        self.tabWidget.removeTab(index)

    def ongletChange(self, index):
        '''
        S'occupe de gérer l'onglet actif
        '''
        imageView = self.tabWidget.widget(index)
        if isinstance(imageView, ImageView):
            self.imageViewActif = imageView
            imageView.itemAdded.connect(self.itemWidget.ajouterItemVersListe)
        else:
            self.imageViewActif = None
