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

import os, shutil
from PyQt4.QtGui import *
from PyQt4.QtCore import SIGNAL, Qt, QSettings, QCoreApplication, QFile, QFileInfo, QDate, QVariant, \
    pyqtSignal, QRegExp, QDateTime, QTranslator, QSize
from PyQt4.QtSql import *
from PyQt4.QtXml import *

from qgis.core import QgsField, QgsSpatialIndex, QgsMessageLog, QgsProject, \
    QgsCoordinateTransform, QGis, QgsVectorFileWriter, QgsMapLayerRegistry, QgsFeature, \
    QgsGeometry, QgsFeatureRequest, QgsPoint, QgsVectorLayer, QgsCoordinateReferenceSystem, \
    QgsRectangle, QgsDataSourceURI, QgsDataProvider, QgsComposition, QgsComposerMap, QgsAtlasComposition
from qgis.gui import QgsMapTool, QgsMapToolEmitPoint, QgsMessageBar, QgsRubberBand

from plugin import buffer, caser, select, outbreaklayer, xabout, poi, dbtbs, dbmaint, xsettings, \
    qvfuncs, xcoordtrafo, query, zone, export, xprint
import resources_rc
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

        self.vers = '0.77'
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
        dbuidpath = os.path.join(dbfold, dbuid)
        if not os.path.isfile(dbuidpath):
            shutil.copy(os.path.join(dbfold, 'base.sqlite'), dbuidpath)

        self.uri = QgsDataSourceURI()
        self.uri.setDatabase(dbuidpath)

        self.db = QSqlDatabase.addDatabase('QSPATIALITE')
        self.db.setDatabaseName(self.uri.database())

        self.loadLists()
        self.sldLoader()
        self.loadModel()

        self.dockw.tableView.doubleClicked.connect(self.layersinDBLoad)

        self.polyn = 0

        self.obrflds = ['gid', 'localid', 'code', 'largescale', 'disease', 'animalno', 'species', 'production', 'year', 'status', 'suspect', 'confirmation', 'expiration', 'notes', 'hrid', 'timestamp', 'grouping']
        self.poiflds = self.obrflds[0:3]
        self.poiflds.append('activity')
        self.poiflds.append('hrid')

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

        self.sep = QAction(self.iface.mainWindow())
        self.sep.setSeparator(True);
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

        self.sep2 = QAction(self.iface.mainWindow())
        self.sep2.setSeparator(True);
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
        self.sep3.setSeparator(True);
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.sep3)

        self.dbtabs = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/data112.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Show/hide VetEpiGIS database layers"),
            self.iface.mainWindow())
        self.dbtabs.setCheckable(True)
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.dbtabs)
        self.dbtabs.triggered.connect(self.layersinDB)

        self.recedit = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/pencil148.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Edit data (case and POI)"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.recedit)
        self.recedit.triggered.connect(self.featEdit)

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
            QCoreApplication.translate('VetEpiGIS-Tool', "Export layer"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.xprt)
        self.xprt.triggered.connect(self.expLayer)

        self.xprnt = QAction(
            QIcon(':/plugins/VetEpiGIStool/images/tool-1.png'),
            QCoreApplication.translate('VetEpiGIS-Tool', "Print VetEpiGIS template"),
            self.iface.mainWindow())
        self.iface.addPluginToMenu('&VetEpiGIS-Tool', self.xprnt)
        self.xprnt.triggered.connect(self.printMap)

        self.sep4 = QAction(self.iface.mainWindow())
        self.sep4.setSeparator(True);
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
        self.sep5.setSeparator(True);
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

        self.grp1 = QToolButton(self.toolbar)
        self.grp1.setPopupMode(QToolButton.MenuButtonPopup)
        self.grp1.addActions([self.newoutbreak, self.Caser, self.handy, self.copyselected])
        self.grp1.setDefaultAction(self.newoutbreak)
        self.toolbar.addWidget(self.grp1)

        self.grp2 = QToolButton(self.toolbar)
        self.grp2.setPopupMode(QToolButton.MenuButtonPopup)
        self.grp2.addActions([self.newpoilayer, self.poier])
        self.grp2.setDefaultAction(self.newpoilayer)
        self.toolbar.addWidget(self.grp2)

        self.grp3 = QToolButton(self.toolbar)
        self.grp3.setPopupMode(QToolButton.MenuButtonPopup)
        self.grp3.addActions([self.Bufferer, self.POIer, self.Zoner])
        self.grp3.setDefaultAction(self.Bufferer)
        self.toolbar.addWidget(self.grp3)

        self.grp4 = QToolButton(self.toolbar)
        self.grp4.setPopupMode(QToolButton.MenuButtonPopup)
        self.grp4.addActions([self.dbtabs, self.recedit, self.Saver, self.dbmaintain, self.xprt, self.xprnt])
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
            rend = canv.mapRenderer()
            rect = QgsRectangle(self.iface.mapCanvas().extent())

            qpt = os.path.join(self.plugin_dir, 'templates/qvet_h_template.qpt')
            if dlg.radioButton_2.isChecked():
                qpt = os.path.join(self.plugin_dir, 'templates/qvet_v_template.qpt')

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

            comp = QgsComposition(rend)
            comp.loadFromTemplate(doc)

            pdfpath = dlg.lineEdit_3.text()
            xt = os.path.splitext(pdfpath)[-1].lower()
            if xt!='.pdf':
                pdfpath = '%s.pdf' % pdfpath

            out = comp.exportAsPDF(pdfpath)
            QApplication.restoreOverrideCursor()


    def expLayer(self):
        self.grp4.setDefaultAction(self.xprt)
        dlg = export.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Export selected layer')

        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            lyr = self.checklayer()
            ln = str(lyr.name()).lower()
            prv = lyr.dataProvider()
            if dlg.comboBox.currentText()=='ESRI shape file':
                wrt = QgsVectorFileWriter.writeAsVectorFormat(lyr,
                    os.path.join(dlg.lineEdit.text(), '%s.shp' % ln ),
                    'system',
                    QgsCoordinateReferenceSystem(prv.crs().srsid()),
                    'ESRI Shapefile')
            elif dlg.comboBox.currentText()=='Comma separated value (CSV)':
                lops = []
                if dlg.comboBox_2.currentText()==';':
                    lops.append('SEPARATOR=SEMICOLON')
                elif dlg.comboBox_2.currentText()==',':
                    lops.append('SEPARATOR=COMMA')
                elif dlg.comboBox_2.currentText()=='tab':
                    lops.append('SEPARATOR=TAB')

                if dlg.checkBox.isChecked():
                    lops.append('GEOMETRY=AS_WKT')

                wrt = QgsVectorFileWriter.writeAsVectorFormat(lyr,
                    os.path.join(dlg.lineEdit.text(), '%s.csv' % ln ),
                    'system',
                    None,
                    'CSV', layerOptions=lops)

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
            for i in xrange(len(sl)):
                slst.append(sl[i])
            pl = str(attr[7]).split(' | ')
            for i in xrange(len(pl)):
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
            for i in xrange(rn):
                items.append(dlg.tableWidget.item(i, 0).text())
                aliases.append(dlg.tableWidget.item(i, 1).text())

            lyr.startEditing()
            while feats.nextFeature(feat):
                attr = feat.attributes()
                lanc = str(attr[n])
                fid = feat.id()
                for i in xrange(len(items)):
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
        self.iface.messageBar().pushMessage('Information', 'For editing the VetEpiGIS database all layers are removed from the workspace.', level=QgsMessageBar.INFO)
        QgsMapLayerRegistry.instance().removeAllMapLayers()

        dlg = dbmaint.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)

        dlg.setWindowTitle('Database maintenance')
        dlg.toolButton.setIcon(QIcon(':/plugins/VetEpiGIStool/images/verify8.png'))

        dlg.comboBox.addItem('')
        dlg.comboBox.addItem('Diseases')
        dlg.comboBox.addItem('POI types')
        dlg.comboBox.addItem('Species')

        dlg.comboBox_2.addItem('en')
        dlg.comboBox_2.addItem('it')

        dlg.db = self.db
        dlg.loadLayers()

        if dlg.exec_() == QDialog.Accepted:
            self.loadModel()

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


    def featEdit(self):
        self.grp4.setDefaultAction(self.recedit)
        lyr = self.checklayer()
        if lyr is None:
            return

        if lyr.selectedFeatureCount()!=1:
            # only one object selection allowed
            return

        flds = lyr.dataProvider().fields()
        flst = []
        for fld in flds:
            flst.append(fld.name())

        tn = ''
        if flst == self.poiflds:
            tn = 'poi'
        if flst == self.obrflds:
            tn = 'outbreak'

        if tn=='':
            return

        feat = lyr.selectedFeatures()[0]
        attr = feat.attributes()
        fid = feat.id()

        if tn == 'poi':
            dlg = poi.Dialog()
            x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
            y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
            dlg.move(x,y)
            dlg.setWindowTitle('Point of Interest')

            dlg.comboBox.addItem('')
            for it in self.lstpt:
                dlg.comboBox.addItem(it)

            dlg.label.setVisible(False)
            dlg.lineEdit.setVisible(False)
            dlg.toolButton.setVisible(False)
            dlg.label_2.setVisible(False)
            dlg.lineEdit_2.setVisible(False)
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


        elif tn == 'outbreak':
            dlg = caser.Dialog()
            x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
            y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
            dlg.move(x,y)
            dlg.setWindowTitle('Create new case')
            dlg.label_10.setVisible(False)
            dlg.comboBox_5.setVisible(False)
            dlg.label.setVisible(False)
            dlg.lineEdit.setVisible(False)
            dlg.toolButton_3.setVisible(False)
            dlg.label_2.setVisible(False)
            dlg.lineEdit_2.setVisible(False)
            dlg.label_4.setVisible(False)
            dlg.comboBox.setVisible(False)

            dlg.comboBox_2.addItem('')
            for it in self.lsta:
                dlg.comboBox_2.addItem(it)

            dlg.lstb = self.lstb

            dlg.lineEdit_3.setText(str(attr[1]))
            dlg.lineEdit_5.setText(str(attr[2]))
            dlg.comboBox_4.setCurrentIndex(dlg.comboBox_4.findText(attr[3], Qt.MatchExactly))
            dlg.comboBox_2.setCurrentIndex(dlg.comboBox_2.findText(attr[4], Qt.MatchExactly))
            dlg.lineEdit_6.setText(str(attr[5]))

            slst = str(attr[6]).split(' | ')
            plst = str(attr[7]).split(' | ')
            for i in xrange(len(slst)):
                dlg.tableWidget.insertRow(dlg.tableWidget.rowCount())
                nr = dlg.tableWidget.rowCount() - 1
                item = QTableWidgetItem(slst[i])
                dlg.tableWidget.setItem(nr, 0, item)
                item = QTableWidgetItem(str(plst[i]))
                dlg.tableWidget.setItem(nr, 1, item)

            dlg.lineEdit_4.setText(str(attr[8]))
            dlg.comboBox_3.setCurrentIndex(dlg.comboBox_3.findText(attr[9], Qt.MatchExactly))
            k = '01/01/2000'
            f = 'dd/MM/yyyy'
            s = k
            if attr[10]!='':
                s = attr[10]
                dlg.dateEdit.setEnabled(True)
                dlg.checkBox.setChecked(True)
            qd = QDate.fromString(s, f)
            dlg.dateEdit.setDate(qd)
            s = k
            if attr[11]!='':
                s = attr[11]
                dlg.dateEdit_2.setEnabled(True)
                dlg.checkBox_2.setChecked(True)
            qd = QDate.fromString(s, f)
            dlg.dateEdit_2.setDate(qd)
            s = k
            if attr[12]!='':
                s = attr[12]
                dlg.dateEdit_3.setEnabled(True)
                dlg.checkBox_3.setChecked(True)
            qd = QDate.fromString(s, f)
            dlg.dateEdit_3.setDate(qd)

            dlg.textEdit.setText(attr[13])
            if dlg.exec_() == QDialog.Accepted:
                QApplication.setOverrideCursor(Qt.WaitCursor)

                lyr.startEditing()
                species = ''
                production = ''
                rn = dlg.tableWidget.rowCount()
                for i in xrange(rn):
                    if i==0:
                        species = dlg.tableWidget.item(i, 0).text()
                        production = dlg.tableWidget.item(i, 1).text()
                    else:
                        species = species + ' | ' + dlg.tableWidget.item(i, 0).text()
                        production = production + ' | ' + dlg.tableWidget.item(i, 1).text()

                lyr.changeAttributeValue(fid, 1, dlg.lineEdit_3.text())
                lyr.changeAttributeValue(fid, 2, dlg.lineEdit_5.text())
                lyr.changeAttributeValue(fid, 3, dlg.comboBox_4.currentText())
                lyr.changeAttributeValue(fid, 4, dlg.comboBox_2.currentText())
                lyr.changeAttributeValue(fid, 5, dlg.lineEdit_6.text())
                lyr.changeAttributeValue(fid, 6, species)
                lyr.changeAttributeValue(fid, 7, production)
                lyr.changeAttributeValue(fid, 8, dlg.lineEdit_4.text())
                lyr.changeAttributeValue(fid, 9, dlg.comboBox_3.currentText())
                lyr.changeAttributeValue(fid, 10, self.dateCheck(dlg.dateEdit.date()))
                lyr.changeAttributeValue(fid, 11, self.dateCheck(dlg.dateEdit_2.date()))
                lyr.changeAttributeValue(fid, 12, self.dateCheck(dlg.dateEdit_3.date()))
                lyr.changeAttributeValue(fid, 13, dlg.textEdit.toPlainText())
                lyr.changeAttributeValue(fid, 15, QDateTime.currentDateTimeUtc().toString('dd/MM/yyyy hh:mm:ss'))
                lyr.commitChanges()

                QApplication.restoreOverrideCursor()


    def checklayer(self):
        if QgsMapLayerRegistry.instance().count()==0:
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
            self.iface.messageBar().pushMessage(' ', 'spatialite', level=QgsMessageBar.INFO)


    def layersinDB(self):
        self.grp4.setDefaultAction(self.dbtabs)
        if self.dbtabs.isChecked():
            self.iface.addDockWidget( Qt.LeftDockWidgetArea, self.dockw)
            self.dockw.setWindowTitle('VetEpiGIS layers')
        elif not self.dbtabs.isChecked():
            self.iface.removeDockWidget(self.dockw)


    def layersinDBLoad(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        idx = self.dockw.tableView.selectionModel().selectedIndexes()[0]
        ln = str(self.model.itemData(idx)[0])
        self.uri.setDataSource('', ln, 'geom')
        vl = QgsVectorLayer(self.uri.uri(), ln, 'spatialite')
        QgsMapLayerRegistry.instance().addMapLayer(vl)
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
        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)

            lnb = dlg.lineEdit.text().lower()
            self.layer2db(lyr, lnb)
            self.loadModel()

            self.uri.setDataSource('', lnb,'geom')
            vl = QgsVectorLayer(self.uri.uri(), lnb, 'spatialite')
            QgsMapLayerRegistry.instance().addMapLayer(vl)

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
        for i in xrange(len(ntlst)):
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
        for i in xrange(len(lst)):
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
                self.iface.messageBar().pushMessage(' ', 'It is not an OUTBREAK layer!', level=QgsMessageBar.WARNING)
                self.handy.setChecked(False)
                return

            if flst == self.obrflds and lyr.geometryType() != QGis.Polygon:
                self.iface.messageBar().pushMessage(' ', 'It is not an AREA outbreak layer!', level=QgsMessageBar.WARNING)
                self.handy.setChecked(False)
                return

            self.prevcur = self.iface.mapCanvas().cursor()
            self.iface.mapCanvas().setCursor(Qt.CrossCursor)

            dlg = caser.Dialog()
            x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
            y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
            dlg.move(x,y)
            dlg.setWindowTitle('Create new case')
            dlg.label_10.setVisible(False)
            dlg.comboBox_5.setVisible(False)

            for it in self.lsta:
                dlg.comboBox_2.addItem(it)

            dlg.lstb = self.lstb

            if lyr.geometryType() == QGis.Polygon:
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
        dlg.label_4.setText('Source layer:')

        for it in self.lsta:
            dlg.comboBox_2.addItem(it)

        dlg.lstb = self.lstb

        lyrs = self.iface.legendInterface().layers()
        lrs = []
        tlrs = []
        n = 0
        fldn = 0
        for lyr in lyrs:
            if lyr.type()==0:
                if lyr.geometryType() != QGis.Line:
                    flst = self.funcs.ofielder(lyr)
                    if flst == self.obrflds:
                        fldn += 1

                    lrs.append(lyr.name())
                    if lyr.geometryType() == QGis.Point:
                        tlrs.append('point')
                    if lyr.geometryType() == QGis.Polygon:
                        tlrs.append('poly')
                    if lyr.selectedFeatureCount()==1:
                        dlg.comboBox.addItem(lyr.name())
                        n += 1
        if n==0:
            self.iface.messageBar().pushMessage(' ', 'There is no selected object to copy!', level=QgsMessageBar.WARNING)
            return

        if fldn==0:
            self.iface.messageBar().pushMessage(' ', 'There is no OUTBREAK layer!', level=QgsMessageBar.WARNING)
            return

        dlg.lrs = lrs
        dlg.tlrs = tlrs
        dlg.comboBox.currentIndexChanged.connect(dlg.outLSel)
        dlg.outLSel()

        dlg.label.setVisible(False)
        dlg.lineEdit.setVisible(False)
        dlg.toolButton_3.setVisible(False)
        dlg.label_2.setVisible(False)
        dlg.lineEdit_2.setVisible(False)

        if dlg.exec_() == QDialog.Accepted:
            src = ''
            dst = ''
            for lyr in lyrs:
                if lyr.name()== dlg.comboBox.currentText():
                    src = lyr
                elif lyr.name()== dlg.comboBox_5.currentText():
                    dst = lyr

            sfeats = src.selectedFeatures()
            sg = QgsGeometry()
            self.iface.emit(SIGNAL('rangeCalculated( PyQt_PyObject)'), len(sfeats))
            for sf in sfeats:
                sg = sf.geometry()
                self.iface.emit(SIGNAL('featureProcessed()'))

            dst.startEditing()
            feat = self.funcs.outattrPrep(dlg, dst)
            feat.setGeometry(QgsGeometry(sg))
            feat.setValid(True)
            dst.addFeature(feat)
            dst.commitChanges()
            dst.updateExtents()


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
            QgsMapLayerRegistry.instance().addMapLayer(vl)
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
            QgsMapLayerRegistry.instance().addMapLayer(vl)
            self.loadModel()
            QApplication.restoreOverrideCursor()


    def selectPOIs(self):
        self.grp3.setDefaultAction(self.POIer)
        dlg = select.Dialog()
        x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
        y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
        dlg.move(x,y)
        dlg.setWindowTitle('Select POIs by polygons')

        lyrs = self.iface.legendInterface().layers()
        for lyr in lyrs:
            if lyr.type()==0:
                if lyr.geometryType() == QGis.Polygon:
                    dlg.comboBox.addItem(lyr.name())
                if lyr.geometryType() == QGis.Point:
                    dlg.comboBox_2.addItem(lyr.name())

        dlg.lineEdit.setText('_selected_by_')
        dlg.tablst = self.tablst
        dlg.nameCtrl()
        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)

            l1 = l2 = QgsVectorLayer

            for lyr in lyrs:
                if lyr.name()==dlg.comboBox.currentText():
                    l1 = lyr
                    prv1 = l1.dataProvider()
                if lyr.name()==dlg.comboBox_2.currentText():
                    l2 = lyr
                    prv2 = l2.dataProvider()

            ln = dlg.lineEdit.text()
            vl = QgsVectorLayer('Point?crs=' + prv1.crs().toWkt(), ln, 'memory')

            oattrs = prv2.fields().toList()
            nattrs = []
            for attr in oattrs:
                if vl.fieldNameIndex(attr.name())==-1:
                    nattrs.append(QgsField(attr.name(),attr.type()))
                    vl.dataProvider().addAttributes(nattrs)
                    vl.updateFields()

            oattrs = prv1.fields().toList()
            nattrs = []
            for attr in oattrs:
                s = 'selby_%s' % attr.name()
                if vl.fieldNameIndex(s)==-1:
                    nattrs.append(QgsField(s, attr.type()))
                    vl.dataProvider().addAttributes(nattrs)
                    vl.updateFields()

            vl.startEditing()

            index = QgsSpatialIndex()
            ftbs = l2.getFeatures()
            if prv1.crs().toWkt()==prv2.crs().toWkt():
                for ft in ftbs:
                    index.insertFeature(ft)
            else:
                trA = QgsCoordinateTransform(prv2.crs().toWkt(), prv1.crs().toWkt())
                for ft in ftbs:
                    ft.geometry().transform(trA)
                    index.insertFeature(ft)

            feat = QgsFeature()

            if l1.selectedFeatureCount()==0:
                feats = prv1.getFeatures()
                while feats.nextFeature(feat):
                    geom = feat.constGeometry()
                    idxs = index.intersects(geom.boundingBox())
                    for idx in idxs:
                        rqst = QgsFeatureRequest().setFilterFid(idx)
                        featB = prv2.getFeatures(rqst).next()
                        geomB = QgsGeometry(featB.geometry())
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
                self.iface.emit(SIGNAL('rangeCalculated( PyQt_PyObject)'), len(feats))
                for feat in feats:
                    geom = feat.constGeometry()
                    idxs = index.intersects(geom.boundingBox())
                    for idx in idxs:
                        rqst = QgsFeatureRequest().setFilterFid(idx)
                        featB = prv2.getFeatures(rqst).next()
                        geomB = QgsGeometry(featB.geometry())
                        attrs=[]
                        attrs.extend(featB.attributes())
                        attrs.extend(feat.attributes())
                        if geom.intersects(geomB):
                            featC = QgsFeature()
                            featC.setGeometry(geomB)
                            featC.setAttributes(attrs)
                            vl.addFeature(featC)

                    self.iface.emit(SIGNAL('featureProcessed()'))


            vl.commitChanges()
            vl.updateExtents()

            if dlg.checkBox.isChecked():
                self.layer2db(vl, ln)
                self.loadModel()
                self.uri.setDataSource('', ln,'geom')
                vl = QgsVectorLayer(self.uri.uri(), ln, 'spatialite')

            QgsMapLayerRegistry.instance().addMapLayer(vl)
            QApplication.restoreOverrideCursor()


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
        lyrs = self.iface.legendInterface().layers()
        for lyr in lyrs:
            if lyr.type()==0:
                if lyr.geometryType() == QGis.Polygon:
                    dlg.comboBox.addItem(lyr.name())
                    dlg.comboBox_2.addItem(lyr.name())
                    dlg.comboBox_13.addItem(lyr.name())

        dlg.lineEdit.setText('zone_selected_by_')

        if dlg.exec_() == QDialog.Accepted:
            if dlg.comboBox.currentText()==dlg.comboBox_2.currentText():
                return False

            QApplication.setOverrideCursor(Qt.WaitCursor)
            l1 = l2 = QgsVectorLayer

            for lyr in lyrs:
                if lyr.name()==dlg.comboBox.currentText():
                    l1 = lyr
                    prv1 = l1.dataProvider()
                if lyr.name()==dlg.comboBox_2.currentText():
                    l2 = lyr
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

            zonetype = dlg.comboBox_3.currentText()

            subpopulation = ''
            rn = dlg.tableWidget.rowCount()
            for i in xrange(rn):
                if i==0:
                    subpopulation = dlg.tableWidget.item(i, 0).text()
                else:
                    subpopulation = subpopulation + ', ' + dlg.tableWidget.item(i, 0).text()

            validity_start = self.funcs.dateCheck(dlg.dateEdit.date())
            validity_end = self.funcs.dateCheck(dlg.dateEdit_2.date())
            legal_framework = dlg.lineEdit_2.text()
            competent_authority = dlg.lineEdit_3.text()
            biosecurity_measures = dlg.comboBox_5.currentText()
            control_of_vectors = dlg.comboBox_6.currentText()
            control_of_wildlife_reservoir = dlg.comboBox_7.currentText()
            modified_stamping_out = dlg.comboBox_8.currentText()
            movement_restriction = dlg.comboBox_9.currentText()
            stamping_out = dlg.comboBox_10.currentText()
            surveillance = dlg.comboBox_11.currentText()
            vaccination = dlg.comboBox_12.currentText()
            other_measure = dlg.lineEdit_4.text()
            timestamp = QDateTime.currentDateTimeUtc().toString('dd/MM/yyyy hh:mm:ss')
            related = dlg.comboBox_13.currentText()

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
                    if prv1.crs().toWkt()!=prv2.crs().toWkt():
                        trA = QgsCoordinateTransform(prv1.crs().toWkt(), prv2.crs().toWkt())
                        trB = QgsCoordinateTransform(prv2.crs().toWkt(), prv1.crs().toWkt())
                        while feats.nextFeature(feat):
                            geom = feat.constGeometry()
                            geom.transform(trA)
                            idxs = index.intersects(geom.boundingBox())
                            for idx in idxs:
                                rqst = QgsFeatureRequest().setFilterFid(idx)
                                featB = prv2.getFeatures(rqst).next()
                                geomB = QgsGeometry(featB.geometry())

                                attrs[0] = feat.attributes()[feat.fieldNameIndex('localid')]
                                attrs[1] = feat.attributes()[feat.fieldNameIndex('code')]
                                attrs[2] = feat.attributes()[feat.fieldNameIndex('disease')]
                                most = QDateTime.currentDateTimeUtc()
                                attrs[19] = self.funcs.hashIDer(most)

                                if geom.intersects(geomB):
                                    featC = QgsFeature()
                                    geomBa = QgsGeometry(geomB)
                                    geomBa.transform(trB)
                                    featC.setGeometry(geomBa)
                                    featC.setAttributes(attrs)
                                    vl.addFeature(featC)
                    else:
                        while feats.nextFeature(feat):
                            geom = feat.constGeometry()
                            idxs = index.intersects(geom.boundingBox())
                            for idx in idxs:
                                rqst = QgsFeatureRequest().setFilterFid(idx)
                                featB = prv2.getFeatures(rqst).next()
                                geomB = QgsGeometry(featB.geometry())

                                attrs[0] = feat.attributes()[feat.fieldNameIndex('localid')]
                                attrs[1] = feat.attributes()[feat.fieldNameIndex('code')]
                                attrs[2] = feat.attributes()[feat.fieldNameIndex('disease')]
                                most = QDateTime.currentDateTimeUtc()
                                attrs[19] = self.funcs.hashIDer(most)

                                if geom.intersects(geomB):
                                    featC = QgsFeature()
                                    featC.setGeometry(geomB)
                                    featC.setAttributes(attrs)
                                    vl.addFeature(featC)
                else:
                    feats = l1.selectedFeatures()
                    self.iface.emit(SIGNAL('rangeCalculated( PyQt_PyObject)'), len(feats))
                    if prv1.crs().toWkt()!=prv2.crs().toWkt():
                        trA = QgsCoordinateTransform(prv1.crs().toWkt(), prv2.crs().toWkt())
                        trB = QgsCoordinateTransform(prv2.crs().toWkt(), prv1.crs().toWkt())
                        for feat in feats:
                            geom = feat.constGeometry()
                            geom.transform(trA)
                            idxs = index.intersects(geom.boundingBox())
                            for idx in idxs:
                                rqst = QgsFeatureRequest().setFilterFid(idx)
                                featB = prv2.getFeatures(rqst).next()
                                geomB = QgsGeometry(featB.geometry())

                                attrs[0] = feat.attributes()[feat.fieldNameIndex('localid')]
                                attrs[1] = feat.attributes()[feat.fieldNameIndex('code')]
                                attrs[2] = feat.attributes()[feat.fieldNameIndex('disease')]
                                most = QDateTime.currentDateTimeUtc()
                                attrs[19] = self.funcs.hashIDer(most)

                                if geom.intersects(geomB):
                                    featC = QgsFeature()
                                    geomBa = QgsGeometry(geomB)
                                    geomBa.transform(trB)
                                    featC.setGeometry(geomBa)
                                    featC.setAttributes(attrs)
                                    vl.addFeature(featC)

                            self.iface.emit(SIGNAL('featureProcessed()'))
                    else:
                        for feat in feats:
                            geom = feat.constGeometry()
                            idxs = index.intersects(geom.boundingBox())
                            for idx in idxs:
                                rqst = QgsFeatureRequest().setFilterFid(idx)
                                featB = prv2.getFeatures(rqst).next()
                                geomB = QgsGeometry(featB.geometry())

                                attrs[0] = feat.attributes()[feat.fieldNameIndex('localid')]
                                attrs[1] = feat.attributes()[feat.fieldNameIndex('code')]
                                attrs[2] = feat.attributes()[feat.fieldNameIndex('disease')]
                                most = QDateTime.currentDateTimeUtc()
                                attrs[19] = self.funcs.hashIDer(most)

                                if geom.intersects(geomB):
                                    featC = QgsFeature()
                                    featC.setGeometry(geomB)
                                    featC.setAttributes(attrs)
                                    vl.addFeature(featC)

                            self.iface.emit(SIGNAL('featureProcessed()'))

            elif dlg.comboBox_4.currentText()=='Intersections only':
                zonsty = self.sldZoneB
                if l1.selectedFeatureCount()==0:
                    feats = prv1.getFeatures()
                    if prv1.crs().toWkt()!=prv2.crs().toWkt():
                        trA = QgsCoordinateTransform(prv1.crs().toWkt(), prv2.crs().toWkt())
                        trB = QgsCoordinateTransform(prv2.crs().toWkt(), prv1.crs().toWkt())
                        while feats.nextFeature(feat):
                            geom = feat.constGeometry()
                            geom.transform(trA)
                            idxs = index.intersects(geom.boundingBox())
                            for idx in idxs:
                                rqst = QgsFeatureRequest().setFilterFid(idx)
                                featB = prv2.getFeatures(rqst).next()
                                geomB = QgsGeometry(featB.geometry())

                                attrs[0] = feat.attributes()[feat.fieldNameIndex('localid')]
                                attrs[1] = feat.attributes()[feat.fieldNameIndex('code')]
                                attrs[2] = feat.attributes()[feat.fieldNameIndex('disease')]
                                most = QDateTime.currentDateTimeUtc()
                                attrs[19] = self.funcs.hashIDer(most)

                                if geom.intersects(geomB):
                                    geomD = QgsGeometry(geom.intersection(geomB))
                                    geomD.transform(trB)
                                    featD = QgsFeature()
                                    featD.setGeometry(geomD)
                                    featD.setAttributes(attrs)
                                    vl.addFeature(featD)
                    else:
                        while feats.nextFeature(feat):
                            geom = feat.constGeometry()
                            idxs = index.intersects(geom.boundingBox())
                            for idx in idxs:
                                rqst = QgsFeatureRequest().setFilterFid(idx)
                                featB = prv2.getFeatures(rqst).next()
                                geomB = QgsGeometry(featB.geometry())

                                attrs[0] = feat.attributes()[feat.fieldNameIndex('localid')]
                                attrs[1] = feat.attributes()[feat.fieldNameIndex('code')]
                                attrs[2] = feat.attributes()[feat.fieldNameIndex('disease')]
                                most = QDateTime.currentDateTimeUtc()
                                attrs[19] = self.funcs.hashIDer(most)

                                if geom.intersects(geomB):
                                    geomD = QgsGeometry(geom.intersection(geomB))
                                    featD = QgsFeature()
                                    featD.setGeometry(geomD)
                                    featD.setAttributes(attrs)
                                    vl.addFeature(featD)
                else:
                    feats = l1.selectedFeatures()
                    self.iface.emit(SIGNAL('rangeCalculated( PyQt_PyObject)'), len(feats))
                    if prv1.crs().toWkt()!=prv2.crs().toWkt():
                        trA = QgsCoordinateTransform(prv1.crs().toWkt(), prv2.crs().toWkt())
                        trB = QgsCoordinateTransform(prv2.crs().toWkt(), prv1.crs().toWkt())
                        for feat in feats:
                            geom = feat.constGeometry()
                            geom.transform(trA)
                            idxs = index.intersects(geom.boundingBox())
                            for idx in idxs:
                                rqst = QgsFeatureRequest().setFilterFid(idx)
                                featB = prv2.getFeatures(rqst).next()
                                geomB = QgsGeometry(featB.geometry())

                                attrs[0] = feat.attributes()[feat.fieldNameIndex('localid')]
                                attrs[1] = feat.attributes()[feat.fieldNameIndex('code')]
                                attrs[2] = feat.attributes()[feat.fieldNameIndex('disease')]
                                most = QDateTime.currentDateTimeUtc()
                                attrs[19] = self.funcs.hashIDer(most)

                                if geom.intersects(geomB):
                                    geomD = QgsGeometry(geom.intersection(geomB))
                                    geomD.transform(trB)
                                    featD = QgsFeature()
                                    featD.setGeometry(geomD)
                                    featD.setAttributes(attrs)
                                    vl.addFeature(featD)
                            self.iface.emit(SIGNAL('featureProcessed()'))
                    else:
                        for feat in feats:
                            geom = feat.constGeometry()
                            idxs = index.intersects(geom.boundingBox())
                            for idx in idxs:
                                rqst = QgsFeatureRequest().setFilterFid(idx)
                                featB = prv2.getFeatures(rqst).next()
                                geomB = QgsGeometry(featB.geometry())

                                attrs[0] = feat.attributes()[feat.fieldNameIndex('localid')]
                                attrs[1] = feat.attributes()[feat.fieldNameIndex('code')]
                                attrs[2] = feat.attributes()[feat.fieldNameIndex('disease')]
                                most = QDateTime.currentDateTimeUtc()
                                attrs[19] = self.funcs.hashIDer(most)

                                if geom.intersects(geomB):
                                    geomD = QgsGeometry(geom.intersection(geomB))
                                    featD = QgsFeature()
                                    featD.setGeometry(geomD)
                                    featD.setAttributes(attrs)
                                    vl.addFeature(featD)
                            self.iface.emit(SIGNAL('featureProcessed()'))


            vl.commitChanges()
            vl.updateExtents()

            if dlg.checkBox.isChecked():
                ln = vl.name()
                self.layer2db(vl, ln)
                self.uri.setDataSource('', ln,'geom')
                vl = QgsVectorLayer(self.uri.uri(), ln, 'spatialite')

                self.loadModel()

            vl.loadSldStyle(zonsty)
            QgsMapLayerRegistry.instance().addMapLayer(vl)
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

        if dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)

            lyr = self.iface.mapCanvas().currentLayer()
            provider = lyr.dataProvider()

            provider.reloadData()
            psrid = provider.crs().srsid()
