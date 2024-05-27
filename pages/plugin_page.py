from PyQt6.QtWidgets import QMainWindow
from PyQt6 import QtWidgets
from utils.qt_util import QtUtil

interface_ui = QtUtil.load_ui_type("plugin_page.ui")
class PluginPage(QMainWindow, interface_ui):
    def __init__(self, parent=None):
        super(PluginPage, self).__init__(parent)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.add_plugin_button.clicked.connect(self.add_plugin)
        self.delete_plugin_button.clicked.connect(self.delete_plugin)

    def add_plugin(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)  # 设置为目录选择模式
        if file_dialog.exec():
            selected_folder = file_dialog.selectedFiles()  # 这将返回选中的文件夹列表
            print("Selected folder:", selected_folder[0])

    def delete_plugin(self):
        print("delete_plugin")
