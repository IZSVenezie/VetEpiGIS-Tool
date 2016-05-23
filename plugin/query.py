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

from PyQt4.QtGui import QDialog, QTableWidgetItem


from query_dialog import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):         
    def __init__(self):
        """Constructor for the dialog.
        
        """
        
        QDialog.__init__(self)                               

        self.upl=[]
        self.usl=[]

        self.setupUi(self)

        self.toolButton.setToolTip('Add new alias')
        self.toolButton_2.setToolTip('Remove selected record')

        self.comboBox_2.currentIndexChanged.connect(self.lister)
        self.toolButton_2.clicked.connect(self.removeRec)
        self.toolButton.clicked.connect(self.addNew)


    def lister(self):
        self.comboBox.clear()
        if self.comboBox_2.currentText()=='Species':
            for e in self.usl:
                self.comboBox.addItem(e)
        else:
            for e in self.upl:
                self.comboBox.addItem(e)

        # self.tableWidget.clear()
        self.tableWidget.setRowCount(0)


    def addNew(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        nr = self.tableWidget.rowCount() - 1
        item = QTableWidgetItem(self.comboBox.currentText())
        self.tableWidget.setItem(nr, 0, item)
        item = QTableWidgetItem(self.lineEdit.text())
        self.tableWidget.setItem(nr, 1, item)

        
    def removeRec(self):
        if self.tableWidget.currentRow()>=0:
            self.tableWidget.removeRow(self.tableWidget.currentRow())
            item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
            self.tableWidget.setCurrentItem(item)


