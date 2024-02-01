from PySide6.QtWidgets import (
    QApplication,
    QProgressBar,
    QDialog,
    QVBoxLayout,
    QLabel,
)


class ProgressBar(QDialog):
    def __init__(self, total_images: int, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Exportation des images en cours...")
        self.setGeometry(600, 400, 600, 100)
        layout = QVBoxLayout(self)

        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(total_images)
        layout.addWidget(self.progressBar)

        # Ajout d'un label pour afficher l'image en cours d'exportation
        self.currentImageLabel = QLabel(self)
        layout.addWidget(self.currentImageLabel)
        self.loading = False

    def start_loading(self) -> None:
        if not self.loading:
            self.loading = True
            self.progressBar.setValue(0)
            self.load_data()

    def load_data(self) -> None:
        # Simuler un chargement en augmentant la valeur de la barre de progression
        for i in range(101):
            self.progressBar.setValue(i)
            QApplication.processEvents()
        self.loading = False
        self.start_button.setEnabled(True)

    def update_progress(self, current_image: int, image_name: str) -> None:
        self.progressBar.setValue(current_image)
        self.currentImageLabel.setText(f"Exportation en cours : {image_name}")
