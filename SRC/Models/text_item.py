"""
Module contenant les classes pour les éléments de texte et d'image.
"""

import os


class TextColonneItem:
    """Représente un élément de texte associé à une colonne."""

    def __init__(self, nom: str, text: list[str], x: int=20, y: int=20, font: str="Arial", fontSize: str=12, fontColor : str="black") -> None:
        self.nom = nom
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.fontSize = fontSize
        self.fontColor = fontColor

    def __str__(self) -> str:
        return self.nom


class ImageColonneItem:
    """Représente une image associé à une colonne."""
    def __init__(self, imagePath: list[str], nom: str='SRC/Assets/images/default.png', x: int=20, y: int=20, largeur: int=20, hauteur: int=20) -> None:
        self.nom = nom
        self.imagePath = imagePath
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur

    def __str__(self) -> str:
        return self.nom
    
class TextUniqueItem:
    """Représente un élément de texte unique."""

    def __init__(self, nom: str, x: int, y: int, font: str="Arial", fontSize: str=12, fontColor: str="black") -> None:
        self.nom = nom
        self.x = x
        self.y = y
        self.font = font
        self.fontSize = fontSize
        self.fontColor = fontColor

    def __str__(self) -> str:
        return self.nom


class ImageUniqueItem:
    """Représente un élément d'image unique."""

    def __init__(self, imagePath: str, x: int, y: int, largeur: int, hauteur: int) -> None:
        self.imagePath = imagePath
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur

    def __str__(self) -> str:
        return os.path.basename(self.imagePath)

class FormeGeometriqueItem:
    """Réprésente un élément forme géométrique"""

    def __init__(self, nom:str='test', x:int=20, y:int=20, largeur:int=20, hauteur:int=20, radius:int=0, color: str='black') -> None:
        self.nom = nom
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.radius = radius
        self.color = color

    def __str__(self) -> str:
        return self.nom