# -*- coding: utf-8 -*-
#
# File: MetadataContainer.py
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
from zope.interface import implements
import interfaces
from Globals import package_home
import time
from datetime import datetime


from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.Communities.config import *
from Products.ZMetadata import Global

##code-section module-header #fill in your manual code here
from Products.ATContentTypes.content.topic import ATTopic
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

MetadataContainer_schema = ATFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class MetadataContainer(ATFolder):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IMetadataContainer)

    meta_type = 'MetadataContainer'
    _at_rename_after_creation = True

    schema = MetadataContainer_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    security.declarePublic('_renameAfterCreation')
    def _renameAfterCreation(self, check_auto_id=True):
        """"""
        self._setObject("content", ATTopic("content"))
        self['content'].setTitle("Content")
        self['content'].addCriterion('Type', 'ATPortalTypeCriterion')
        self['content'].crit__Type_ATPortalTypeCriterion.setValue(['Metadata', 'MetadataContainer'])
        self['content'].addCriterion('path', 'ATRelativePathCriterion')
        self['content'].setCustomView(True)
        self['content'].setCustomViewFields(['Title', 'ModificationDate', 'review_state', 'CreationDate', 'Type'])
        self.portal_workflow.doActionFor(self['content'], "publish", comment="")        
        self.setDefaultPage('content')

registerType(MetadataContainer, PROJECTNAME)
# end of class MetadataContainer

##code-section module-footer #fill in your manual code here
##/code-section module-footer



