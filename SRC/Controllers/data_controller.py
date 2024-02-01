""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Ce module contient la classe DataController, responsable de la gestion des données,
notamment l'importation des fichiers et la manipulation des DataFrames pandas.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from typing import Union, Optional
import pandas as pd
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QObject, Signal


class DataController(QObject):
    """
    Contrôleur pour gérer l'importation et la manipulation des données.
    """
    fichierImporte = Signal(pd.DataFrame)

    def __init__(self) -> None:
        super().__init__()
        self.data_frame: Union[pd.DataFrame, None] = None

    def importFichier(self) -> None:
        """
        Ouvre un dialogue pour importer un fichier Excel et émet le DataFrame chargé.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Sélectionner un fichier XLSX", "", "Fichiers Excel (*.xlsx)"
        )
        if file_path:
            self.data_frame = pd.read_excel(file_path)
            self.fichierImporte.emit(self.data_frame)

    def get_data_frame(self) ->Optional[pd.DataFrame]:
        """
        Retourne le DataFrame actuellement chargé.
        """
        return self.data_frame
