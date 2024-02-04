from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton

class TextDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter Texte")
        
        layout = QVBoxLayout(self)
        self.textEdit = QTextEdit()
        layout.addWidget(self.textEdit)
        
        btnValider = QPushButton("Valider")
        btnValider.clicked.connect(self.accept)
        layout.addWidget(btnValider)
        
    def getText(self):
        return self.textEdit.toPlainText()