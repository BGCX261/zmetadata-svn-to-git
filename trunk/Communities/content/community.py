# -*- coding: utf-8 -*-
#
# File: community.py
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
from Products.Communities.interfaces.community import ICommunity
from Products.Communities.content.communitysearch import CommunitySearch
from Products.Communities.content.ontologies import Ontologies
from Products.Communities.content.content import Content
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.Communities.config import *

# additional imports from tagged value 'import'
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

##code-section module-header #fill in your manual code here
from Products.ATContentTypes.content.topic import ATTopic
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='members',
        widget=ReferenceBrowserWidget(
            label='Members',
            label_msgid='Communities_label_members',
            i18n_domain='Communities',
        ),
        allowed_types="CSIRUser",
        relationship="community_members",
        multiValued=True,
        searchable=1,
    ),
    BooleanField(
        name='isGlobalCommunity',
        default="False",
        widget=BooleanField._properties['widget'](
            label='Isglobalcommunity',
            label_msgid='Communities_label_isGlobalCommunity',
            i18n_domain='Communities',
        ),
        searchable=1,
    ),

),
)

##code-section after-local-schema #fill in your manual code here\
import transaction
##/code-section after-local-schema

Community_schema = ATFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Community(ATFolder):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ICommunity, ICommunity)

    meta_type = 'Community'
    _at_rename_after_creation = True

    schema = Community_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('_renameAfterCreation')
    def _renameAfterCreation(self, check_auto_id=True):
        """
        """
        plone_tool = getToolByName(self, 'plone_utils')
        
        new_id = plone_tool.normalizeString(self.title_or_id())
        invalid_id = False
        transaction.commit(1)
        self.setId(new_id)
        
        self._setObject("ontologies", Ontologies("ontologies"))
        self["ontologies"].setTitle("Ontologies")
        self["ontologies"].reindexObject()
        self._setObject("search", CommunitySearch("search"))
        self["search"].setTitle("Search")
        self["search"]._renameAfterCreation(check_auto_id)
        self["search"].reindexObject()
        self._setObject("content", ATFolder("content"))
        self["content"].setTitle("Content")
        self["content"]._renameAfterCreation(check_auto_id)
        self["content"].reindexObject()
        
        self['content']._setObject("content", ATTopic("content"))
        self['content']['content'].setTitle("Content")
        self['content']['content'].addCriterion('review_state', 'ATSelectionCriterion')
        self['content']['content'].addCriterion('path', 'ATRelativePathCriterion')
        self['content']['content'].setCustomView(True)
        self['content']['content'].setCustomViewFields(['Title', 'ModificationDate', 'review_state', 'CreationDate', 'Type'])
        self.portal_workflow.doActionFor(self['content']['content'], "publish", comment="")        
        self['content'].setDefaultPage('content')
        
        groups = getToolByName(self, 'portal_groups')
        groupname = 'Community_' + new_id
        groups.addGroup(groupname,)
        return new_id
        

    security.declarePublic('getMyStandards')
    def getMyStandards(self):
        """
        """
        interfaceTool = getToolByName(self, 'portal_interface')

        return self['search']['setup'].objectIds()

    security.declarePublic('assembleDisplayFields')
    def assembleDisplayFields(self):
        """
        """
        result = {}
        standards = self['search']['setup'].getShowStandards()
        for standard in standards:
            result[standard] = []
            fields = self['search']['setup'][standard].getShowFields()
            for field in fields:
                result[standard] += [self['search']['setup'][standard].getFieldInfo(field)]
        return result
        
    security.declarePublic('setMembers')
    def setMembers(self, value, REQUEST=[]):
        """
        """
        groupname = 'Community_' + self.id
        group = self.portal_groups.getGroupById(groupname)

        for user in self.getField('members').get(self):
            group.removeMember(user.id)

        self.getField('members').set(self, value)
        
        for user in self.getField('members').get(self):
            group.addMember(user.id)
    
    security.declarePrivate('manage_beforeDelete')
    def manage_beforeDelete(self, item, container):
        """
        """
        print '2Community_' + item.id
        plone_tool = getToolByName(self, 'plone_utils')
        groups = getToolByName(self, 'portal_groups')
        groupname = 'Community_' + item.id
        groups.removeGroup(groupname,)


registerType(Community, PROJECTNAME)
# end of class Community

##code-section module-footer #fill in your manual code here
##/code-section module-footer



