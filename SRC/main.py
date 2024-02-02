import os
from PySide6.QtWidgets import QApplication
from Views.application import MainWindow
import sys, logging
current_directory = os.getcwd()
print("Répertoire de travail actuel :", current_directory)
logging.basicConfig(
    filename="app.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.ERROR,
)


def main() -> None:
    try:
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logging.error(f"Exception non anticipée capturée \n {e}", exc_info=True)


if __name__ == "__main__":
    main()
