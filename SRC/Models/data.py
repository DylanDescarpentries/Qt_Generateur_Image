"""
Module contenant la classe PandasTableModel pour représenter
un modèle de données basé sur un DataFrame pandas
"""

from PySide6.QtCore import Qt
from PySide6.QtCore import QAbstractTableModel
import pandas as pd


class PandasTableModel(QAbstractTableModel):
    """
    Modèle de table pour afficher les données d'un DataFrame pandas dans une vue Qt.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialise le modèle avec un DataFrame pandas.

        :param data: DataFrame pandas à afficher.
        """
        super().__init__()
        self.data_frame = data

    def rowCount(self, _=None):
        """
        Retourne le nombre de lignes dans le modèle.

        :param _: Paramètre non utilisé, présent pour la compatibilité avec l'API.
        :return: Nombre de lignes dans le DataFrame.
        """
        return self.data_frame.shape[0]

    def columnCount(self, _=None):
        """
        Retourne le nombre de colonnes dans le modèle.

        :param _: Paramètre non utilisé, présent pour la compatibilité avec l'API.
        :return: Nombre de colonnes dans le DataFrame.
        """
        return self.data_frame.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        """
        Retourne les données à l'index spécifié.

        :param index: Index de l'élément dans le modèle.
        :param role: Rôle pour lequel les données sont requises.
        :return: Données à l'index spécifié.
        """
        if index.isValid() and role == Qt.DisplayRole:
            value = self.data_frame.iloc[index.row(), index.column()]
            if pd.isna(value):
                return ""  # Ou toute autre représentation de votre choix pour NaN
            return str(value)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Retourne les données d'en-tête pour la section donnée.

        :param section: Section de l'en-tête.
        :param orientation: Orientation de l'en-tête (horizontal ou vertical).
        :param role: Rôle pour lequel les données d'en-tête sont requises.
        :return: Données d'en-tête pour la section donnée.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.data_frame.columns[section])
            return str(self.data_frame.index[section])
        return None

    def columnData(self, column):
        """
        Retourne les données pour une colonne spécifique.

        :param column: Index de la colonne.
        :return: Liste des données dans la colonne.
        """
        return self.data_frame.iloc[:, column].tolist()

    def set_data(self, new_data):
        self.beginResetModel()
        self.data_frame = new_data
        self.endResetModel()
