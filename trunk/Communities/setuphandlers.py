# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2009 by []
# Generator: ArchGenXML Version 2.3
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('Communities: setuphandlers')
from Products.Communities.config import PROJECTNAME
from Products.Communities.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction
##code-section HEAD
##/code-section HEAD

def isNotCommunitiesProfile(context):
    return context.readDataFile("Communities_marker.txt") is None

def setupHideToolsFromNavigation(context):
    """hide tools"""
    if isNotCommunitiesProfile(context): return 
    # uncatalog tools
    site = context.getSite()
    toolnames = ['portal_communitytool']
    portalProperties = getToolByName(site, 'portal_properties')
    navtreeProperties = getattr(portalProperties, 'navtree_properties')
    if navtreeProperties.hasProperty('idsNotToList'):
        for toolname in toolnames:
            try:
                portal[toolname].unindexObject()
            except:
                pass
            current = list(navtreeProperties.getProperty('idsNotToList') or [])
            if toolname not in current:
                current.append(toolname)
                kwargs = {'idsNotToList': current}
                navtreeProperties.manage_changeProperties(**kwargs)


from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.utils import generateCategorySetIdForType
from Products.remember.utils import getAdderUtility

def setupMemberTypes(context):
    """Adds our member types to MemberDataContainer.allowed_content_types."""
    if isNotCommunitiesProfile(context): return 
    site = context.getSite()
    types_tool = getToolByName(site, 'portal_types')
    act = types_tool.MemberDataContainer.allowed_content_types
    types_tool.MemberDataContainer.manage_changeProperties(allowed_content_types=act+('CSIRUser', ))
    # registers with membrane tool ...
    membrane_tool = getToolByName(site, 'membrane_tool')
    

def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotCommunitiesProfile(context): return 
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotCommunitiesProfile(context): return
    site = context.getSite()



##code-section FOOT
##/code-section FOOT
