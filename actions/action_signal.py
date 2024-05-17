from PyQt6.QtCore import QObject, pyqtSignal

class ActionSignal(QObject):
    size_changed = pyqtSignal()
    cancel_selection_to_son = pyqtSignal()
    cancel_selection_to_father = pyqtSignal()
    def __init__(self):
        super().__init__()
        

    def size_changed_emit(self):
        self.size_changed.emit()

    def cancel_selection_to_son_emit(self):
        self.cancel_selection_to_son.emit()

    def cancel_selection_to_father_emit(self):
        self.cancel_selection_to_father.emit()
