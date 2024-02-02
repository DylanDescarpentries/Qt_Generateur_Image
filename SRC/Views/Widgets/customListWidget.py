from PySide6.QtWidgets import QListWidget
from PySide6.QtCore import Signal


class CustomListWidget(QListWidget):
    itemsReordered = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QListWidget.InternalMove)

    def dropEvent(self, event):
        super().dropEvent(event)
        # Après le dépôt, notifier le widget parent ou émettre un signal personnalisé
        self.parent().onItemsReordonnes()
        self.itemsReordered.emit()
