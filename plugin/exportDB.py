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

from qgis.PyQt.QtCore import QFileInfo, QDir
from qgis.PyQt.QtWidgets import QDialog, QFileDialog

from .exportDB_dialog import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):
    def __init__(self):
        """Constructor for the dialog.

        """

        QDialog.__init__(self)

        self.setupUi(self)
        self.toolFileButton.clicked.connect(self.filer)


    def filer(self):
        sf = QFileDialog.getSaveFileName(self, 'Export complete database', QDir.homePath(),"SQlite (*.sqlite)")
        sf = sf[0]

        if not sf or sf =='':
            self.lineEdit_file.setText('')
        else:
            self.lineEdit_file.setText(sf)



