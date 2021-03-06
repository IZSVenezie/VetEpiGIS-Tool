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

import os, shutil, math
from osgeo import ogr
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import Qt, QSettings, QCoreApplication, QFile, QFileInfo, QDate, QVariant, \
    pyqtSignal, QRegExp, QDateTime, QTranslator, QSize
from qgis.PyQt.QtSql import *
from qgis.PyQt.QtXml import *
from qgis.PyQt.QtWidgets import *

from qgis.core import QgsField, QgsSpatialIndex, QgsMessageLog, QgsProject, \
    QgsCoordinateTransform, Qgis, QgsVectorFileWriter, QgsFeature, \
    QgsGeometry, QgsFeatureRequest, QgsPoint, QgsVectorLayer, QgsCoordinateReferenceSystem, \
    QgsRectangle, QgsDataSourceUri, QgsDataProvider, QgsWkbTypes, QgsPointXY, QgsLayout, \
    QgsReadWriteContext, QgsLayoutExporter, QgsLayoutItemPage, QgsVectorDataProvider

#Composer
#All composer related methods have been removed from the public API and Python bindings. These classes have been replaced with the new layouts engine, based on QgsLayout, QgsLayoutItem, and the other related classes.
#, QgsComposition, QgsComposerMap, QgsAtlasComposition

from qgis.gui import QgsMapTool, QgsMapToolEmitPoint, QgsMessageBar, QgsRubberBand

from .plugin import buffer, caser, select, outbreaklayer, xabout, poi, dbtbs, dbmaint, xsettings, \
    qvfuncs, xcoordtrafo, query, zone, export, xprint, exportDB

from .resources_rc import *
# import lxml.etree as etree

from uuid import getnode as get_mac


mutato = QCursor(
    QPixmap(
        ["16 16 3 1",
        "      c None",
        ".     c #FE0000",
        "+     c #000E52",
        "                ",
        "        .       ",
        "       +.+      ",
        "     +.....+    ",
        "    +.     .+   ",
        "   +.   .   .+  ",
        "  +.    .    .+ ",
        "  +.    .    .+ ",
        " ... ...+... ...",
        "  +.    .    .+ ",
        "  +.    .    .+ ",
        "   +.   .   .+  ",
        "    +.     .+   ",
        "     +.....+    ",
        "       +.+      ",
        "        .       "]
    )
)



class VetEpiGIStool:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        self.loadSettings()

        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'VetEpiGIStool_{}.qm'.format(locale))

        self.vers = '0.800'
        self.prevcur = self.iface.mapCanvas().cursor()

        self.origtool = QgsMapTool(self.iface.mapCanvas())

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.dockw = dbtbs.DockWidget()

        self.mac = '_'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))
        dbuid = 'db_%s.sqlite' % self.mac
        dbfold = os.path.join(self.plugin_dir, 'db')
        self.dbuidpath = os.path.join(dbfold, dbuid)
        if not os.path.isfile(self.dbuidpath):
            shutil.copy(os.path.join(dbfold, 'base.sqlite'), self.dbuidpath)

        self.uri = QgsDataSourceUri()
        self.uri.setDatabase(self.dbuidpath)

        self.db = QSqlDatabase.addDatabase('QSPATIALITE')
        self.db.setDatabaseName(self.uri.database())

        self.loadLists()
        self.sldLoader()
        self.loadModel()

        self.dockw.tableView.doubleClicked.connect(self.layersinDBLoad)

        self.polyn = 0

        self.obrflds = ['gid', 'localid', 'code', 'largescale', 'disease', 'animalno', 'species', 'production', \
            'year', 'status', 'suspect', 'confirmation', 'expiration', 'notes', 'hrid', 'timestamp', 'grouping']
        self.poiflds = self.obrflds[0:3]
        self.poiflds.append('activity')
        self.poiflds.append('hrid')
        self.bufflds = self.obrflds[0:-1]
        self.zonflds = ['localid', 'code', 'disease', 'zonetype', 'subpopulation', 'validity_start', \
                'validity_end', 'legal_framework', 'competent_authority', 'biosecurity_measures', \
                'control_of_vectors', 'control_of_wildlife_reservoir', 'modified_stamping_out', \
                'movement_restriction', 'stamping_out', 'surveillance', 'vaccination', \
                'other_measure', 'related', 'hrid', 'timestamp']

        self.funcs = qvfuncs.VetEpiGISFuncs()


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('VetEpiGIS-Tool', message)


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.newoutbreak = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/biological1.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Create new outbreak layer"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.newoutbreak)
        self.newoutbreak.triggered.connect(self.createOlayer)

        self.Caser = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/icon01.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Add case (POINT)"),
            self.iface.mainWindow())
        self.Caser.setCheckable(True)
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.Caser)
        self.Caser.triggered.connect(self.caseCapture)
