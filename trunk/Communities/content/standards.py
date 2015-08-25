# -*- coding: utf-8 -*-
#
# File: standards.py
#
# Copyright (c) 2009 by []
# Generator: ArchGenXML Version 2.2
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
from Products.Communities.interfaces.standards import IStandardsSetup
from Products.Communities.content.standardfields import CommonFields
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.Communities.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    LinesField(
        name='showFields',
        widget=MultiSelectionWidget(
            format="checkbox",
            label='Showfields',
            label_msgid='Communities_label_showFields',
            i18n_domain='Communities',
        ),
        vocabulary="getMyFields",
        searchable=1,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CommonSetup_schema = ATFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class CommonSetup(ATFolder):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ICommonSetup, IStandardsSetup)

    meta_type = 'CommonSetup'
    _at_rename_after_creation = True

    schema = CommonSetup_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getMyFields')
    def getMyFields(self):
        """
        """
        names = []
        for field in self['fields'].schema.fields():
            print field.schemata
            if (field.schemata != 'categorization') and \
               (field.schemata != 'metadata') and \
               (field.getName() not in ('id', 'title', 'description')):
                names += [field.getName()]
        return names

    security.declarePublic('_renameAfterCreation')
    def _renameAfterCreation(self,check_auto_id=True):
        """
        """
        self._setObject("fields", CommonFields("fields"))
        self["fields"].setTitle("Common Standard Fields Setup")
        self["fields"].reindexObject()


registerType(CommonSetup, PROJECTNAME)
# end of class CommonSetup

##code-section module-footer #fill in your manual code here
##/code-section module-footer



