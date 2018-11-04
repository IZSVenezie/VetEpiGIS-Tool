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

import os, hashlib, datetime
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import Qt, QSettings, QCoreApplication, QFile, QFileInfo, QDate, QVariant, \
    pyqtSignal, QRegExp, QDateTime, QTranslator
from qgis.PyQt.QtSql import *
from uuid import getnode as get_mac

from qgis.core import QgsField, QgsSpatialIndex, QgsMessageLog, QgsProject, \
    QgsCoordinateTransform, Qgis, QgsVectorFileWriter, QgsFeature, \
    QgsGeometry, QgsFeatureRequest, QgsPoint, QgsVectorLayer, QgsCoordinateReferenceSystem, \
    QgsRectangle, QgsDataSourceUri, QgsDataProvider
from qgis.gui import QgsMapTool, QgsMapToolEmitPoint, QgsMessageBar, QgsRubberBand

class VetEpiGISFuncs:
    def __init__(self):
        """Constructor for the class.

        """
    def hashIDer(self, most):
        mac = '_'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))
        uid = '%s %s' % (mac, most.toString('dd/MM/yyyy hh:mm:ss.z'))
        hrid = hashlib.sha256(uid.encode('utf-8')).hexdigest()
        return hrid


    def outattrPrep(self, dlg, lyr):
        feat = QgsFeature()

        species = ''
        production = ''
        most = QDateTime.currentDateTimeUtc()

        rn = dlg.tableWidget.rowCount()
        for i in range(rn):
            if i==0:
                species = dlg.tableWidget.item(i, 0).text()
                production = dlg.tableWidget.item(i, 1).text()
            else:
                species = species + ' | ' + dlg.tableWidget.item(i, 0).text()
                production = production + ' | ' + dlg.tableWidget.item(i, 1).text()

        flds = lyr.dataProvider().fields()
        feat.setFields(flds, True)
        feat.setAttribute(feat.fieldNameIndex('localid'), dlg.lineEdit_3.text())
        feat.setAttribute(feat.fieldNameIndex('code'), dlg.lineEdit_5.text())
        feat.setAttribute(feat.fieldNameIndex('largescale'), dlg.comboBox_4.currentText())
        feat.setAttribute(feat.fieldNameIndex('disease'), dlg.comboBox_2.currentText())
        feat.setAttribute(feat.fieldNameIndex('animalno'), dlg.lineEdit_6.text())
        feat.setAttribute(feat.fieldNameIndex('species'), species)
        feat.setAttribute(feat.fieldNameIndex('production'), production)
        feat.setAttribute(feat.fieldNameIndex('year'), dlg.lineEdit_4.text())
        feat.setAttribute(feat.fieldNameIndex('status'), dlg.comboBox_3.currentText())
        feat.setAttribute(feat.fieldNameIndex('suspect'), self.dateCheck(dlg.dateEdit.date()))
        feat.setAttribute(feat.fieldNameIndex('confirmation'), self.dateCheck(dlg.dateEdit_2.date()))
        feat.setAttribute(feat.fieldNameIndex('expiration'), self.dateCheck(dlg.dateEdit_3.date()))
        feat.setAttribute(feat.fieldNameIndex('notes'), dlg.textEdit.toPlainText())
        feat.setAttribute(feat.fieldNameIndex('hrid'), self.hashIDer(most))
        feat.setAttribute(feat.fieldNameIndex('timestamp'), most.toString('dd/MM/yyyy hh:mm:ss'))
        return feat


    def dateCheck(self, qd):
        dt = qd.toString('dd/MM/yyyy')
        if dt=='01/01/2000':
            dt = ''
        return  dt


    def dec2deg(self, coord):
        dec = float(coord)
        d = int(dec)
        t = (dec-d)*60
        m = int(t)
        s = (t-m)*60
        res = [str(d), str(m), str(s)]
        return res


    def deg2dec(self, d, m, s):
        res = float(d)+float(m)/60+float(s)/3600
        return res


    def ofielder(self, lyr):
        flds = lyr.dataProvider().fields()
        flst = []
        for fld in flds:
            flst.append(fld.name())
        return flst