# http://www.lutraconsulting.co.uk/blog/2014/10/17/getting-started-writing-qgis-python-plugins/

        self.handy = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/love62.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Add case (POLYGON drawing)"),
            self.iface.mainWindow())
        self.handy.setCheckable(True)
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.handy)
        self.handy.triggered.connect(self.handDrawing)

        self.copyselected = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/copy32.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Copy an element to outbreak layer"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.copyselected)
        self.copyselected.triggered.connect(self.copySel)

        self.recedit = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/pencil148.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Edit case data"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.recedit)
        self.recedit.triggered.connect(self.featEdit)

        self.sep = QAction(self.iface.mainWindow())
        self.sep.setSeparator(True)
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.sep)

        self.newpoilayer = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/mappointer15.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Create new POI layer"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.newpoilayer)
        self.newpoilayer.triggered.connect(self.createPOIlayer)

        self.poier = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/pin56.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Add POI"),
            self.iface.mainWindow())
        self.poier.setCheckable(True)
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.poier)
        self.poier.triggered.connect(self.addPOI)

        self.receditPOI = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/pencil148.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Edit POI data"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.receditPOI)
        self.receditPOI.triggered.connect(self.featEditPOI)

        self.sep2 = QAction(self.iface.mainWindow())
        self.sep2.setSeparator(True)
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.sep2)

        self.Bufferer = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/icon03.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Create buffers"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.Bufferer)
        self.Bufferer.triggered.connect(self.createBuffers)

        self.POIer = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/icon05.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Select points from POI layer"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.POIer)
        self.POIer.triggered.connect(self.selectPOIs)

        self.Zoner = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/icon04.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Create zones"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.Zoner)
        self.Zoner.triggered.connect(self.selectROIs)

        self.sep3 = QAction(self.iface.mainWindow())
        self.sep3.setSeparator(True)
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.sep3)

        self.dbtabs = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/data112.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Show/hide VetEpiGIS database layers"),
            self.iface.mainWindow())
        self.dbtabs.setCheckable(True)
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.dbtabs)
        self.dbtabs.triggered.connect(self.layersinDB)


        # self.grouping = QAction(
        #     QIcon(':/plugins/VetEpiGIStool/images/filter11.png'),
        #     QCoreApplication.translate('VetEpiGIS-Tool', "Query tool"),
        #     self.iface.mainWindow())
        # self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.grouping)
        # self.grouping.triggered.connect(self.aliasing)

        self.Saver = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/save26.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Save layer into VetEpiGIS database"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.Saver)
        self.Saver.triggered.connect(self.saveLayer)

        self.dbmaintain = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/database19.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Database maintenance"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.dbmaintain)
        self.dbmaintain.triggered.connect(self.dbMaintain)

        self.xprt = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/arrows.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Export selected layer"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.xprt)
        self.xprt.triggered.connect(self.expLayer)

        self.xprtDB = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/arrows.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Export complete database"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.xprtDB)
        self.xprtDB.triggered.connect(self.expDB)

        self.xprnt = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/tool-1.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Print VetEpiGIS template"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.xprnt)
        self.xprnt.triggered.connect(self.printMap)

        self.sep4 = QAction(self.iface.mainWindow())
        self.sep4.setSeparator(True)
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.sep4)

        self.prop = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/music236.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Settings"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.prop)
        self.prop.triggered.connect(self.saveSettings)

        self.copydb = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/music236.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Copy database"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.copydb)
        # self.copydb.triggered.connect(self.fcopydb)

        # self.pluginupdate = QAction(
        #     QIcon(':/plugins/VetEpiGIStool/images/music236.png'),
        #     QCoreApplication.translate('VetEpiGIS-Tool', "Update VetEpiGIS-Tool plugin"),
        #     self.iface.mainWindow())
        # self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.pluginupdate)
        # self.pluginupdate.triggered.connect(self.fpluginupdate)

        self.sep5 = QAction(self.iface.mainWindow())
        self.sep5.setSeparator(True)
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.sep5)

        self.actAbout = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/icon02.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', 'About'),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.actAbout)
        self.actAbout.triggered.connect(self.about)

        self.toolbar = self.iface.addToolBar(
            QCoreApplication.translate('VetEpiGIS-Tool', 'VetEpiGIS-Tool'))
        self.toolbar.setObjectName(
            QCoreApplication.translate('VetEpiGIS-Tool', 'VetEpiGIS-Tool'))

        """Add buttons to the toolbar"""
        # self.toolbar.addAction(self.newoutbreak)
        # self.toolbar.addAction(self.Caser)
        # self.toolbar.addAction(self.handy)
        # self.toolbar.addAction(self.copyselected)
        # self.toolbar.addAction(self.sep)
        # self.toolbar.addAction(self.newpoilayer)
        # self.toolbar.addAction(self.poier)
        # self.toolbar.addAction(self.sep2)
        # self.toolbar.addAction(self.Bufferer)
        # self.toolbar.addAction(self.POIer)
        # self.toolbar.addAction(self.Zoner)
        # self.toolbar.addAction(self.sep3)
        # self.toolbar.addAction(self.dbtabs)
        # self.toolbar.addAction(self.recedit)
        # # self.toolbar.addAction(self.grouping)
        # self.toolbar.addAction(self.Saver)
        # self.toolbar.addAction(self.dbmaintain)
        # self.toolbar.addAction(self.xprt)
        # self.toolbar.addAction(self.xprnt)
        # # self.toolbar.addAction(self.sep5)
        # # self.toolbar.addAction(self.prop)

        self.sep10 = QAction(self.iface.mainWindow())
        self.sep10.setSeparator(True)

        self.grp1 = QToolButton(self.toolbar)
        self.grp1.setPopupMode(QToolButton.MenuButtonPopup)
        self.grp1.addActions([self.newoutbreak, self.Caser, self.handy, self.copyselected, self.sep10, self.recedit])
        self.grp1.setDefaultAction(self.newoutbreak)
        self.toolbar.addWidget(self.grp1)

        self.grp2 = QToolButton(self.toolbar)
        self.grp2.setPopupMode(QToolButton.MenuButtonPopup)
        self.grp2.addActions([self.newpoilayer, self.poier, self.sep10, self.receditPOI])
        self.grp2.setDefaultAction(self.newpoilayer)
        self.toolbar.addWidget(self.grp2)

        self.grp3 = QToolButton(self.toolbar)
        self.grp3.setPopupMode(QToolButton.MenuButtonPopup)
        self.grp3.addActions([self.Bufferer, self.POIer, self.Zoner])
        self.grp3.setDefaultAction(self.Bufferer)
        self.toolbar.addWidget(self.grp3)

        self.grp4 = QToolButton(self.toolbar)
        self.grp4.setPopupMode(QToolButton.MenuButtonPopup)
        self.grp4.addActions([self.dbtabs, self.Saver, self.dbmaintain, self.xprt, self.xprtDB, self.xprnt])
        self.grp4.setDefaultAction(self.xprnt)
        self.toolbar.addWidget(self.grp4)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.iface.removePluginMenu('&VetEpiGIS-Tool', self.actAbout)
        del self.toolbar


    def printMap(self):
        self.grp4.setDefaultAction(self.xprnt)
        dlg = xprint.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Print map')
        logopath = os.path.join(self.plugin_dir, 'templates/logo.png')
        dlg.label.setPixmap(QPixmap(logopath))

        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            if dlg.logopath!='':
                shutil.copy(dlg.logopath, logopath)

            canv = self.iface.mapCanvas()
            #rend = canv.mapRenderer()
            rect = QgsRectangle(self.iface.mapCanvas().extent())

            qpt = os.path.join(self.plugin_dir, 'templates/qvet_h_template_vqgis3.qpt')
            if dlg.radioButton_2.isChecked():
                qpt = os.path.join(self.plugin_dir, 'templates/qvet_v_template_vqgis3.qpt')

            # with open(qpt, 'r') as f:
            #     tree = etree.parse(f)
            #     for elem in tree.iter(tag = 'Extent'):
            #         elem.attrib['xmax'] = str(rect.xMaximum())
            #         elem.attrib['xmin'] = str(rect.xMinimum())
            #         elem.attrib['ymax'] = str(rect.yMaximum())
            #         elem.attrib['ymin'] = str(rect.yMinimum())
            #
            # tmplt = etree.tostring(tree, encoding='utf8', method='xml')

            ff = open(qpt, 'r')
            tmplt = ff.read()
            ff.close()
            tmplt = tmplt.replace("iymin", str(rect.yMinimum()))
            tmplt = tmplt.replace("iymax", str(rect.yMaximum()))
            tmplt = tmplt.replace("ixmin", str(rect.xMinimum()))
            tmplt = tmplt.replace("ixmax", str(rect.xMaximum()))

            s1 = '%s&#' % dlg.lineEdit.text()
            tmplt = tmplt.replace("TITLE&#", s1.upper())
            s2 = dlg.lineEdit_2.text()
            tmplt = tmplt.replace("Subtitle", s2.title())
            tmplt = tmplt.replace('logo.png', logopath)

            doc = QDomDocument()
            doc.setContent(tmplt)

            project = QgsProject.instance()
            l = QgsLayout(project)
            l.initializeDefaults()

            items, ok = l.loadFromTemplate(doc, QgsReadWriteContext(), False)
            #Add in legend only visible layers
            llegend = l.itemById("legend")
            llegend.setLegendFilterByMapEnabled(True)

            pdfpath = dlg.lineEdit_3.text()
            xt = os.path.splitext(pdfpath)[-1].lower()
            if xt!='.pdf':
                pdfpath = '%s.pdf' % pdfpath

            #Set portait page size if "Portrait" is checked
            if dlg.radioButton_2.isChecked():
                pc = l.pageCollection()
                pc.page(0).setPageSize('A4', QgsLayoutItemPage.Orientation.Portrait)

            exporter = QgsLayoutExporter(l)
            res = exporter.exportToPdf(pdfpath, QgsLayoutExporter.PdfExportSettings())
            if res == 0:
                self.iface.messageBar().pushMessage('Print map', 'Layout exported', level=Qgis.Info)
                self.handy.setChecked(False)
                QApplication.restoreOverrideCursor()
            else:
                self.iface.messageBar().pushMessage('Print map', 'Error exporting layout', level=Qgis.Warning)
                self.handy.setChecked(False)
                QApplication.restoreOverrideCursor()
                return

    def expLayer(self):
        self.grp4.setDefaultAction(self.xprt)
        plugin_title = 'Export selected layer'
        dlg = export.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle(plugin_title)

        lyr = self.checklayer()
        if lyr is None:
            return

        ln = str(lyr.name()).lower()
        prv = lyr.dataProvider()
        didx = lyr.fields().indexFromName('disease')
        yidx = lyr.fields().indexFromName('year')
        nslst = []
        tlst = []
        flds = lyr.dataProvider().fields()
        for fld in flds:
            nslst.append(fld.name())
            tlst.append(fld.type())

        lst1 = []
        lst2 = []
        feats = prv.getFeatures()
        feat = QgsFeature()
        vetLayer = False #check if it is a layer of vetepigis tool
        if (nslst==self.obrflds or nslst==self.bufflds or nslst == self.zonflds or nslst == self.poiflds):
            #outbreak and/or buffer layers
            vetLayer = True
            if (nslst==self.obrflds or nslst==self.bufflds):
                while feats.nextFeature(feat):
                    lst1.append(feat.attributes()[didx])
                    lst2.append(feat.attributes()[yidx])

            #zone layer
            elif nslst == self.zonflds:
                yidx = lyr.fields().indexFromName('zonetype')
                while feats.nextFeature(feat):
                    lst1.append(feat.attributes()[didx])
                    lst2.append(feat.attributes()[yidx])
                #change the label of the table
                dlg.label_year.setText('Zone type:')
                item = dlg.tableWidget_right.horizontalHeaderItem(0)
                item.setText('Zone type')

            #poi layer
            elif nslst == self.poiflds:
                didx = lyr.fields().indexFromName('activity')
                while feats.nextFeature(feat):
                    lst1.append(feat.attributes()[didx])

                #change the label of the table
                dlg.label_disease.setText('Activity:')
                dlg.label_year.setText('')
                dlg.label_year.setEnabled(False)
                dlg.tableWidget_right.setVisible(False)
                item = dlg.tableWidget_left.horizontalHeaderItem(0)
                item.setText('Activity')

            lst1 = sorted(set(lst1))

            for it in lst1:
                dlg.tableWidget_left.insertRow(dlg.tableWidget_left.rowCount())
                nr = dlg.tableWidget_left.rowCount() - 1
                item = QTableWidgetItem(it)
                dlg.tableWidget_left.setItem(nr, 0, item)

            dlg.tableWidget_left.selectAll()

            if lst2:
                lst2 = sorted(set(lst2))
                for it in lst2:
                    dlg.tableWidget_right.insertRow(dlg.tableWidget_right.rowCount())
                    nr = dlg.tableWidget_right.rowCount() - 1
                    item = QTableWidgetItem(str(it))
                    dlg.tableWidget_right.setItem(nr, 0, item)

                dlg.tableWidget_right.selectAll()
        else:
            dlg.tableWidget_left.setEnabled(False)
            dlg.tableWidget_right.setEnabled(False)
            dlg.label_year.setEnabled(False)
            dlg.label_disease.setEnabled(False)
            dlg.checkBox_selection.setChecked(False)
            dlg.checkBox_selection.setEnabled(False)

        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)

            if dlg.lineEdit_output.text()=='':
                self.iface.messageBar().pushMessage('Export selected layer','Set the output path', level=Qgis.Warning)
                QApplication.restoreOverrideCursor()
                return

            if dlg.comboBox_format.currentText()=='ESRI shape file':
                #TODO: is it useful to check if the layer selected is a buffer, poi, outbreak...?
                wrt = QgsVectorFileWriter.writeAsVectorFormat(lyr,
                    dlg.lineEdit_output.text(),
                    'system',
                    QgsCoordinateReferenceSystem(prv.crs().srsid(), QgsCoordinateReferenceSystem.InternalCrsId),
                    'ESRI Shapefile')

            elif dlg.comboBox_format.currentText()=='Comma separated value (CSV)':
                lops = []
                if dlg.comboBox_separator.currentText()==';':
                    lops.append('SEPARATOR=SEMICOLON')
                elif dlg.comboBox_separator.currentText()==',':
                    lops.append('SEPARATOR=COMMA')
                elif dlg.comboBox_separator.currentText()=='tab':
                    lops.append('SEPARATOR=TAB')

                if dlg.checkBox_wkt.isChecked():
                    lops.append('GEOMETRY=AS_WKT')

                wrt = QgsVectorFileWriter.writeAsVectorFormat(lyr,
                    dlg.lineEdit_output.text(),
                    'system',
                    QgsCoordinateReferenceSystem(prv.crs().srsid(), QgsCoordinateReferenceSystem.InternalCrsId),
                    'CSV', layerOptions=lops)

            elif dlg.comboBox_format.currentText()=='SQLite database':
                lsta = []
                lstb = []
                existing_layer = 'False'
                if vetLayer:
                    for it in dlg.tableWidget_left.selectedItems():
                        lsta.append(it.text())
                        # self.iface.messageBar().pushMessage('Information', '%s' % it.text(), level=Qgis.Info)

                    for it in dlg.tableWidget_right.selectedItems():
                        lstb.append(str(it.text()))

                outputDBName = dlg.lineEdit_output.text()
                dbfold = os.path.join(self.plugin_dir, 'db')

                #Ckeck if "create database" is checked
                if dlg.checkBox_newdb.isChecked():

                    dbpath = QFileInfo(outputDBName).absoluteFilePath()

                    if not os.path.isfile(outputDBName):
                        shutil.copy(os.path.join(dbfold, 'base.sqlite'), dbpath)

                uri = QgsDataSourceUri()
                uri.setDatabase(outputDBName)
                edb = QSqlDatabase.addDatabase('QSPATIALITE')
                edb.setDatabaseName(uri.database())
                edb.open()

                layer_name = lyr.sourceName()
                #TODO: check if layer already exixst
                tablst = edb.tables()

                if layer_name in tablst:
                    #message box for overwrite layer
                    # overwrite_msg = QMessageBox.question(self.iface.mainWindow(),
                    #     "Warning", "Do you want overwrite existing layer?",
                    #     QMessageBox.Yes, QMessageBox.No)
                    # #if ok overwrite
                    # if overwrite_msg == QMessageBox.Yes:
                    #     existing_layer = True

                    #TODO: don't delete the existing layer but save the "old" layer
                    #and create a new one.
                    #By now only display a message that the layer already exist and exits from the tool.

                    #Issue in ALTER TABLE RENAME command in spatialite, the geometry is removed
                    #https://github.com/qgis/QGIS/issues/27425
                    #https://github.com/qgis/QGIS/issues/22236

                    existing_msg = QMessageBox.information(self.iface.mainWindow(),"Existing layer", \
                        'There is already a layer with the same name.')
                    QApplication.restoreOverrideCursor()
                    return

                lgt = lyr.geometryType()

                ntlst = self.fieldCheck(nslst)

                sql = 'create table %s (' % ln
                for i in range(len(ntlst)):
                    t = 'text'
                    if tlst[i] == 2:
                        t = 'numeric'

                    sql += '%s %s, ' % (ntlst[i], t)

                sql += ')'
                sql = sql.replace(', )', ')')

                q = edb.exec_(sql)

                prv = lyr.dataProvider()
                if vetLayer:
                    if lgt == 0:
                        sql = "SELECT AddGeometryColumn('%s', 'geom', 4326, 'POINT', 'XY')" % ln
                    elif lgt == 2:
                        sql = "SELECT AddGeometryColumn('%s', 'geom', 4326, 'MULTIPOLYGON', 'XY')" % ln
                else:
                    #Add any kind of geometry type
                    sql = self.addGeometryColumnSL(lyr,ln)

                q = edb.exec_(sql)
                edb.commit()
                edb.close()

                uri.setDataSource('', ln, 'geom')
                vl = QgsVectorLayer(uri.uri(), ln, 'spatialite')
                vl.startEditing()

                feats = prv.getFeatures()
                feat = QgsFeature()
                #TODO: manage the SRS
                while feats.nextFeature(feat):
                    # self.iface.messageBar().pushMessage('Information', '%s %s' % (feat.attributes()[didx], feat.attributes()[yidx]), level=Qgis.Info)
                    if lstb:
                        if (feat.attributes()[didx] in lsta) and (str(feat.attributes()[yidx]) in lstb):
                            vl.addFeature(feat)
                    elif lsta:
                        if (feat.attributes()[didx] in lsta):
                            vl.addFeature(feat)
                    else:
                        vl.addFeature(feat)

                vl.commitChanges()
                vl.updateExtents()

            QApplication.restoreOverrideCursor()
            self.iface.messageBar().pushMessage(plugin_title, 'Layer exported.', level=Qgis.Info)


    def expDB(self):
        self.grp4.setDefaultAction(self.xprtDB)
        dlg = exportDB.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Export complete database')
        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            if dlg.lineEdit_file.text()!='':
                ret = shutil.copy(self.dbuidpath, dlg.lineEdit_file.text())
                #TODO: check how better verify if the database is exported
                if 'ret' in locals():
                    self.iface.messageBar().pushMessage('Export complete database', 'Database exported', level=Qgis.Info)
                else:
                    self.iface.messageBar().pushMessage('Export complete database', 'Error exporting database', level=Qgis.Warning)
            else:
                self.iface.messageBar().pushMessage('Export complete database', 'Select the output path of sqlite database!', level=Qgis.Warning)

        QApplication.restoreOverrideCursor()


    def sldLoader(self):
        sldpath = os.path.join(self.plugin_dir, 'sld')
        if not self.db.open():
            self.db.open()

        query = self.db.exec_("select sld from xstyles where ltype='outbreak_point'")
        while query.next():
            self.sldOutbreakPoint = os.path.join(sldpath, query.value(0))

        query = self.db.exec_("select sld from xstyles where ltype='outbreak_area'")
        while query.next():
            self.sldOutbreakArea = os.path.join(sldpath, query.value(0))

        query = self.db.exec_("select sld from xstyles where ltype='poi'")
        while query.next():
            self.sldPOI = os.path.join(sldpath, query.value(0))

        query = self.db.exec_("select sld from xstyles where ltype='buffer'")
        while query.next():
            self.sldBuffer = os.path.join(sldpath, query.value(0))

        query = self.db.exec_("select sld from xstyles where ltype='zone_a'")
        while query.next():
            self.sldZoneA = os.path.join(sldpath, query.value(0))

        query = self.db.exec_("select sld from xstyles where ltype='zone_b'")
        while query.next():
            self.sldZoneB = os.path.join(sldpath, query.value(0))

        self.db.close()


    def aliasing(self):
        lyr = self.checklayer()
        if lyr is None:
            return

        prv = lyr.dataProvider()
        flds = prv.fields()
        flst = []
        for fld in flds:
            flst.append(fld.name())

        if flst != self.obrflds:
            return

        dlg = query.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Create aliases')

        feat = QgsFeature()
        feats = prv.getFeatures()
        slst = []
        plst = []

        while feats.nextFeature(feat):
            attr = feat.attributes()
            sl = str(attr[6]).split(' | ')
            for i in range(len(sl)):
                slst.append(sl[i])
            pl = str(attr[7]).split(' | ')
            for i in range(len(pl)):
                plst.append(pl[i])

        dlg.usl = list(set(slst))
        dlg.upl = list(set(plst))
        dlg.comboBox_2.addItem('Species')
        dlg.comboBox_2.addItem('Type of production')
        dlg.lister()


        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            feats = prv.getFeatures()
            n = 6
            if dlg.comboBox_2.currentText()!='Species':
                n = 7

            items = []
            aliases = []
            rn = dlg.tableWidget.rowCount()
            for i in range(rn):
                items.append(dlg.tableWidget.item(i, 0).text())
                aliases.append(dlg.tableWidget.item(i, 1).text())

            lyr.startEditing()
            while feats.nextFeature(feat):
                attr = feat.attributes()
                lanc = str(attr[n])
                fid = feat.id()
                for i in range(len(items)):
                    if lanc.find(items[i])!=-1:
                        lyr.changeAttributeValue(fid, 15, aliases[i])

            lyr.commitChanges()
            QApplication.restoreOverrideCursor()


    def saveSettings(self):
        dlg = xsettings.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('VetEpiGIStool settings')

        dlg.comboBox.addItem('en')
        dlg.comboBox.addItem('it')

        dlg.comboBox.setCurrentIndex(dlg.comboBox.findText(self.lang, Qt.MatchExactly))

        dlg.plugin_dir = self.plugin_dir

        if not self.db.open():
            self.db.open()

        query = self.db.exec_("select ltype, sld from xstyles order by id")
        while query.next():
            if query.value(0)=='outbreak_point':
                dlg.lineEdit.setText(query.value(1))
            if query.value(0)=='outbreak_area':
                dlg.lineEdit_2.setText(query.value(1))
            if query.value(0)=='buffer':
                dlg.lineEdit_3.setText(query.value(1))
            if query.value(0)=='poi':
                dlg.lineEdit_4.setText(query.value(1))
            if query.value(0)=='zone_a':
                dlg.lineEdit_5.setText(query.value(1))
            if query.value(0)=='zone_b':
                dlg.lineEdit_6.setText(query.value(1))
        self.db.close()

        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            s = QSettings()
            s.setValue('vetepigis/lang', dlg.comboBox.currentText())

            if not self.db.open():
                self.db.open()

            s = dlg.lineEdit.text()
            if s!='':
                q = self.db.exec_("update xstyles set sld='%s' where ltype='outbreak_point'" % s)
            s = dlg.lineEdit_2.text()
            if s!='':
                q = self.db.exec_("update xstyles set sld='%s' where ltype='outbreak_area'" % s)
            s = dlg.lineEdit_3.text()
            if s!='':
                q = self.db.exec_("update xstyles set sld='%s' where ltype='buffer'" % s)
            s = dlg.lineEdit_4.text()
            if s!='':
                q = self.db.exec_("update xstyles set sld='%s' where ltype='poi'" % s)
            s = dlg.lineEdit_5.text()
            if s!='':
                q = self.db.exec_("update xstyles set sld='%s' where ltype='zone_a'" % s)
            s = dlg.lineEdit_6.text()
            if s!='':
                q = self.db.exec_("update xstyles set sld='%s' where ltype='zone_b'" % s)

            self.db.close()

            self.loadSettings()
            self.sldLoader()

            QApplication.restoreOverrideCursor()


    def loadSettings(self):
        s = QSettings()
        self.lang = s.value('qvet/lang', 'en')


    def dbMaintain(self):
        self.grp4.setDefaultAction(self.dbmaintain)
        self.iface.messageBar().pushMessage('Information', 'Layers modified by the tool will be removed from the workspace.', level=Qgis.Info)
        #QgsProject.instance().removeAllMapLayers()

        dlg = dbmaint.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)

        dlg.setWindowTitle('Database maintenance')
        dlg.toolButton_translation.setIcon(QIcon(':/plugins/VetEpiGIStool/images/verify8.png'))

        dlg.comboBox_lists.addItem('')
        dlg.comboBox_lists.addItem('Diseases')
        dlg.comboBox_lists.addItem('POI types')
        dlg.comboBox_lists.addItem('Species')

        dlg.comboBox_translation.addItem('en')
        dlg.comboBox_translation.addItem('it')

        dlg.db = self.db
        dlg.loadLayers()

        if dlg.exec_() == QDialog.Accepted:
            self.loadModel()
            self.loadLists() #reload lists after the upadate

        self.iface.messageBar().clearWidgets()


    def loadLists(self):
        if not self.db.open():
            self.db.open()

        self.lsta = []
        query = self.db.exec_("select disease from xdiseases where lang='%s' order by disease" % self.lang)
        while query.next():
            self.lsta.append(query.value(0))

        self.lstb = []
        query = self.db.exec_("select species from xspecies where lang='%s' order by species" % self.lang)
        while query.next():
            self.lstb.append(query.value(0))

        self.lstpt = []
        query = self.db.exec_("select poitype from xpoitypes where lang='%s' order by poitype" % self.lang)
        while query.next():
            self.lstpt.append(query.value(0))

        self.db.close()


    # def dbMaintain2(self):
    #     self.grp4.setDefaultAction(self.dbmaintain)
    #     self.iface.messageBar().pushMessage('Information', 'Layers modified by the tool will be removed from the workspace.', level=Qgis.Info)
    #     #QgsProject.instance().removeAllMapLayers()

    #     dlg = dbmaint2.Dialog()
    #     x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
    #     y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
    #     dlg.move(x,y)

    #     dlg.setWindowTitle('Database maintenance')
    #     dlg.toolButton_translation.setIcon(QIcon(':/plugins/VetEpiGIStool/images/verify8.png'))

    #     dlg.comboBox_lists.addItem('')
    #     dlg.comboBox_lists.addItem('Diseases')
    #     dlg.comboBox_lists.addItem('POI types')
    #     dlg.comboBox_lists.addItem('Species')

    #     dlg.comboBox_translation.addItem('en')
    #     dlg.comboBox_translation.addItem('it')

    #     dlg.db = self.db
    #     dlg.loadLayers()

    #     if dlg.exec_() == QDialog.Accepted:
    #         self.loadModel()

    #     self.iface.messageBar().clearWidgets()


    def featEdit(self):
        self.grp1.setDefaultAction(self.recedit)
        lyr = self.checklayer()
        if lyr is None:
            return

        if lyr.selectedFeatureCount()!=1:
            # only one object selection allowed
            self.iface.messageBar().pushMessage('Edit case data ', 'Select ONE object from outbreak layer', level=Qgis.Warning)
            return

        flds = lyr.dataProvider().fields()
        flst = []
        for fld in flds:
            flst.append(fld.name())

        tn = ''

        if flst == self.obrflds:
            tn = 'outbreak'

        if (tn=='' or tn != 'outbreak'):
            self.iface.messageBar().pushMessage('Edit case data ', 'Select ONE object from outbreak layer', level=Qgis.Warning)
            return

        feat = lyr.selectedFeatures()[0]
        attr = feat.attributes()
        fid = feat.id()


        dlg = caser.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Create new case')
        dlg.label_10_outbreak_layer.setVisible(False)
        dlg.comboBox_5_outbreak_layer.setVisible(False)
        dlg.label_longitude.setVisible(False)
        dlg.lineEdit_longitude.setVisible(False)
        dlg.toolButton_3_dms.setVisible(False)
        dlg.label_2_latitude.setVisible(False)
        dlg.lineEdit_2_latitude.setVisible(False)
        dlg.label_4_reference.setVisible(False)
        dlg.comboBox_reference.setVisible(False)

        dlg.comboBox_2_disease.addItem('')
        for it in self.lsta:
            dlg.comboBox_2_disease.addItem(it)

        dlg.lstb = self.lstb

        dlg.lineEdit_3_id.setText(str(attr[1]))
        dlg.lineEdit_5_code.setText(str(attr[2]))
        dlg.comboBox_4_large_scale.setCurrentIndex(dlg.comboBox_4_large_scale.findText(attr[3], Qt.MatchExactly))
        dlg.comboBox_2_disease.setCurrentIndex(dlg.comboBox_2_disease.findText(attr[4], Qt.MatchExactly))
        dlg.lineEdit_6_num_animals.setText(str(attr[5]))

        slst = str(attr[6]).split(' | ')
        plst = str(attr[7]).split(' | ')
        for i in range(len(slst)):
            dlg.tableWidget.insertRow(dlg.tableWidget.rowCount())
            nr = dlg.tableWidget.rowCount() - 1
            item = QTableWidgetItem(slst[i])
            dlg.tableWidget.setItem(nr, 0, item)
            item = QTableWidgetItem(str(plst[i]))
            dlg.tableWidget.setItem(nr, 1, item)

        dlg.lineEdit_4_year.setText(str(attr[8]))
        dlg.comboBox_3_status.setCurrentIndex(dlg.comboBox_3_status.findText(attr[9], Qt.MatchExactly))
        k = '01/01/2000'
        f = 'dd/MM/yyyy'
        s = k
        if attr[10]!='' and not attr[10].isNull():
            s = attr[10]
            dlg.dateEdit_dates_suspect.setEnabled(True)
            dlg.checkBox_dates_suspect.setChecked(True)
            qd = QDate.fromString(s, f)
            dlg.dateEdit_dates_suspect.setDate(qd)
        s = k
        if attr[11]!='' and not attr[11].isNull():
            s = attr[11]
            dlg.dateEdit_2_dates_confirmation.setEnabled(True)
            dlg.checkBox_2_dates_confirmation.setChecked(True)
            qd = QDate.fromString(s, f)
            dlg.dateEdit_2_dates_confirmation.setDate(qd)
        s = k
        if attr[12]!='' and not attr[12].isNull():
            s = attr[12]
            dlg.dateEdit_3_dates_expiration.setEnabled(True)
            dlg.checkBox_3_dates_expiration.setChecked(True)
            qd = QDate.fromString(s, f)
            dlg.dateEdit_3_dates_expiration.setDate(qd)

        if attr[13]!='' and not attr[13].isNull():
            dlg.textEdit_notes.setText(attr[13])
        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)

            lyr.startEditing()
            species = ''
            production = ''
            rn = dlg.tableWidget.rowCount()
            for i in range(rn):
                if i==0:
                    species = dlg.tableWidget.item(i, 0).text()
                    production = dlg.tableWidget.item(i, 1).text()
                else:
                    species = species + ' | ' + dlg.tableWidget.item(i, 0).text()
                    production = production + ' | ' + dlg.tableWidget.item(i, 1).text()

            lyr.changeAttributeValue(fid, 1, dlg.lineEdit_3_id.text())
            lyr.changeAttributeValue(fid, 2, dlg.lineEdit_5_code.text())
            lyr.changeAttributeValue(fid, 3, dlg.comboBox_4_large_scale.currentText())
            lyr.changeAttributeValue(fid, 4, dlg.comboBox_2_disease.currentText())
            lyr.changeAttributeValue(fid, 5, dlg.lineEdit_6_num_animals.text())
            lyr.changeAttributeValue(fid, 6, species)
            lyr.changeAttributeValue(fid, 7, production)
            lyr.changeAttributeValue(fid, 8, dlg.lineEdit_4_year.text())
            lyr.changeAttributeValue(fid, 9, dlg.comboBox_3_status.currentText())
            lyr.changeAttributeValue(fid, 10, self.funcs.dateCheck(dlg.dateEdit_dates_suspect.date()))
            lyr.changeAttributeValue(fid, 11, self.funcs.dateCheck(dlg.dateEdit_2_dates_confirmation.date()))
            lyr.changeAttributeValue(fid, 12, self.funcs.dateCheck(dlg.dateEdit_3_dates_expiration.date()))
            lyr.changeAttributeValue(fid, 13, dlg.textEdit_notes.toPlainText())
            lyr.changeAttributeValue(fid, 15, QDateTime.currentDateTimeUtc().toString('dd/MM/yyyy hh:mm:ss'))
            lyr.commitChanges()

            QApplication.restoreOverrideCursor()

    def featEditPOI(self):
        self.grp2.setDefaultAction(self.receditPOI)
        lyr = self.checklayer()
        if lyr is None:
            return

        if lyr.selectedFeatureCount()!=1:
            # only one object selection allowed
            self.iface.messageBar().pushMessage('Edit poi data ', 'Select ONE object from poi layer', level=Qgis.Warning)
            return

        flds = lyr.dataProvider().fields()
        flst = []
        for fld in flds:
            flst.append(fld.name())

        tn = ''
        if flst == self.poiflds:
            tn = 'poi'

        if tn=='' or tn != 'poi':
            self.iface.messageBar().pushMessage('Edit poi data ', 'Select ONE object from poi layer', level=Qgis.Warning)
            return

        feat = lyr.selectedFeatures()[0]
        attr = feat.attributes()
        fid = feat.id()

        dlg = poi.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Point of Interest')

        dlg.comboBox.addItem('')
        for it in self.lstpt:
            dlg.comboBox.addItem(it)

        dlg.label.setVisible(False)
        dlg.lineEdit_longitude.setVisible(False)
        dlg.toolButton.setVisible(False)
        dlg.label_2.setVisible(False)
        dlg.lineEdit_2_latitude.setVisible(False)
        dlg.setMaximumHeight(150)

        dlg.lineEdit_3.setText(attr[1])
        dlg.lineEdit_5.setText(attr[2])
        dlg.comboBox.setCurrentIndex(dlg.comboBox.findText(attr[3], Qt.MatchExactly))

        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)

            lyr.startEditing()
            lyr.changeAttributeValue(fid, 1, dlg.lineEdit_3.text())
            lyr.changeAttributeValue(fid, 2, dlg.lineEdit_5.text())
            lyr.changeAttributeValue(fid, 3, dlg.comboBox.currentText())
            lyr.commitChanges()

            QApplication.restoreOverrideCursor()


    def checklayer(self):
        if QgsProject.instance().count()==0:
            QMessageBox.warning(self.iface.mainWindow(),
                "Warning", "Please add a vector layer.",
                buttons=QMessageBox.Ok, defaultButton=QMessageBox.NoButton)
            return

        mLayer = self.iface.activeLayer()
        if mLayer is None:
            QMessageBox.warning(self.iface.mainWindow(),
                "Warning", "Please select an input layer.",
                buttons=QMessageBox.Ok, defaultButton=QMessageBox.NoButton)
            return

        if mLayer.type()!=0:
            QMessageBox.warning(self.iface.mainWindow(),
                "Warning", "Please select a vector layer.",
                buttons=QMessageBox.Ok, defaultButton=QMessageBox.NoButton)
            return

        return mLayer


    def loadModel(self):
        self.db.open()
        self.model = QSqlQueryModel()
        self.model.setQuery("select f_table_name as Layer from geometry_columns order by f_table_name", self.db)
        self.dockw.tableView.setModel(self.model)
        self.dockw.tableView.setColumnWidth(0, self.dockw.tableView.width())

        self.tablst = []

        query = self.db.exec_("SELECT name FROM sqlite_master WHERE type='table'")
        while query.next():
            self.tablst.append(query.value(0))

        self.db.close()


    def layerCheck(self, l):
        s = l.dataProvider().dataSourceUri()
        if s.find('db.sqlite')> -1:
            self.iface.messageBar().pushMessage(' ', 'spatialite', level=Qgis.Info)


    def layersinDB(self):
        self.grp4.setDefaultAction(self.dbtabs)
        if self.dbtabs.isChecked():
            self.iface.addDockWidget( Qt.LeftDockWidgetArea, self.dockw)
            self.dockw.setWindowTitle('VetEpiGIS layers')
            css="""
                QDockWidget::title {
                    text-align: left; /* align the text to the left */
                    font-size:12px;
                    font-weight:bold;
                    background-color: lightgray;
                    padding-left: 5px;
                }
                """
            self.dockw.setStyleSheet(css)

            dbname = os.path.basename(self.dbuidpath)
            dbpath = os.path.dirname(self.dbuidpath)
            #https://stackoverflow.com/questions/32831754/how-to-embed-url-link-to-qlabel
            pathlink = '<a href="' + dbpath + '"> Click here to open the folder </a>'
            self.dockw.label_db_name.setText(dbname)
            self.dockw.label_db_path.setText(pathlink)
            self.dockw.label_db_path.mousePressEvent = self.clickLink
            self.dockw.label_db_path.setOpenExternalLinks(True)

        elif not self.dbtabs.isChecked():
            self.iface.removeDockWidget(self.dockw)

    # https://stackoverflow.com/questions/23859613/pyqt-how-to-open-a-directory-folder
    def clickLink(self,eve):
        os.startfile(os.path.dirname(self.dbuidpath))

    def layersinDBLoad(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        idx = self.dockw.tableView.selectionModel().selectedIndexes()[0]
        ln = str(self.model.itemData(idx)[0])
        self.uri.setDataSource('', ln, 'geom')
        vl = QgsVectorLayer(self.uri.uri(), ln, 'spatialite')
        QgsProject.instance().addMapLayer(vl)
        QApplication.restoreOverrideCursor()


    def saveLayer(self):
        self.grp4.setDefaultAction(self.Saver)
        dlg = outbreaklayer.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Save layer to database')
        dlg.comboBox.setVisible(False)
        dlg.label.setVisible(False)
        dlg.label_2.setText('Save as:')
        lyr = self.iface.activeLayer()
        ln = str(lyr.name()).lower()
        dlg.lineEdit.setText(ln)
        dlg.tablst = self.tablst
        dlg.nameCtrl()
        self.iface.messageBar().pushMessage('Information', "Layer name must not be already exists in the database and the name must not contains withespace", level=Qgis.Info)

        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)

            lnb = dlg.lineEdit.text().lower()
            self.layer2db(lyr, lnb)
            self.loadModel()

            self.uri.setDataSource('', lnb,'geom')
            vl = QgsVectorLayer(self.uri.uri(), lnb, 'spatialite')
            vl.setCrs(lyr.crs())
            QgsProject.instance().addMapLayer(vl)

            QApplication.restoreOverrideCursor()


    def layer2db(self, lyr, ln):
        lgt = lyr.geometryType()
        if lgt==1:
            return

        nslst = []
        tlst = []
        flds = lyr.dataProvider().fields()
        for fld in flds:
            nslst.append(fld.name())
            tlst.append(fld.type())

        ntlst = self.fieldCheck(nslst)
        sql = 'create table %s (' % ln
        for i in range(len(ntlst)):
            t = 'text'
            if tlst[i]==2:
                t = 'numeric'

            sql += '%s %s, ' % (ntlst[i], t)

        sql += ')'
        sql = sql.replace(', )', ')')

        self.db.open()
        q = self.db.exec_(sql)
        if lgt==0:
            sql = "SELECT AddGeometryColumn('%s', 'geom', 4326, 'POINT', 'XY')" % ln
        elif lgt==2:
            sql = "SELECT AddGeometryColumn('%s', 'geom', 4326, 'MULTIPOLYGON', 'XY')" % ln
        q = self.db.exec_(sql)
        self.db.commit()
        self.db.close()

        self.uri.setDataSource('', ln,'geom')
        vl = QgsVectorLayer(self.uri.uri(), ln, 'spatialite')
        vl.startEditing()

        prv = lyr.dataProvider()
        feats = prv.getFeatures()
        feat = QgsFeature()
        while feats.nextFeature(feat):
            vl.addFeature(feat)

        vl.commitChanges()
        vl.updateExtents()


    def fieldCheck(self, lst):
        for i in range(len(lst)):
            if lst[i].lower()=='geom':
               lst[i]='ge_om_old'

        return lst


    def handDrawing(self):
        self.grp1.setDefaultAction(self.handy)
        if self.handy.isChecked():
            lyr = self.checklayer()
            if lyr is None:
                return

            flst = self.funcs.ofielder(lyr)

            if flst != self.obrflds:
                self.iface.messageBar().pushMessage(' ', 'It is not an OUTBREAK layer!', level=Qgis.Warning)
                self.handy.setChecked(False)
                return

            if flst == self.obrflds and lyr.geometryType() != QgsWkbTypes.PolygonGeometry:
                self.iface.messageBar().pushMessage(' ', 'It is not an AREA outbreak layer!', level=Qgis.Warning)
                self.handy.setChecked(False)
                self.iface.actionPan().trigger()
                return

            self.prevcur = self.iface.mapCanvas().cursor()
            self.iface.mapCanvas().setCursor(Qt.CrossCursor)

            dlg = caser.Dialog()
            x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
            y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
            dlg.move(x,y)
            dlg.setWindowTitle('Create new case')
            dlg.label_10_outbreak_layer.setVisible(False)
            dlg.comboBox_5_outbreak_layer.setVisible(False)

            for it in self.lsta:
                dlg.comboBox_2_disease.addItem(it)

            dlg.lstb = self.lstb

            if lyr.geometryType() == QgsWkbTypes.PolygonGeometry:
                psrid = self.iface.mapCanvas().mapSettings().destinationCrs().srsid()
                tool = polyDraw(dlg, psrid, self.iface, self.handy)
                self.iface.mapCanvas().setMapTool(tool)

            else:
                self.iface.mapCanvas().setCursor(self.prevcur)
                self.iface.mapCanvas().setMapTool(self.origtool)
                self.iface.actionPan().trigger()

        else:
            self.iface.mapCanvas().setCursor(self.prevcur)
            self.iface.mapCanvas().setMapTool(self.origtool)
            self.iface.actionPan().trigger()


    def copySel(self):
        self.grp1.setDefaultAction(self.copyselected)
        dlg = caser.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Copy selected object')
        dlg.label_4_reference.setText('Source layer:')

        for it in self.lsta:
            dlg.comboBox_2_disease.addItem(it)

        dlg.lstb = self.lstb

        lyrs = [layer for layer in QgsProject.instance().mapLayers().values()]
        lrs = []
        tlrs = []
        n = 0
        fldn = 0
        for lyr in lyrs:
            if lyr.type()==0:
                if lyr.geometryType() != QgsWkbTypes.LineGeometry:
                    flst = self.funcs.ofielder(lyr)
                    if flst == self.obrflds:
                        fldn += 1

                    lrs.append(lyr.name())
                    if lyr.geometryType() == QgsWkbTypes.PointGeometry:
                        tlrs.append('point')
                    if lyr.geometryType() == QgsWkbTypes.PolygonGeometry:
                        tlrs.append('poly')
                    if lyr.selectedFeatureCount()==1:
                        dlg.comboBox_reference.addItem(lyr.name())
                        n += 1
        if n==0:
            self.iface.messageBar().pushMessage('Copy an element to outbreak layer', ' Select ONE object to copy!', level=Qgis.Warning)
            return

        if fldn==0:
            self.iface.messageBar().pushMessage('Copy an element to outbreak layer', 'There is no OUTBREAK layer!', level=Qgis.Warning)
            return

        dlg.lrs = lrs
        dlg.tlrs = tlrs
        dlg.comboBox_reference.currentIndexChanged.connect(dlg.outLSel)
        dlg.outLSel()

        dlg.label_longitude.setVisible(False)
        dlg.lineEdit_longitude.setVisible(False)
        dlg.toolButton_3_dms.setVisible(False)
        dlg.label_2_latitude.setVisible(False)
        dlg.lineEdit_2_latitude.setVisible(False)

        if dlg.exec_() == QDialog.Accepted:
            src = ''
            dst = ''
            for lyr in lyrs:
                if lyr.name()== dlg.comboBox_reference.currentText():
                    src = lyr
                elif lyr.name()== dlg.comboBox_5_outbreak_layer.currentText():
                    dst = lyr

            prvsrc = src.dataProvider()
            prvdst = dst.dataProvider()

            sfeats = src.selectedFeatures()
            destType = dst.geometryType()
            destIsMulti = QgsWkbTypes.isMultiType(dst.wkbType())
            sg = QgsGeometry()
            if prvsrc.crs().toWkt()!=prvdst.crs().toWkt():
                trafo = QgsCoordinateTransform(prvsrc.crs(), prvdst.crs(),QgsProject.instance())
                #self.iface.emit(SIGNAL('rangeCalculated( PyQt_PyObject)'), len(sfeats))
                for sf in sfeats:
                    sg = sf.geometry()
                    sg.transform(trafo)
                    #self.iface.emit(SIGNAL('featureProcessed()'))
            else:
                #self.iface.emit(SIGNAL('rangeCalculated( PyQt_PyObject)'), len(sfeats))
                for sf in sfeats:
                    sg = sf.geometry()
                    #self.iface.emit(SIGNAL('featureProcessed()'))

            # Reference used for writing the follow code rows derived from plugin AppendFeaturesToLayer:
            # https://github.com/gacarrillor/AppendFeaturesToLayer
            if destType != QgsWkbTypes.UnknownGeometry:
                newGeometry = sg.convertToType(destType, destIsMulti)
                sg = newGeometry

            sg.avoidIntersections(QgsProject.instance().avoidIntersectionsLayers())

            feat = self.funcs.outattrPrep(dlg, dst)
            feat.setGeometry(QgsGeometry(sg))
            feat.setValid(True)

            dst.startEditing()
            dst.addFeature(feat)
            dst.commitChanges()
            dst.updateExtents()
            dst.triggerRepaint()


    def createPOIlayer(self):
        self.grp2.setDefaultAction(self.newpoilayer)
        dlg = outbreaklayer.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Create POI layer')
        dlg.comboBox.setVisible(False)
        dlg.label.setVisible(False)
        dlg.label_2.setText('POI layer name:')
        dt = '%s_%s_%s' %(QDate.currentDate().year(), QDate.currentDate().month(), QDate.currentDate().day())
        dlg.lineEdit.setText('poi_%s' % dt)
        dlg.tablst = self.tablst
        dlg.nameCtrl()
        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            s = dlg.lineEdit.text()
            self.db.open()
            q = self.db.exec_("create table %s (gid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, localid text, code text, activity text, hrid text)" % s)
            q = self.db.exec_("SELECT AddGeometryColumn('%s', 'geom', 4326, 'POINT', 'XY')" % s)
            self.db.commit()
            self.db.close()
            self.uri.setDataSource('', s,'geom')
            vl = QgsVectorLayer(self.uri.uri(), s, 'spatialite')
            sld = self.sldPOI
            vl.loadSldStyle(sld)
            QgsProject.instance().addMapLayer(vl)
            self.poier.activate(0)

            self.loadModel()
            QApplication.restoreOverrideCursor()


    def createOlayer(self):
        self.grp1.setDefaultAction(self.newoutbreak)
        dlg = outbreaklayer.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Create outbreak layer')
        dlg.comboBox.addItem('Point')
        dlg.comboBox.addItem('Area')
        dt = '%s_%s_%s' %(QDate.currentDate().year(), QDate.currentDate().month(), QDate.currentDate().day())
        dlg.lineEdit.setText('outbreak_%s' % dt)
        dlg.tablst = self.tablst
        dlg.nameCtrl()
        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            s = dlg.lineEdit.text()
            self.db.open()
            q = self.db.exec_("create table %s (gid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, localid text, code text, largescale text, disease text, animalno numeric, species text, production text, year numeric, status text, suspect text, confirmation text, expiration text, notes text, hrid text, timestamp text, grouping text)" % s)
            if dlg.comboBox.currentText()=='Point':
                sld = self.sldOutbreakPoint
                q = self.db.exec_("SELECT AddGeometryColumn('%s', 'geom', 4326, 'POINT', 'XY')" % s)
            else:
                sld = self.sldOutbreakArea
                q = self.db.exec_("SELECT AddGeometryColumn('%s', 'geom', 4326, 'POLYGON', 'XY')" % s)
            self.db.commit()
            self.db.close()
            self.uri.setDataSource('', s,'geom')
            vl = QgsVectorLayer(self.uri.uri(), s, 'spatialite')
            vl.loadSldStyle(sld)

            QgsProject.instance().addMapLayer(vl)
            self.loadModel()
            QApplication.restoreOverrideCursor()


    def selectPOIs(self):
        self.grp3.setDefaultAction(self.POIer)
        dlg = select.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Select POIs by polygons')

        lyrs = [layer for layer in QgsProject.instance().mapLayers().values()]
        for lyr in lyrs:
            if lyr.type()==0:
                if lyr.geometryType() == QgsWkbTypes.PolygonGeometry:
                    dlg.comboBox.addItem(lyr.name())
                if lyr.geometryType() == QgsWkbTypes.PointGeometry:
                    dlg.comboBox_2.addItem(lyr.name())

        dlg.lineEdit.setText('_selected_by_')
        dlg.tablst = self.tablst
        dlg.nameCtrl()
        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)

            l1 = l2 = QgsVectorLayer
            prv1 = prv2 = QgsVectorDataProvider

            for lyr in lyrs:
                if lyr.name()==dlg.comboBox.currentText():
                    l1 = lyr
                    if l1.dataProvider().crs().srsid() != 3452:
                        l1 = self.transformLayerToWGS84(l1)
                    prv1 = l1.dataProvider()
                if lyr.name()==dlg.comboBox_2.currentText():
                    l2 = lyr
                    if l2.dataProvider().crs().srsid() != 3452:
                        l2 = self.transformLayerToWGS84(l2)
                    prv2 = l2.dataProvider()

            ln = dlg.lineEdit.text()
            #The output layer will be in epsg 4326 (crs 3452)
            crs_out = QgsCoordinateReferenceSystem()
            crs_out.createFromSrsId(3452)
            vl = QgsVectorLayer('Point?crs=' + crs_out.toWkt(), ln, 'memory')

            oattrs = prv2.fields().toList()
            nattrs = []
            for attr in oattrs:
                # if vl.fieldNameIndex(attr.name())==-1:
                if vl.fields().indexFromName(attr.name()) == -1:
                    nattrs.append(QgsField(attr.name(),attr.type()))
                    vl.dataProvider().addAttributes(nattrs)
                    vl.updateFields()

            oattrs = prv1.fields().toList()
            nattrs = []
            for attr in oattrs:
                s = 'selby_%s' % attr.name()
                # if vl.fieldNameIndex(s)==-1:
                if vl.fields().indexFromName(s) == -1:
                    nattrs.append(QgsField(s, attr.type()))
                    vl.dataProvider().addAttributes(nattrs)
                    vl.updateFields()

            vl.startEditing()

            index = QgsSpatialIndex()
            ftbs = l2.getFeatures()
            for ft in ftbs:
                index.insertFeature(ft)

            feat = QgsFeature()

            if l1.selectedFeatureCount()==0:
                feats = prv1.getFeatures()
                while feats.nextFeature(feat):
                    # geom = feat.constGeometry()
                    geom = feat.geometry()
                    idxs = index.intersects(geom.boundingBox())
                    for idx in idxs:
                        rqst = QgsFeatureRequest().setFilterFid(idx)
                        featB = QgsFeature()
                        prv2.getFeatures(rqst).nextFeature(featB)
                        geomB = QgsGeometry(featB.geometry())
                        #geomB.transform(trA)
                        attrs=[]
                        attrs.extend(featB.attributes())
                        attrs.extend(feat.attributes())
                        if geom.intersects(geomB):
                            featC = QgsFeature()
                            featC.setGeometry(geomB)
                            featC.setAttributes(attrs)
                            vl.addFeature(featC)
            else:
                feats = l1.selectedFeatures()
                #self.iface.emit(SIGNAL('rangeCalculated( PyQt_PyObject)'), len(feats))
                for feat in feats:
                    # geom = feat.constGeometry()
                    geom = feat.geometry()
                    idxs = index.intersects(geom.boundingBox())
                    for idx in idxs:
                        rqst = QgsFeatureRequest().setFilterFid(idx)
                        featB = QgsFeature()
                        prv2.getFeatures(rqst).nextFeature(featB)
                        geomB = QgsGeometry(featB.geometry())
                        #geomB.transform(trA)
                        attrs=[]
                        attrs.extend(featB.attributes())
                        attrs.extend(feat.attributes())
                        if geom.intersects(geomB):
                            featC = QgsFeature()
                            featC.setGeometry(geomB)
                            featC.setAttributes(attrs)
                            vl.addFeature(featC)

                    #self.iface.emit(SIGNAL('featureProcessed()'))


            vl.commitChanges()
            vl.updateExtents()

            if dlg.checkBox.isChecked():
                self.layer2db(vl, ln)
                self.loadModel()
                self.uri.setDataSource('', ln,'geom')
                vl = QgsVectorLayer(self.uri.uri(), ln, 'spatialite')

            QgsProject.instance().addMapLayer(vl)
            QApplication.restoreOverrideCursor()

    def transformLayerToWGS84(self,vecLayer): #PB
        """
        Return the vector layer in the reference system EPSG: 4326.

        Parameters:
            vectLayer(QgsVectorLayer): input layer which convert coordinate reference system.

        Return:
            new_vec(QgsVectorLayer): vector layer in EPSG: 4326.

        """

        prv1 = vecLayer.dataProvider()

        crs1 = vecLayer.sourceCrs()

        crs_out = QgsCoordinateReferenceSystem()
        crs_out.createFromSrsId(3452)

        #create new layer
        fn1 = 'lay_test_1'
        if vecLayer.geometryType() == QgsWkbTypes.PointGeometry:
            uri1 = QgsVectorLayer('Point?crs=' + crs_out.toWkt(), fn1, 'memory')
        elif vecLayer.geometryType() == QgsWkbTypes.LineGeometry:
            uri1 = QgsVectorLayer('LineString?crs=' + crs_out.toWkt(), fn1, 'memory')
        elif vecLayer.geometryType() == QgsWkbTypes.PolygonGeometry:
            uri1 = QgsVectorLayer('Polygon?crs=' + crs_out.toWkt(), fn1, 'memory')

        #add attribute to new layer
        pruri1 = uri1.dataProvider()
        pruri1.addAttributes(prv1.fields())

        #set crs transformation
        trA = QgsCoordinateTransform()
        if crs1.srsid() != 3452:
            trA = QgsCoordinateTransform(crs1, crs_out, QgsProject.instance())

        #Add features to new layer
        feats = []
        for f in prv1.getFeatures():
            g = f.geometry()
            g.transform(trA)
            f.setGeometry(g)
            f.setAttributes(f.attributes())
            f.setValid(True)
            feats.append(f)

        #update layer with new features
        uri1.dataProvider().addFeatures(feats)
        uri1.updateFields()

        # Check if there are selected features
        # TODO: The only method I found to add the selected feature in the new layer is comparing the geometries,
        # by id() it doesn't work. Check if there are other solutions.
        # https://gis.stackexchange.com/questions/256569/select-features-from-another-layer-based-on-a-selection-in-pyqgis/256646
        if vecLayer.selectedFeatureCount()!=0:
            for selected_feat in vecLayer.selectedFeatures():
                to_select = []
                for feat_to_select in uri1.getFeatures():
                    if feat_to_select.geometry().equals(selected_feat.geometry()):
                        to_select.append(feat_to_select.id())
                uri1.modifySelection(to_select,[])
        return uri1

    def checkMultiType(self,layerIn, layerOut, geometryOut):
        destType = layerIn.geometryType()
        destIsMulti = QgsWkbTypes.isMultiType(layerOut.wkbType())

        if destType != QgsWkbTypes.UnknownGeometry:
            newGeometry = geometryOut.convertToType(destType, destIsMulti)
            geometryOut = newGeometry

        return geometryOut

    # Followed this code https://gis.stackexchange.com/questions/112095/converting-huge-multipolygon-to-polygons
    def fromMultiPolygonToSinglePolygon(self, geom, attrs):
        gw = geom.ExportToWkt()
        gg = QgsGeometry.fromWkt(gw)
        new_feat = QgsFeature()
        new_feat.setAttributes(attrs)
        new_feat.setGeometry(gg)

        return new_feat

    def selectROIs(self):
        self.grp3.setDefaultAction(self.Zoner)
        dlg = zone.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Select ROIs by polygons')
        dlg.label_2.setText("ROI layer:")
        dlg.lstb = self.lstb
        dlg.comboBox_13.addItem('No related zone layer')
        lyrs = [layer for layer in QgsProject.instance().mapLayers().values()]
        for lyr in lyrs:
            if lyr.type()==0:
                if lyr.geometryType() == QgsWkbTypes.PolygonGeometry:
                    dlg.comboBox.addItem(lyr.name())
                    dlg.comboBox_2.addItem(lyr.name())
                    dlg.comboBox_13.addItem(lyr.name())

        dlg.lineEdit.setText('zone_selected_by_')

        if dlg.exec_() == QDialog.Accepted:
            count_hrid = 1
            if dlg.comboBox.currentText()==dlg.comboBox_2.currentText():
                return False

            QApplication.setOverrideCursor(Qt.WaitCursor)
            l1 = l2 = QgsVectorLayer

            for lyr in lyrs:
                if lyr.name()==dlg.comboBox.currentText():
                    l1 = lyr
                    l1 = self.transformLayerToWGS84(l1) #convert layer CRS if not in EPSG:4326
                    prv1 = l1.dataProvider()
                if lyr.name()==dlg.comboBox_2.currentText():
                    l2 = lyr
                    l2 = self.transformLayerToWGS84(l2) #convert layer CRS if not in EPSG:4326
                    prv2 = l2.dataProvider()

            fn = str('zones_') + dlg.lineEdit.text()
            vl = QgsVectorLayer('Polygon?crs=' + l1.dataProvider().crs().toWkt(), fn, 'memory')

            nattrs = []
            nattrs.append(QgsField('localid', QVariant.String))
            nattrs.append(QgsField('code', QVariant.String))
            nattrs.append(QgsField('disease', QVariant.String))
            nattrs.append(QgsField('zonetype', QVariant.String))
            nattrs.append(QgsField('subpopulation', QVariant.String))
            nattrs.append(QgsField('validity_start', QVariant.String))
            nattrs.append(QgsField('validity_end', QVariant.String))
            nattrs.append(QgsField('legal_framework', QVariant.String))
            nattrs.append(QgsField('competent_authority', QVariant.String))
            nattrs.append(QgsField('biosecurity_measures', QVariant.String))
            nattrs.append(QgsField('control_of_vectors', QVariant.String))
            nattrs.append(QgsField('control_of_wildlife_reservoir', QVariant.String))
            nattrs.append(QgsField('modified_stamping_out', QVariant.String))
            nattrs.append(QgsField('movement_restriction', QVariant.String))
            nattrs.append(QgsField('stamping_out', QVariant.String))
            nattrs.append(QgsField('surveillance', QVariant.String))
            nattrs.append(QgsField('vaccination', QVariant.String))
            nattrs.append(QgsField('other_measure', QVariant.String))
            nattrs.append(QgsField('related', QVariant.String))
            nattrs.append(QgsField('hrid', QVariant.String))
            nattrs.append(QgsField('timestamp', QVariant.String))

            vl.dataProvider().addAttributes(nattrs)
            vl.updateFields()

            vl.startEditing()

            zonetype = dlg.comboBox_3.currentText() #mandatory no check the value

            subpopulation = ''
            rn = dlg.tableWidget.rowCount()
            for i in range(rn):
                if i==0:
                    subpopulation = dlg.tableWidget.item(i, 0).text()
                else:
                    subpopulation = subpopulation + ', ' + dlg.tableWidget.item(i, 0).text()

            validity_start = self.funcs.dateCheck(dlg.dateEdit.date())
            validity_end = self.funcs.dateCheck(dlg.dateEdit_2.date())
            legal_framework = self.checkValue(dlg.lineEdit_2.text())
            competent_authority = self.checkValue(dlg.lineEdit_3.text())
            biosecurity_measures = self.checkValue(dlg.comboBox_5.currentText())
            control_of_vectors = self.checkValue(dlg.comboBox_6.currentText())
            control_of_wildlife_reservoir = self.checkValue(dlg.comboBox_7.currentText())
            modified_stamping_out = self.checkValue(dlg.comboBox_8.currentText())
            movement_restriction = self.checkValue(dlg.comboBox_9.currentText())
            stamping_out = self.checkValue(dlg.comboBox_10.currentText())
            surveillance = self.checkValue(dlg.comboBox_11.currentText())
            vaccination = self.checkValue(dlg.comboBox_12.currentText())
            other_measure = self.checkValue(dlg.lineEdit_4.text())
            timestamp = QDateTime.currentDateTimeUtc().toString('dd/MM/yyyy hh:mm:ss')
            related = self.checkValue(dlg.comboBox_13.currentText())

            attrs = []
            attrs.append('')
            attrs.append('')
            attrs.append('')
            attrs.append(zonetype)
            attrs.append(subpopulation)
            attrs.append(validity_start)
            attrs.append(validity_end)
            attrs.append(legal_framework)
            attrs.append(competent_authority)
            attrs.append(biosecurity_measures)
            attrs.append(control_of_vectors)
            attrs.append(control_of_wildlife_reservoir)
            attrs.append(modified_stamping_out)
            attrs.append(movement_restriction)
            attrs.append(stamping_out)
            attrs.append(surveillance)
            attrs.append(vaccination)
            attrs.append(other_measure)
            attrs.append(related)
            attrs.append('')
            attrs.append(timestamp)

            index = QgsSpatialIndex()
            ftbs = l2.getFeatures()
            for ft in ftbs:
                index.insertFeature(ft)

            feat = QgsFeature()

            if dlg.comboBox_4.currentText()=='Overlapped ROIs':
                zonsty = self.sldZoneA
                if l1.selectedFeatureCount()==0:
                    feats = prv1.getFeatures()

                    while feats.nextFeature(feat):
                        # geom = feat.constGeometry()
                        geom = feat.geometry()
                        idxs = index.intersects(geom.boundingBox())
                        for idx in idxs:
                            rqst = QgsFeatureRequest().setFilterFid(idx)
                            # featB = prv2.getFeatures(rqst).next()
                            featB = QgsFeature()
                            prv2.getFeatures(rqst).nextFeature(featB)
                            geomB = QgsGeometry(featB.geometry())

                            attrs[0] = feat.attributes()[feat.fieldNameIndex('localid')]
                            attrs[1] = feat.attributes()[feat.fieldNameIndex('code')]
                            attrs[2] = feat.attributes()[feat.fieldNameIndex('disease')]

                            if geom.intersects(geomB):
                                gwkt = ogr.CreateGeometryFromWkt(geomB.asWkt())
                                if gwkt.GetGeometryName() == 'MULTIPOLYGON':
                                    for geom_part in gwkt:
                                        most = QDateTime.currentDateTimeUtc()
                                        attrs[19] = self.funcs.hashIDer(most, count_hrid)
                                        count_hrid += 1
                                        vl.addFeature(self.fromMultiPolygonToSinglePolygon(geom_part,attrs))
                                else:
                                    most = QDateTime.currentDateTimeUtc()
                                    attrs[19] = self.funcs.hashIDer(most, count_hrid)
                                    count_hrid += 1
                                    vl.addFeature(self.fromMultiPolygonToSinglePolygon(gwkt_tmp,attrs))
                else:
                    feats = l1.selectedFeatures()

                    for feat in feats:
                        # geom = feat.constGeometry()
                        geom = feat.geometry()
                        idxs = index.intersects(geom.boundingBox())
                        for idx in idxs:
                            rqst = QgsFeatureRequest().setFilterFid(idx)
                            # featB = prv2.getFeatures(rqst).next()
                            featB = QgsFeature()
                            prv2.getFeatures(rqst).nextFeature(featB)
                            geomB = QgsGeometry(featB.geometry())

                            attrs[0] = feat.attributes()[feat.fieldNameIndex('localid')]
                            attrs[1] = feat.attributes()[feat.fieldNameIndex('code')]
                            attrs[2] = feat.attributes()[feat.fieldNameIndex('disease')]


                            if geom.intersects(geomB):
                                gwkt = ogr.CreateGeometryFromWkt(geomB.asWkt())
                                if gwkt.GetGeometryName() == 'MULTIPOLYGON':
                                    for geom_part in gwkt:
                                        most = QDateTime.currentDateTimeUtc()
                                        attrs[19] = self.funcs.hashIDer(most, count_hrid)
                                        count_hrid += 1
                                        vl.addFeature(self.fromMultiPolygonToSinglePolygon(geom_part,attrs))
                                else:
                                    most = QDateTime.currentDateTimeUtc()
                                    attrs[19] = self.funcs.hashIDer(most, count_hrid)
                                    count_hrid += 1
                                    vl.addFeature(self.fromMultiPolygonToSinglePolygon(gwkt_tmp,attrs))

                        #self.iface.emit(SIGNAL('featureProcessed()'))

            elif dlg.comboBox_4.currentText()=='Intersections only':
                zonsty = self.sldZoneB
                if l1.selectedFeatureCount()==0:
                    feats = prv1.getFeatures()

                    while feats.nextFeature(feat):
                        # geom = feat.constGeometry()
                        geom = feat.geometry()
                        idxs = index.intersects(geom.boundingBox())
                        for idx in idxs:
                            rqst = QgsFeatureRequest().setFilterFid(idx)
                            # featB = prv2.getFeatures(rqst).next()
                            featB = QgsFeature()
                            prv2.getFeatures(rqst).nextFeature(featB)
                            geomB = QgsGeometry(featB.geometry())

                            attrs[0] = feat.attributes()[feat.fieldNameIndex('localid')]
                            attrs[1] = feat.attributes()[feat.fieldNameIndex('code')]
                            attrs[2] = feat.attributes()[feat.fieldNameIndex('disease')]

                            if geom.intersects(geomB):
                                g1wkt = ogr.CreateGeometryFromWkt(geom.asWkt())
                                g2wkt = ogr.CreateGeometryFromWkt(geomB.asWkt())
                                g_tmp = g1wkt.Intersection(g2wkt)
                                if g_tmp.GetGeometryName() == 'MULTIPOLYGON':
                                    for geom_part in g_tmp:
                                        most = QDateTime.currentDateTimeUtc()
                                        attrs[19] = self.funcs.hashIDer(most, count_hrid)
                                        count_hrid += 1
                                        vl.addFeature(self.fromMultiPolygonToSinglePolygon(geom_part,attrs))
                                else:
                                    most = QDateTime.currentDateTimeUtc()
                                    attrs[19] = self.funcs.hashIDer(most, count_hrid)
                                    count_hrid += 1
                                    vl.addFeature(self.fromMultiPolygonToSinglePolygon(g_tmp,attrs))
                else:
                    feats = l1.selectedFeatures()

                    for feat in feats:
                        # geom = feat.constGeometry()
                        geom = feat.geometry()
                        idxs = index.intersects(geom.boundingBox())
                        for idx in idxs:
                            rqst = QgsFeatureRequest().setFilterFid(idx)
                            # featB = prv2.getFeatures(rqst).next()
                            featB = QgsFeature()
                            prv2.getFeatures(rqst).nextFeature(featB)
                            geomB = QgsGeometry(featB.geometry())

                            attrs[0] = feat.attributes()[feat.fieldNameIndex('localid')]
                            attrs[1] = feat.attributes()[feat.fieldNameIndex('code')]
                            attrs[2] = feat.attributes()[feat.fieldNameIndex('disease')]

                            if geom.intersects(geomB):
                                g1wkt = ogr.CreateGeometryFromWkt(geom.asWkt())
                                g2wkt = ogr.CreateGeometryFromWkt(geomB.asWkt())
                                g_tmp = g1wkt.Intersection(g2wkt)

                                if g_tmp.GetGeometryName() == 'MULTIPOLYGON':
                                    for geom_part in g_tmp:
                                        most = QDateTime.currentDateTimeUtc()
                                        attrs[19] = self.funcs.hashIDer(most, count_hrid)
                                        count_hrid += 1
                                        vl.addFeature(self.fromMultiPolygonToSinglePolygon(geom_part,attrs))
                                else:
                                    most = QDateTime.currentDateTimeUtc()
                                    attrs[19] = self.funcs.hashIDer(most, count_hrid)
                                    count_hrid += 1
                                    vl.addFeature(self.fromMultiPolygonToSinglePolygon(g_tmp,attrs))

                        #self.iface.emit(SIGNAL('featureProcessed()'))

            vl.commitChanges()
            vl.updateExtents()

            if dlg.checkBox.isChecked():
                ln = vl.name()
                self.layer2db(vl, ln)
                self.uri.setDataSource('', ln,'geom')
                vl = QgsVectorLayer(self.uri.uri(), ln, 'spatialite')

                self.loadModel()

            vl.loadSldStyle(zonsty)
            QgsProject.instance().addMapLayer(vl)
            QApplication.restoreOverrideCursor()


    def createBuffers(self):
        self.grp3.setDefaultAction(self.Bufferer)
        dlg = buffer.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Create buffers')
        dlg.lineEdit.setText('buffer_1000')
        dlg.tablst = self.tablst
        dlg.nameCtrl()
        lyr = self.checklayer()
        if lyr is None:
            return

        #add check about selected layer
        flds = lyr.dataProvider().fields()
        flst = []
        for fld in flds:
            flst.append(fld.name())
        tn = ''

        #check type of geometry: point
        """
        geom = lyr.geometryType()
        if geom != QgsWkbTypes.PointGeometry:
           msgBox = QMessageBox.information(dlg, "Warning", "Select a point layer")
           return
        """

        #Check if layer selected is outbreak or poi
        if flst == self.poiflds:
            tn = 'poi'
        if flst == self.obrflds:
            tn = 'outbreak'
        if tn=='':
            msgBox = QMessageBox.information(dlg, "Warning", "Select Outbreak or POI layer")
            return

        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            count_hrid = 1
            lyr = self.iface.mapCanvas().currentLayer()
            provider = lyr.dataProvider()

            provider.reloadData()
            psrid = provider.crs().srsid()

            r = dlg.spinBox.value()

            ln = dlg.lineEdit.text()

            vl = QgsVectorLayer('Polygon?crs=' + provider.crs().toWkt(), ln, 'memory')

            oattrs = provider.fields().toList()
            nattrs = []
            for attr in oattrs:
                # if (vl.fieldNameIndex(attr.name())==-1) and attr.name()!='grouping':
                #if vl.fieldNameIndex(attr.name()) == -1:
                if vl.fields().indexFromName(attr.name()) == -1:
                    nattrs.append(QgsField(attr.name(),attr.type()))
                    vl.dataProvider().addAttributes(nattrs)
                    vl.updateFields()

            vl.startEditing()

            lyp = self.iface.mapCanvas().currentLayer()
            provi = lyp.dataProvider()
            feat = QgsFeature()
            polynum = lyp.featureCount()
            #prendo solo la prima coordinata del poligono per capire in quale sitestema di riferimento sono
            if lyp.selectedFeatureCount()==0:
                for feat in provi.getFeatures(QgsFeatureRequest()):

                    utm = self.getUTMzone(feat, psrid)

                    crss = QgsCoordinateReferenceSystem()
                    # crss.createFromId(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
                    # self.iface.messageBar().pushMessage(' ', "%s" % psrid, level=Qgis.Info)

                    crss.createFromSrsId(psrid)
                    crsd = QgsCoordinateReferenceSystem()
                    # crsd.createFromId(23700, QgsCoordinateReferenceSystem.EpsgCrsId)

                    crsd.createFromSrsId(utm.srsid())
                    trafo = QgsCoordinateTransform(crss, crsd, QgsProject.instance())

                    #ba = QgsGeometry(feat.geometry()).asPoint()
                    ba = feat.geometry()

                    #tba = trafo.transform(ba, QgsCoordinateTransform.ForwardTransform)
                    ba.transform(trafo, QgsCoordinateTransform.ForwardTransform)

                    #tbb = QgsGeometry.fromPointXY(tba)
                    #tbb = tba

                    #bar = QgsGeometry.asQPolygonF(tbb.buffer(r, r))
                    tbar = ba.buffer(r,r)
                    tbar.transform(trafo, QgsCoordinateTransform.ReverseTransform)
                    #trafo.transformPolygon(bar, QgsCoordinateTransform.ReverseTransform)
                    #tbar = QgsGeometry.fromPolygonXY(QgsGeometry.createPolygonFromQPolygonF(bar))
                    # self.iface.messageBar().pushMessage(' ', "%s" % tbar.asWkt(), level=Qgis.Info)

                    bf = QgsFeature()
                    bf.setGeometry(tbar)
                    attrs=[]
                    attrs.extend(feat.attributes())
                    # del attrs[-16]
                    bf.setAttributes(attrs)
                    most = QDateTime.currentDateTimeUtc()
                    bf.setAttribute(feat.fieldNameIndex('hrid'), self.funcs.hashIDer(most, count_hrid))
                    count_hrid += 1
                    vl.addFeature(bf)
            else:
                feats = lyp.selectedFeatures()
                #self.iface.emit(SIGNAL('rangeCalculated( PyQt_PyObject)'), len(feats))
                for feat in feats:

                    utm = self.getUTMzone(feat, psrid)

                    crss = QgsCoordinateReferenceSystem()
                    crss.createFromSrsId(psrid)
                    crsd = QgsCoordinateReferenceSystem()
                    crsd.createFromSrsId(utm.srsid())
                    trafo = QgsCoordinateTransform(crss, crsd, QgsProject.instance())

                    #ba = QgsGeometry(feat.geometry()).asPoint()
                    ba = feat.geometry()

                    #tba = trafo.transform(ba, QgsCoordinateTransform.ForwardTransform)
                    ba.transform(trafo, QgsCoordinateTransform.ForwardTransform)

                    #tbb = QgsGeometry.fromPointXY(tba)
                    #bar = QgsGeometry.asQPolygonF(tbb.buffer(r, r))

                    #trafo.transformPolygon(bar, QgsCoordinateTransform.ReverseTransform)
                    #tbar = QgsGeometry.fromPolygonXY(QgsGeometry.createPolygonFromQPolygonF(bar))

                    tbar = ba.buffer(r,r)
                    tbar.transform(trafo, QgsCoordinateTransform.ReverseTransform)

                    bf = QgsFeature()
                    bf.setGeometry(tbar)
                    attrs=[]
                    attrs.extend(feat.attributes())
                    # del attrs[-16]
                    bf.setAttributes(attrs)
                    most = QDateTime.currentDateTimeUtc()
                    bf.setAttribute(feat.fieldNameIndex('hrid'), self.funcs.hashIDer(most, count_hrid))
                    count_hrid += 1
                    vl.addFeature(bf)
                    #self.iface.emit(SIGNAL('featureProcessed()'))

            vl.commitChanges()
            # vl.updateExtents()

            if tn is 'outbreak':
                dfl = list()
                dfl.append(16)
                vl.dataProvider().deleteAttributes(dfl)

            vl.commitChanges()
            vl.updateExtents()

            if dlg.checkBox.isChecked():
                self.layer2db(vl, ln)
                self.loadModel()
                self.uri.setDataSource('', ln,'geom')
                vl = QgsVectorLayer(self.uri.uri(), ln, 'spatialite')

            sld = self.sldBuffer
            vl.loadSldStyle(sld)
            QgsProject.instance().addMapLayer(vl)

            QApplication.restoreOverrideCursor()

    def getUTMzone(self, feat, psrid):
        #http://www.qgistutorials.com/tr/docs/custom_python_functions.html
        tfeat = feat

        if psrid != 3452:
            trA = QgsCoordinateTransform(psrid, 3452)
            tfeat = trA.transform(feat)

        # If geometry is different from point, take only the first coordinate to understand
        # the UTM zone
        geom = tfeat.geometry()
        pt = ''
        if geom.type() == QgsWkbTypes.PolygonGeometry:
            pt = geom.asPolygon()[0][0]
        elif geom.type() == QgsWkbTypes.LineGeometry:
            pt = geom.asPolyline()[0][0]
        else:
            pt = geom.asPoint()

        zn = int(math.floor(((pt.x()+180)/6) % 60)+1)
        if pt.y()>0:
            epsg = int('326%s' % str(zn).zfill(2))
        else:
            epsg = int('327%s' % str(zn).zfill(2))

        utmz = QgsCoordinateReferenceSystem(epsg, QgsCoordinateReferenceSystem.EpsgCrsId)

        return utmz


    def about(self):
        dlg = xabout.Dialog()
        dlg.setWindowTitle('About')
        dlg.label.setPixmap(QPixmap(':/plugins/VetEpiGIStool/images/qvettool-about-banner.png'))
        ow = dlg.textEdit.fontWeight()

        dlg.textEdit.setFontWeight(QFont.Bold)
        dlg.textEdit.append('VetEpiGIS-Tool ' + self.vers +'\n')
        dlg.textEdit.setFontWeight(ow)
        dlg.textEdit.append("VetEpiGIS-Tool is a free QGIS tool that helps veterinarian users in the management of spatial data related to animal disease. This plug-in combined the huge amount of GIS functions offered by QGIS with a simple user interface that allows to the user the possibility to manage data without the necessity to define the data model, the data organization model, and the data presentation, because these issues are pre-organised in the 'piece' of software specifically developed.\n")
        dlg.textEdit.setFontWeight(QFont.Bold)
        dlg.textEdit.append('Developers:')
        dlg.textEdit.setFontWeight(ow)
        dlg.textEdit.append('Paola Bonato *;\nMatteo Mazzucato *;\n* from Istituto Zooprofilattico Sperimentale delle Venezie.\n')
        dlg.textEdit.append('Norbert Solymosi *;\n* from University of Veterinary Medicine, Budapest.\n')
        dlg.textEdit.setFontWeight(QFont.Bold)
        dlg.textEdit.append('Contributors:')
        dlg.textEdit.setFontWeight(ow)
        dlg.textEdit.append(u'Nicola Ferrè *;\nPaolo Mulatti *;\n* from Istituto Zooprofilattico Sperimentale delle Venezie.\n')
        dlg.textEdit.setFontWeight(QFont.Bold)
        dlg.textEdit.append('Contacts:')
        dlg.textEdit.setFontWeight(ow)
        dlg.textEdit.append('Send an email to gis@izsvenezie.it\n\n')
        dlg.textEdit.append('Original icons designed by Feepik. They were modified for this project by IZSVe.')
        dlg.textEdit.moveCursor(QTextCursor.Start, QTextCursor.MoveAnchor)
        dlg.textEdit.setReadOnly(True)

        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.exec_()


    def caseCapture(self):
        self.grp1.setDefaultAction(self.Caser)
        if self.Caser.isChecked():
            lyr = self.checklayer()
            if lyr is None:
                return

            flst = self.funcs.ofielder(lyr)

            if flst != self.obrflds:
                self.iface.messageBar().pushMessage(' ', 'It is not an OUTBREAK layer!', level=Qgis.Warning)
                self.Caser.setChecked(False)
                return

            if flst == self.obrflds and lyr.geometryType() != QgsWkbTypes.PointGeometry:
                self.iface.messageBar().pushMessage(' ', 'It is not a POINT OUTBREAK layer!', level=Qgis.Warning)
                self.Caser.setChecked(False)
                self.iface.actionPan().trigger()
                #self.iface.mapCanvas().setCursor(Qt.ArrowCursor)
                return

            self.prevcur = self.iface.mapCanvas().cursor()
            self.iface.mapCanvas().setCursor(Qt.CrossCursor)

            dlg = caser.Dialog()
            x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
            y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
            dlg.move(x,y)

            dlg.setWindowTitle('Create new case')
            dlg.label_10_outbreak_layer.setVisible(False)
            dlg.comboBox_5_outbreak_layer.setVisible(False)

            for it in self.lsta:
                dlg.comboBox_2_disease.addItem(it)

            dlg.lstb = self.lstb

            if lyr.geometryType() == QgsWkbTypes.PolygonGeometry:
                lyrs = [layer for layer in QgsProject.instance().mapLayers().values()]
                dlg.comboBox_reference.addItem('')
                for lr in lyrs:
                    if lr.type()==0:
                        if lr.geometryType() == QgsWkbTypes.PolygonGeometry:
                            dlg.comboBox_reference.addItem(lr.name())
            else:
                dlg.label_4_reference.setVisible(False)
                dlg.comboBox_reference.setVisible(False)

            #psrid = self.iface.mapCanvas().mapRenderer().destinationCrs().srsid()
            psrid = self.iface.mapCanvas().mapSettings().destinationCrs().srsid()
            #self.iface.messageBar().pushMessage(' ', '%s' % psrid, level=Qgis.Warning)
            tool = casePicker(dlg, psrid, self.iface, self.Caser, 'case', lyr)
            self.iface.mapCanvas().setMapTool(tool)

        else:
            self.iface.mapCanvas().setCursor(self.prevcur)
            self.iface.mapCanvas().setMapTool(self.origtool)
            self.iface.actionPan().trigger()


    def addPOI(self):
        self.grp2.setDefaultAction(self.poier)
        if self.poier.isChecked():
            lyr = self.checklayer()
            if lyr is None:
                self.iface.messageBar().pushMessage(' ', 'It is not a POI layer!', level=Qgis.Warning)
                self.poier.setChecked(False)
                return

            flds = lyr.dataProvider().fields()
            flst = []
            for fld in flds:
                flst.append(fld.name())

            if flst != self.poiflds:
                self.iface.messageBar().pushMessage(' ', 'It is not a POI layer!', level= Qgis.Warning)
                self.poier.setChecked(False)
                return

            self.prevcur = self.iface.mapCanvas().cursor()
            self.iface.mapCanvas().setCursor(Qt.CrossCursor)

            dlg = poi.Dialog()
            x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
            y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
            dlg.move(x,y)
            dlg.setWindowTitle('Point of Interest')

            dlg.comboBox.addItem('')
            for it in self.lstpt:
                dlg.comboBox.addItem(it)

            psrid = self.iface.mapCanvas().mapSettings().destinationCrs().srsid()
            tool = casePicker(dlg, psrid, self.iface, self.poier, 'poi', lyr)
            self.iface.mapCanvas().setMapTool(tool)

        else:
            self.iface.mapCanvas().setCursor(self.prevcur)
            self.iface.mapCanvas().setMapTool(self.origtool)
            self.iface.actionPan().trigger()



    def addGeometryColumnSL(self, lyr, lyr_name):
        """
        Function that allows to create a sql query for SpatiaLite database and
        add geometry column for different type of input layer.

        Input:
            lyr: QgsVectorLayer input layer
            lyr_name: String with the name of the layer
        """
        crs_in = lyr.sourceCrs()
        crs_epsg = crs_in.postgisSrid()

        f_type = ''
        lgt = lyr.geometryType()
        if lgt == 0:
            f_type = 'POINT'
        elif lgt == 1:
            f_type = 'LINESTRING'
        elif lgt == 2:
            f_type = 'POLYGON'

        #TODO: linestring or multistring, polygon or multipoligon, 2D or 3D
        l_type = QgsWkbTypes.isMultiType(lyr.getGeometry(0).wkbType())

        if l_type:
            f_type = 'MULTI' + f_type

        dimension = 'XY'
        if QgsWkbTypes.hasZ(lyr.wkbType()):
            dimension = dimension + 'Z'
        if QgsWkbTypes.hasM(lyr.wkbType()):
            dimension = dimension + 'M'

        sql = "SELECT AddGeometryColumn('%s', 'geom', %d, '%s', '%s')" % (lyr_name, crs_epsg,f_type,dimension)

        return sql


    def checkValue(self, value):
        v = value
        if not value:
            v = None
        return v


