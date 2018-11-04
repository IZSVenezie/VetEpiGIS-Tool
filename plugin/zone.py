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

from qgis.PyQt.QtGui import QRegExpValidator, QPalette, QFont
from qgis.PyQt.QtWidgets import QDialog, QTableWidgetItem, QDialogButtonBox
from qgis.PyQt.QtCore import QRegExp, Qt
from qgis.PyQt.QtSql import *


from .zone_dialog import Ui_Dialog
from .xaffected import Dialog as xaffdlg


class Dialog(QDialog, Ui_Dialog):         
    def __init__(self):
        """Constructor for the dialog.
        
        """
        
        QDialog.__init__(self)                               
                        
        self.setupUi(self)

        self.btnok = self.buttonBox.button(QDialogButtonBox.Ok)

        self.toolButton.setToolTip('Add new cases')
        self.toolButton.clicked.connect(self.addNew)
        self.toolButton_2.setToolTip('Delete selected row')
        self.toolButton_2.clicked.connect(self.removeRec)
        
        # self.model = QSqlQueryModel()
        self.tablst = []
        re = QRegExp('[a-z0-9\_]+')
        val = QRegExpValidator(re)
        self.lineEdit.setValidator(val)

        self.lineEdit.textChanged.connect(self.nameCtrl)
        # self.lineEdit.editingFinished.connect(self.nameCtrl)
        self.comboBox.currentIndexChanged.connect(self.nameCrea)
        self.comboBox_2.currentIndexChanged.connect(self.nameCrea)

        self.comboBox_3.addItem('')
        self.comboBox_3.addItem('Control')
        self.comboBox_3.addItem('Protection')
        self.comboBox_3.addItem('Surveillance')
        self.comboBox_3.addItem('Restriction')
        self.comboBox_3.addItem('Vaccination')
        # self.comboBox_3.addItem('Containment')
        # self.comboBox_3.addItem('Protection')
        # self.comboBox_3.addItem('Vaccination')
        self.comboBox_3.currentIndexChanged.connect(self.saveCtrl)

        self.comboBox_4.addItem('Intersections only')
        self.comboBox_4.addItem('Overlapped ROIs')
        self.comboBox_4.currentIndexChanged.connect(self.info)
        self.info()

        self.comboBox_5.addItem('')
        self.comboBox_5.addItem('Yes')
        self.comboBox_5.addItem('No')
        self.comboBox_6.addItem('')
        self.comboBox_6.addItem('Yes')
        self.comboBox_6.addItem('No')
        self.comboBox_7.addItem('')
        self.comboBox_7.addItem('Yes')
        self.comboBox_7.addItem('No')
        self.comboBox_8.addItem('')
        self.comboBox_8.addItem('Yes')
        self.comboBox_8.addItem('No')
        self.comboBox_9.addItem('')
        self.comboBox_9.addItem('Yes')
        self.comboBox_9.addItem('No')
        self.comboBox_10.addItem('')
        self.comboBox_10.addItem('Yes')
        self.comboBox_10.addItem('No')
        self.comboBox_11.addItem('')
        self.comboBox_11.addItem('Yes')
        self.comboBox_11.addItem('No')
        self.comboBox_12.addItem('')
        self.comboBox_12.addItem('Yes')
        self.comboBox_12.addItem('No')


    def info(self):
        if self.comboBox_4.currentText()=='Intersections only':
            self.textEdit.setText(u'The new zone layer will contain only the intersection of the buffer and the ROIs layer.')
        else:
            self.textEdit.setText(u'The new zone layer will contain all the areas are overlapped by the buffer.')


    def nameCrea(self):
        s = '%s_selected_by_%s' % (self.comboBox_2.currentText(), self.comboBox.currentText())
        self.lineEdit.setText(s.lower())


    def nameCtrl(self):
        ss = 'zone_a_%s' % self.lineEdit.text()
        if ss in self.tablst:
            self.btnok.setEnabled(False)
            pal = QPalette()
            pal.setColor(self.label_17.backgroundRole(), Qt.red)
            pal.setColor(self.label_17.foregroundRole(), Qt.red)
            self.label_17.setPalette(pal)
            self.label_17.setText('Database contain layer with tis name!')
        else:
            self.btnok.setEnabled(True)

        self.saveCtrl()

        
    def addNew(self):
        dlg = xaffdlg()
        x = (self.x()+self.width()/2)-dlg.width()/2
        y = (self.y()+self.height()/2)-dlg.height()/2
        dlg.move(x,y)

        dlg.setWindowTitle('Susceptible species')
        dlg.lineEdit.setVisible(False)
        dlg.label_2.setVisible(False)

        for it in self.lstb:
            dlg.comboBox.addItem(it)

        if dlg.exec_() == QDialog.Accepted:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            nr = self.tableWidget.rowCount() - 1
            item = QTableWidgetItem(dlg.comboBox.currentText())
            self.tableWidget.setItem(nr, 0, item)
            self.saveCtrl()

    def removeRec(self):
        if self.tableWidget.currentRow()>=0:
            self.tableWidget.removeRow(self.tableWidget.currentRow())
            item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
            self.tableWidget.setCurrentItem(item)
            self.saveCtrl()


    def saveCtrl(self):
        n = 0
        if self.lineEdit.text()=='':
            n += 1
        if self.comboBox_3.currentText()=='':
            n += 1
        if self.tableWidget.rowCount()==0:
            n += 1

        if n==0:
            self.btnok.setEnabled(True)
            self.label_17.setText('')
        else:
            self.btnok.setEnabled(False)
            pal = QPalette()
            pal.setColor(self.label_17.backgroundRole(), Qt.red)
            pal.setColor(self.label_17.foregroundRole(), Qt.red)
            self.label_17.setPalette(pal)
            self.label_17.setText('All bold field must be given!')

