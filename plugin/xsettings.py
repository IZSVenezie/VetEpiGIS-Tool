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

from qgis.PyQt.QtWidgets import QDialog, QFileDialog
from qgis.PyQt.QtCore import QFileInfo
import os, shutil

from .xsettings_dialog import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):
    def __init__(self):
        """Constructor for the dialog.

        """

        QDialog.__init__(self)
        self.plugin_dir = ''

        self.setupUi(self)

        self.toolButton.clicked.connect(self.namer1)
        self.pushButton.clicked.connect(self.default1)
        self.toolButton_2.clicked.connect(self.namer2)
        self.pushButton_2.clicked.connect(self.default2)
        self.toolButton_3.clicked.connect(self.namer3)
        self.pushButton_3.clicked.connect(self.default3)
        self.toolButton_4.clicked.connect(self.namer4)
        self.pushButton_4.clicked.connect(self.default4)
        self.toolButton_5.clicked.connect(self.namer5)
        self.pushButton_5.clicked.connect(self.default5)
        self.toolButton_6.clicked.connect(self.namer6)
        self.pushButton_6.clicked.connect(self.default6)


    def namer1(self):
        self.lineEdit.setText(self.selFile())

    def default1(self):
        self.lineEdit.setText('default_outbreak_point.sld')


    def namer2(self):
        self.lineEdit_2.setText(self.selFile())

    def default2(self):
        self.lineEdit_2.setText('default_outbreak_area.sld')


    def namer3(self):
        self.lineEdit_3.setText(self.selFile())

    def default3(self):
        self.lineEdit_3.setText('default_poi.sld')


    def namer4(self):
        self.lineEdit_4.setText(self.selFile())

    def default4(self):
        self.lineEdit_4.setText('default_buffer.sld')


    def namer5(self):
        self.lineEdit_5.setText(self.selFile())

    def default5(self):
        self.lineEdit_5.setText('default_zone_a.sld')


    def namer6(self):
        self.lineEdit_6.setText(self.selFile())

    def default6(self):
        self.lineEdit_6.setText('default_zone_b.sld')


    def selFile(self):
        sf = QFileInfo(QFileDialog.getOpenFileName(self, 'Select SLD file', '', 'SLD files (*.sld)')[0])
        f = sf.fileName()
        if f!='':
            df = os.path.join(os.path.join(self.plugin_dir, 'sld'), f)
            if not (os.path.samefile(sf, df)):
                shutil.copy(sf.absoluteFilePath(), df)
        return f
