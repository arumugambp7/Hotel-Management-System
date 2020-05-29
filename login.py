# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(578, 426)
        Dialog.setStyleSheet("QDialog{\n"
"background-color: qconicalgradient(cx:0.5, cy:0.5, angle:0, stop:0 rgba(35, 40, 3, 255), stop:0.16 rgba(136, 106, 22, 255), stop:0.225 rgba(166, 140, 41, 255), stop:0.285 rgba(204, 181, 74, 255), stop:0.345 rgba(235, 219, 102, 255), stop:0.415 rgba(245, 236, 112, 255), stop:0.52 rgba(209, 190, 76, 255), stop:0.57 rgba(187, 156, 51, 255), stop:0.635 rgba(168, 142, 42, 255), stop:0.695 rgba(202, 174, 68, 255), stop:0.75 rgba(218, 202, 86, 255), stop:0.815 rgba(208, 187, 73, 255), stop:0.88 rgba(187, 156, 51, 255), stop:0.935 rgba(137, 108, 26, 255), stop:1 rgba(35, 40, 3, 255));\n"
"}")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(140, 50, 341, 61))
        font = QtGui.QFont()
        font.setFamily("Bookman Old Style")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(110, 160, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Bookman Old Style")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(110, 220, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Bookman Old Style")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.le_username = QtWidgets.QLineEdit(Dialog)
        self.le_username.setGeometry(QtCore.QRect(250, 160, 281, 41))
        self.le_username.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 127, 255), stop:1 rgba(255, 255, 255, 255));\n"
"font: 25 12pt \"Bookman Old Style\";")
        self.le_username.setObjectName("le_username")
        self.le_password = QtWidgets.QLineEdit(Dialog)
        self.le_password.setGeometry(QtCore.QRect(250, 220, 281, 41))
        self.le_password.setStyleSheet("font: 25 12pt \"Bookman Old Style\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 127, 255), stop:1 rgba(255, 255, 255, 255));")
        self.le_password.setObjectName("le_password")
        self.pb_login = QtWidgets.QPushButton(Dialog)
        self.pb_login.setGeometry(QtCore.QRect(210, 310, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Bookman Old Style")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pb_login.setFont(font)
        self.pb_login.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 178, 102, 255), stop:0.55 rgba(235, 148, 61, 255), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));")
        self.pb_login.setObjectName("pb_login")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "XYZ RESTAURANT"))
        self.label_2.setText(_translate("Dialog", "USERNAME"))
        self.label_3.setText(_translate("Dialog", "PASSWORD"))
        self.pb_login.setText(_translate("Dialog", "Login"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
