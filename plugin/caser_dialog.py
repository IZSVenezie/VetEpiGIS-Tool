# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caser_dialog_base.ui'
#
# Created: Mon Nov 21 18:12:47 2016
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
        Dialog.resize(436, 341)
        self.gridLayout_14 = QtGui.QGridLayout(Dialog)
        self.gridLayout_14.setObjectName(_fromUtf8("gridLayout_14"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_11 = QtGui.QGridLayout(self.tab)
        self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        self.label_3 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_11.addWidget(self.label_3, 0, 0, 1, 1)
        self.lineEdit_3 = QtGui.QLineEdit(self.tab)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(311, 0))
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.gridLayout_11.addWidget(self.lineEdit_3, 0, 1, 1, 3)
        self.label_6 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_11.addWidget(self.label_6, 1, 0, 1, 1)
        self.lineEdit_5 = QtGui.QLineEdit(self.tab)
        self.lineEdit_5.setMinimumSize(QtCore.QSize(311, 0))
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.gridLayout_11.addWidget(self.lineEdit_5, 1, 1, 1, 3)
        self.label_9 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_11.addWidget(self.label_9, 2, 0, 1, 2)
        self.comboBox_4 = QtGui.QComboBox(self.tab)
        self.comboBox_4.setMaximumSize(QtCore.QSize(78, 16777215))
        self.comboBox_4.setObjectName(_fromUtf8("comboBox_4"))
        self.gridLayout_11.addWidget(self.comboBox_4, 2, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(189, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem, 2, 3, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.tab)
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.toolButton_3 = QtGui.QToolButton(self.tab)
        self.toolButton_3.setMinimumSize(QtCore.QSize(0, 59))
        self.toolButton_3.setObjectName(_fromUtf8("toolButton_3"))
        self.gridLayout_2.addWidget(self.toolButton_3, 0, 2, 2, 1)
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.tab)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_2, 3, 0, 1, 4)
        spacerItem1 = QtGui.QSpacerItem(20, 11, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_11.addItem(spacerItem1, 4, 3, 1, 1)
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_6.addWidget(self.label_4, 0, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(self.tab)
        self.comboBox.setMinimumSize(QtCore.QSize(241, 0))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout_6.addWidget(self.comboBox, 0, 1, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_6, 5, 0, 1, 4)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_10 = QtGui.QLabel(self.tab)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_3.addWidget(self.label_10, 0, 0, 1, 1)
        self.comboBox_5 = QtGui.QComboBox(self.tab)
        self.comboBox_5.setMinimumSize(QtCore.QSize(241, 0))
        self.comboBox_5.setObjectName(_fromUtf8("comboBox_5"))
        self.gridLayout_3.addWidget(self.comboBox_5, 0, 1, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_3, 6, 0, 1, 4)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_12 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_12.setObjectName(_fromUtf8("gridLayout_12"))
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_5 = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_5.addWidget(self.label_5, 0, 0, 1, 1)
        self.comboBox_2 = QtGui.QComboBox(self.tab_2)
        self.comboBox_2.setMinimumSize(QtCore.QSize(280, 0))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.gridLayout_5.addWidget(self.comboBox_2, 0, 1, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_5, 0, 0, 1, 2)
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_11 = QtGui.QLabel(self.tab_2)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_4.addWidget(self.label_11, 0, 0, 1, 1)
        self.lineEdit_6 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.gridLayout_4.addWidget(self.lineEdit_6, 0, 1, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_4, 1, 0, 1, 2)
        self.tableWidget = QtGui.QTableWidget(self.tab_2)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tableWidget.setFont(font)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.gridLayout_12.addWidget(self.tableWidget, 2, 0, 1, 1)
        self.gridLayout_10 = QtGui.QGridLayout()
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.toolButton = QtGui.QToolButton(self.tab_2)
        self.toolButton.setMinimumSize(QtCore.QSize(25, 25))
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.gridLayout_10.addWidget(self.toolButton, 0, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_10.addItem(spacerItem2, 1, 0, 1, 1)
        self.toolButton_5 = QtGui.QToolButton(self.tab_2)
        self.toolButton_5.setObjectName(_fromUtf8("toolButton_5"))
        self.gridLayout_10.addWidget(self.toolButton_5, 2, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_10.addItem(spacerItem3, 3, 0, 1, 1)
        self.toolButton_2 = QtGui.QToolButton(self.tab_2)
        self.toolButton_2.setMinimumSize(QtCore.QSize(25, 25))
        self.toolButton_2.setObjectName(_fromUtf8("toolButton_2"))
        self.gridLayout_10.addWidget(self.toolButton_2, 4, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_10, 2, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.gridLayout_9 = QtGui.QGridLayout(self.tab_3)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.gridLayout_7 = QtGui.QGridLayout()
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.label_8 = QtGui.QLabel(self.tab_3)
        self.label_8.setMinimumSize(QtCore.QSize(46, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_7.addWidget(self.label_8, 0, 0, 1, 1)
        self.lineEdit_4 = QtGui.QLineEdit(self.tab_3)
        self.lineEdit_4.setMaximumSize(QtCore.QSize(81, 16777215))
        self.lineEdit_4.setInputMask(_fromUtf8(""))
        self.lineEdit_4.setText(_fromUtf8(""))
        self.lineEdit_4.setMaxLength(4)
        self.lineEdit_4.setFrame(True)
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.gridLayout_7.addWidget(self.lineEdit_4, 0, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(118, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem4, 0, 2, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_7, 0, 0, 1, 1)
        self.gridLayout_8 = QtGui.QGridLayout()
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.label_7 = QtGui.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_8.addWidget(self.label_7, 0, 0, 1, 1)
        self.comboBox_3 = QtGui.QComboBox(self.tab_3)
        self.comboBox_3.setMinimumSize(QtCore.QSize(181, 0))
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.gridLayout_8.addWidget(self.comboBox_3, 0, 1, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem5, 0, 2, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_8, 1, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.tab_3)
        font = QtGui.QFont()
        font.setItalic(False)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkBox = QtGui.QCheckBox(self.groupBox)
        self.checkBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)
        self.dateEdit = QtGui.QDateEdit(self.groupBox)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.gridLayout.addWidget(self.dateEdit, 0, 1, 1, 1)
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.gridLayout.addWidget(self.checkBox_2, 1, 0, 1, 1)
        self.dateEdit_2 = QtGui.QDateEdit(self.groupBox)
        self.dateEdit_2.setCalendarPopup(True)
        self.dateEdit_2.setObjectName(_fromUtf8("dateEdit_2"))
        self.gridLayout.addWidget(self.dateEdit_2, 1, 1, 1, 1)
        self.checkBox_3 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.gridLayout.addWidget(self.checkBox_3, 2, 0, 1, 1)
        self.dateEdit_3 = QtGui.QDateEdit(self.groupBox)
        self.dateEdit_3.setCalendarPopup(True)
        self.dateEdit_3.setObjectName(_fromUtf8("dateEdit_3"))
        self.gridLayout.addWidget(self.dateEdit_3, 2, 1, 1, 1)
        self.gridLayout_9.addWidget(self.groupBox, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.gridLayout_13 = QtGui.QGridLayout(self.tab_4)
        self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
        self.textEdit = QtGui.QTextEdit(self.tab_4)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout_13.addWidget(self.textEdit, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.gridLayout_14.addWidget(self.tabWidget, 0, 0, 1, 2)
        self.label_12 = QtGui.QLabel(Dialog)
        self.label_12.setText(_fromUtf8(""))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_14.addWidget(self.label_12, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_14.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_3.setText(_translate("Dialog", "ID:", None))
        self.label_6.setText(_translate("Dialog", "Code:", None))
        self.label_9.setText(_translate("Dialog", "Large scale:", None))
        self.label.setText(_translate("Dialog", "Longitude:", None))
        self.toolButton_3.setText(_translate("Dialog", "dms", None))
        self.label_2.setText(_translate("Dialog", "Latitude:", None))
        self.label_4.setText(_translate("Dialog", "Reference layer:", None))
        self.label_10.setText(_translate("Dialog", "Outbreak layer:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Location", None))
        self.label_5.setText(_translate("Dialog", "Disease:", None))
        self.label_11.setText(_translate("Dialog", "Number of animals:", None))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Species", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Type of production", None))
        self.toolButton.setText(_translate("Dialog", "+", None))
        self.toolButton_5.setText(_translate("Dialog", "...", None))
        self.toolButton_2.setText(_translate("Dialog", "-", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Disease", None))
        self.label_8.setText(_translate("Dialog", "Year:", None))
        self.label_7.setText(_translate("Dialog", "Status:", None))
        self.groupBox.setTitle(_translate("Dialog", "Dates", None))
        self.checkBox.setText(_translate("Dialog", "Suspect:", None))
        self.checkBox_2.setText(_translate("Dialog", "Confirmation:", None))
        self.checkBox_3.setText(_translate("Dialog", "Expiration:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Status", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog", "Notes", None))

