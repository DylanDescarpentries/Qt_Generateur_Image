class TextItem:
    def __init__(self, nom, text, x=0, y=0, font="Arial", fontSize=12):
        self.nom = nom
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.fontSize = fontSize

    def __str__(self):
        return self.nom 