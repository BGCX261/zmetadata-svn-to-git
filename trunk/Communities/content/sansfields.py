# -*- coding: utf-8 -*-
#
# File: sansfields.py
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
        name='sans1878_DatasetResponsibleParty',
        widget=StringField._properties['widget'](
            label="Dataset Responsible Party",
            label_msgid='Communities_label_sans1878_DatasetResponsibleParty',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_DatasetResponsiblePartyOrganization',
        widget=StringField._properties['widget'](
            label="Dataset Responsible Party Organization",
            label_msgid='Communities_label_sans1878_DatasetResponsiblePartyOrganization',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_DatasetResponsiblePartyPosition',
        widget=StringField._properties['widget'](
            label="Dataset Responsible Party Position",
            label_msgid='Communities_label_sans1878_DatasetResponsiblePartyPosition',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_DatasetCharacterSet',
        widget=StringField._properties['widget'](
            label="Dataset Language",
            label_msgid='Communities_label_sans1878_DatasetCharacterSet',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_DatasetTopicCategory',
        widget=StringField._properties['widget'](
            label="Dataset Topic Category",
            label_msgid='Communities_label_sans1878_DatasetTopicCategory',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_DatasetScale',
        widget=StringField._properties['widget'](
            label="Dataset Scale",
            label_msgid='Communities_label_sans1878_DatasetScale',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_DatasetFormatName',
        widget=StringField._properties['widget'](
            label="Dataset Format Name",
            label_msgid='Communities_label_sans1878_DatasetFormatName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_DatasetFormatVersion',
        widget=StringField._properties['widget'](
            label="Dataset Format Version",
            label_msgid='Communities_label_sans1878_DatasetFormatVersion',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    DateTimeField(
        name='sans1878_SpatialBeginDate',
        widget=DateTimeField._properties['widget'](
            label="Spatial Begin Date",
            label_msgid='Communities_label_sans1878_SpatialBeginDate',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    DateTimeField(
        name='sans1878_SpatialEndDate',
        widget=DateTimeField._properties['widget'](
            label="Spatial End Date",
            label_msgid='Communities_label_sans1878_SpatialEndDate',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_SpatialVerticalExtentMinimum',
        widget=StringField._properties['widget'](
            label="Spatial Vertical Extent Minimum",
            label_msgid='Communities_label_sans1878_SpatialVerticalExtentMinimum',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_SpatialMaximum',
        widget=StringField._properties['widget'](
            label="Spatial Maximum",
            label_msgid='Communities_label_sans1878_SpatialMaximum',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_SpatialVerticalExtentUnits',
        widget=StringField._properties['widget'](
            label="Spatial Vertical Extent Units",
            label_msgid='Communities_label_sans1878_SpatialVerticalExtentUnits',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_SpatialVerticalExtentDatum',
        widget=StringField._properties['widget'](
            label="Spatial Vertical Extent Datum",
            label_msgid='Communities_label_sans1878_SpatialVerticalExtentDatum',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_SpatialRepresentation',
        widget=StringField._properties['widget'](
            label="Spatial Representation",
            label_msgid='Communities_label_sans1878_SpatialRepresentation',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_SpatialReferenceSystem',
        widget=StringField._properties['widget'](
            label="Spatial Reference System",
            label_msgid='Communities_label_sans1878_SpatialReferenceSystem',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_SpatialLinageStatement',
        widget=StringField._properties['widget'](
            label="Spatial Linage Statement",
            label_msgid='Communities_label_sans1878_SpatialLinageStatement',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_SpatialOnlineResourceURL',
        widget=StringField._properties['widget'](
            label="Spatial Online Resource URL",
            label_msgid='Communities_label_sans1878_SpatialOnlineResourceURL',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_SpatialOnlineResourceProtocol',
        widget=StringField._properties['widget'](
            label="Spatial Online Resource Protocol",
            label_msgid='Communities_label_sans1878_SpatialOnlineResourceProtocol',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_SpatialOnlineResourceName',
        widget=StringField._properties['widget'](
            label="Spatial Online Resource Name",
            label_msgid='Communities_label_sans1878_SpatialOnlineResourceName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_SpatialOnlineResourceDescription',
        widget=StringField._properties['widget'](
            label="Spatial Online Resource Description",
            label_msgid='Communities_label_sans1878_SpatialOnlineResourceDescription',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_MetadataFileIdentifier',
        widget=StringField._properties['widget'](
            label="Metadata File Identifier",
            label_msgid='Communities_label_sans1878_MetadataFileIdentifier',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_MetadataStandardName',
        widget=StringField._properties['widget'](
            label="Metadata Standard Name",
            label_msgid='Communities_label_sans1878_MetadataStandardName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_MetadataStandardVersion',
        widget=StringField._properties['widget'](
            label="Metadata Standard Version",
            label_msgid='Communities_label_sans1878_MetadataStandardVersion',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_MetadataLanguage',
        widget=StringField._properties['widget'](
            label="Metadata Language",
            label_msgid='Communities_label_sans1878_MetadataLanguage',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_MetadataCharacterSet',
        widget=StringField._properties['widget'](
            label="Metadata Character Set",
            label_msgid='Communities_label_sans1878_MetadataCharacterSet',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_MetadataTimeStamp',
        widget=StringField._properties['widget'](
            label="Metadata Time Stamp",
            label_msgid='Communities_label_sans1878_MetadataTimeStamp',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_MetadataPointOfContactIndividualName',
        widget=StringField._properties['widget'](
            label="Metadata Point Of Contact Individual Name",
            label_msgid='Communities_label_sans1878_MetadataPointOfContactIndividualName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_MetadataPointOfContactOrganizationName',
        widget=StringField._properties['widget'](
            label="Metadata Point Of Contact Organization Name",
            label_msgid='Communities_label_sans1878_MetadataPointOfContactOrganizationName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_MetadataPointOfContactPositionName',
        widget=StringField._properties['widget'](
            label="Metadata Point Of Contact Position Name",
            label_msgid='Communities_label_sans1878_MetadataPointOfContactPositionName',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),
    StringField(
        name='sans1878_MetadataPointOfContactRole',
        widget=StringField._properties['widget'](
            label="Metadata Point Of Contact Role",
            label_msgid='Communities_label_sans1878_MetadataPointOfContactRole',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

SANSFields_schema = getattr(Fields, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class SANSFields(Fields):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ISANSFields)

    meta_type = 'SANSFields'
    _at_rename_after_creation = True

    schema = SANSFields_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(SANSFields, PROJECTNAME)
# end of class SANSFields

##code-section module-footer #fill in your manual code here
##/code-section module-footer



