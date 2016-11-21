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

from PyQt4.QtGui import QDialog, QFileDialog
from PyQt4.QtCore import QFileInfo, QDir

from export_dialog import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):         
    def __init__(self):
        """Constructor for the dialog.
        
        """

        QDialog.__init__(self)                               
                        
        self.setupUi(self)

        self.comboBox.addItem('ESRI shape file')
        self.comboBox.addItem('Comma separated value (CSV)')
        self.comboBox.addItem('SQLite database')
        self.comboBox.addItem('Copy complete database')
        # self.comboBox.addItem('INSPIRE')
        self.comboBox.currentIndexChanged.connect(self.seler)

        self.comboBox_2.addItem(';')
        self.comboBox_2.addItem(',')
        self.comboBox_2.addItem('tab')

        self.seler()

        self.toolButton.clicked.connect(self.filer)


    def filer(self):
        if self.comboBox.currentText()=='ESRI shape file':
            a = 'Save as ESRI shape file'
            sf = QFileDialog.getExistingDirectory(self, a, QDir.homePath())
            # b = 'ESRI shape files (*.shp)'
        elif self.comboBox.currentText()=='Comma separated value (CSV)':
            a = 'Save as comma separated value (CSV)'
            sf = QFileDialog.getExistingDirectory(self, a, QDir.homePath())
            # b = 'CSV files (*.csv)'
        elif self.comboBox.currentText()=='SQLite database':
            a = 'SQLite database'
            sf = QFileDialog.getOpenFileName(self, a, QDir.homePath())
        elif self.comboBox.currentText()=='Copy complete database':
            a = 'Copy complete database'
            sf = QFileDialog.getSaveFileName(self, a, QDir.homePath())

        self.lineEdit.setText(sf)


    def seler(self):
        # self.buttonBox.setEnabled(True)
        if self.comboBox.currentText()=='ESRI shape file':
            self.comboBox_2.setEnabled(False)
            self.checkBox.setEnabled(False)
            self.setWindowTitle('Export selected layer')
        elif self.comboBox.currentText()=='Comma separated value (CSV)':
            self.comboBox_2.setEnabled(True)
            self.checkBox.setEnabled(True)
            self.setWindowTitle('Export selected layer')
        if self.comboBox.currentText()=='SQLite database':
            self.comboBox_2.setEnabled(False)
            self.checkBox.setEnabled(False)
            self.setWindowTitle('Export selected layer')
        elif self.comboBox.currentText()=='Copy complete database':
            self.comboBox_2.setEnabled(False)
            self.checkBox.setEnabled(False)
            self.setWindowTitle('Copy complete database')
        # elif self.comboBox.currentText()=='INSPIRE':
        #     self.comboBox_2.setEnabled(False)
        #     self.checkBox.setEnabled(False)
        #     self.buttonBox.setEnabled(False)


