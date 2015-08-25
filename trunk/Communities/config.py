# -*- coding: utf-8 -*-
#
# File: Communities.py
#
# Copyright (c) 2009 by []
# Generator: ArchGenXML Version 2.3
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles
from Products.remember.permissions import ADD_MEMBER_PERMISSION
##code-section config-head #fill in your manual code here
##/code-section config-head


PROJECTNAME = "Communities"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))
ADD_CONTENT_PERMISSIONS = {
    'Communities': 'Communities: Add Communities',
    'Community': 'Communities: Add Community',
    'Content': 'Communities: Add Content',
    'Ontology': 'Communities: Add Ontology',
    'STDSetup': 'Communities: Add STDSetup',
    'CommonFields': 'Communities: Add CommonFields',
    'CSIRUser': ADD_MEMBER_PERMISSION,
    'StandardSetups': 'Communities: Add StandardSetups',
    'Ontologies': 'Communities: Add Ontologies',
    'SANSSetup': 'Communities: Add SANSSetup',
    'SANSFields': 'Communities: Add SANSFields',
    'CommonSetup': 'Communities: Add CommonSetup',
    'Fields': 'Communities: Add Fields',
    'ISO19139Fields': 'Communities: Add ISO19139Fields',
    'ISO19139Setup': 'Communities: Add ISO19139Setup',
    'ISO19115Setup': 'Communities: Add ISO19115Setup',
    'ISO19115Fields': 'Communities: Add ISO19115Fields',
    'EMLSetup': 'Communities: Add EMLSetup',
    'EMLFields': 'Communities: Add EMLFields',
    'DCSetup': 'Communities: Add DCSetup',
    'DCFields': 'Communities: Add DCFields',
    'CommunitySearch': 'Communities: Add CommunitySearch',
}

setDefaultRoles('Communities: Add Communities', '("Manager",)')
setDefaultRoles('Communities: Add Community', ('Manager','Owner'))
setDefaultRoles('Communities: Add Content', ('Manager','Owner'))
setDefaultRoles('Communities: Add Ontology', ('Manager','Owner'))
setDefaultRoles('Communities: Add STDSetup', ('Manager','Owner'))
setDefaultRoles('Communities: Add CommonFields', ('Manager','Owner'))
setDefaultRoles('Communities: Add StandardSetups', ('Manager','Owner'))
setDefaultRoles('Communities: Add Ontologies', 'Manager')
setDefaultRoles('Communities: Add SANSSetup', ('Manager','Owner'))
setDefaultRoles('Communities: Add SANSFields', ('Manager','Owner'))
setDefaultRoles('Communities: Add CommonSetup', ('Manager','Owner'))
setDefaultRoles('Communities: Add Fields', ('Manager','Owner'))
setDefaultRoles('Communities: Add ISO19139Fields', ('Manager','Owner'))
setDefaultRoles('Communities: Add ISO19139Setup', ('Manager','Owner'))
setDefaultRoles('Communities: Add ISO19115Setup', ('Manager','Owner'))
setDefaultRoles('Communities: Add ISO19115Fields', ('Manager','Owner'))
setDefaultRoles('Communities: Add EMLSetup', ('Manager','Owner'))
setDefaultRoles('Communities: Add EMLFields', ('Manager','Owner'))
setDefaultRoles('Communities: Add DCSetup', ('Manager','Owner'))
setDefaultRoles('Communities: Add DCFields', ('Manager','Owner'))
setDefaultRoles('Communities: Add CommunitySearch', ('Manager','Owner'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

##code-section config-bottom #fill in your manual code here
##/code-section config-bottom


# Load custom configuration not managed by archgenxml
try:
    from Products.Communities.AppConfig import *
except ImportError:
    pass

