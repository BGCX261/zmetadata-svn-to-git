# -*- coding: utf-8 -*-
#
# File: fields.py
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
from zope import interface
from zope.interface import implements
import interfaces
from Products.Communities.interfaces.standardfields import IStandardFields
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Communities.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Fields_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Fields(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IFields, IStandardFields)

    meta_type = 'Fields'
    _at_rename_after_creation = True

    schema = Fields_schema

    ##code-section class-header #fill in your manual code here
    vocabs = {}
    ##/code-section class-header

    # Methods

    security.declarePublic('getMyFields')
    def getMyFields(self):
        """
        """
        names = []
        for field in self.schema.fields():
            if (field.schemata != 'categorization') and \
               (field.schemata != 'metadata') and \
               (field.getName() not in ('id', 'title', 'description')):
                names += [field.getName()]
        return names

    security.declarePublic('getFieldInfo')
    def getFieldInfo(self, fieldName):
        """
        """
        try:
            field           = self.schema[fieldName]
            fieldName       = fieldName
            fieldType       = self.schema[fieldName].getWidgetName()
            fieldLabel      = self.schema[fieldName].widget.label
            fieldXSL        = ''
            fieldDefault    = ''
        except:
            print 'ERROR FIELDS:', fieldName


        #if self.vocabs.has_key(fieldName):
        if self.getField(fieldName).vocabulary:
            vocab = getattr(self, self.getField(fieldName).vocabulary)
            fieldVocabulary = vocab()
        else:
            fieldVocabulary = {}
        return {'name': fieldName, 'label': fieldLabel, 'type': fieldType, 'xsl' : fieldXSL, 'default': fieldDefault, 'vocabulary': fieldVocabulary}


registerType(Fields, PROJECTNAME)
# end of class Fields

##code-section module-footer #fill in your manual code here
##/code-section module-footer



