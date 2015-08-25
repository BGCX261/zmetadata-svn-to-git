# -*- coding: utf-8 -*-
#
# File: csiruser.py
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
from Products.Communities.interfaces.csiruser import ICSIRUser
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

# imports needed by remember
from Products.remember.content.member import BaseMember
from Products.remember.permissions import \
        VIEW_PUBLIC_PERMISSION, EDIT_ID_PERMISSION, \
        EDIT_PROPERTIES_PERMISSION, VIEW_OTHER_PERMISSION,  \
        VIEW_SECURITY_PERMISSION, EDIT_PASSWORD_PERMISSION, \
        EDIT_SECURITY_PERMISSION, MAIL_PASSWORD_PERMISSION, \
        ADD_MEMBER_PERMISSION
from AccessControl import ModuleSecurityInfo
from Products.Communities.config import *

# additional imports from tagged value 'import'
from Products.CMFCore.utils import getToolByName

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='defaultCommunity',
        widget=SelectionWidget(
            label='Defaultcommunity',
            label_msgid='Communities_label_defaultCommunity',
            i18n_domain='Communities',
        ),
        vocabulary="getMyCommunities",
        searchable=1,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CSIRUser_schema = BaseSchema.copy() + \
    BaseMember.schema.copy() + \
    ExtensibleMetadata.schema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class CSIRUser(BaseMember, BrowserDefaultMixin, BaseContent):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ICSIRUser, ICSIRUser)

    meta_type = 'CSIRUser'
    _at_rename_after_creation = True

    schema = CSIRUser_schema

    base_archetype = BaseContent

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # A member's __call__ should not render itself, this causes recursion
    def __call__(self, *args, **kwargs):
        return self.getId()
        

    # Methods

    security.declarePublic('getMyCommunities')
    def getMyCommunities(self):
        """
        """
        ctool = getToolByName(self, 'portal_communitytool')
        communities = ctool.getMyCommunities()

        result = [('None', '<None>')]
        #community = ctool.getDefaultCommunity()
        #result += [(community.id, community.title_or_id())]
        for community in communities:
            result += [(community.id, community.title_or_id())]
        return result


registerType(CSIRUser, PROJECTNAME)
# end of class CSIRUser

##code-section module-footer #fill in your manual code here
##/code-section module-footer



