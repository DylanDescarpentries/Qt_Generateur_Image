from PySide6.QtWidgets import QScrollArea, QApplication
from Views.image_view import ImageView


class UiController:
    def __init__(
        self,
        tabWidget,
        dataViewDockWidget,
        proprieteDockWidget,
        itemWidget,
        itemDockWidget,
        boiteOutilsDockWidget,
    ):
        self.dataViewDockWidget = dataViewDockWidget
        self.proprieteDockWidget = proprieteDockWidget
        self.itemDockWidget = itemDockWidget
        self.tabWidget = tabWidget
        self.itemWidget = itemWidget
        self.boiteOutilsDockWidget = boiteOutilsDockWidget

    """ //////////////////////////////////////////
    S'occupe de basculer la visibilité des widget.
    C'est methode sont appelé par la barre de menu
    //////////////////////////////////////////"""

    def toggleDataView(self) -> None:
        # Basculer la visibilité de DataView DockWidget
        self.dataViewDockWidget.setVisible(not self.dataViewDockWidget.isVisible())

    def toggleProprietes(self) -> None:
        # Basculer la visibilité de Proprietes DockWidget
        self.proprieteDockWidget.setVisible(not self.proprieteDockWidget.isVisible())

    def toggleItem(self) -> None:
        # Basculer la visibilité de Item DockWidget
        self.itemDockWidget.setVisible(not self.itemDockWidget.isVisible())

    def toggleBoiteOutils(self) -> None:
        # Basculer la visibilité de BoiteOutils DockWidget
        self.boiteOutilsDockWidget.setVisible(
            not self.boiteOutilsDockWidget.isVisible()
        )

    def fermerOnglet(self, index: int) -> None:
        """
        Ferme l'onglet spécifié dans le QTabWidget.
        :param index: L'index de l'onglet à fermer.
        """
        self.tabWidget.removeTab(index)

    def changeThemeVersWindows(self) -> None:
        QApplication.setStyle("Windows")

    def changeThemeVersFusion(self) -> None:
        QApplication.setStyle("Fusion")

    def changeThemeVersWindowsVista(self) -> None:
        QApplication.setStyle("windowsvista")

    def ongletChange(self, index: int) -> None:
        scrollArea = self.tabWidget.widget(index)
        if isinstance(scrollArea, QScrollArea):
            imageView = scrollArea.widget()
            if isinstance(imageView, ImageView):
                self.imageViewActif = imageView

                imageView.itemAdded.connect(self.itemWidget.ajouterItemVersListe)
                self.itemWidget.updateList(imageView.items)

            else:
                self.imageViewActif = None
        else:
            self.imageViewActif = None

            self.itemWidget.clearMask()
