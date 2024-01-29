import os

class TextColonneteItem:
    def __init__(self, nom, text, x=20, y=20, font='Arial', fontSize=12, fontColor='black'):
        self.nom = nom
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.fontSize = fontSize
        self.fontColor = fontColor

    def __str__(self):
        return self.nom 


class TextUniqueItem:
    def __init__(self, nom, x, y, font='Arial', fontSize=12, fontColor='black'):
        self.nom = nom
        self.x = x
        self.y = y
        self.font = font
        self.fontSize = fontSize
        self.fontColor = fontColor
    
    def __str__(self):
        return self.nom

class ImageUniqueItem:
    def __init__(self, imagePath, x, y, width, height):
        self.imagePath = imagePath
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return os.path.basename(self.imagePath)