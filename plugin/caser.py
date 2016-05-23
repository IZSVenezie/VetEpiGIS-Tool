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

# import os
from PyQt4.QtGui import QDialog, QTableWidgetItem, QRegExpValidator, QPalette, QDialogButtonBox, QFont
from PyQt4.QtCore import QRegExp, Qt
from PyQt4.QtSql import *


from caser_dialog import Ui_Dialog
import xaffected as xaff
import xcoordtrafo as xtrafo
import qvfuncs as funcs


class Dialog(QDialog, Ui_Dialog):         
    def __init__(self):
        """Constructor for the dialog.
        
        """

        QDialog.__init__(self)                               
                        
        self.setupUi(self)

        self.btnsave = self.buttonBox.button(QDialogButtonBox.Save)

        # self.plugin_dir = os.path.dirname(__file__)
        # self.db = QSqlDatabase.addDatabase('QSPATIALITE')
        # self.db.setDatabaseName(os.path.join(self.plugin_dir, 'db.sqlite'))

        self.lrs = []
        self.tlrs = []

        self.toolButton.setToolTip('Add new cases')
        self.toolButton.clicked.connect(self.addNew)

        self.toolButton_2.setToolTip('Delete selected row')
        self.toolButton_2.clicked.connect(self.removeRec)

        self.toolButton_5.setToolTip('Edit selected row')
        self.toolButton_5.clicked.connect(self.editRec)

        self.toolButton_3.setToolTip('Degree - decimal conversion')
        self.toolButton_3.clicked.connect(self.trafo)

        self.comboBox_3.addItem('')
        self.comboBox_3.addItem('Suspected')
        self.comboBox_3.addItem('Confirmed')
        self.comboBox_3.addItem('Not confirmed')
        self.comboBox_3.addItem('Expired')

        self.comboBox_4.addItem('')
        self.comboBox_4.addItem('No')
        self.comboBox_4.addItem('Yes')

        re = QRegExp('[0-9]+')
        val = QRegExpValidator(re)
        self.lineEdit_4.setValidator(val)
        self.lineEdit_6.setValidator(val)

        re2 = QRegExp('[0-9.]+')
        val2 = QRegExpValidator(re2)
        self.lineEdit.setValidator(val2)
        self.lineEdit_2.setValidator(val2)

        # self.db.open()
        # query = QSqlQuery("select disease from xdiseases where lang='en' order by disease")
        # query.exec_()
        # while query.next():
        #     self.comboBox_2.addItem(query.value(0))
        #
        # self.db.close()

        # # fnt = QFont()
        # fnt = self.tableWidget.horizontalHeader().font()
        # fnt.setBold(True)
        # fnt.setItalic(True)
        # # fnt.setFamily(u"DejaVu Sans")
        # # fnt.setPointSize(18)
        # # fnt.setWeight(8)
        # self.tableWidget.horizontalHeader().setFont(fnt)

        self.checkBox.clicked.connect(self.date1set)
        self.checkBox_2.clicked.connect(self.date2set)
        self.checkBox_3.clicked.connect(self.date3set)

        self.checkBox.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.dateEdit.setEnabled(False)
        self.dateEdit_2.setEnabled(False)
        self.dateEdit_3.setEnabled(False)

        self.funcs = funcs.VetEpiGISFuncs()

        self.lineEdit_3.textChanged.connect(self.saveCtrl)
        self.lineEdit_4.textChanged.connect(self.saveCtrl)
        self.lineEdit_5.textChanged.connect(self.saveCtrl)
        self.comboBox_2.currentIndexChanged.connect(self.saveCtrl)
        self.comboBox_3.currentIndexChanged.connect(self.saveCtrl)
        self.comboBox_4.currentIndexChanged.connect(self.saveCtrl)

        self.saveCtrl()


    def date1set(self):
        if self.checkBox.isChecked():
            self.dateEdit.setEnabled(True)
        else:
            self.dateEdit.setEnabled(False)


    def date2set(self):
        if self.checkBox_2.isChecked():
            self.dateEdit_2.setEnabled(True)
        else:
            self.dateEdit_2.setEnabled(False)


    def date3set(self):
        if self.checkBox_3.isChecked():
            self.dateEdit_3.setEnabled(True)
        else:
            self.dateEdit_3.setEnabled(False)


    def outLSel(self):
        self.comboBox_5.clear()
        id = self.lrs.index(self.comboBox.currentText())
        tp = self.tlrs[id]
        n = 0
        for l in self.lrs:
            if self.tlrs[n]==tp and self.lrs[n]!=self.comboBox.currentText():
                self.comboBox_5.addItem(l)
            n += 1


    def addNew(self):
        dlg = xaff.Dialog()
        x = (self.x()+self.width()/2)-dlg.width()/2
        y = (self.y()+self.height()/2)-dlg.height()/2
        dlg.move(x,y)

        dlg.setWindowTitle('Affected animals')

        for it in self.lstb:
            dlg.comboBox.addItem(it)

        # self.db.open()
        # query = QSqlQuery("select species from xspecies where lang='en' order by species")
        # query.exec_()
        # while query.next():
        #     dlg.comboBox.addItem(query.value(0))

        # self.db.close()

        if dlg.exec_() == QDialog.Accepted:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            nr = self.tableWidget.rowCount() - 1
            item = QTableWidgetItem(dlg.comboBox.currentText())
            self.tableWidget.setItem(nr, 0, item)
            s = '-'
            if dlg.lineEdit.text()!='':
                s = dlg.lineEdit.text()
            item = QTableWidgetItem(str(s))
            self.tableWidget.setItem(nr, 1, item)
            self.saveCtrl()


    def editRec(self):
        r = self.tableWidget.currentRow()
        if r<0:
            return

        dlg = xaff.Dialog()
        x = (self.x()+self.width()/2)-dlg.width()/2
        y = (self.y()+self.height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Affected animals')

        for it in self.lstb:
            dlg.comboBox.addItem(it)

        dlg.comboBox.setCurrentIndex(dlg.comboBox.findText(self.tableWidget.item(r, 0).text(), Qt.MatchExactly))
        dlg.lineEdit.setText(str(self.tableWidget.item(r, 1).text()))

        if dlg.exec_() == QDialog.Accepted:
            item = QTableWidgetItem(dlg.comboBox.currentText())
            self.tableWidget.setItem(r, 0, item)
            s = '-'
            if dlg.lineEdit.text()!='':
                s = dlg.lineEdit.text()
            item = QTableWidgetItem(str(s))
            self.tableWidget.setItem(r, 1, item)
            self.saveCtrl()


    def removeRec(self):
        if self.tableWidget.currentRow()>=0:
            self.tableWidget.removeRow(self.tableWidget.currentRow())
            item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
            self.tableWidget.setCurrentItem(item)
            self.saveCtrl()


    def trafo(self):
        dlg = xtrafo.Dialog()
        x = (self.x()+self.width()/2)-dlg.width()/2
        y = (self.y()+self.height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Degree to decimal conversion')

        res = self.funcs.dec2deg(self.lineEdit.text())
        dlg.lineEdit.setText(res[0])
        dlg.lineEdit_2.setText(res[1])
        dlg.lineEdit_3.setText(res[2])

        res = self.funcs.dec2deg(self.lineEdit_2.text())
        dlg.lineEdit_4.setText(res[0])
        dlg.lineEdit_5.setText(res[1])
        dlg.lineEdit_6.setText(res[2])

        if dlg.exec_() == QDialog.Accepted:
            res = self.funcs.deg2dec(dlg.lineEdit.text(), dlg.lineEdit_2.text(), dlg.lineEdit_3.text())
            self.lineEdit.setText(str(res))
            res = self.funcs.deg2dec(dlg.lineEdit_4.text(), dlg.lineEdit_5.text(), dlg.lineEdit_6.text())
            self.lineEdit_2.setText(str(res))


    def saveCtrl(self):
        n = 0
        if self.lineEdit_3.text()=='':
            n += 1
        if self.lineEdit_4.text()=='':
            n += 1
        if self.lineEdit_5.text()=='':
            n += 1
        if self.comboBox_2.currentText()=='':
            n += 1
        if self.comboBox_3.currentText()=='':
            n += 1
        if self.comboBox_4.currentText()=='':
            n += 1
        if self.tableWidget.rowCount()==0:
            n += 1

        if n==0:
            self.btnsave.setEnabled(True)
            self.label_12.setText('')
        else:
            self.btnsave.setEnabled(False)
            pal = QPalette()
            pal.setColor(self.label_12.backgroundRole(), Qt.red)
            pal.setColor(self.label_12.foregroundRole(), Qt.red)
            self.label_12.setPalette(pal)
            self.label_12.setText('All bold field must be given!')


