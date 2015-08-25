# -*- coding: utf-8 -*-
#
# File: sansstandard.py
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
from Products.Communities.interfaces.standards import IStandardMarker
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Communities.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    LinesField(
        name='redneredFields',
        widget=LinesField._properties['widget'](
            label='Redneredfields',
            label_msgid='Communities_label_redneredFields',
            i18n_domain='Communities',
        ),
    ),
    BooleanField(
        name='active',
        widget=BooleanField._properties['widget'](
            label='Active',
            label_msgid='Communities_label_active',
            i18n_domain='Communities',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

SANSSetup_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class SANSSetup(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ISANSSetup, IStandardMarker)

    meta_type = 'SANSSetup'
    _at_rename_after_creation = True

    schema = SANSSetup_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(SANSSetup, PROJECTNAME)
# end of class SANSSetup

##code-section module-footer #fill in your manual code here
##/code-section module-footer



