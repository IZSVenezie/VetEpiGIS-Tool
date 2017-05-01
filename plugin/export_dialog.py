# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export_dialog_base.ui'
#
# Created: Mon May  1 07:15:34 2017
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
        Dialog.resize(378, 272)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout_2.addWidget(self.comboBox, 0, 1, 1, 2)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setMinimumSize(QtCore.QSize(270, 0))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout_2.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.toolButton = QtGui.QToolButton(Dialog)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.gridLayout_2.addWidget(self.toolButton, 1, 2, 1, 1)
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_6 = QtGui.QGridLayout(self.tab)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.comboBox_2 = QtGui.QComboBox(self.tab)
        self.comboBox_2.setEditable(True)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.gridLayout.addWidget(self.comboBox_2, 0, 1, 1, 1)
        self.checkBox = QtGui.QCheckBox(self.tab)
        self.checkBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 2)
        self.gridLayout_6.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.tab_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_3.addWidget(self.label_5, 0, 1, 1, 1)
        self.tableWidget = QtGui.QTableWidget(self.tab_2)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.gridLayout_3.addWidget(self.tableWidget, 1, 0, 1, 1)
        self.tableWidget_2 = QtGui.QTableWidget(self.tab_2)
        self.tableWidget_2.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tableWidget_2.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget_2.setObjectName(_fromUtf8("tableWidget_2"))
        self.tableWidget_2.setColumnCount(1)
        self.tableWidget_2.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        self.tableWidget_2.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.verticalHeader().setStretchLastSection(False)
        self.gridLayout_3.addWidget(self.tableWidget_2, 1, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidget, 2, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 3, 1, 1, 2)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Output:", None))
        self.label_3.setText(_translate("Dialog", "File:", None))
        self.toolButton.setText(_translate("Dialog", "...", None))
        self.label_2.setText(_translate("Dialog", "Separator:", None))
        self.checkBox.setText(_translate("Dialog", "Export geometry as WKT", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "CSV", None))
        self.label_4.setText(_translate("Dialog", "Disease:", None))
        self.label_5.setText(_translate("Dialog", "Year:", None))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Disease", None))
        self.tableWidget_2.setSortingEnabled(True)
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Year", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "SQLite filter", None))

