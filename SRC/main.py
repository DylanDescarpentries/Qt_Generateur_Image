from PySide6.QtWidgets import QApplication
from Views.application import MainWindow
import sys, logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.ERROR)

def main() -> None:
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logging.error("Exception non anticipée capturée", exc_info=True)

if __name__ == "__main__":
    main()