from PyQt6.QtCore import Qt


class FunctionBase:
    name = ""
    description = ""
    uni_tag = ""

    def __init__(self):
        self.config_ui = None

    def run(self, *args, **kwargs):
        pass

    def config_page_ui(self):
        raise TypeError("please config config_page_ui")

    def config_page_show(self):
        self.config_page_ui()
        if self.config_ui is None:
            raise TypeError("config_ui not config")
        # 居上对齐
        self.config_ui.config_list.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.config_ui.show()