#            Pseudo Mercator: srid 3857
            trA = QgsCoordinateTransform(psrid, 3857)
            trB = QgsCoordinateTransform(3857, psrid)

            r = dlg.spinBox.value()

            ln = dlg.lineEdit.text()

            vl = QgsVectorLayer('Polygon?crs=' + provider.crs().toWkt(), ln, 'memory')

            oattrs = provider.fields().toList()
            nattrs = []
            for attr in oattrs:
                # if (vl.fieldNameIndex(attr.name())==-1) and attr.name()!='grouping':
                if vl.fieldNameIndex(attr.name()) == -1:
                    nattrs.append(QgsField(attr.name(),attr.type()))
                    vl.dataProvider().addAttributes(nattrs)
                    vl.updateFields()

            vl.startEditing()

            lyp = self.iface.mapCanvas().currentLayer()
            provi = lyp.dataProvider()
            feat = QgsFeature()
            polynum = lyp.featureCount()

            if lyp.selectedFeatureCount()==0:
                for feat in provi.getFeatures(QgsFeatureRequest()):
                    ba = QgsGeometry(feat.geometry())
                    ba.transform(trA)
                    bfa = ba.buffer(r, r)
                    bfa.transform(trB)
                    bf = QgsFeature()
                    bf.setGeometry(bfa)
                    attrs=[]
                    attrs.extend(feat.attributes())
                    # del attrs[-16]
                    bf.setAttributes(attrs)
                    most = QDateTime.currentDateTimeUtc()
                    bf.setAttribute(feat.fieldNameIndex('hrid'), self.funcs.hashIDer(most))
                    vl.addFeature(bf)
            else:
                feats = lyp.selectedFeatures()
                self.iface.emit(SIGNAL('rangeCalculated( PyQt_PyObject)'), len(feats))
                for feat in feats:
                    ba = QgsGeometry(feat.geometry())
                    ba.transform(trA)
                    bfa = ba.buffer(r, r)
                    bfa.transform(trB)
                    bf = QgsFeature()
                    bf.setGeometry(bfa)
                    attrs=[]
                    attrs.extend(feat.attributes())
                    # del attrs[-16]
                    bf.setAttributes(attrs)
                    most = QDateTime.currentDateTimeUtc()
                    bf.setAttribute(feat.fieldNameIndex('hrid'), self.funcs.hashIDer(most))
                    vl.addFeature(bf)
                    self.iface.emit(SIGNAL('featureProcessed()'))

            vl.commitChanges()
            # vl.updateExtents()

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
            QgsMapLayerRegistry.instance().addMapLayer(vl)

            QApplication.restoreOverrideCursor()


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
        dlg.textEdit.append('Norbert Solymosi *;\n* from University of Veterinary Medicine, Budapest.\n')
        dlg.textEdit.setFontWeight(QFont.Bold)
        dlg.textEdit.append('Contributors:')
        dlg.textEdit.setFontWeight(ow)
        dlg.textEdit.append(u'Nicola Ferrè *;\nMatteo Mazzucato *;\n* from Istituto Zooprofilattico Sperimentale delle Venezie.\n')
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
                self.iface.messageBar().pushMessage(' ', 'It is not an OUTBREAK layer!', level=QgsMessageBar.WARNING)
                self.Caser.setChecked(False)
                return

            self.prevcur = self.iface.mapCanvas().cursor()
            self.iface.mapCanvas().setCursor(Qt.CrossCursor)

            dlg = caser.Dialog()
            x = (self.iface.mainWindow().x()+self.iface.mainWindow().width()/2)-dlg.width()/2
            y = (self.iface.mainWindow().y()+self.iface.mainWindow().height()/2)-dlg.height()/2
            dlg.move(x,y)

            dlg.setWindowTitle('Create new case')
            dlg.label_10.setVisible(False)
            dlg.comboBox_5.setVisible(False)

            for it in self.lsta:
                dlg.comboBox_2.addItem(it)

            dlg.lstb = self.lstb

            if lyr.geometryType() == QGis.Polygon:
                lyrs = self.iface.legendInterface().layers()
                dlg.comboBox.addItem('')
                for lr in lyrs:
                    if lr.type()==0:
                        if lr.geometryType() == QGis.Polygon:
                            dlg.comboBox.addItem(lr.name())
            else:
                dlg.label_4.setVisible(False)
                dlg.comboBox.setVisible(False)

            psrid = self.iface.mapCanvas().mapRenderer().destinationCrs().srsid()
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
                self.iface.messageBar().pushMessage(' ', 'It is not a POI layer!', level=QgsMessageBar.WARNING)
                self.poier.setChecked(False)
                return

            flds = lyr.dataProvider().fields()
            flst = []
            for fld in flds:
                flst.append(fld.name())

            if flst != self.poiflds:
                self.iface.messageBar().pushMessage(' ', 'It is not a POI layer!', level=QgsMessageBar.WARNING)
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

            psrid = self.iface.mapCanvas().mapRenderer().destinationCrs().srsid()
            tool = casePicker(dlg, psrid, self.iface, self.poier, 'poi', lyr)
            self.iface.mapCanvas().setMapTool(tool)

        else:
            self.iface.mapCanvas().setCursor(self.prevcur)
            self.iface.mapCanvas().setMapTool(self.origtool)
            self.iface.actionPan().trigger()


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
            trA = QgsCoordinateTransform(self.psrid, 3452)
            ptb = trA.transform(pt)
            x = ptb.x()
            y = ptb.y()

        self.dlg.lineEdit.setText('%s' % x)
        self.dlg.lineEdit_2.setText('%s' % y)

        if self.dlg.exec_() == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            x = float(self.dlg.lineEdit.text())
            y = float(self.dlg.lineEdit_2.text())
            self.addFeat(x, y)
            self.tt.setChecked(False)

            QApplication.restoreOverrideCursor()


    def addFeat(self, x, y):
        self.lyr.startEditing()
        feat = QgsFeature()

        if self.lab=='case':
            feat = self.funcs.outattrPrep(self.dlg, self.lyr)
            pnt = QgsGeometry.fromPoint(QgsPoint(x,y))

            if self.lyr.geometryType() == QGis.Point:
                feat.setGeometry(pnt)

            elif self.lyr.geometryType() == QGis.Polygon:
                lyrB = None
                for l in QgsMapLayerRegistry.instance().mapLayers().values():
                    if l.name() == self.dlg.comboBox.currentText():
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
                polyfeat = lyrB.getFeatures(req).next()
                polyg = QgsGeometry(polyfeat.geometry())
                if srid!=3452:
                    tr = QgsCoordinateTransform(srid, 3452)
                    polyg.transform(tr)

                feat.setGeometry(polyg)

            else:
                pass

        elif self.lab=='poi':
            if self.lyr.geometryType() == QGis.Point:
                flds = self.lyr.dataProvider().fields()
                feat.setFields(flds, True)
                feat.setAttribute(feat.fieldNameIndex('localid'), self.dlg.lineEdit_3.text())
                feat.setAttribute(feat.fieldNameIndex('code'), self.dlg.lineEdit_5.text())
                feat.setAttribute(feat.fieldNameIndex('activity'), self.dlg.comboBox.currentText())
                feat.setAttribute(feat.fieldNameIndex('hrid'), self.funcs.hashIDer(QDateTime.currentDateTimeUtc()))

                pnt = QgsGeometry.fromPoint(QgsPoint(x,y))
                feat.setGeometry(pnt)
            else:
                self.iface.messageBar().pushMessage(' ', 'Point layer must be selected!', level=QgsMessageBar.WARNING)

        feat.setValid(True)
        self.lyr.addFeature(feat)
        self.lyr.commitChanges()
        self.lyr.updateExtents()


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
                self.rb.setToGeometry(QgsGeometry.fromPoint(pt), None)
            elif self.pn == 2:
                self.rb.setToGeometry(QgsGeometry.fromPolyline(self.pts), None)
            elif self.pn > 2:
                self.rb.setToGeometry(QgsGeometry.fromPolygon([self.pts]), None)

        elif (event.button()==Qt.RightButton):
            if self.pn > 2:
                self.dlg.label_4.setVisible(False)
                self.dlg.comboBox.setVisible(False)
                self.dlg.label_10.setVisible(False)
                self.dlg.comboBox_5.setVisible(False)

                self.dlg.label.setVisible(False)
                self.dlg.lineEdit.setVisible(False)
                self.dlg.toolButton_3.setVisible(False)
                self.dlg.label_2.setVisible(False)
                self.dlg.lineEdit_2.setVisible(False)

                if self.dlg.exec_() == QDialog.Accepted:
                    QApplication.setOverrideCursor(Qt.WaitCursor)
                    geom = QgsGeometry.fromPolygon([self.pts])
                    self.addFeat(geom)
                    self.tt.setChecked(False)
                    QApplication.restoreOverrideCursor()

                self.pn = 0
                self.pts = []
                self.rb.reset()


    def addFeat(self, geom):
        self.lyr = self.iface.activeLayer()
        self.lyr.startEditing()

        self.feat = self.funcs.outattrPrep(self.dlg, self.lyr)

        self.feat.setGeometry(geom)
        self.feat.setValid(True)
        self.lyr.addFeature(self.feat)
        self.lyr.commitChanges()
        self.lyr.updateExtents()


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

