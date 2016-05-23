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

from PyQt4.QtSql import *
from PyQt4.QtCore import QRegExp, SIGNAL, Qt, QModelIndex
from PyQt4.QtGui import *

from dbmaint_dialog import Ui_Dialog
import xitem as insdlg


class Dialog(QDialog, Ui_Dialog):         
    def __init__(self):
        """Constructor for the dialog.
        
        """
        
        QDialog.__init__(self)                               
                        
        self.setupUi(self)

        re = QRegExp("""[^|'"]+""")
        val = QRegExpValidator(re)
        self.lineEdit.setValidator(val)

        self.toolButton.setToolTip('Add or update list item')
        self.toolButton_2.setToolTip('Record new English list item')

        self.db = QSqlDatabase()

        self.tabUpdate()
        self.comboBox.currentIndexChanged.connect(self.tabUpdate)
        self.tableView.selectionModel().selectionChanged.connect(self.itemSel)
        self.tableView.clicked.connect(self.itemSel)
        self.toolButton.clicked.connect(self.saveTrans)
        self.lineEdit.returnPressed.connect(self.saveTrans)
        self.toolButton_2.clicked.connect(self.saveEn)

        self.bb = self.buttonBox.button(QDialogButtonBox.Close)
        self.bb.setDefault(False)
        self.bb.setAutoDefault(False)
        self.bb.clicked.connect(self.accept)

        self.comboBox_2.currentIndexChanged.connect(self.itemSel)

        self.toolButton_4.clicked.connect(self.deLayer)
        self.toolButton_4.setToolTip('Delete selected layer')
        self.toolButton_3.clicked.connect(self.renameLayer)
        self.toolButton_3.setToolTip('Rename selected layer')

        self.loadLayers()

    # def closeEvent(self, event):
    #     event.accept()


    def loadLayers(self):
        sql = 'select f_table_name as layer from geometry_columns order by f_table_name'
        self.db.open()
        self.model2 = QSqlQueryModel()
        self.model2.setQuery(sql, self.db)
        self.tableView_2.setModel(self.model2)
        self.tableView_2.setColumnWidth(0, self.tableView_2.width())
        self.db.close()


    def renameLayer(self):
        if len(self.tableView_2.selectedIndexes())!=1:
            return
        dlg = insdlg.Dialog()
        dlg.setWindowTitle('Rename layer')
        dlg.label.setText('New name:')
        x = (self.x()+self.width()/2)-dlg.width()/2
        y = (self.y()+self.height()/2)-dlg.height()/2
        dlg.move(x,y)
        if dlg.exec_() == QDialog.Accepted:
            self.db.open()
            idx = self.tableView_2.selectionModel().selectedIndexes()[0]
            oname = str(self.model2.itemData(idx)[0])
            nname = dlg.lineEdit.text()
            sql = 'alter table %s rename to %s' % (oname, nname)
            q = self.db.exec_(sql)
            sql = "update geometry_columns set f_table_name='%s' where f_table_name='%s'" % (nname, oname)
            q = self.db.exec_(sql)
            sql = "update geometry_columns_auth set f_table_name='%s' where f_table_name='%s'" % (nname, oname)
            q = self.db.exec_(sql)
            sql = "update geometry_columns_field_infos set f_table_name='%s' where f_table_name='%s'" % (nname, oname)
            q = self.db.exec_(sql)
            sql = "update geometry_columns_statistics set f_table_name='%s' where f_table_name='%s'" % (nname, oname)
            q = self.db.exec_(sql)
            sql = "update geometry_columns_time set f_table_name='%s' where f_table_name='%s'" % (nname, oname)
            q = self.db.exec_(sql)
            self.db.close()
            self.loadLayers()


    def deLayer(self):
        if len(self.tableView_2.selectedIndexes())!=1:
            return

        msgBox = QMessageBox()
        msgBox.setInformativeText("Do you delete the layer?")
        msgBox.addButton(QMessageBox.Yes)
        msgBox.addButton(QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        msgBox.setWindowTitle("Confirmation")
        msgBox.setIcon(QMessageBox.Question)
        if msgBox.exec_() == QMessageBox.Yes:
            self.db.open()
            idx = self.tableView_2.selectionModel().selectedIndexes()[0]
            tname = str(self.model2.itemData(idx)[0])
            sql = "drop table %s" % tname
            q = self.db.exec_(sql)
            sql = "delete from geometry_columns where f_table_name='%s'" % tname
            q = self.db.exec_(sql)
            sql = "delete from geometry_columns_auth where f_table_name='%s'" % tname
            q = self.db.exec_(sql)
            sql = "delete from geometry_columns_field_infos where f_table_name='%s'" % tname
            q = self.db.exec_(sql)
            sql = "delete from geometry_columns_statistics where f_table_name='%s'" % tname
            q = self.db.exec_(sql)
            sql = "delete from geometry_columns_time where f_table_name='%s'" % tname
            q = self.db.exec_(sql)
            self.db.commit()
            self.db.close()
            self.loadLayers()


    def tabUpdate(self):
        sql = ''
        if self.comboBox.currentText()=='Species':
            sql = "select species, id from xspecies where lang='en' order by species"
        elif self.comboBox.currentText()=='Diseases':
            sql = "select disease, id from xdiseases where lang='en' order by disease"
        elif self.comboBox.currentText()=='POI types':
            sql = "select poitype, id from xpoitypes where lang='en' order by poitype"

        self.db.open()
        self.model = QSqlQueryModel()
        self.model.setQuery(sql, self.db)
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(0, self.tableView.width())
        self.db.close()
        

    def itemSel(self):
        if len(self.tableView.selectedIndexes())==0:
            return

        res = ''
        lang = self.comboBox_2.currentText()
        if lang=='en':
            idx = self.tableView.selectionModel().selectedIndexes()[0]
            res = str(self.model.itemData(idx)[0])
        else:
            sql = ''
            idx = self.tableView.selectionModel().selectedIndexes()[1]
            id = str(self.model.itemData(idx)[0])
            if self.comboBox.currentText()=='Species':
                sql = "select species from xspecies where enid=%s and lang='%s'" % (id, lang)
            elif self.comboBox.currentText()=='Diseases':
                sql = "select disease from xdiseases where enid=%s and lang='%s'" % (id, lang)
            elif self.comboBox.currentText()=='POI types':
                sql = "select poitype from xpoitypes where enid=%s and lang='%s'" % (id, lang)

            self.db.open()
            qq = self.db.exec_(sql)
            # if qq.isValid():
            qq.first()
            res = qq.value(0)
            # else:
            #     res = '???'
            self.db.close()

        self.lineEdit.setText(res)
        self.lineEdit.setFocus()


    def saveEn(self):
        dlg = insdlg.Dialog()
        x = (self.x()+self.width()/2)-dlg.width()/2
        y = (self.y()+self.height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle(self.comboBox.currentText())
        if dlg.exec_() == QDialog.Accepted:
            if self.comboBox.currentText()=='Species':
                sql = "insert into xspecies (species, lang) values('%s', 'en')" % (dlg.lineEdit.text())
            elif self.comboBox.currentText()=='Diseases':
                sql = "insert into xdiseases (disease, lang) values('%s', 'en')" % (dlg.lineEdit.text())
            elif self.comboBox.currentText()=='POI types':
                sql = "insert into xpoitypes (poitype, lang) values('%s', 'en')" % (dlg.lineEdit.text())
            self.db.open()
            q = self.db.exec_(sql)
            self.db.commit()
            self.db.close()
            self.tabUpdate()


    def saveTrans(self):
        if self.lineEdit.text()=='':
            return

        sql = ''
        self.db.open()
        idx = self.tableView.selectionModel().selectedIndexes()[1]
        lang = self.comboBox_2.currentText()
        s = self.lineEdit.text()
        id = str(self.model.itemData(idx)[0])
        if self.comboBox.currentText()=='Species':
            if lang=='en':
                sql = "update xspecies set species='%s' where id=%s" % (s, id)
            else:
                sql = "select * from xspecies where enid=%s and lang='%s'" % (id, lang)
                q = self.db.exec_(sql)
                q.last()
                if q.at()==0:
                    sql = "update xspecies set species='%s' where enid=%s and lang='%s'" % (s, id, lang)
                else:
                    sql = "insert into xspecies (species, enid, lang) values('%s', %s, '%s')" % (s, id, lang)
        elif self.comboBox.currentText()=='Diseases':
            if lang=='en':
                sql = "update xdiseases set disease='%s' where id=%s" % (s, id)
            else:
                sql = "select * from xdiseases where enid=%s and lang='%s'" % (id, lang)
                q = self.db.exec_(sql)
                q.last()
                if q.at()==0:
                    sql = "update xdiseases set disease='%s' where enid=%s and lang='%s'" % (s, id, lang)
                else:
                    sql = "insert into xdiseases (disease, enid, lang) values('%s', %s, '%s')" % (s, id, lang)
        elif self.comboBox.currentText()=='POI types':
            if lang=='en':
                sql = "update xpoitypes set poitype='%s' where id=%s" % (s, id)
            else:
                sql = "select * from xpoitypes where enid=%s and lang='%s'" % (id, lang)
                q = self.db.exec_(sql)
                q.last()
                if q.at()==0:
                    sql = "update xpoitypes set poitype='%s' where enid=%s and lang='%s'" % (s, id, lang)
                else:
                    sql = "insert into xpoitypes (poitype, enid, lang) values('%s', %s, '%s')" % (s, id, lang)

        q = self.db.exec_(sql)
        self.db.commit()
        self.db.close()
        self.tabUpdate()
        self.lineEdit.setText('')
        self.tableView.setFocus()

