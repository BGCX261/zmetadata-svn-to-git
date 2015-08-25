# -*- coding: utf-8 -*-
#
# File: iso1939fields.py
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
from Products.Communities.content.iso19139fields import ISO19139Fields
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Communities.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ISO19139Setup_schema = BaseSchema.copy() + \
    getattr(STDSetup, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class ISO19139Setup(STDSetup, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IISO19139Setup)

    meta_type = 'ISO19139Setup'
    _at_rename_after_creation = True

    schema = ISO19139Setup_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(ISO19139Setup, PROJECTNAME)
# end of class ISO19139Setup

##code-section module-footer #fill in your manual code here
##/code-section module-footer



