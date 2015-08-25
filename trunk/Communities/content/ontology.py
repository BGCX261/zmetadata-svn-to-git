# -*- coding: utf-8 -*-
#
# File: ontology.py
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
from Products.Communities.interfaces.ontology import IOntology
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.ATContentTypes.content.document import ATDocumentSchema
from Products.Communities.config import *


##code-section module-header #fill in your manual code here
from Products.AddRemoveWidget import AddRemoveWidget
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
##/code-section module-header

schema = Schema((

    LinesField(
        name='keywords',
        vocabulary=NamedVocabulary("""GlobalCommunityKeywords"""),
        widget=AddRemoveWidget(
                 label=u"Keywords",
                 description=u"Keywords.",
             ),
        searchable=1,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Ontology_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Ontology(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IOntology, IOntology)

    meta_type = 'Ontology'
    _at_rename_after_creation = True

    schema = Ontology_schema

    ##code-section class-header #fill in your manual code here
    def availableSubjects(self):
        """
        """
        return []
    ##/code-section class-header

    # Methods


registerType(Ontology, PROJECTNAME)
# end of class Ontology

##code-section module-footer #fill in your manual code here
##/code-section module-footer



