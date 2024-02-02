"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"
Ce module contient la classe DataController, responsable de la gestion des données,
notamment l'importation des fichiers et la manipulation des DataFrames pandas.
""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

from typing import Dict, Optional
import pandas as pd
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QObject, Signal


class DataController(QObject):
    """
    Contrôleur pour gérer l'importation et la manipulation des données.
    """

    fichierImporte = Signal(dict)

    def __init__(self) -> None:
        super().__init__()
        self.dataFrames = None
        self.filePath = ""

    def importFichier(self) -> None:
        """
        Ouvre un dialogue pour importer un fichier Excel.
        """
        self.filePath, _ = QFileDialog.getOpenFileName(
            None, "Sélectionner un fichier XLSX", "", "Fichiers Excel (*.xlsx)"
        )
        if self.filePath:
            self.chargerFeuille()

    def chargerFeuille(self) -> Optional[Dict[str, pd.DataFrame]]:
        if self.filePath:
            dataFrames = pd.read_excel(self.filePath, sheet_name=None)
            self.fichierImporte.emit(dataFrames)
