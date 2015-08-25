# -*- coding: utf-8 -*-
#
# File: standardfields.py
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
        name='common_Title',
        widget=StringField._properties['widget'](
            label="Title",
            label_msgid='Communities_label_common_Title',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    DateTimeField(
        name='common_Date',
        widget=DateTimeField._properties['widget'](
            label="Date",
            label_msgid='Communities_label_common_Date',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='common_Keywords',
        widget=KeywordWidget(
            label='Common_keywords',
            label_msgid='Communities_label_common_Keywords',
            i18n_domain='Communities',
        ),
        vocabulary=qqqq,
        searchable=1,
    ),
    StringField(
        name='common_Abstract',
        widget=StringField._properties['widget'](
            label='Common_abstract',
            label_msgid='Communities_label_common_Abstract',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='common_Organization',
        widget=StringField._properties['widget'](
            label='Common_organization',
            label_msgid='Communities_label_common_Organization',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='common_Bounds',
        widget=StringField._properties['widget'](
            label='Common_bounds',
            label_msgid='Communities_label_common_Bounds',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='common_Language',
        widget=StringField._properties['widget'](
            label='Common_language',
            label_msgid='Communities_label_common_Language',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CommonFields_schema = getattr(Fields, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class CommonFields(Fields):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ICommonFields)

    meta_type = 'CommonFields'
    _at_rename_after_creation = True

    schema = CommonFields_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(CommonFields, PROJECTNAME)
# end of class CommonFields

##code-section module-footer #fill in your manual code here
##/code-section module-footer



