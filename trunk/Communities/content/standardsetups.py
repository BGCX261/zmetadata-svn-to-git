# -*- coding: utf-8 -*-
#
# File: standardsetups.py
#
# Copyright (c) 2009 by []
# Generator: ArchGenXML Version 2.3
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope import interface
from zope.interface import implements
import interfaces
from Products.Communities.interfaces.standardsetups import IStandardSetups
from Products.Communities.content.dc import DCSetup
from Products.Communities.content.eml import EMLSetup
from Products.Communities.content.iso19115 import ISO19115Setup
from Products.Communities.content.iso19139 import ISO19139Setup
from Products.Communities.content.commonsetup import CommonSetup
from Products.Communities.content.sanssetup import SANSSetup
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.Communities.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    LinesField(
        name='showStandards',
        widget=MultiSelectionWidget(
            format="checkbox",
            label='Showstandards',
            label_msgid='Communities_label_showStandards',
            i18n_domain='Communities',
        ),
        vocabulary="getMyStandards",
        searchable=1,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

StandardSetups_schema = ATFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class StandardSetups(ATFolder):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IStandardSetups, IStandardSetups)

    meta_type = 'StandardSetups'
    _at_rename_after_creation = True

    schema = StandardSetups_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('_renameAfterCreation')
    def _renameAfterCreation(self, check_auto_id=True):
        """"""
        self._setObject("COMMON", CommonSetup("COMMON"))
        self["COMMON"].setTitle("Common")
        self['COMMON']._renameAfterCreation(check_auto_id)
        self['COMMON']._setupFields()
        self["COMMON"].reindexObject()

        self._setObject("SANS1878", SANSSetup("SANS1878"))
        self["SANS1878"].setTitle("SANS1878")
        self['SANS1878']._renameAfterCreation(check_auto_id)
        self['SANS1878']._setupFields()
        self["SANS1878"].reindexObject()

        self._setObject("ISO19139", ISO19139Setup("ISO19139"))
        self["ISO19139"].setTitle("ISO19139")
        self['ISO19139']._renameAfterCreation(check_auto_id)
        self['ISO19139']._setupFields()
        self["ISO19139"].reindexObject()

        self._setObject("ISO19115", ISO19115Setup("ISO19115"))
        self["ISO19115"].setTitle("ISO19115")
        self['ISO19115']._renameAfterCreation(check_auto_id)
        self['ISO19115']._setupFields()
        self["ISO19115"].reindexObject()

        self._setObject("EML", EMLSetup("EML"))
        self["EML"].setTitle("EML")
        self['EML']._renameAfterCreation(check_auto_id)
        self['EML']._setupFields()
        self["EML"].reindexObject()

        self._setObject("DublinCore", DCSetup("DublinCore"))
        self["DublinCore"].setTitle("DublinCore")
        self['DublinCore']._renameAfterCreation(check_auto_id)
        self['DublinCore']._setupFields()
        self["DublinCore"].reindexObject()

    security.declarePublic('getMyStandards')
    def getMyStandards(self):
        """
        """
        return self.objectIds()


registerType(StandardSetups, PROJECTNAME)
# end of class StandardSetups

##code-section module-footer #fill in your manual code here
##/code-section module-footer



