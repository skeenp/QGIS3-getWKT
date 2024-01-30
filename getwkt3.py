# -*- coding: utf-8 -*-
"""
/***************************************************************************
 getwkt3
                                 A QGIS plugin
 This plugin displays the selected features' WKT representation.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-03-13
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Paul Skeen
        email                : paulskeen@spatialecology.com.au
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
import os.path

# Load Core
from qgis.core import QgsMapLayerType, QgsUnitTypes, QgsSettings

# Load PyQt5
from PyQt5.QtCore import QLocale, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QToolButton

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .getwkt3_dialog import getwkt3Dialog
from .getwkt3_config import getwkt3Config

class getwkt3:
    """QGIS Plugin Implementation."""

    s = QgsSettings()

    def __init__(self, iface):
        """Constructor.

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
        self.locale: str = QgsSettings().value("locale/userLocale", QLocale().name())[0:2]
        locale_path: str = os.path.join(self.plugin_dir , "resources" , "i18n" , f"getwkt3_{self.locale}.qm")
        if os.path.exists(self.locale):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)   
        # Create the dialog (after translation) and keep reference
        self.dlg = getwkt3Dialog()
        self.cfg = getwkt3Config()
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Get WKT')
        self.toolbar = self.iface.addToolBar(u'getwkt3')
        self.toolbar.setObjectName(u'getwkt3')

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
        return QCoreApplication.translate('getwkt3', message)


    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=None,
            status_tip=None,
            whats_this=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Toolbar to add action to. Defaults to None.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, self.iface.mainWindow())
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            add_to_toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        # Setup wkt button
        icon_path = ':/plugins/getwkt3/wkt.png'
        self.btn_wkt = self.add_action(
            icon_path,
            text=self.tr(u'Get WKT String'),
            callback=self.run_wkt)
        # Setup ewkt button
        icon_path = ':/plugins/getwkt3/ewkt.png'
        self.btn_ewkt = self.add_action(
            icon_path,
            text=self.tr(u'Get EWKT String'),
            callback=self.run_ewkt)
        # Setup json button
        icon_path = ':/plugins/getwkt3/json.png'
        self.btn_json = self.add_action(
            icon_path,
            text=self.tr(u'Get JSON String'),
            callback=self.run_json)
        # Setup config button
        icon_path = ':/plugins/getwkt3/config.png'
        self.btn_settings = self.add_action(
            icon_path,
            text=self.tr(u'Open Config'),
            callback=self.open_config)
        # Build popup menu
        self.popupMenu = QMenu( self.iface.mainWindow() )
        self.popupMenu.addAction( self.btn_wkt )
        self.popupMenu.addAction( self.btn_ewkt )
        self.popupMenu.addAction( self.btn_json )
        # Setup tll button
        self.toolButton = QToolButton()
        self.toolButton.setMenu( self.popupMenu )
        # Set default button
        self.set_default_button()
        # Set popup mode
        self.toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        #Add widget to toolbar
        self.toolbar.addWidget(self.toolButton)
    
    # Helper function to set default button
    def set_default_button(self):
        if self.s.value("getwkt3/toolmethod") == "EWKT":
            self.toolButton.setDefaultAction(self.btn_ewkt)
        elif self.s.value("getwkt3/toolmethod") == "JSON":
            self.toolButton.setDefaultAction(self.btn_json)
        else:
            self.toolButton.setDefaultAction(self.btn_wkt)
        
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Get WKT'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run_wkt(self):
        """Runs tool to extract WKT"""
        self.run('wkt')

    def run_ewkt(self):
        """Runs tool to extract EWKT"""
        self.run('ewkt')

    def run_json(self):
        """Runs tool to extract JSON"""
        self.run('json')

    def run(self, out_type):
        """Run method that performs all the real work"""
        mc = self.iface.mapCanvas()
        layer = mc.currentLayer()
        if layer is None:
            self.dlg.wktTextEdit.setHtml('<strong style="color:red">'\
            'ERROR:</strong> No selected layer')
        elif layer.type() != QgsMapLayerType.VectorLayer:
            self.dlg.wktTextEdit.setHtml('<strong style="color:red">'\
            'ERROR:</strong> Layer selected is not vector')
        elif layer.selectedFeatureCount() == 0:
            self.dlg.wktTextEdit.setHtml('<strong style="color:red">'\
            'ERROR:</strong> No feature selected')
        elif layer.selectedFeatureCount() > 1:
            self.dlg.wktTextEdit.setHtml('<strong style="color:red">'\
            'ERROR:</strong> More than one feature is selected')
        else:
            feat = layer.selectedFeatures()
            if feat is None:
                self.dlg.wktTextEdit.setHtml('<strong style="color:red">'\
                'ERROR:</strong> No selected features')
            else:
                #Get geom
                geom = feat[0].geometry()
                #Get srid
                try:
                    crs = layer.crs()
                    authid = crs.authid()
                    auth, srid = authid.split(':')
                    if auth != 'EPSG':
                        srid = -1
                except Exception:
                    srid = -1
                #Setup dp for output
                dp_method = self.s.value("getwkt3/dpmethod")
                if dp_method == "custom":
                    try:
                        dp_count = int(self.s.value("getwkt3/dpcustom"))
                    except ValueError:
                        dp_count = None
                elif dp_method == "auto":
                    #Determine crs units
                    crs_units = crs.mapUnits()
                    #Allocate auto dp count based on crs units
                    if crs_units == QgsUnitTypes.DistanceUnit.DistanceFeet:
                        dp_count = 3
                    elif crs_units == QgsUnitTypes.DistanceUnit.DistanceNauticalMiles:
                        dp_count = 8
                    elif crs_units == QgsUnitTypes.DistanceUnit.DistanceYards:
                        dp_count = 3
                    elif crs_units == QgsUnitTypes.DistanceUnit.DistanceMiles:
                        dp_count = 8
                    elif crs_units == QgsUnitTypes.DistanceUnit.DistanceMillimeters:
                        dp_count = 0
                    elif crs_units == QgsUnitTypes.DistanceUnit.DistanceCentimeters:
                        dp_count = 2
                    elif crs_units == QgsUnitTypes.DistanceUnit.DistanceMeters:
                        dp_count = 4
                    elif crs_units == QgsUnitTypes.DistanceUnit.DistanceKilometers:
                        dp_count = 7
                    elif crs_units == QgsUnitTypes.DistanceUnit.DistanceDegrees:
                        dp_count = 8
                    else:
                        dp_count = None
                else:
                    dp_count = None
                #Process export type
                if out_type == 'wkt':
                    wkt = geom.asWkt(dp_count) if not dp_count is None else geom.asWkt()
                    wkt = self.standardise_wkt(wkt)
                    text = wkt
                elif out_type == 'ewkt':
                    wkt = geom.asWkt(dp_count) if not dp_count is None  else geom.asWkt()
                    wkt = self.standardise_wkt(wkt)
                    text = 'SRID={0};{1}'.format(srid, wkt)
                elif out_type == 'json':
                    text = geom.asJson(dp_count) if not dp_count is None  else geom.asJson()
                else:
                    text = '[{0}] Not Implemented'.format(out_type)
                self.dlg.wktTextEdit.setText("{0}".format(text))
        self.dlg.show()
        self.dlg.activateWindow()
        # Run the dialog event loop
        self.dlg.exec_()

    def open_config(self):
        """Opens config menu"""
        self.cfg.show()
        self.cfg.exec_()
        
    def standardise_wkt(self, wkt):
        #Setup standardisers
        standards = {
            "PointZM":"Point Z M",
            "LineStringZM":"LineString Z M",
            "PolygonZM":"Polygon Z M",
            "MultiPointZM":"MultiPoint Z M",
            "MultiLineStringZM":"MultiLineString Z M",
            "MultiPolygonZM":"MultiPolygon Z M",
            "GeometryCollectionZM":"GeometryCollection Z M",
            "CircularStringZM":"CircularString Z M",
            "CompoundCurveZM":"CompoundCurve Z M",
            "CurvePolygonZM":"CurvePolygon Z M",
            "MultiCurveZM":"MultiCurve Z M",
            "MultiSurfaceZM":"MultiSurface Z M",
            "TriangleZM":"Triangle Z M",
            "Point25D":"Point Z",
            "LineString25D":"LineString Z",
            "Polygon25D":"Polygon Z",
            "MultiPoint25D":"MultiPoint Z",
            "MultiLineString25D":"MultiLineString Z",
            "MultiPolygon25D":"MultiPolygon Z",
            "PointZ":"Point Z",
            "LineStringZ":"LineString Z",
            "PolygonZ":"Polygon Z",
            "TriangleZ":"Triangle Z",
            "MultiPointZ":"MultiPoint Z",
            "MultiLineStringZ":"MultiLineString Z",
            "MultiPolygonZ":"MultiPolygon Z",
            "GeometryCollectionZ":"GeometryCollection Z",
            "CircularStringZ":"CircularString Z",
            "CompoundCurveZ":"CompoundCurve Z",
            "CurvePolygonZ":"CurvePolygon Z",
            "MultiCurveZ":"MultiCurve Z",
            "MultiSurfaceZ":"MultiSurface Z",
            "PointM":"Point M",
            "LineStringM":"LineString M",
            "PolygonM":"Polygon M",
            "TriangleM":"Triangle M",
            "MultiPointM":"MultiPoint M",
            "MultiLineStringM":"MultiLineString M",
            "MultiPolygonM":"MultiPolygon M",
            "GeometryCollectionM":"GeometryCollection M",
            "CircularStringM":"CircularString M",
            "CompoundCurveM":"CompoundCurve M",
            "CurvePolygonM":"CurvePolygon M",
            "MultiCurveM":"MultiCurve M",
            "MultiSurfaceM":"MultiSurface M",
            # "Point":"Point",
            # "LineString":"LineString",
            # "Polygon":"Polygon",
            # "Triangle":"Triangle",
            # "MultiPoint":"MultiPoint",
            # "MultiLineString":"MultiLineString",
            # "MultiPolygon":"MultiPolygon",
            # "GeometryCollection":"GeometryCollection",
            # "CircularString":"CircularString",
            # "CompoundCurve":"CompoundCurve",
            # "CurvePolygon":"CurvePolygon",
            # "MultiCurve":"MultiCurve",
            # "MultiSurface":"MultiSurface",
            # "NoGeometry":"NoGeometry",
            # "Unknown":"Unknown",
            }
        #Process all standisers
        for key, value in standards.items():
            wkt = wkt.replace(key,value)
        #Return result
        return wkt