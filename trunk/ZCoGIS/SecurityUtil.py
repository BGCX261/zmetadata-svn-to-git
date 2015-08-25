from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.PermissionRole import rolesForPermissionOn
from Acquisition import Implicit

class Login:
    def loginAsManager(self):
        user = OmnipotentUser()
        newSecurityManager(None, user)   
        
    def loginAsUser(self, user):
        newSecurityManager(None, user)

class OmnipotentUser(Implicit):
    def getId( self ):
        return 'all_powerful_Oz'

    getUserName = getId

    def getRoles(self):
        return ('Manager',)

    def allowed( self, object, object_roles=None ):
        return 1

    def getRolesInContext(self, object):
        return ('Manager',)

    def _check_context(self, object):
        return True