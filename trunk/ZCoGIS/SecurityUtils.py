import AccessControl
import types

_protectionPermissions = {
    'User':('View',),
    'Owner':('Add portal content',),
    'Editor':('Add portal content',),
    'Reviewer':('Review portal content',),
    'Administrator':('Change permissions',),
    'Manager':('View management screens',),
    'Financial':('Add portal member',)
    }


# XXX maybe add this later?
##tuple(SAISISPricing.getAccessLevels(1)) +\

_peckingOrder = ('User',) +\
        ('Owner','Editor','Reviewer','Administrator','Financial','Manager')

def getRoleFor(permission):
    for role, permissions in _protectionPermissions.items():
        if type(permissions) in [types.StringType, types.UnicodeType]:
            permissions = (permissions,)
        if permission in permissions:
            return role
        if permission == role:
            return role
    raise ValueError('No role could be found for permission %s' %permission)
        

def getPermissionsFor(role):
    return _protectionPermissions[role]

def hasPermissionsFor(role):
    return _protectionPermissions.has_key(role)

def getPeckingOrder(fromRole=None, toRole=None):
    '''Returns the role ids in "pecking order"
    fromRole : role to start from (inclusive)
    toRole : role to end at (inclusive)'''
    po = list(_peckingOrder)
    if fromRole is not None or toRole is not None:
        if fromRole is not None:
            frm = po.index(fromRole)
        if toRole is not None:
            to = po.index(toRole)+1
            
        if fromRole is None:
            return tuple(po[:to])
        elif toRole is None:
            return tuple(po[frm:])
        else:
            return tuple(po[frm:to])
    else:
        return _peckingOrder

def getRolesBelow(role):
    '''Get all the roles below "role" in the pecking order'''
    po = list(getPeckingOrder())
    idx = po.index(role)
    return po[:idx]

def getRolesAbove(role):
    '''Get all the roles above "role" in the pecking order'''
    po = list(getPeckingOrder())
    idx = po.index(role)
    return po[idx:+1]

# XXX It may be a bug in AccessControl.User that the System user is given the
# role manage and not Manager - not sure, but adding Manager makes the System
# user able to search the portal catalog, so I'm happy :)
AccessControl.User.system=AccessControl.User.UnrestrictedUser(
    'System Processes','',('manage','Manager',), [])

def loginAsSystemUser():
    '''Login as the Zope system user.'''
    loginAsUser(AccessControl.User.system)

def loginAsUser(user):
    '''Login as a specific user'''
    AccessControl.SecurityManagement.newSecurityManager(
        None, user)

def getLoggedInUser():
    '''Get the current logged in user for this thread.'''
    sm=AccessControl.SecurityManagement.getSecurityManager()
    return sm.getUser()

def logoutUser():
    '''Logout'''
    AccessControl.SecurityManagement.noSecurityManager()

class ClassSecurityInfo(AccessControl.ClassSecurityInfo):
    def declareProtected(self, roleOrPermission, methodName):
        '''Declare a method protected.
        roleOrRight : the minimum role that can see this.
        methodName : the method name to protect'''
        try:
            permissions = getPermissionsFor(roleOrPermission)
        except KeyError:
            permissions = (roleOrPermission,)
            
        for permission in permissions:
            AccessControl.ClassSecurityInfo.declareProtected(
                self, permission, methodName)
