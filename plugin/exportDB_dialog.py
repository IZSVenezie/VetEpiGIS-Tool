# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(301, 50)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_file = QtWidgets.QLabel(Dialog)
        self.label_file.setObjectName("label_file")
        self.gridLayout_2.addWidget(self.label_file, 0, 0, 1, 1)
        self.lineEdit_file = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_file.setMinimumSize(QtCore.QSize(270, 0))
        self.lineEdit_file.setReadOnly(True)
        self.lineEdit_file.setObjectName("lineEdit_file")
        self.gridLayout_2.addWidget(self.lineEdit_file, 0, 1, 1, 1)
        self.toolFileButton = QtWidgets.QToolButton(Dialog)
        self.toolFileButton.setObjectName("toolFileButton")
        self.gridLayout_2.addWidget(self.toolFileButton, 0, 2, 1, 1)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 3, 1, 1, 2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_file.setText(_translate("Dialog", "File:"))
        self.toolFileButton.setText(_translate("Dialog", "..."))

