from Views.image_view import ImageView

class UiController:
    def __init__(self,tabWidget, dataViewDockWidget, proprieteDockWidget, itemWidget):
        self.dataViewDockWidget = dataViewDockWidget
        self.proprieteDockWidget = proprieteDockWidget
        self.tabWidget = tabWidget
        self.itemWidget = itemWidget

    def toggleDataView(self):
        # Basculer la visibilité de DataView DockWidget
        self.dataViewDockWidget.setVisible(not self.dataViewDockWidget.isVisible())

    def toggleProprietes(self):
        # Basculer la visibilité de Proprietes DockWidget
        self.proprieteDockWidget.setVisible(not self.proprieteDockWidget.isVisible())

    def ongletChange(self, index):
        imageView = self.tabWidget.widget(index)
        if isinstance(imageView, ImageView):
            # Supposons que imageViewActif est défini quelque part dans votre contrôleur
            self.imageViewActif = imageView
            imageView.itemAdded.connect(self.itemWidget.addItem)
        else:
            self.imageViewActif = None


    def fermerOnglet(self, index):
        """
        Ferme l'onglet spécifié dans le QTabWidget.
        :param index: L'index de l'onglet à fermer.
        """
        self.tabWidget.removeTab(index)