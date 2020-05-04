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
    #deprecated, when more features are create they have the same timestamp and
    #are not possibile to differentiate the hrid
    # def hashIDer(self, most):
    #     mac = '_'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))
    #     uid = '%s %s' % (mac, most.toString('dd/MM/yyyy hh:mm:ss.z'))
    #     hrid = hashlib.sha256(uid.encode('utf-8')).hexdigest()
    #     return hrid


    def hashIDer(self, most, counter):
        mac = '_'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))
        uid = '%s %s %d' % (mac, most.toString('dd/MM/yyyy hh:mm:ss.z'), counter)
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
        feat.setAttribute(feat.fieldNameIndex('localid'), dlg.lineEdit_3_id.text())#mandatory
        feat.setAttribute(feat.fieldNameIndex('code'), dlg.lineEdit_5_code.text())#mandatory
        feat.setAttribute(feat.fieldNameIndex('largescale'), dlg.comboBox_4_large_scale.currentText())
        feat.setAttribute(feat.fieldNameIndex('disease'), dlg.comboBox_2_disease.currentText())#mandatory
        feat.setAttribute(feat.fieldNameIndex('animalno'), dlg.lineEdit_6_num_animals.text())#mandatory
        feat.setAttribute(feat.fieldNameIndex('species'), species)#mandatory
        feat.setAttribute(feat.fieldNameIndex('production'), production)
        feat.setAttribute(feat.fieldNameIndex('year'), self.checkIntValue(dlg.lineEdit_4_year.text()))#mandatory
        feat.setAttribute(feat.fieldNameIndex('status'), dlg.comboBox_3_status.currentText())#mandatory
        feat.setAttribute(feat.fieldNameIndex('suspect'), self.dateCheck(dlg.dateEdit_dates_suspect.date()))
        feat.setAttribute(feat.fieldNameIndex('confirmation'), self.dateCheck(dlg.dateEdit_2_dates_confirmation.date()))
        feat.setAttribute(feat.fieldNameIndex('expiration'), self.dateCheck(dlg.dateEdit_3_dates_expiration.date()))
        feat.setAttribute(feat.fieldNameIndex('notes'),  self.checkValue(dlg.textEdit_notes.toPlainText()))
        feat.setAttribute(feat.fieldNameIndex('hrid'), self.hashIDer(most,0))
        feat.setAttribute(feat.fieldNameIndex('timestamp'), most.toString('dd/MM/yyyy hh:mm:ss'))
        return feat


    def dateCheck(self, qd):
        dt = qd.toString('dd/MM/yyyy')
        if dt=='01/01/2000':
            dt = None
        return  dt

    def checkIntValue(self, value):
        try:
            v = int(value)
        except ValueError:
            v = None
        return v

    def checkValue(self, value):
        v = value
        if not value:
            v = None
        return v

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


