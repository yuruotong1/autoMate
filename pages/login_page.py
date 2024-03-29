# Form implementation generated from reading pages file 'login.pages'
#
# Created by: PyQt6 pages code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.
import leancloud
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QWidget, QLineEdit

from pages.edit_page import EditPage


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.edit_page = None
        self.password_text_edit = None
        self.username_text_edit = None
        self.label = None
        self.label_3 = None
        self.password_label = None
        self.pushButton = None
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(508, 424)
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(60, 120, 54, 16))
        self.label.setObjectName("username_label")
        self.username_text_edit = QtWidgets.QLineEdit(parent=Form)
        self.username_text_edit.setGeometry(QtCore.QRect(130, 110, 251, 41))
        self.username_text_edit.setObjectName("username_input")
        self.password_text_edit = QtWidgets.QLineEdit(parent=Form)
        self.password_text_edit.setGeometry(QtCore.QRect(130, 210, 251, 41))
        self.password_text_edit.setObjectName("password_input")
        self.password_text_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_label = QtWidgets.QLabel(parent=Form)
        self.password_label.setGeometry(QtCore.QRect(60, 220, 54, 16))
        self.password_label.setObjectName("password_label")
        self.label_3 = QtWidgets.QLabel(parent=Form)
        self.label_3.setGeometry(QtCore.QRect(190, 280, 121, 16))
        self.label_3.setObjectName("register_label")
        self.pushButton = QtWidgets.QPushButton(parent=Form)
        self.pushButton.setGeometry(QtCore.QRect(200, 320, 81, 31))
        self.pushButton.setObjectName("login_button")
        self.pushButton.clicked.connect(self.login_button_click)
        self.translate_ui(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def login_button_click(self):
        username = self.username_text_edit.text()
        password = self.password_text_edit.text()
        leancloud.User().login(username, password)
        authenticated = leancloud.User.get_current().is_authenticated()
        if authenticated:
            # 写入文件
            tmp_file = "./session"
            with open(tmp_file, 'wb') as file:
                session = leancloud.User().get_current().get_session_token()
                file.write(session.encode())
            self.hide()
            self.edit_page = EditPage()

    def translate_ui(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "autoMate"))
        self.label.setText(_translate("Form", "用户"))
        self.password_label.setText(_translate("Form", "密码"))
        self.label_3.setText(_translate("Form", "没有账户？点击注册"))
        self.pushButton.setText(_translate("Form", "登陆"))
