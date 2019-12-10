# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VetEpiGIS-Tool
   A QGIS plugin
   Spatial functions for vet epidemiology
                              -------------------
        begin                : 2015-11-10
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Norbert Solymosi
        email                : solymosi.norbert@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtCore import QFileInfo, QDir
from qgis.PyQt.QtWidgets import QDialog, QFileDialog

from .export_dialog import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):
    def __init__(self):
        """Constructor for the dialog.

        """

        QDialog.__init__(self)

        self.setupUi(self)

        self.comboBox_format.addItem('ESRI shape file')
        self.comboBox_format.addItem('Comma separated value (CSV)')
        self.comboBox_format.addItem('SQLite database')
        # self.comboBox.addItem('INSPIRE')
        self.comboBox_format.currentIndexChanged.connect(self.seler)

        self.comboBox_separator.addItem(';')
        self.comboBox_separator.addItem(',')
        self.comboBox_separator.addItem('tab')

        self.tabWidget.setTabEnabled(0, False)
        self.tabWidget.setTabEnabled(1, False)

        self.seler()

        self.toolButton_fileDialog.clicked.connect(self.filer)
        self.checkBox_selection.clicked.connect(self.selItems)


    def filer(self):
        if self.comboBox_format.currentText()=='ESRI shape file':
            a = 'Save as ESRI shape file'
            sf = QFileDialog.getSaveFileName(self, a, QDir.homePath(), "ESRI shape file (*.shp)")
            # b = 'ESRI shape files (*.shp)'
        elif self.comboBox_format.currentText()=='Comma separated value (CSV)':
            a = 'Save as comma separated value (CSV)'
            sf = QFileDialog.getSaveFileName(self, a, QDir.homePath(), "Comma Separated Value (*.csv)")
            # b = 'CSV files (*.csv)'
        elif self.comboBox_format.currentText()=='SQLite database':
            a = 'SQLite database'
            if self.checkBox_newdb.isChecked():
               sf = QFileDialog.getSaveFileName(self, 'Create ' + a, QDir.homePath(),"SQlite (*.sqlite)")
            else:
                #TODO: check if there are other extension
                sf = QFileDialog.getOpenFileName(self, a, QDir.homePath(),"SQlite (*.sqlite)")

        sf = sf[0]
        if not sf or sf =='':
            self.lineEdit_output.setText('')
        else:
            self.lineEdit_output.setText(sf)


    def seler(self):
        # self.buttonBox.setEnabled(True)
        if self.comboBox_format.currentText()=='ESRI shape file':
            self.tabWidget.setTabEnabled(0, False)
            self.tabWidget.setTabEnabled(1, False)
            # self.comboBox_2.setEnabled(False)
            # self.checkBox.setEnabled(False)
            self.setWindowTitle('Export selected layer')
        elif self.comboBox_format.currentText()=='Comma separated value (CSV)':
            # self.comboBox_2.setEnabled(True)
            # self.checkBox.setEnabled(True)
            self.tabWidget.setTabEnabled(0, True)
            self.tabWidget.setTabEnabled(1, False)
            self.tabWidget.setCurrentIndex(0)
            self.setWindowTitle('Export selected layer')
        if self.comboBox_format.currentText()=='SQLite database':
            self.tabWidget.setTabEnabled(0, False)
            self.tabWidget.setTabEnabled(1, True)
            self.tabWidget.setCurrentIndex(1)
            # self.comboBox_2.setEnabled(False)
            # self.checkBox.setEnabled(False)
            self.setWindowTitle('Export selected layer')

    def selItems(self):
        if self.checkBox_selection.isChecked():
            self.tableWidget_left.selectAll()
            self.tableWidget_right.selectAll()
        else:
            self.tableWidget_left.clearSelection()
            self.tableWidget_right.clearSelection()
