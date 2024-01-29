from PySide6.QtWidgets import QApplication, QGroupBox, QPushButton, QVBoxLayout, QWidget

class MyGroupBox(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        groupbox = QGroupBox("Outils")
        layout.addWidget(groupbox)

        innerLayout = QVBoxLayout(groupbox)
        button1 = QPushButton("Ajouter image")
        button2 = QPushButton("Ajouter texte")
        innerLayout.addWidget(button1)
        innerLayout.addWidget(button2)

app = QApplication([])
window = MyGroupBox()
window.show()
app.exec()