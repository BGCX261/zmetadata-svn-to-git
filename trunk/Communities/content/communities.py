# -*- coding: utf-8 -*-
#
# File: communities.py
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
from Products.Communities.interfaces.communities import ICommunities
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.Communities.config import *

# additional imports from tagged value 'import'
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Communities_schema = ATFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Communities(ATFolder):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ICommunities, ICommunities)

    meta_type = 'Communities'
    _at_rename_after_creation = True

    schema = Communities_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    security.declarePrivate('manage_beforeDelete')
    def manage_beforeDelete(self, item, container):
        """
        """
        print '1Community_' + item.id
        plone_tool = getToolByName(self, 'plone_utils')
        groups = getToolByName(self, 'portal_groups')
        groupname = 'Community_' + item.id
        groups.removeGroup(groupname,)


registerType(Communities, PROJECTNAME)
# end of class Communities

##code-section module-footer #fill in your manual code here
##/code-section module-footer



