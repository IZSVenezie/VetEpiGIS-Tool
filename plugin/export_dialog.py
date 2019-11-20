# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(378, 272)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.label_format = QtWidgets.QLabel(Dialog)
        self.label_format.setObjectName("label_format")
        self.gridLayout_2.addWidget(self.label_format, 0, 0, 1, 1)

        self.comboBox_format = QtWidgets.QComboBox(Dialog)
        self.comboBox_format.setObjectName("comboBox_format")
        self.gridLayout_2.addWidget(self.comboBox_format, 0, 1, 1, 2)

        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_csv = QtWidgets.QWidget()
        self.tab_csv.setObjectName("tab_csv")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_csv)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.gridLayout_csv = QtWidgets.QGridLayout()
        self.gridLayout_csv.setObjectName("gridLayout_csv")

        self.label_separator = QtWidgets.QLabel(self.tab_csv)
        self.label_separator.setObjectName("label_separator")
        self.gridLayout_csv.addWidget(self.label_separator, 0, 0, 1, 1)

        self.comboBox_separator = QtWidgets.QComboBox(self.tab_csv)
        self.comboBox_separator.setEditable(True)
        self.comboBox_separator.setObjectName("comboBox_separator")
        self.gridLayout_csv.addWidget(self.comboBox_separator, 0, 1, 1, 1)

        self.checkBox_wkt = QtWidgets.QCheckBox(self.tab_csv)
        self.checkBox_wkt.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_wkt.setChecked(True)
        self.checkBox_wkt.setObjectName("checkBox_wkt")
        self.gridLayout_csv.addWidget(self.checkBox_wkt, 1, 0, 1, 2)

        self.gridLayout_6.addLayout(self.gridLayout_csv, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_csv, "")

        self.tab_sqlite = QtWidgets.QWidget()
        self.tab_sqlite.setObjectName("tab_sqlite")

        self.gridLayout_sqlite = QtWidgets.QGridLayout(self.tab_sqlite)
        self.gridLayout_sqlite.setObjectName("gridLayout_sqlite")

        self.checkBox_newdb = QtWidgets.QCheckBox(self.tab_sqlite)
        self.checkBox_newdb.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_newdb.setText('Create new database')
        self.checkBox_newdb.setChecked(False)
        self.checkBox_newdb.setObjectName("checkBoxcheckBox_newdb")
        self.gridLayout_sqlite.addWidget(self.checkBox_newdb, 0, 0, 1, 2)

        self.checkBox_selection = QtWidgets.QCheckBox(self.tab_sqlite)
        self.checkBox_selection.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_selection.setText('Select all elements')
        self.checkBox_selection.setChecked(True)
        self.checkBox_selection.setObjectName("checkBoxcheckBox_selection")
        self.gridLayout_sqlite.addWidget(self.checkBox_selection, 1, 0, 1, 2)

        self.label_disease = QtWidgets.QLabel(self.tab_sqlite)
        self.label_disease.setObjectName("label_disease")
        self.gridLayout_sqlite.addWidget(self.label_disease, 2, 0, 1, 1)

        self.label_year = QtWidgets.QLabel(self.tab_sqlite)
        self.label_year.setObjectName("label_year")
        self.gridLayout_sqlite.addWidget(self.label_year, 2, 1, 1, 1)

        css = """
                QTableWidget::item:selected {
                    color: white;
                    background-color: #336eff;
                }
              """

        self.tableWidget_left = QtWidgets.QTableWidget(self.tab_sqlite)
        self.tableWidget_left.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_left.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tableWidget_left.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_left.setObjectName("tableWidget_left")
        self.tableWidget_left.setColumnCount(1)
        self.tableWidget_left.setRowCount(0)
        self.tableWidget_left.setStyleSheet(css)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_left.setHorizontalHeaderItem(0, item)
        self.tableWidget_left.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget_left.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_left.verticalHeader().setVisible(False)
        self.tableWidget_left.verticalHeader().setStretchLastSection(False)
        self.gridLayout_sqlite.addWidget(self.tableWidget_left, 3, 0, 1, 1)

        self.tableWidget_right = QtWidgets.QTableWidget(self.tab_sqlite)
        self.tableWidget_right.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_right.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tableWidget_right.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_right.setObjectName("tableWidget_right")
        self.tableWidget_right.setColumnCount(1)
        self.tableWidget_right.setRowCount(0)
        self.tableWidget_right.setStyleSheet(css)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_right.setHorizontalHeaderItem(0, item)
        self.tableWidget_right.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget_right.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_right.verticalHeader().setVisible(False)
        self.tableWidget_right.verticalHeader().setStretchLastSection(False)
        self.gridLayout_sqlite.addWidget(self.tableWidget_right, 3, 1, 1, 1)

        self.tabWidget.addTab(self.tab_sqlite, "")
        self.gridLayout_2.addWidget(self.tabWidget, 1, 0, 1, 3)

        self.label_output = QtWidgets.QLabel(Dialog)
        self.label_output.setObjectName("label_output")
        self.label_output.setText("Output file:")
        self.gridLayout_2.addWidget(self.label_output, 2, 0, 1, 1)

        self.lineEdit_output = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_output.setMinimumSize(QtCore.QSize(270, 0))
        self.lineEdit_output.setReadOnly(True)
        self.lineEdit_output.setObjectName("lineEdit_output")
        self.gridLayout_2.addWidget(self.lineEdit_output, 2, 1, 1, 1)

        self.toolButton_fileDialog = QtWidgets.QToolButton(Dialog)
        self.toolButton_fileDialog.setObjectName("toolButton_fileDialog")
        #self.toolButton_fileDialog.setIcon(QIcon(':/plugins/VetEpiGIStool/images/folder_16.png'))
        self.gridLayout_2.addWidget(self.toolButton_fileDialog, 2, 2, 1, 1)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 3, 1, 1, 2)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_format.setText(_translate("Dialog", "Format:"))
        self.label_output.setText(_translate("Dialog", "Outut file:"))
        self.toolButton_fileDialog.setText(_translate("Dialog", "..."))
        self.label_separator.setText(_translate("Dialog", "Separator:"))
        self.checkBox_wkt.setText(_translate("Dialog", "Export geometry as WKT"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_csv), _translate("Dialog", "CSV"))
        self.label_disease.setText(_translate("Dialog", "Disease:"))
        self.label_year.setText(_translate("Dialog", "Year:"))
        self.tableWidget_left.setSortingEnabled(True)
        item = self.tableWidget_left.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Disease"))
        self.tableWidget_right.setSortingEnabled(True)
        item = self.tableWidget_right.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Year"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_sqlite), _translate("Dialog", "SQLite filter"))
        self.checkBox_selection.setText(_translate("Dialog", 'Select all elements'))
        self.checkBox_newdb.setText(_translate("Dialog", 'Create new database'))
