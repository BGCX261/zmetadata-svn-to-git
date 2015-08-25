# -*- coding: utf-8 -*-
#
# File: iso19115.py
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
from Products.Communities.content.setup import STDSetup
from Products.Communities.content.iso19115Fields import ISO19115Fields
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Communities.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ISO19115Setup_schema = BaseSchema.copy() + \
    getattr(STDSetup, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class ISO19115Setup(STDSetup, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IISO19115Setup)

    meta_type = 'ISO19115Setup'
    _at_rename_after_creation = True

    schema = ISO19115Setup_schema

    ##code-section class-header #fill in your manual code here
    _Fields = ISO19115Fields
    ##/code-section class-header

    # Methods


registerType(ISO19115Setup, PROJECTNAME)
# end of class ISO19115Setup

##code-section module-footer #fill in your manual code here
##/code-section module-footer



