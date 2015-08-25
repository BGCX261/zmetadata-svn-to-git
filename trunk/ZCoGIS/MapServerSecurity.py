# Python imports
import time

# Zope imports
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Acquisition import aq_base

# CMF imports
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName

# Products imports
from Products.PloneBooking.Extensions.Install import install as installPloneBooking

# Plone imports
#from Products.CMFPlone.tests import PloneTestCase

import cStringIO
import StringIO
import logging
import time

class MapServerSecurity:    
    def __init__(self):
        self.originalUser = None      
    
    def setOriginalUser(user):
        self.originalUser = user
        
    def getOriginalUser():
        return self.originalUser    

    def loginAsPortalMember(self):
        '''Use if you need to manipulate an object as member.'''
        uf = self.portal.acl_users
        user = uf.getUserById(portal_member).__of__(uf)
        newSecurityManager(None, user)    
        
    def loginAsPortalOwner(self):
        '''Use if you need to manipulate an object as portal owner.'''
        uf = self.portal.acl_users
        user = uf.getUserById(portal_owner).__of__(uf)
        newSecurityManager(None, user)