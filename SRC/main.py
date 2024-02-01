from PySide6.QtWidgets import QApplication
from Views.application import MainWindow
import sys


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
