# -*- coding: utf-8 -*-
"""
/***************************************************************************
 getwkt3Dialog
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
import os

from PyQt5 import uic
from PyQt5 import QtWidgets

from qgis.core import QgsSettings

from PyQt5.QtWidgets import QButtonGroup

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'getwkt3_config_base.ui'))

class getwkt3Config(QtWidgets.QDialog, FORM_CLASS):
    """"Setup variables"""
    s = QgsSettings()
    """Get dialog class"""
    def __init__(self, parent=None):
        """Constructor."""
        super(getwkt3Config, self).__init__(parent)
        self.setupUi(self)
        self.btnAccept.clicked.connect(self.handleHide)
        #Load saved settings
        dpmethod = self.s.value("getwkt3/dpmethod")
        if dpmethod == 'auto':
            self.dp_radAuto.setChecked(True)
        elif dpmethod == 'custom':
            self.dp_radCustom.setChecked(True)
        else:
            self.dp_radDefault.setChecked(True)
        #Custom value
        val = self.s.value("getwkt3/dpcustom")
        if not val:
            val = 10
        self.dp_numCustom.setValue(int(val))
        if dpmethod == 'custom':
            self.dp_numCustom.setEnabled(True)
        else:
            self.dp_numCustom.setEnabled(False)
        # Setup selected default tool
        self.tool_cmbDefault.clear()
        self.tool_cmbDefault.addItems(["WKT", "EWKT", "JSON"])
        tool = self.s.value("getwkt3/toolmethod")
        tool_idx = self.tool_cmbDefault.findText(tool)
        if tool_idx == -1:
            tool_idx = 0
        self.tool_cmbDefault.setCurrentIndex(tool_idx)
        #Multi select support value
        multiselect = self.s.value("getwkt3/multiselect", False, bool)
        self.ms_chkMultiExport.setChecked(multiselect)
        #Load saved settings
        multiselecttype = self.s.value("getwkt3/multiselecttype")
        if multiselecttype == 'multi':
            self.ms_radMulti.setChecked(True)
        elif multiselecttype == 'collection':
            self.ms_radGeomCollection.setChecked(True)
        if multiselect:
            self.ms_radMulti.setEnabled(True)
            self.ms_radMulti.setEnabled(True)
        else:
            self.ms_radMulti.setEnabled(False)
            self.ms_radMulti.setEnabled(False)
        #SRID value
        val = self.s.value("getwkt3/srid")
        if not val:
            val = -1
        self.srs_intOutSrs.setText(str(val))
        #Connect events
        self.dp_radDefault.clicked.connect(self.dp_handleChange_Default)
        self.dp_radAuto.clicked.connect(self.dp_handleChange_Auto)
        self.dp_radCustom.clicked.connect(self.dp_handleChange_Custom)
        self.dp_numCustom.valueChanged.connect(self.dp_handleChange_CustomValue)
        self.tool_cmbDefault.currentIndexChanged.connect(self.tool_handleDefaultChange)
        self.ms_chkMultiExport.stateChanged.connect(self.ms_handleMultiSelectChange)
        self.ms_radMulti.clicked.connect(self.ms_handleChange_Multi)
        self.ms_radGeomCollection.clicked.connect(self.ms_handleChange_GeomCollection)
        self.srs_intOutSrs.textChanged.connect(self.srs_handleChange_SRID)

    def setupUi(self, Dialog):
        # Call the original setupUi method
        super(getwkt3Config, self).setupUi(Dialog)
        # Create button groups
        self.setupButtonGroups()
 
    def setupButtonGroups(self):
        # Create button group for dp methods
        self.dp_buttongroup = QButtonGroup(self)
        self.dp_buttongroup.addButton(self.dp_radDefault)
        self.dp_buttongroup.addButton(self.dp_radAuto)
        self.dp_buttongroup.addButton(self.dp_radCustom)
        # Create button group for multi select methods
        self.ms_buttongroup = QButtonGroup(self)
        self.ms_buttongroup.addButton(self.ms_radMulti)
        self.ms_buttongroup.addButton(self.ms_radGeomCollection)
    
    def handleHide(self):
        """Hide handle"""
        self.hide()

    def tool_handleDefaultChange(self, value):
        """Handle change to tool default method"""
        #Update dp setting
        self.s.setValue("getwkt3/toolmethod", self.tool_cmbDefault.currentText())
    
    def dp_handleChange(self, t):
        """Handle change to dp method"""
        #Update dp setting
        self.s.setValue("getwkt3/dpmethod", t)

    def dp_handleChange_Default(self):
        """Handle change to dp method to default"""
        #Update dp setting
        self.dp_handleChange('default')
        self.dp_numCustom.setEnabled(False)
    
    def dp_handleChange_Auto(self):
        """Handle change to dp method to auto"""
        #Update dp setting
        self.dp_handleChange('auto')
        self.dp_numCustom.setEnabled(False)

    def dp_handleChange_Custom(self):
        """Handle change to dp method to custom"""
        #Update dp setting
        self.dp_handleChange('custom')
        self.dp_numCustom.setEnabled(True)

    def dp_handleChange_CustomValue(self):
        """Handle change to dp custom value"""
        #Update dp setting
        value = self.dp_numCustom.value()
        self.s.setValue("getwkt3/dpcustom",value)
        
    def ms_handleMultiSelectChange(self, state):
        """Handle change to multi-selection export option"""
        ms_enabled = bool(state)
        # Update multi export setting
        self.s.setValue("getwkt3/multiselect", ms_enabled)
        # Enable or disable the radio buttons based on the state
        self.ms_radGeomCollection.setEnabled(ms_enabled)
        self.ms_radMulti.setEnabled(ms_enabled)
        
    def ms_handleChange(self, t):
        """Handle change to dp method"""
        #Update dp setting
        self.s.setValue("getwkt3/multiselecttype", t)

    def ms_handleChange_Multi(self):
        """Handle change to dp method to default"""
        #Update dp setting
        self.ms_handleChange('multi')
    
    def ms_handleChange_GeomCollection(self):
        """Handle change to dp method to auto"""
        #Update dp setting
        self.ms_handleChange('collection')
        
    def srs_handleChange_SRID(self):
        """Handle change to srs SRID value"""
        #Update dp setting
        value = self.srs_intOutSrs.text()
        value = value.replace('EPSG', '').replace(':', '').replace(' ', '')
        try:
            value = int(value)
        except ValueError:
            value = -1
        self.s.setValue("getwkt3/srid",value)