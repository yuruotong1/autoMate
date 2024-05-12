from pages.edit_action_list_view import ActionList
from pages.edit_function_page import FunctionListView
from utils.global_util import GlobalUtil
from utils.qt_util import QtUtil
from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QUndoStack, QKeySequence



interface_ui = QtUtil.load_ui_type("edit_page.ui")
   

class EditPage(QMainWindow, interface_ui):
    # 页面关闭的信号
    page_closed = pyqtSignal(str)

    
    def __init__(self, func_status, func_list_pos_row, func_list_pos_column, output_save_dict=None, action_list: ActionList = None, func_name="默认名称", func_description="无", send_to_ai_selection_text=""):
        super().__init__()
        self.func_list_pos_column = func_list_pos_column
        self.func_list_pos_row = func_list_pos_row
        # 属于通用还是专属
        self.func_status = func_status
        self.func_description = func_description
        # 在func上的名称
        self.func_name = func_name
        if not output_save_dict:
            output_save_dict = {}
        # 保存action的输出结果
        self.output_save_dict = output_save_dict
        self.send_to_ai_selection_text = send_to_ai_selection_text
        if not action_list:
            action_list = ActionList(parent_widget=self)
        self.action_list = action_list
        self.q_undo_stack = QUndoStack()
        redo_action = self.q_undo_stack.createRedoAction(self, "Redo")
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        undo_action = self.q_undo_stack.createUndoAction(self, "Undo")
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.addAction(redo_action)
        self.addAction(undo_action)
        self.setupUi(self)
        self.setup_up()

    def closeEvent(self, event):
        self.page_closed.emit(self.func_name)

    def dump(self):
        return {"func_list_pos_column": self.func_list_pos_column,
                "func_list_pos_row": self.func_list_pos_row,
                "func_name": self.func_name,
                "func_status": self.func_status,
                "func_description": self.func_description,
                # 只保存结果名，不保存输出的结果值
                "output_save_dict": {i: {i1: None for i1,_ in j.items()} for i,j  in self.output_save_dict.items()},
                "action_list": self.action_list.dump(),
                "send_to_ai_selection_text": self.send_to_ai_selection_text
                }


    def setup_up(self):
        self.func_name_edit.setText(self.func_name)
        self.func_description_edit.setText(self.func_description)
        function_list_view = FunctionListView()
        self.function_list_layout.addWidget(function_list_view)
        self.action_list_view_layout.addWidget(self.action_list)
        self.run_button.clicked.connect(self.action_list.run)
        self.save_button.clicked.connect(self.__save_button_click)
        self.cancel_button.clicked.connect(self.__cancel_button_click)
        # 设置间距
        self.action_list_view_layout.setStretch(0, 1)
        self.action_list_view_layout.setStretch(1, 2)
        self.action_list_view_layout.setStretch(2, 10)
        # 设置居上对齐
        self.run_output_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.send_to_ai_selection.setCurrentText(self.send_to_ai_selection_text)

    # 将返回结果发送到 ai
    def update_send_to_ai_selection(self):
        self.send_to_ai_selection.clear()
        for k,_ in self.get_output_dict().items():
            self.send_to_ai_selection.addItem(k)

    def get_output_dict(self):
        res = {}
        for _, v in self.output_save_dict.items():
            if v:
                for k2, v2 in v.items():
                    res[k2] = v2
        return res

    def update_runing_terminal(self):
        i = 0
        for k, v in self.get_output_dict().items():
            self.run_output_layout.addWidget(QLabel(k), i, 0)
            self.run_output_layout.addWidget(QLabel(" : "), i, 1) 
            self.run_output_layout.addWidget(QLabel(v), i, 2) 
            i += 1       

    def __save_button_click(self):
        self.func_name = self.func_name_edit.text()
        self.func_description = self.func_description_edit.text()
        self.send_to_ai_selection_text = self.send_to_ai_selection.currentText()
        GlobalUtil.edit_page_global.append(self)
        GlobalUtil.save_to_local()
        self.close()


    def __cancel_button_click(self):
        # GlobalUtil.delete_edit_page(GlobalUtil.current_page)
        self.close()


    def get_chain(self):
        chain = []
        for index in range(self.action_list.count()):
            func = self.action_list.item(index)
            chain.append(func.__getattribute__("get_action")().convert_langchain_tool())
        return chain


    @staticmethod
    def global_load():
        # 从本地缓存数据读取数据
        edit_pages_json = GlobalUtil.read_from_local()
        for edit_page_json in edit_pages_json:
            from pages.edit_page import EditPage
            from pages.edit_action_list_view import ActionList
            action_list = ActionList.load(edit_page_json["action_list"])
            edit_page = EditPage(
                func_status=edit_page_json["func_status"],
                func_list_pos_row=edit_page_json["func_list_pos_row"],
                func_list_pos_column=edit_page_json["func_list_pos_column"],
                func_name = edit_page_json["func_name"],
                func_description = edit_page_json["func_description"],
                action_list=action_list,
                # 保存结果输出变量名，运行结果只有在运行时才会被保存
                output_save_dict=edit_page_json["output_save_dict"],
                send_to_ai_selection_text=edit_page_json["send_to_ai_selection_text"]
                )
            edit_page.update_runing_terminal()
            action_list.setParent(edit_page)
            edit_page.func_name = edit_page_json["func_name"]
            edit_page.func_description = edit_page_json["func_description"]
            GlobalUtil.edit_page_global.append(edit_page)


    @staticmethod
    def get_edit_page_by_position(func_status, row, column):
        for i in GlobalUtil.edit_page_global:
            if i.func_list_pos_row == row and i.func_list_pos_column == column \
                    and i.func_status == func_status:
                return i
        return None
    
    @staticmethod
    def delete_edite_page(edit_page):
        GlobalUtil.edit_page_global.remove(edit_page)
        GlobalUtil.save_to_local()
        




    

