from PySide6.QtWidgets import QApplication, QMainWindow
from ui_generated.main_gui import Ui_MainWindow
from ui_logic.fretboard_tab_handler import FretboardTab
from ui_logic.tuner_tab_handler import TunerTab
from PySide6.QtGui import QPixmap

class TunerApplication(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.fretboard_tab = FretboardTab()
        self.tabWidget.addTab(self.fretboard_tab, "Fretboard")

        self.tuner_tab = TunerTab()
        self.tabWidget.addTab(self.tuner_tab, "Tuner")



# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = TunerApplication()
    window.show()
    app.exec()
