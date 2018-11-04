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

from qgis.PyQt.QtGui import QRegExpValidator
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtCore import QRegExp
from qgis.PyQt.QtSql import *


from .buffer_dialog import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):         
    def __init__(self):
        """Constructor for the dialog.
        
        """
        
        QDialog.__init__(self)                               
                        
        self.setupUi(self)

        # self.model = QSqlQueryModel()
        self.tablst = []
        re = QRegExp('[a-z0-9\_]+')
        val = QRegExpValidator(re)
        self.lineEdit.setValidator(val)

        self.lineEdit.textChanged.connect(self.nameCtrl)
        # self.lineEdit.editingFinished.connect(self.nameCtrl)
        self.spinBox.valueChanged.connect(self.nameCrea)


    def nameCrea(self):
        s = 'buffer_%s' % self.spinBox.value()
        self.lineEdit.setText(s)


    def nameCtrl(self):
        if self.lineEdit.text() in self.tablst:
            self.buttonBox.setEnabled(False)
        else:
            self.buttonBox.setEnabled(True)
        # if self.checkBox.isChecked():
        #     n = 0
        #     for row in range(0, self.model.rowCount()):
        #         if str(self.model.itemData(self.model.index(row, 0))[0]) == self.lineEdit.text():
        #             n+=1
        #
        #     if n!=0:
        #         self.buttonBox.setEnabled(False)
        #     else:
        #         self.buttonBox.setEnabled(True)
        
