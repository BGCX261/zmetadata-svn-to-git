# -*- coding: utf-8 -*-
#
# File: dcfields.py
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
from Products.Communities.content.fields import Fields
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Communities.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='dc_Contributor',
        widget=StringField._properties['widget'](
            label='Dc_contributor',
            label_msgid='Communities_label_dc_Contributor',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='dc_Type',
        widget=StringField._properties['widget'](
            label='Dc_type',
            label_msgid='Communities_label_dc_Type',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='dc_Format',
        widget=StringField._properties['widget'](
            label='Dc_format',
            label_msgid='Communities_label_dc_Format',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='dc_Identifier',
        widget=StringField._properties['widget'](
            label='Dc_identifier',
            label_msgid='Communities_label_dc_Identifier',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='dc_Source',
        widget=StringField._properties['widget'](
            label='Dc_source',
            label_msgid='Communities_label_dc_Source',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='dc_Relation',
        widget=StringField._properties['widget'](
            label='Dc_relation',
            label_msgid='Communities_label_dc_Relation',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='dc_Rights',
        widget=StringField._properties['widget'](
            label='Dc_rights',
            label_msgid='Communities_label_dc_Rights',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    DateTimeField(
        name='dc_Date',
        widget=DateTimeField._properties['widget'](
            label='Dc_date',
            label_msgid='Communities_label_dc_Date',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

DCFields_schema = getattr(Fields, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class DCFields(Fields):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IDCFields)

    meta_type = 'DCFields'
    _at_rename_after_creation = True

    schema = DCFields_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(DCFields, PROJECTNAME)
# end of class DCFields

##code-section module-footer #fill in your manual code here
##/code-section module-footer



