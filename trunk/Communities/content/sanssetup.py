# -*- coding: utf-8 -*-
#
# File: sanssetup.py
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
from Products.Communities.content.sansfields import SANSFields
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Communities.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

SANSSetup_schema = BaseSchema.copy() + \
    getattr(STDSetup, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class SANSSetup(STDSetup, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ISANSSetup)

    meta_type = 'SANSSetup'
    _at_rename_after_creation = True

    schema = SANSSetup_schema

    ##code-section class-header #fill in your manual code here
    _Fields = SANSFields
    ##/code-section class-header

    # Methods


registerType(SANSSetup, PROJECTNAME)
# end of class SANSSetup

##code-section module-footer #fill in your manual code here
##/code-section module-footer



