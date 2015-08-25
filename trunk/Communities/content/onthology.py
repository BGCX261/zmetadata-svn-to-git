# -*- coding: utf-8 -*-
#
# File: onthology.py
#
# Copyright (c) 2009 by []
# Generator: ArchGenXML Version 2.1
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

from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.document import ATDocumentSchema
from Products.Communities.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    LinesField(
        name='keywords',
        widget=LinesField._properties['widget'](
            label='Keywords',
            label_msgid='Communities_label_keywords',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Onthology_schema = ATDocumentSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Onthology(ATDocument):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IOnthology)

    meta_type = 'Onthology'
    _at_rename_after_creation = True

    schema = Onthology_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(Onthology, PROJECTNAME)
# end of class Onthology

##code-section module-footer #fill in your manual code here
##/code-section module-footer



