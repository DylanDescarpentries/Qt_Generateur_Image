"""
Module contenant les classes pour les éléments de texte et d'image.
"""

import os


class TextColonneItem:
    """Représente un élément de texte associé à une colonne."""

    def __init__(self, nom, text, x=20, y=20, font="Arial", fontSize=12, fontColor="black") -> None:
        self.nom = nom
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.fontSize = fontSize
        self.fontColor = fontColor

    def __str__(self) -> str:
        return self.nom


class TextUniqueItem:
    """Représente un élément de texte unique."""

    def __init__(self, nom, x, y, font="Arial", fontSize=12, fontColor="black") -> None:
        self.nom = nom
        self.x = x
        self.y = y
        self.font = font
        self.fontSize = fontSize
        self.fontColor = fontColor

    def __str__(self):
        return self.nom


class ImageUniqueItem:
    """Représente un élément d'image unique."""

    def __init__(self, imagePath, x, y, largeur, hauteur) -> None:
        self.imagePath = imagePath
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur

    def __str__(self) -> str:
        return os.path.basename(self.imagePath)
