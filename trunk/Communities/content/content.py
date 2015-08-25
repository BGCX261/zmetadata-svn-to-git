# -*- coding: utf-8 -*-
#
# File: content.py
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
from Products.Communities.interfaces.content import IContent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.Communities.config import *

# additional imports from tagged value 'import'
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

##code-section module-header #fill in your manual code here
from Products.ATContentTypes.content.topic import ATTopic
##/code-section module-header

schema = Schema()


##code-section after-local-schema #fill in your manual code here\
import transaction
##/code-section after-local-schema

Content_schema = ATFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Content(ATFolder):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IContent, IContent)

    meta_type = 'Content'
    _at_rename_after_creation = True

    schema = Content_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(Content, PROJECTNAME)
# end of class Content

##code-section module-footer #fill in your manual code here
##/code-section module-footer




