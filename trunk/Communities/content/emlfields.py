# -*- coding: utf-8 -*-
#
# File: emlfields.py
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
        name='eml_DataOwnerSalutation',
        widget=StringField._properties['widget'](
            label='Eml_dataownersalutation',
            label_msgid='Communities_label_eml_DataOwnerSalutation',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='eml_DataOwnerGivenName',
        widget=StringField._properties['widget'](
            label='Eml_dataownergivenname',
            label_msgid='Communities_label_eml_DataOwnerGivenName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='eml_DataOwnerSurname',
        widget=StringField._properties['widget'](
            label='Eml_dataownersurname',
            label_msgid='Communities_label_eml_DataOwnerSurname',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    DateTimeField(
        name='eml_TemporalCoverageBeginDate',
        widget=DateTimeField._properties['widget'](
            label='Eml_temporalcoveragebegindate',
            label_msgid='Communities_label_eml_TemporalCoverageBeginDate',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    DateTimeField(
        name='eml_TemporalCoverageEndDate',
        widget=DateTimeField._properties['widget'](
            label='Eml_temporalcoverageenddate',
            label_msgid='Communities_label_eml_TemporalCoverageEndDate',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='eml_TaxonomicCoverageRankName',
        widget=StringField._properties['widget'](
            label='Eml_taxonomiccoveragerankname',
            label_msgid='Communities_label_eml_TaxonomicCoverageRankName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='eml_ContactSalutation',
        widget=StringField._properties['widget'](
            label='Eml_contactsalutation',
            label_msgid='Communities_label_eml_ContactSalutation',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='eml_ContactGivenName',
        widget=StringField._properties['widget'](
            label='Eml_contactgivenname',
            label_msgid='Communities_label_eml_ContactGivenName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='eml_ContactSurname',
        widget=StringField._properties['widget'](
            label='Eml_contactsurname',
            label_msgid='Communities_label_eml_ContactSurname',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='eml_ContactOrganizationName',
        widget=StringField._properties['widget'](
            label='Eml_contactorganizationname',
            label_msgid='Communities_label_eml_ContactOrganizationName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

EMLFields_schema = getattr(Fields, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class EMLFields(Fields):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IEMLFields)

    meta_type = 'EMLFields'
    _at_rename_after_creation = True

    schema = EMLFields_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(EMLFields, PROJECTNAME)
# end of class EMLFields

##code-section module-footer #fill in your manual code here
##/code-section module-footer



