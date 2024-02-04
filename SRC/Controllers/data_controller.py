"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"
Ce module contient la classe DataController, responsable de la gestion des données,
notamment l'importation des fichiers et la manipulation des DataFrames pandas.
""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

from typing import Dict, Optional
import pandas as pd
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QObject, Signal
from Models.itemsModels import TextColonneItem


class DataController(QObject):
    """
    Contrôleur pour gérer l'importation et la manipulation des données.
    """

    fichierImporte = Signal(dict)

    def __init__(self, mainWindow) -> None:
        super().__init__()
        self.mainWindow = mainWindow
        self.dataFrames = None
        self.filePath = ""
        self.view_mode = "Nom de Colonne"

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

    def getLePlusGrandContenu(self, colonneData):
        """Retourne l'élément le plus long de la colonne."""
        longest_element = max(colonneData, key=lambda x: len(str(x)))
        return longest_element

    def switchAffichageElementSetup(self):
        # Bascule entre les modes d'affichage
        if self.view_mode == "Nom de Colonne":
            self.view_mode = "Item le plus grand"
        else:
            self.view_mode = "Nom de Colonne"
        self.update_display()

    def update_display(self):
        text_colonne_items = self.get_text_colonne_items()
        if self.view_mode == "Item le plus grand":
            self.mainWindow.imageViewActif.afficherElementLePlusGrand(
                text_colonne_items
            )
        else:
            for item in text_colonne_items:
                item.nom = item.id
            self.mainWindow.imageViewActif.mettreAJourImage()

    def get_text_colonne_items(self):
        text_colonne_items = []
        item_widget = self.mainWindow.itemWidget
        for index in range(item_widget.itemsList.count()):
            listItem = item_widget.itemsList.item(index)
            item = item_widget.getItemFor(listItem)
            if isinstance(item, TextColonneItem):
                text_colonne_items.append(item)
        return text_colonne_items
