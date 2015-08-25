# -*- coding: utf-8 -*-
#
# File: StandardSetup.py
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
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Communities.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

StandardSetup_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class StandardSetup(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IStandardSetup)

    meta_type = 'StandardSetup'
    _at_rename_after_creation = True

    schema = StandardSetup_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(StandardSetup, PROJECTNAME)
# end of class StandardSetup

##code-section module-footer #fill in your manual code here
##/code-section module-footer



