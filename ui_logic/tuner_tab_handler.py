from PySide6.QtWidgets import QWidget
from ui_generated.tuner_tab import Ui_tuner_tab

class TunerTab(QWidget, Ui_tuner_tab):
    def __init__(self):
        super().__init__()
        self.setupUi(self)