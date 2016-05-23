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

from PyQt4.QtCore import QRegExp
from PyQt4.QtGui import QDialog, QRegExpValidator


from xcoordtrafo_dialog import Ui_Dialog

class Dialog(QDialog, Ui_Dialog):         
    def __init__(self):
        """Constructor for the dialog.
        
        """
        
        QDialog.__init__(self)                               
                        
        self.setupUi(self)

        re = QRegExp('[0-9.]+')
        val = QRegExpValidator(re)
        self.lineEdit.setValidator(val)
        self.lineEdit_2.setValidator(val)
        self.lineEdit_3.setValidator(val)
        self.lineEdit_4.setValidator(val)
        self.lineEdit_5.setValidator(val)
        self.lineEdit_6.setValidator(val)




