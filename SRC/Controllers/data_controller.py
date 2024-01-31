import pandas as pd
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QObject, Signal

class DataController(QObject):
    fichierImporte = Signal(pd.DataFrame)

    def __init__(self):
        super().__init__()
        self.dataFrame = None

    def importFichier(self):
        filePath, _ = QFileDialog.getOpenFileName(None, "Sélectionner un fichier XLSX", "", "Fichiers Excel (*.xlsx)")
        if filePath:
            self.dataFrame = pd.read_excel(filePath)
            self.fichierImporte.emit(self.dataFrame)

    def getDataFrame(self):
        return self.dataFrame
