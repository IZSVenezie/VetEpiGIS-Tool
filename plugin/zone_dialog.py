# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zone_dialog_base.ui'
#
# Created: Mon Nov 21 13:42:17 2016
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
        Dialog.resize(455, 396)
        self.gridLayout_5 = QtGui.QGridLayout(Dialog)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_6 = QtGui.QGridLayout(self.tab)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.label_4 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_6.addWidget(self.label_4, 0, 0, 1, 1)
        self.comboBox_3 = QtGui.QComboBox(self.tab)
        self.comboBox_3.setMinimumSize(QtCore.QSize(250, 0))
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.gridLayout_6.addWidget(self.comboBox_3, 0, 1, 1, 4)
        self.label_5 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_6.addWidget(self.label_5, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tableWidget = QtGui.QTableWidget(self.tab)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tableWidget.setFont(font)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 3, 1)
        self.toolButton = QtGui.QToolButton(self.tab)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.gridLayout.addWidget(self.toolButton, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.toolButton_2 = QtGui.QToolButton(self.tab)
        self.toolButton_2.setObjectName(_fromUtf8("toolButton_2"))
        self.gridLayout.addWidget(self.toolButton_2, 2, 1, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout, 1, 1, 2, 4)
        spacerItem1 = QtGui.QSpacerItem(20, 169, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem1, 2, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.tab)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_6.addWidget(self.label_6, 3, 0, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.tab)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout_6.addWidget(self.lineEdit_2, 3, 1, 1, 4)
        self.label_18 = QtGui.QLabel(self.tab)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_6.addWidget(self.label_18, 4, 0, 1, 1)
        self.dateEdit = QtGui.QDateEdit(self.tab)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(QtCore.QDate(2000, 1, 1))
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.gridLayout_6.addWidget(self.dateEdit, 4, 1, 1, 2)
        self.label_19 = QtGui.QLabel(self.tab)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout_6.addWidget(self.label_19, 4, 3, 1, 1)
        self.dateEdit_2 = QtGui.QDateEdit(self.tab)
        self.dateEdit_2.setCalendarPopup(True)
        self.dateEdit_2.setDate(QtCore.QDate(2000, 1, 1))
        self.dateEdit_2.setObjectName(_fromUtf8("dateEdit_2"))
        self.gridLayout_6.addWidget(self.dateEdit_2, 4, 4, 1, 1)
        self.label_7 = QtGui.QLabel(self.tab)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_6.addWidget(self.label_7, 5, 0, 1, 2)
        self.lineEdit_3 = QtGui.QLineEdit(self.tab)
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.gridLayout_6.addWidget(self.lineEdit_3, 5, 2, 1, 3)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_8 = QtGui.QLabel(self.tab_2)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 0, 0, 1, 1)
        self.comboBox_5 = QtGui.QComboBox(self.tab_2)
        self.comboBox_5.setMaximumSize(QtCore.QSize(85, 16777215))
        self.comboBox_5.setObjectName(_fromUtf8("comboBox_5"))
        self.gridLayout_2.addWidget(self.comboBox_5, 0, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.tab_2)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 1, 0, 1, 1)
        self.comboBox_6 = QtGui.QComboBox(self.tab_2)
        self.comboBox_6.setMaximumSize(QtCore.QSize(85, 16777215))
        self.comboBox_6.setObjectName(_fromUtf8("comboBox_6"))
        self.gridLayout_2.addWidget(self.comboBox_6, 1, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.tab_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 2, 0, 1, 1)
        self.comboBox_7 = QtGui.QComboBox(self.tab_2)
        self.comboBox_7.setMaximumSize(QtCore.QSize(85, 16777215))
        self.comboBox_7.setObjectName(_fromUtf8("comboBox_7"))
        self.gridLayout_2.addWidget(self.comboBox_7, 2, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.tab_2)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_2.addWidget(self.label_11, 3, 0, 1, 1)
        self.comboBox_8 = QtGui.QComboBox(self.tab_2)
        self.comboBox_8.setMaximumSize(QtCore.QSize(85, 16777215))
        self.comboBox_8.setObjectName(_fromUtf8("comboBox_8"))
        self.gridLayout_2.addWidget(self.comboBox_8, 3, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.tab_2)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_2.addWidget(self.label_12, 4, 0, 1, 1)
        self.comboBox_9 = QtGui.QComboBox(self.tab_2)
        self.comboBox_9.setMaximumSize(QtCore.QSize(85, 16777215))
        self.comboBox_9.setObjectName(_fromUtf8("comboBox_9"))
        self.gridLayout_2.addWidget(self.comboBox_9, 4, 1, 1, 1)
        self.label_13 = QtGui.QLabel(self.tab_2)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_2.addWidget(self.label_13, 5, 0, 1, 1)
        self.comboBox_10 = QtGui.QComboBox(self.tab_2)
        self.comboBox_10.setMaximumSize(QtCore.QSize(85, 16777215))
        self.comboBox_10.setObjectName(_fromUtf8("comboBox_10"))
        self.gridLayout_2.addWidget(self.comboBox_10, 5, 1, 1, 1)
        self.label_14 = QtGui.QLabel(self.tab_2)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_2.addWidget(self.label_14, 6, 0, 1, 1)
        self.comboBox_11 = QtGui.QComboBox(self.tab_2)
        self.comboBox_11.setMaximumSize(QtCore.QSize(85, 16777215))
        self.comboBox_11.setObjectName(_fromUtf8("comboBox_11"))
        self.gridLayout_2.addWidget(self.comboBox_11, 6, 1, 1, 1)
        self.label_15 = QtGui.QLabel(self.tab_2)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_2.addWidget(self.label_15, 7, 0, 1, 1)
        self.comboBox_12 = QtGui.QComboBox(self.tab_2)
        self.comboBox_12.setMaximumSize(QtCore.QSize(85, 16777215))
        self.comboBox_12.setObjectName(_fromUtf8("comboBox_12"))
        self.gridLayout_2.addWidget(self.comboBox_12, 7, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 2)
        self.label_16 = QtGui.QLabel(self.tab_2)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout_4.addWidget(self.label_16, 1, 0, 1, 1)
        self.lineEdit_4 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.gridLayout_4.addWidget(self.lineEdit_4, 1, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab_3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label = QtGui.QLabel(self.tab_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(self.tab_3)
        self.comboBox.setMinimumSize(QtCore.QSize(250, 0))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout_3.addWidget(self.comboBox, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.tab_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.comboBox_2 = QtGui.QComboBox(self.tab_3)
        self.comboBox_2.setMinimumSize(QtCore.QSize(250, 0))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.gridLayout_3.addWidget(self.comboBox_2, 1, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(155, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 2, 0, 1, 1)
        self.checkBox = QtGui.QCheckBox(self.tab_3)
        self.checkBox.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.checkBox.setFont(font)
        self.checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout_3.addWidget(self.checkBox, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 3, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.tab_3)
        self.lineEdit.setMinimumSize(QtCore.QSize(251, 0))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout_3.addWidget(self.lineEdit, 3, 1, 1, 1)
        self.label_21 = QtGui.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.gridLayout_3.addWidget(self.label_21, 4, 0, 1, 1)
        self.comboBox_13 = QtGui.QComboBox(self.tab_3)
        self.comboBox_13.setEditable(True)
        self.comboBox_13.setObjectName(_fromUtf8("comboBox_13"))
        self.gridLayout_3.addWidget(self.comboBox_13, 4, 1, 1, 1)
        self.label_20 = QtGui.QLabel(self.tab_3)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout_3.addWidget(self.label_20, 5, 0, 1, 1)
        self.comboBox_4 = QtGui.QComboBox(self.tab_3)
        self.comboBox_4.setObjectName(_fromUtf8("comboBox_4"))
        self.gridLayout_3.addWidget(self.comboBox_4, 5, 1, 1, 1)
        self.textEdit = QtGui.QTextEdit(self.tab_3)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout_3.addWidget(self.textEdit, 6, 0, 1, 2)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.gridLayout_5.addWidget(self.tabWidget, 0, 0, 1, 2)
        self.label_17 = QtGui.QLabel(Dialog)
        self.label_17.setText(_fromUtf8(""))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout_5.addWidget(self.label_17, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_5.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_4.setText(_translate("Dialog", "Zone type:", None))
        self.label_5.setText(_translate("Dialog", "Subpopulation:", None))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Species", None))
        self.toolButton.setText(_translate("Dialog", "+", None))
        self.toolButton_2.setText(_translate("Dialog", "-", None))
        self.label_6.setText(_translate("Dialog", "Legal framework:", None))
        self.label_18.setText(_translate("Dialog", "Validity start:", None))
        self.label_19.setText(_translate("Dialog", "End:", None))
        self.label_7.setText(_translate("Dialog", "Competent authority:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Definition", None))
        self.label_8.setText(_translate("Dialog", "Biosecurity measures:", None))
        self.label_9.setText(_translate("Dialog", "Control of vectors:", None))
        self.label_10.setText(_translate("Dialog", "Control of wildlife reservoir:", None))
        self.label_11.setText(_translate("Dialog", "Modified stamping out:", None))
        self.label_12.setText(_translate("Dialog", "Movement restriction:", None))
        self.label_13.setText(_translate("Dialog", "Stamping out:", None))
        self.label_14.setText(_translate("Dialog", "Surveillance:", None))
        self.label_15.setText(_translate("Dialog", "Vaccination:", None))
        self.label_16.setText(_translate("Dialog", "Other:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Measures", None))
        self.label.setText(_translate("Dialog", "Selector layer:", None))
        self.label_2.setText(_translate("Dialog", "POI layer:", None))
        self.checkBox.setText(_translate("Dialog", "Save the result into the database", None))
        self.label_3.setText(_translate("Dialog", "Layer name base:", None))
        self.label_21.setText(_translate("Dialog", "Related zone layer:", None))
        self.label_20.setText(_translate("Dialog", "Zone layer style:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Layer", None))

