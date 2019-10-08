# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dbtbs_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(225, 377)
        DockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")

        self.label_name = QtWidgets.QLabel(DockWidget)
        self.label_name.setText('DB name')
        self.label_name.setObjectName('label_name')
        self.label_name.setScaledContents(False)
        self.label_name.setMaximumWidth(50)
        self.gridLayout.addWidget(self.label_name,0,0,1,1)

        self.label_db_name = QtWidgets.QLabel(DockWidget)
        self.label_db_name.setText('DB_name')
        self.label_db_name.setObjectName('label_db_name')
        self.label_db_name.setScaledContents(True)
        self.gridLayout.addWidget(self.label_db_name,0,1,1,1)

        self.label_path = QtWidgets.QLabel(DockWidget)
        self.label_path.setText('DB path:')
        self.label_path.setObjectName('label_path')
        self.label_path.setScaledContents(False)
        self.label_path.setMaximumWidth(50)
        self.gridLayout.addWidget(self.label_path,1,0,1,1)

        self.label_db_path = QtWidgets.QLabel(DockWidget)
        self.label_db_path.setText('DB_path:')
        self.label_db_path.setObjectName('label_db_path')
        self.label_db_path.setScaledContents(True)
        self.label_db_path.setWordWrap(True)
        self.gridLayout.addWidget(self.label_db_path,1,1,1,1)

        #Added a label as vertical space
        self.label_empty = QtWidgets.QLabel(DockWidget)
        self.label_empty.setText('')
        self.label_empty.setObjectName('label_empty')
        self.label_empty.setMaximumHeight(5)
        self.gridLayout.addWidget(self.label_empty,2,0,1,1)

        self.tableView = QtWidgets.QTableView(self.dockWidgetContents)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setVisible(False)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tableView, 3, 0, 1, 2)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "Qvet maps"))

