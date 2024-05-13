from PyQt6.QtCore import QObject, pyqtSignal

class ActionSignal(QObject):
    size_changed = pyqtSignal()
    def __init__(self):
        super().__init__()
        

    def emit(self):
        self.size_changed.emit()

