# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xsettings_dialog_base.ui'
#
# Created: Mon Nov 21 13:42:16 2016
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
        Dialog.resize(598, 343)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.a = QtGui.QGridLayout(self.tab)
        self.a.setObjectName(_fromUtf8("a"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(self.tab)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout_2.addWidget(self.comboBox, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.a.addLayout(self.gridLayout_2, 2, 0, 1, 1)
        self.info_label = QtGui.QLabel(self.tab)
        self.info_label.setMinimumSize(QtCore.QSize(0, 40))
        self.info_label.setMaximumSize(QtCore.QSize(16777213, 40))
        self.info_label.setBaseSize(QtCore.QSize(0, 0))
        self.info_label.setFrameShape(QtGui.QFrame.NoFrame)
        self.info_label.setLineWidth(1)
        self.info_label.setText(_fromUtf8("Select the language of the plugin. Automatically all the data derived by dictionary tables will be saved in the database in that language."))
        self.info_label.setTextFormat(QtCore.Qt.AutoText)
        self.info_label.setScaledContents(False)
        self.info_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.info_label.setWordWrap(True)
        self.info_label.setObjectName(_fromUtf8("info_label"))
        self.a.addWidget(self.info_label, 0, 0, 2, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 303, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.a.addItem(spacerItem1, 4, 0, 1, 1)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setContentsMargins(-1, -1, 0, -1)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout.setItem(0, QtGui.QFormLayout.FieldRole, spacerItem2)
        self.a.addLayout(self.formLayout, 3, 0, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setEnabled(True)
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.info_label_2 = QtGui.QLabel(self.tab_2)
        self.info_label_2.setMinimumSize(QtCore.QSize(548, 40))
        self.info_label_2.setMaximumSize(QtCore.QSize(548, 40))
        self.info_label_2.setBaseSize(QtCore.QSize(0, 0))
        self.info_label_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.info_label_2.setLineWidth(1)
        self.info_label_2.setText(_fromUtf8("Select the style for each primary layer. By default some layers have specific SLD file linked."))
        self.info_label_2.setTextFormat(QtCore.Qt.AutoText)
        self.info_label_2.setScaledContents(False)
        self.info_label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.info_label_2.setWordWrap(True)
        self.info_label_2.setObjectName(_fromUtf8("info_label_2"))
        self.gridLayout_3.addWidget(self.info_label_2, 0, 0, 1, 4)
        self.label_2 = QtGui.QLabel(self.tab_2)
        self.label_2.setMinimumSize(QtCore.QSize(140, 0))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.tab_2)
        self.lineEdit.setMinimumSize(QtCore.QSize(291, 0))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout_3.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.toolButton = QtGui.QToolButton(self.tab_2)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.gridLayout_3.addWidget(self.toolButton, 1, 2, 1, 1)
        self.pushButton = QtGui.QPushButton(self.tab_2)
        self.pushButton.setMaximumSize(QtCore.QSize(60, 50))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout_3.addWidget(self.pushButton, 1, 3, 1, 1)
        self.label_7 = QtGui.QLabel(self.tab_2)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_3.addWidget(self.label_7, 2, 0, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(291, 0))
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout_3.addWidget(self.lineEdit_2, 2, 1, 1, 1)
        self.toolButton_2 = QtGui.QToolButton(self.tab_2)
        self.toolButton_2.setObjectName(_fromUtf8("toolButton_2"))
        self.gridLayout_3.addWidget(self.toolButton_2, 2, 2, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.tab_2)
        self.pushButton_2.setMaximumSize(QtCore.QSize(60, 50))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout_3.addWidget(self.pushButton_2, 2, 3, 1, 1)
        self.label_6 = QtGui.QLabel(self.tab_2)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_3.addWidget(self.label_6, 3, 0, 1, 1)
        self.lineEdit_3 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(291, 0))
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.gridLayout_3.addWidget(self.lineEdit_3, 3, 1, 1, 1)
        self.toolButton_3 = QtGui.QToolButton(self.tab_2)
        self.toolButton_3.setObjectName(_fromUtf8("toolButton_3"))
        self.gridLayout_3.addWidget(self.toolButton_3, 3, 2, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(self.tab_2)
        self.pushButton_3.setMaximumSize(QtCore.QSize(60, 50))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout_3.addWidget(self.pushButton_3, 3, 3, 1, 1)
        self.label_3 = QtGui.QLabel(self.tab_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 4, 0, 1, 1)
        self.lineEdit_4 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(291, 0))
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.gridLayout_3.addWidget(self.lineEdit_4, 4, 1, 1, 1)
        self.toolButton_4 = QtGui.QToolButton(self.tab_2)
        self.toolButton_4.setObjectName(_fromUtf8("toolButton_4"))
        self.gridLayout_3.addWidget(self.toolButton_4, 4, 2, 1, 1)
        self.pushButton_4 = QtGui.QPushButton(self.tab_2)
        self.pushButton_4.setMaximumSize(QtCore.QSize(60, 50))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.gridLayout_3.addWidget(self.pushButton_4, 4, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 5, 0, 1, 1)
        self.lineEdit_5 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_5.setMinimumSize(QtCore.QSize(291, 0))
        self.lineEdit_5.setReadOnly(True)
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.gridLayout_3.addWidget(self.lineEdit_5, 5, 1, 1, 1)
        self.toolButton_5 = QtGui.QToolButton(self.tab_2)
        self.toolButton_5.setObjectName(_fromUtf8("toolButton_5"))
        self.gridLayout_3.addWidget(self.toolButton_5, 5, 2, 1, 1)
        self.pushButton_5 = QtGui.QPushButton(self.tab_2)
        self.pushButton_5.setMaximumSize(QtCore.QSize(60, 50))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.gridLayout_3.addWidget(self.pushButton_5, 5, 3, 1, 1)
        self.label_5 = QtGui.QLabel(self.tab_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_3.addWidget(self.label_5, 6, 0, 1, 1)
        self.lineEdit_6 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_6.setMinimumSize(QtCore.QSize(291, 0))
        self.lineEdit_6.setReadOnly(True)
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.gridLayout_3.addWidget(self.lineEdit_6, 6, 1, 1, 1)
        self.toolButton_6 = QtGui.QToolButton(self.tab_2)
        self.toolButton_6.setObjectName(_fromUtf8("toolButton_6"))
        self.gridLayout_3.addWidget(self.toolButton_6, 6, 2, 1, 1)
        self.pushButton_6 = QtGui.QPushButton(self.tab_2)
        self.pushButton_6.setMaximumSize(QtCore.QSize(60, 50))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.gridLayout_3.addWidget(self.pushButton_6, 6, 3, 1, 1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Language:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Internationalisation", None))
        self.label_2.setText(_translate("Dialog", "Ourtbreaks (point):", None))
        self.toolButton.setText(_translate("Dialog", "...", None))
        self.pushButton.setText(_translate("Dialog", "Default", None))
        self.label_7.setText(_translate("Dialog", "Ourtbreaks (area):", None))
        self.toolButton_2.setText(_translate("Dialog", "...", None))
        self.pushButton_2.setText(_translate("Dialog", "Default", None))
        self.label_6.setText(_translate("Dialog", "POI (point):", None))
        self.toolButton_3.setText(_translate("Dialog", "...", None))
        self.pushButton_3.setText(_translate("Dialog", "Default", None))
        self.label_3.setText(_translate("Dialog", "Buffers:", None))
        self.toolButton_4.setText(_translate("Dialog", "...", None))
        self.pushButton_4.setText(_translate("Dialog", "Default", None))
        self.label_4.setText(_translate("Dialog", "Zones A:", None))
        self.toolButton_5.setText(_translate("Dialog", "...", None))
        self.pushButton_5.setText(_translate("Dialog", "Default", None))
        self.label_5.setText(_translate("Dialog", "Zones B:", None))
        self.toolButton_6.setText(_translate("Dialog", "...", None))
        self.pushButton_6.setText(_translate("Dialog", "Default", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Style", None))

