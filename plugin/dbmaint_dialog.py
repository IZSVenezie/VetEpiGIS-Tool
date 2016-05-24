# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dbmaint_dialog_base.ui'
#
# Created: Tue May 24 14:31:32 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(479, 418)
        self.gridLayout_8 = QtGui.QGridLayout(Dialog)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_7 = QtGui.QGridLayout(self.tab)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_7.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(self.tab)
        self.comboBox.setMinimumSize(QtCore.QSize(311, 0))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout_7.addWidget(self.comboBox, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(85, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem, 0, 2, 1, 1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)
        self.toolButton_2 = QtGui.QToolButton(self.tab)
        self.toolButton_2.setObjectName(_fromUtf8("toolButton_2"))
        self.gridLayout_3.addWidget(self.toolButton_2, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 2, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_3, 1, 0, 1, 2)
        self.tableView = QtGui.QTableView(self.tab)
        self.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tableView.verticalHeader().setVisible(False)
        self.gridLayout_7.addWidget(self.tableView, 2, 0, 1, 3)
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_5.addWidget(self.label_5, 0, 0, 1, 1)
        self.comboBox_2 = QtGui.QComboBox(self.tab)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.gridLayout_5.addWidget(self.comboBox_2, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem2, 0, 2, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_5, 3, 0, 1, 2)
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.lineEdit = QtGui.QLineEdit(self.tab)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout_6.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.toolButton = QtGui.QToolButton(self.tab)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.gridLayout_6.addWidget(self.toolButton, 0, 1, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_6, 4, 0, 1, 3)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_10 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.tableView_2 = QtGui.QTableView(self.tab_2)
        self.tableView_2.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView_2.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView_2.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView_2.setObjectName(_fromUtf8("tableView_2"))
        self.tableView_2.horizontalHeader().setVisible(False)
        self.tableView_2.horizontalHeader().setStretchLastSection(True)
        self.tableView_2.verticalHeader().setVisible(False)
        self.gridLayout_10.addWidget(self.tableView_2, 0, 0, 1, 1)
        self.gridLayout_9 = QtGui.QGridLayout()
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.toolButton_3 = QtGui.QToolButton(self.tab_2)
        self.toolButton_3.setObjectName(_fromUtf8("toolButton_3"))
        self.gridLayout_9.addWidget(self.toolButton_3, 0, 0, 1, 1)
        self.toolButton_4 = QtGui.QToolButton(self.tab_2)
        self.toolButton_4.setObjectName(_fromUtf8("toolButton_4"))
        self.gridLayout_9.addWidget(self.toolButton_4, 1, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_9.addItem(spacerItem3, 2, 0, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_9, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout_8.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_8.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "List:", None))
        self.label_4.setText(_translate("Dialog", "English:", None))
        self.toolButton_2.setText(_translate("Dialog", "+", None))
        self.label_5.setText(_translate("Dialog", "Translation:", None))
        self.toolButton.setText(_translate("Dialog", "...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Lists", None))
        self.toolButton_3.setText(_translate("Dialog", "...", None))
        self.toolButton_4.setText(_translate("Dialog", "-", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Layers", None))

