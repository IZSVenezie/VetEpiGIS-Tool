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

from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtWidgets import QDialog, QFileDialog
from qgis.PyQt.QtCore import QFileInfo, QDir

from .xprint_dialog import Ui_Dialog
import os, shutil

class Dialog(QDialog, Ui_Dialog):
    def __init__(self):
        """Constructor for the dialog.

        """

        QDialog.__init__(self)

        self.setupUi(self)
        self.logopath = ''
        self.pdfpath = ''
        self.toolButton.clicked.connect(self.selFile)
        self.toolButton_2.clicked.connect(self.outFile)


    def selFile(self):
        sf = QFileInfo(QFileDialog.getOpenFileName(self, 'Open logo file', QDir.homePath(), 'Image files (*.png)')[0])
        f = sf.fileName()
        if f!='':
            self.logopath = sf.absoluteFilePath()
            self.label.setPixmap(QPixmap(self.logopath))
        return f


    def outFile(self):
        of = QFileInfo(QFileDialog.getSaveFileName(self, 'Output map file', QDir.homePath(), 'PDF files (*.pdf)')[0])
        f = of.fileName()
        if f!='':
            self.lineEdit_3.setText(of.absoluteFilePath())
        return f


