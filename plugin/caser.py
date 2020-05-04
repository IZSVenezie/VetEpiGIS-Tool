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

from qgis.PyQt.QtGui import QRegExpValidator, QPalette, QFont
from qgis.PyQt.QtWidgets import QDialog, QTableWidgetItem, QDialogButtonBox
from qgis.PyQt.QtCore import QRegExp, Qt
from qgis.PyQt.QtSql import *

from .caser_dialog import Ui_Dialog
from .xaffected import Dialog as xaffdial
from .xcoordtrafo import Dialog as xtrafodial
from .qvfuncs import VetEpiGISFuncs as VetEpiGISFuncs


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

        self.toolButton_species_add.setToolTip('Add new cases')
        self.toolButton_species_add.clicked.connect(self.addNew)

        self.toolButton_2_species_remove.setToolTip('Delete selected row')
        self.toolButton_2_species_remove.clicked.connect(self.removeRec)

        self.toolButton_5_species_dots.setToolTip('Edit selected row')
        self.toolButton_5_species_dots.clicked.connect(self.editRec)

        self.toolButton_3_dms.setToolTip('Degree - decimal conversion')
        self.toolButton_3_dms.clicked.connect(self.trafo)

        self.comboBox_3_status.addItem('')
        self.comboBox_3_status.addItem('Suspected')
        self.comboBox_3_status.addItem('Confirmed')
        self.comboBox_3_status.addItem('Not confirmed')
        self.comboBox_3_status.addItem('Expired')

        self.comboBox_4_large_scale.addItem('')
        self.comboBox_4_large_scale.addItem('No')
        self.comboBox_4_large_scale.addItem('Yes')

        re = QRegExp('[0-9]+')
        val = QRegExpValidator(re)
        self.lineEdit_4_year.setValidator(val)
        self.lineEdit_6_num_animals.setValidator(val)

        re2 = QRegExp('[0-9.]+')
        val2 = QRegExpValidator(re2)
        self.lineEdit_longitude.setValidator(val2)
        self.lineEdit_2_latitude.setValidator(val2)

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

        self.checkBox_dates_suspect.clicked.connect(self.date1set)
        self.checkBox_2_dates_confirmation.clicked.connect(self.date2set)
        self.checkBox_3_dates_expiration.clicked.connect(self.date3set)

        self.checkBox_dates_suspect.setChecked(False)
        self.checkBox_2_dates_confirmation.setChecked(False)
        self.checkBox_3_dates_expiration.setChecked(False)
        self.dateEdit_dates_suspect.setEnabled(False)
        self.dateEdit_2_dates_confirmation.setEnabled(False)
        self.dateEdit_3_dates_expiration.setEnabled(False)

        self.funcs = VetEpiGISFuncs()

        self.lineEdit_3_id.textChanged.connect(self.saveCtrl)
        self.lineEdit_4_year.textChanged.connect(self.saveCtrl)
        self.lineEdit_5_code.textChanged.connect(self.saveCtrl)
        self.comboBox_2_disease.currentIndexChanged.connect(self.saveCtrl)
        self.comboBox_3_status.currentIndexChanged.connect(self.saveCtrl)
        self.comboBox_4_large_scale.currentIndexChanged.connect(self.saveCtrl)
        self.lineEdit_6_num_animals.setText(str(1))
        self.saveCtrl()


    def date1set(self):
        if self.checkBox_dates_suspect.isChecked():
            self.dateEdit_dates_suspect.setEnabled(True)
        else:
            self.dateEdit_dates_suspect.setEnabled(False)


    def date2set(self):
        if self.checkBox_2_dates_confirmation.isChecked():
            self.dateEdit_2_dates_confirmation.setEnabled(True)
        else:
            self.dateEdit_2_dates_confirmation.setEnabled(False)


    def date3set(self):
        if self.checkBox_3_dates_expiration.isChecked():
            self.dateEdit_3_dates_expiration.setEnabled(True)
        else:
            self.dateEdit_3_dates_expiration.setEnabled(False)


    def outLSel(self):
        self.comboBox_5_outbreak_layer.clear()
        id = self.lrs.index(self.comboBox_reference.currentText())
        tp = self.tlrs[id]
        n = 0
        for l in self.lrs:
            if self.tlrs[n]==tp and self.lrs[n]!=self.comboBox_reference.currentText():
                self.comboBox_5_outbreak_layer.addItem(l)
            n += 1


    def addNew(self):
        dlg = xaffdial()
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

        dlg = xaffdial()
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
        dlg = xtrafodial()
        x = (self.x()+self.width()/2)-dlg.width()/2
        y = (self.y()+self.height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Degree to decimal conversion')

        res = self.funcs.dec2deg(self.lineEdit_longitude.text())
        dlg.lineEdit.setText(res[0])
        dlg.lineEdit_2.setText(res[1])
        dlg.lineEdit_3.setText(res[2])

        res = self.funcs.dec2deg(self.lineEdit_2_latitude.text())
        dlg.lineEdit_4.setText(res[0])
        dlg.lineEdit_5.setText(res[1])
        dlg.lineEdit_6.setText(res[2])

        if dlg.exec_() == QDialog.Accepted:
            res = self.funcs.deg2dec(dlg.lineEdit.text(), dlg.lineEdit_2.text(), dlg.lineEdit_3.text())
            self.lineEdit_longitude.setText(str(res))
            res = self.funcs.deg2dec(dlg.lineEdit_4.text(), dlg.lineEdit_5.text(), dlg.lineEdit_6.text())
            self.lineEdit_2_latitude.setText(str(res))


    def saveCtrl(self):
        n = 0
        if self.lineEdit_3_id.text()=='':
            n += 1
        if self.lineEdit_4_year.text()=='':
            n += 1
        if self.lineEdit_5_code.text()=='':
            n += 1
        if self.comboBox_2_disease.currentText()=='':
            n += 1
        if self.comboBox_3_status.currentText()=='':
            n += 1
        if self.comboBox_4_large_scale.currentText()=='':
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


