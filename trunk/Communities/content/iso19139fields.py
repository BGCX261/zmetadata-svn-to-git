# -*- coding: utf-8 -*-
#
# File: iso19139fields.py
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
        name='iso19139_DatasetResponsibleParty',
        widget=StringField._properties['widget'](
            label="Dataset Responsible Party",
            label_msgid='Communities_label_iso19139_DatasetResponsibleParty',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_DatasetResponsiblePartyOrganization',
        widget=StringField._properties['widget'](
            label="Dataset Responsible Party Organization",
            label_msgid='Communities_label_iso19139_DatasetResponsiblePartyOrganization',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_DatasetResponsiblePartyPosition',
        widget=StringField._properties['widget'](
            label="Dataset Responsible Party Position",
            label_msgid='Communities_label_iso19139_DatasetResponsiblePartyPosition',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_DatasetCharacterSet',
        widget=StringField._properties['widget'](
            label="Dataset Character Set",
            label_msgid='Communities_label_iso19139_DatasetCharacterSet',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_DatasetTopicCategory',
        widget=StringField._properties['widget'](
            label="Dataset Topic Category",
            label_msgid='Communities_label_iso19139_DatasetTopicCategory',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_DatasetScale',
        widget=StringField._properties['widget'](
            label="Dataset Scale",
            label_msgid='Communities_label_iso19139_DatasetScale',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_DatasetFormatName',
        widget=StringField._properties['widget'](
            label="Dataset Format Name",
            label_msgid='Communities_label_iso19139_DatasetFormatName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_DatasetFormatVersion',
        widget=StringField._properties['widget'](
            label="Dataset Format Version",
            label_msgid='Communities_label_iso19139_DatasetFormatVersion',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    DateTimeField(
        name='iso19139_SpatialBeginDate',
        widget=DateTimeField._properties['widget'](
            label="Spatial Begin Date",
            label_msgid='Communities_label_iso19139_SpatialBeginDate',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    DateTimeField(
        name='iso19139_SpatialEndDate',
        widget=DateTimeField._properties['widget'](
            label="Spatial End Date",
            label_msgid='Communities_label_iso19139_SpatialEndDate',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_SpatialVerticalExtentMinimum',
        widget=StringField._properties['widget'](
            label="Spatial Vertical Extent Minimum",
            label_msgid='Communities_label_iso19139_SpatialVerticalExtentMinimum',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_SpatialMaximum',
        widget=StringField._properties['widget'](
            label="Spatial Maximum",
            label_msgid='Communities_label_iso19139_SpatialMaximum',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_SpatialVerticalExtentUnits',
        widget=StringField._properties['widget'](
            label="Spatial Vertical Extent Units",
            label_msgid='Communities_label_iso19139_SpatialVerticalExtentUnits',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_SpatialVerticalExtentDatum',
        widget=StringField._properties['widget'](
            label="Spatial Vertical Extent Datum",
            label_msgid='Communities_label_iso19139_SpatialVerticalExtentDatum',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_SpatialRepresentation',
        widget=StringField._properties['widget'](
            label="Spatial Representation",
            label_msgid='Communities_label_iso19139_SpatialRepresentation',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_SpatialReferenceSystem',
        widget=StringField._properties['widget'](
            label="Spatial Reference System",
            label_msgid='Communities_label_iso19139_SpatialReferenceSystem',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_SpatialLinageStatement',
        widget=StringField._properties['widget'](
            label="Spatial Linage Statement",
            label_msgid='Communities_label_iso19139_SpatialLinageStatement',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_SpatialOnlineResourceURL',
        widget=StringField._properties['widget'](
            label="Spatial Online Resource URL",
            label_msgid='Communities_label_iso19139_SpatialOnlineResourceURL',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_SpatialOnlineResourceProtocol',
        widget=StringField._properties['widget'](
            label="Spatial Online Resource Protocol",
            label_msgid='Communities_label_iso19139_SpatialOnlineResourceProtocol',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_SpatialOnlineResourceName',
        widget=StringField._properties['widget'](
            label="Spatial Online Resource Name",
            label_msgid='Communities_label_iso19139_SpatialOnlineResourceName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_SpatialOnlineResourceDescription',
        widget=StringField._properties['widget'](
            label="Spatial Online Resource Description",
            label_msgid='Communities_label_iso19139_SpatialOnlineResourceDescription',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_MetadataFileIdentifier',
        widget=StringField._properties['widget'](
            label="Metadata File Identifier",
            label_msgid='Communities_label_iso19139_MetadataFileIdentifier',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_MetadataStandardName',
        widget=StringField._properties['widget'](
            label="Metadata Standard Name",
            label_msgid='Communities_label_iso19139_MetadataStandardName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_MetadataStandardVersion',
        widget=StringField._properties['widget'](
            label="Metadata Standard Version",
            label_msgid='Communities_label_iso19139_MetadataStandardVersion',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_MetadataLanguage',
        widget=StringField._properties['widget'](
            label="Metadata Language",
            label_msgid='Communities_label_iso19139_MetadataLanguage',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_MetadataCharacterSet',
        widget=StringField._properties['widget'](
            label="Metadata Character Set",
            label_msgid='Communities_label_iso19139_MetadataCharacterSet',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_MetadataTimeStamp',
        widget=StringField._properties['widget'](
            label="Metadata Time Stamp",
            label_msgid='Communities_label_iso19139_MetadataTimeStamp',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_MetadataPointOfContactIndividualName',
        widget=StringField._properties['widget'](
            label="Metadata Point Of Contact Individual Name",
            label_msgid='Communities_label_iso19139_MetadataPointOfContactIndividualName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_MetadataPointOfContactOrganizationName',
        widget=StringField._properties['widget'](
            label="Metadata Point Of Contact Organization Name",
            label_msgid='Communities_label_iso19139_MetadataPointOfContactOrganizationName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_MetadataPointOfContactPositionName',
        widget=StringField._properties['widget'](
            label="Metadata Point Of Contact Position Name",
            label_msgid='Communities_label_iso19139_MetadataPointOfContactPositionName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='iso19139_MetadataPointOfContactRole',
        widget=StringField._properties['widget'](
            label="Metadata Point Of Contact Role",
            label_msgid='Communities_label_iso19139_MetadataPointOfContactRole',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ISO19139Fields_schema = getattr(Fields, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class ISO19139Fields(Fields):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IISO19139Fields)

    meta_type = 'ISO19139Fields'
    _at_rename_after_creation = True

    schema = ISO19139Fields_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(ISO19139Fields, PROJECTNAME)
# end of class ISO19139Fields

##code-section module-footer #fill in your manual code here
##/code-section module-footer