class casePicker(QgsMapTool):
    # http://gis.stackexchange.com/questions/45094/how-to-programatically-check-for-a-mouse-click-in-qgis
    afterClick = pyqtSignal()

    def __init__(self, dlg, psrid, iface, tt, lab, lyr):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.dlg = dlg
        self.psrid = psrid
        self.tt = tt
        self.lab = lab
        self.lyr = lyr
        self.funcs = qvfuncs.VetEpiGISFuncs()

        self.canvas.setCursor(mutato)


    def canvasPressEvent(self, event):
        pass


    def canvasMoveEvent(self, event):
        pass


    def canvasReleaseEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        pt = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        x = pt.x()
        y = pt.y()

        # EPSG:4326 = srid:3452
        if self.psrid!=3452:
            #trA = QgsCoordinateTransform(self.psrid, 3452)
            crs1 = QgsCoordinateReferenceSystem()
            crs1.createFromSrsId(self.psrid)
            crs2 = QgsCoordinateReferenceSystem()
            crs2.createFromSrsId(3452)
            trA = QgsCoordinateTransform(crs1, crs2, QgsProject.instance())

            ptb = trA.transform(pt)
            x = ptb.x()
            y = ptb.y()

        self.dlg.lineEdit_longitude.setText('%s' % x)
        self.dlg.lineEdit_2_latitude.setText('%s' % y)

        if self.dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            x = float(self.dlg.lineEdit_longitude.text())
            y = float(self.dlg.lineEdit_2_latitude.text())
            self.addFeat(x, y)
            self.tt.setChecked(False)

            QApplication.restoreOverrideCursor()


    def addFeat(self, x, y):
        self.lyr.startEditing()
        feat = QgsFeature()

        if self.lab=='case':
            feat = self.funcs.outattrPrep(self.dlg, self.lyr)
            pnt = QgsGeometry.fromPointXY(QgsPointXY(x,y))

            if self.lyr.geometryType() == QgsWkbTypes.PointGeometry:
                feat.setGeometry(pnt)

            elif self.lyr.geometryType() == QgsWkbTypes.PolygonGeometry:
                lyrB = None
                for l in QgsProject.instance().mapLayers().values():
                    if l.name() == self.dlg.comboBox_reference.currentText():
                        lyrB = l

                srid = lyrB.dataProvider().crs().srsid()

        #        EPSG:4326 = srid:3452
                if srid!=3452:
                    tr = QgsCoordinateTransform(3452, srid)
                    pta = QgsPoint(x,y)
                    ptb = tr.transform(pta)
                    x = ptb.x()
                    y = ptb.y()

                rect = QgsRectangle(QgsPoint(x,y), QgsPoint(x,y))

                req = QgsFeatureRequest()
                req.setFilterRect(rect)
                # polyfeat = lyrB.getFeatures(req).next()
                polyfeat = QgsFeature()
                lyrB.getFeatures(rqst).nextFeature(polyfeat)
                polyg = QgsGeometry(polyfeat.geometry())
                if srid!=3452:
                    tr = QgsCoordinateTransform(srid, 3452)
                    polyg.transform(tr)

                feat.setGeometry(polyg)

            else:
                pass

        elif self.lab=='poi':
            if self.lyr.geometryType() == QgsWkbTypes.PointGeometry:
                flds = self.lyr.dataProvider().fields()
                feat.setFields(flds, True)
                feat.setAttribute(feat.fieldNameIndex('localid'), self.checkValue2(self.dlg.lineEdit_3.text()))
                feat.setAttribute(feat.fieldNameIndex('code'), self.checkValue2(self.dlg.lineEdit_5.text()))
                feat.setAttribute(feat.fieldNameIndex('activity'), self.dlg.comboBox.currentText())
                feat.setAttribute(feat.fieldNameIndex('hrid'), self.funcs.hashIDer(QDateTime.currentDateTimeUtc(),0))

                pnt = QgsGeometry.fromPointXY(QgsPointXY(x,y))
                feat.setGeometry(pnt)
            else:
                self.iface.messageBar().pushMessage(' ', 'Point layer must be selected!', level=Qgis.Warning)

        feat.setValid(True)
        self.lyr.addFeature(feat)
        self.lyr.commitChanges()
        self.lyr.updateExtents()
        self.iface.actionPan().trigger()

    def checkValue2(self, value):
        v = value
        if not value:
            v = None
        return v

    def activate(self):
        pass


    def deactivate(self):
        pass


    def isZoomTool(self):
        return False


    def isTransient(self):
        return False


    def isEditTool(self):
        return True


