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

from qgis.PyQt.QtCore import QRegExp, Qt
from qgis.PyQt.QtGui import QRegExpValidator, QPalette
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox

from .xcoordtrafo import Dialog as xtrafodial
from .qvfuncs import VetEpiGISFuncs as VetEpiGISFuncs

from .poi_dialog import Ui_Dialog

class Dialog(QDialog, Ui_Dialog):         
    def __init__(self):
        """Constructor for the dialog.
        
        """
        
        QDialog.__init__(self)                               
                        
        self.setupUi(self)

        self.btnsave = self.buttonBox.button(QDialogButtonBox.Save)

        self.saveCtrl()

        re = QRegExp('[0-9.]+')
        val = QRegExpValidator(re)
        self.lineEdit.setValidator(val)
        self.lineEdit_2.setValidator(val)

        self.toolButton.setToolTip('Degree - decimal conversion')
        self.toolButton.clicked.connect(self.trafo)

        self.lineEdit_3.textChanged.connect(self.saveCtrl)
        self.lineEdit_5.textChanged.connect(self.saveCtrl)
        self.comboBox.currentIndexChanged.connect(self.saveCtrl)

        self.funcs = VetEpiGISFuncs()


    def trafo(self):
        dlg = xtrafodial()
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
        if self.lineEdit_5.text()=='':
            n += 1
        if self.comboBox.currentText()=='':
            n += 1

        if n==0:
            self.btnsave.setEnabled(True)
            self.label_5.setText('')
        else:
            self.btnsave.setEnabled(False)
            pal = QPalette()
            pal.setColor(self.label_5.backgroundRole(), Qt.red)
            pal.setColor(self.label_5.foregroundRole(), Qt.red)
            self.label_5.setPalette(pal)
            self.label_5.setText('All bold field must be given!')

