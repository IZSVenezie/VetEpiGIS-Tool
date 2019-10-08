# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dbmaint_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(479, 418)
        self.gridLayout_8 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_lists = QtWidgets.QWidget()
        self.tab_lists.setObjectName("tab_lists")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_lists)
        self.gridLayout_7.setObjectName("gridLayout_7")

        self.label_lists = QtWidgets.QLabel(self.tab_lists)
        self.label_lists.setObjectName("label_lists")
        self.gridLayout_7.addWidget(self.label_lists, 0, 0, 1, 1)

        self.comboBox_lists = QtWidgets.QComboBox(self.tab_lists)
        self.comboBox_lists.setMinimumSize(QtCore.QSize(311, 0))
        self.comboBox_lists.setObjectName("comboBox")
        self.gridLayout_7.addWidget(self.comboBox_lists, 0, 1, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(85, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.gridLayout_7.addItem(spacerItem, 0, 2, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.label_english = QtWidgets.QLabel(self.tab_lists)
        self.label_english.setObjectName("label_english")
        self.gridLayout_3.addWidget(self.label_english, 0, 0, 1, 1)

        self.toolButton_lang = QtWidgets.QToolButton(self.tab_lists)
        self.toolButton_lang.setObjectName("toolButton_lang")
        self.gridLayout_3.addWidget(self.toolButton_lang, 0, 1, 1, 1)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 2, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_3, 1, 0, 1, 2)

        self.tableView_lists = QtWidgets.QTableView(self.tab_lists)
        self.tableView_lists.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView_lists.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView_lists.setObjectName("tableView_lists")
        self.tableView_lists.verticalHeader().setVisible(False)
        self.gridLayout_7.addWidget(self.tableView_lists, 2, 0, 1, 3)

        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")

        self.label_translation = QtWidgets.QLabel(self.tab_lists)
        self.label_translation.setObjectName("label_translation")
        self.gridLayout_5.addWidget(self.label_translation, 0, 0, 1, 1)

        self.comboBox_translation = QtWidgets.QComboBox(self.tab_lists)
        self.comboBox_translation.setObjectName("comboBox_translation")
        self.gridLayout_5.addWidget(self.comboBox_translation, 0, 1, 1, 1)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem2, 0, 2, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_5, 3, 0, 1, 2)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.lineEdit_translation = QtWidgets.QLineEdit(self.tab_lists)
        self.lineEdit_translation.setObjectName("lineEdit_translation")
        self.gridLayout_6.addWidget(self.lineEdit_translation, 0, 0, 1, 1)

        self.toolButton_translation = QtWidgets.QToolButton(self.tab_lists)
        self.toolButton_translation.setObjectName("toolButton_translation")
        self.gridLayout_6.addWidget(self.toolButton_translation, 0, 1, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_6, 4, 0, 1, 3)

        self.tabWidget.addTab(self.tab_lists, "")
        self.tab_layers = QtWidgets.QWidget()
        self.tab_layers.setObjectName("tab_layers")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.tab_layers)
        self.gridLayout_10.setObjectName("gridLayout_10")

        self.tableView_layers = QtWidgets.QTableView(self.tab_layers)
        self.tableView_layers.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView_layers.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView_layers.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView_layers.setObjectName("tableView_2")
        self.tableView_layers.horizontalHeader().setVisible(False)
        self.tableView_layers.horizontalHeader().setStretchLastSection(True)
        self.tableView_layers.verticalHeader().setVisible(False)
        self.gridLayout_10.addWidget(self.tableView_layers, 0, 0, 1, 1)

        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.toolButton_rename = QtWidgets.QToolButton(self.tab_layers)
        self.toolButton_rename.setObjectName("toolButton_3")
        self.gridLayout_9.addWidget(self.toolButton_rename, 0, 0, 1, 1)

        self.toolButton_delete = QtWidgets.QToolButton(self.tab_layers)
        self.toolButton_delete.setObjectName("toolButton_4")
        self.gridLayout_9.addWidget(self.toolButton_delete, 1, 0, 1, 1)

        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_9.addItem(spacerItem3, 2, 0, 1, 1)

        self.gridLayout_10.addLayout(self.gridLayout_9, 0, 1, 1, 1)

        self.tabWidget.addTab(self.tab_layers, "")
        self.gridLayout_8.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_8.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_lists.setText(_translate("Dialog", "List:"))
        self.label_english.setText(_translate("Dialog", "English:"))
        self.toolButton_lang.setText(_translate("Dialog", "+"))
        self.label_translation.setText(_translate("Dialog", "Translation:"))
        self.toolButton_translation.setText(_translate("Dialog", "..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_lists), _translate("Dialog", "Lists"))
        self.toolButton_rename.setText(_translate("Dialog", "..."))
        self.toolButton_delete.setText(_translate("Dialog", "-"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_layers), _translate("Dialog", "Layers"))