class polyDraw(QgsMapTool):
    afterClick = pyqtSignal()

    def __init__(self, dlg, psrid, iface, tt):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.dlg = dlg
        self.psrid = psrid
        self.tt = tt
        self.pn = 0
        self.feat = QgsFeature()
        self.pts = []
        self.funcs = qvfuncs.VetEpiGISFuncs()

        col = QColor(Qt.red)
        col.setAlpha(160)
        self.rb = QgsRubberBand(self.canvas, True)
        self.rb.setColor(col)
        self.rb.setFillColor(col)
        self.rb.setWidth(1)
        self.rb.setLineStyle(Qt.SolidLine)
        self.rb.setBrushStyle(Qt.SolidPattern)

        self.canvas.setCursor(mutato)


    def canvasReleaseEvent(self, event):
        if (event.button()==Qt.LeftButton):
            if self.pn == 0:
                self.feat = QgsFeature()

            x = event.pos().x()
            y = event.pos().y()
            pt = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
            self.pts.append(pt)
            self.pn += 1

            if self.pn == 1:
                self.rb.setToGeometry(QgsGeometry.fromPointXY(pt), None)
            elif self.pn == 2:
                self.rb.setToGeometry(QgsGeometry.fromPolylineXY(self.pts), None)
            elif self.pn > 2:
                self.rb.setToGeometry(QgsGeometry.fromPolygonXY([self.pts]), None)

        elif (event.button()==Qt.RightButton):
            if self.pn > 2:
                self.dlg.label_4_reference.setVisible(False)
                self.dlg.comboBox_reference.setVisible(False)
                self.dlg.label_10_outbreak_layer.setVisible(False)
                self.dlg.comboBox_5_outbreak_layer.setVisible(False)

                self.dlg.label_longitude.setVisible(False)
                self.dlg.lineEdit_longitude.setVisible(False)
                self.dlg.toolButton_3_dms.setVisible(False)
                self.dlg.label_2_latitude.setVisible(False)
                self.dlg.lineEdit_2_latitude.setVisible(False)

                if self.dlg.exec_() == QDialog.Accepted:
                    QApplication.setOverrideCursor(Qt.WaitCursor)
                    geom = QgsGeometry.fromPolygonXY([self.pts])
                    self.addFeat(geom)
                    self.tt.setChecked(False)
                    QApplication.restoreOverrideCursor()

                self.pn = 0
                self.pts = []
                self.rb.reset()


    def addFeat(self, geom):
        self.lyr = self.iface.activeLayer()
        provider = self.lyr.dataProvider()
        provider.reloadData()
        psrid = QgsProject.instance().crs().srsid()

        self.lyr.startEditing()

        self.feat = self.funcs.outattrPrep(self.dlg, self.lyr)

        if psrid != 3452:
            QgsCoordinateReferenceSystem.invalidateCache()
            crssource = QgsCoordinateReferenceSystem()
            crssource.createFromSrsId(psrid)
            crsdest = QgsCoordinateReferenceSystem()
            crsdest.createFromSrsId(3452)
            tr = QgsCoordinateTransform(crssource, crsdest, QgsProject.instance())
            geom.transform(tr)

        self.feat.setGeometry(geom)
        self.feat.setValid(True)
        self.lyr.addFeature(self.feat)
        self.lyr.commitChanges()
        self.lyr.updateExtents()
        self.iface.actionPan().trigger()



    def activate(self):
        pass


    def deactivate(self):
        pass


    def isZoomTool(self):
        return False


    def isTransient(self):
        return False


    def isEditTool(self):
        return True


    def canvasPressEvent(self, event):
        pass


    def canvasMoveEvent(self, event):
        pass

