from PySide6.QtCore import Qt, QAbstractTableModel
import pandas as pd

class PandasTableModel(QAbstractTableModel):
    """
    Un modèle de table Qt personnalisé pour afficher des DataFrame pandas.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialise le modèle avec un DataFrame pandas.

        :param data: DataFrame pandas à afficher.
        """
        super().__init__()
        self.dataFrame = data

    def rowCount(self, parent=None):
        """
        Retourne le nombre de lignes dans le modèle.

        :return: Nombre de lignes du DataFrame.
        """
        return self.dataFrame.shape[0]

    def columnCount(self, parent=None):
        """
        Retourne le nombre de colonnes dans le modèle.

        :return: Nombre de colonnes du DataFrame.
        """
        return self.dataFrame.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        """
        Récupère la donnée à afficher pour une cellule donnée.

        :param index: L'index de la cellule.
        :param role: Le rôle de la donnée (affichage, édition, etc.).
        :return: La valeur à afficher.
        """
        if index.isValid() and role == Qt.DisplayRole:
            return str(self.dataFrame.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Retourne les données d'en-tête pour les lignes/colonnes.

        :param section: Index de la ligne ou de la colonne.
        :param orientation: Orientation de l'en-tête (horizontal ou vertical).
        :param role: Le rôle de la donnée d'en-tête.
        :return: Texte de l'en-tête pour la section donnée.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.dataFrame.columns[section])
            else:
                return str(self.dataFrame.index[section])
        return None

    def columnData(self, column):
        """
        Renvoie les données d'une colonne spécifiée.

        :param column: Index de la colonne.
        :return: Liste des données dans la colonne.
        """
        return self.dataFrame.iloc[:, column].tolist()

    def set_data(self, new_data: pd.DataFrame):
        """
        Met à jour le modèle avec de nouvelles données.

        :param new_data: Nouveau DataFrame pandas à afficher.
        """
        self.beginResetModel()
        self.dataFrame = new_data
        self.endResetModel()
