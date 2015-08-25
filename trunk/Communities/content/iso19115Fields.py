# -*- coding: utf-8 -*-
#
# File: iso19115Fields.py
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
        name='iso19115_DatasetResponsibleParty',
        widget=StringField._properties['widget'](
            label="Dataset Responsible Party",
            label_msgid='Communities_label_iso19115_DatasetResponsibleParty',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_DatasetResponsiblePartyOrganization',
        widget=StringField._properties['widget'](
            label="Dataset Responsible Party Organization",
            label_msgid='Communities_label_iso19115_DatasetResponsiblePartyOrganization',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_DatasetResponsiblePartyPosition',
        widget=StringField._properties['widget'](
            label="Dataset Responsible Party Position",
            label_msgid='Communities_label_iso19115_DatasetResponsiblePartyPosition',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_DatasetCharacterSet',
        widget=StringField._properties['widget'](
            label="Dataset Character Set",
            label_msgid='Communities_label_iso19115_DatasetCharacterSet',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_DatasetTopicCategory',
        widget=StringField._properties['widget'](
            label="Dataset Topic Category",
            label_msgid='Communities_label_iso19115_DatasetTopicCategory',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_DatasetScale',
        widget=StringField._properties['widget'](
            label="Dataset Scale",
            label_msgid='Communities_label_iso19115_DatasetScale',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_DatasetFormatName',
        widget=StringField._properties['widget'](
            label="Dataset Format Name",
            label_msgid='Communities_label_iso19115_DatasetFormatName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_DatasetFormatVersion',
        widget=StringField._properties['widget'](
            label="Dataset Format Version",
            label_msgid='Communities_label_iso19115_DatasetFormatVersion',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    DateTimeField(
        name='iso19115_SpatialBeginDate',
        widget=DateTimeField._properties['widget'](
            label="Spatial Begin Date",
            label_msgid='Communities_label_iso19115_SpatialBeginDate',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    DateTimeField(
        name='iso19115_SpatialEndDate',
        widget=DateTimeField._properties['widget'](
            label="Spatial End Date",
            label_msgid='Communities_label_iso19115_SpatialEndDate',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_SpatialVerticalExtentMinimum',
        widget=StringField._properties['widget'](
            label="Spatial Vertical Extent Minimum",
            label_msgid='Communities_label_iso19115_SpatialVerticalExtentMinimum',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_SpatialMaximum',
        widget=StringField._properties['widget'](
            label="Spatial Maximum",
            label_msgid='Communities_label_iso19115_SpatialMaximum',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_SpatialVerticalExtentUnits',
        widget=StringField._properties['widget'](
            label="Spatial Vertical Extent Units",
            label_msgid='Communities_label_iso19115_SpatialVerticalExtentUnits',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_SpatialVerticalExtentDatum',
        widget=StringField._properties['widget'](
            label="Spatial Vertical Extent Datum",
            label_msgid='Communities_label_iso19115_SpatialVerticalExtentDatum',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_SpatialRepresentation',
        widget=StringField._properties['widget'](
            label="Spatial Representation",
            label_msgid='Communities_label_iso19115_SpatialRepresentation',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_SpatialReferenceSystem',
        widget=StringField._properties['widget'](
            label="Spatial Reference System",
            label_msgid='Communities_label_iso19115_SpatialReferenceSystem',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_SpatialLinageStatement',
        widget=StringField._properties['widget'](
            label="Spatial Linage Statement",
            label_msgid='Communities_label_iso19115_SpatialLinageStatement',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_SpatialOnlineResourceURL',
        widget=StringField._properties['widget'](
            label="Spatial Online Resource URL",
            label_msgid='Communities_label_iso19115_SpatialOnlineResourceURL',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_SpatialOnlineResourceProtocol',
        widget=StringField._properties['widget'](
            label="Spatial Online Resource Protocol",
            label_msgid='Communities_label_iso19115_SpatialOnlineResourceProtocol',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_SpatialOnlineResourceName',
        widget=StringField._properties['widget'](
            label="Spatial Online Resource Name",
            label_msgid='Communities_label_iso19115_SpatialOnlineResourceName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_SpatialOnlineResourceDescription',
        widget=StringField._properties['widget'](
            label="Spatial Online Resource Description",
            label_msgid='Communities_label_iso19115_SpatialOnlineResourceDescription',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_MetadataFileIdentifier',
        widget=StringField._properties['widget'](
            label="Metadata File Identifier",
            label_msgid='Communities_label_iso19115_MetadataFileIdentifier',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_MetadataStandardName',
        widget=StringField._properties['widget'](
            label="Metadata Standard Name",
            label_msgid='Communities_label_iso19115_MetadataStandardName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_MetadataStandardVersion',
        widget=StringField._properties['widget'](
            label="Metadata Standard Version",
            label_msgid='Communities_label_iso19115_MetadataStandardVersion',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_MetadataLanguage',
        widget=StringField._properties['widget'](
            label="Metadata Language",
            label_msgid='Communities_label_iso19115_MetadataLanguage',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_MetadataCharacterSet',
        widget=StringField._properties['widget'](
            label="Metadata Character Set",
            label_msgid='Communities_label_iso19115_MetadataCharacterSet',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_MetadataTimeStamp',
        widget=StringField._properties['widget'](
            label="Metadata Time Stamp",
            label_msgid='Communities_label_iso19115_MetadataTimeStamp',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_MetadataPointOfContactIndividualName',
        widget=StringField._properties['widget'](
            label="Metadata Point Of Contact Individual Name",
            label_msgid='Communities_label_iso19115_MetadataPointOfContactIndividualName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_MetadataPointOfContactOrganizationName',
        widget=StringField._properties['widget'](
            label="Metadata Point Of Contact Organization Name",
            label_msgid='Communities_label_iso19115_MetadataPointOfContactOrganizationName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_MetadataPointOfContactPositionName',
        widget=StringField._properties['widget'](
            label="Metadata Point Of Contact Position Name",
            label_msgid='Communities_label_iso19115_MetadataPointOfContactPositionName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19115_MetadataPointOfContactRole',
        widget=StringField._properties['widget'](
            label="Metadata Point Of Contact Role",
            label_msgid='Communities_label_iso19115_MetadataPointOfContactRole',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ISO19115Fields_schema = getattr(Fields, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class ISO19115Fields(Fields):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IISO19115Fields)

    meta_type = 'ISO19115Fields'
    _at_rename_after_creation = True

    schema = ISO19115Fields_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(ISO19115Fields, PROJECTNAME)
# end of class ISO19115Fields

##code-section module-footer #fill in your manual code here
##/code-section module-footer



