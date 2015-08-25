import Globals
from AccessControl import ClassSecurityInfo
import AccessControl.SecurityManagement, AccessControl.User
import Acquisition
from Products.CMFCore.CMFCatalogAware import CMFCatalogAware
from Products.CMFDefault.DublinCore import DefaultDublinCoreImpl
import urllib
from Products.Archetypes.public import Schema, BaseSchema, registerType,BaseContent,BaseFolder, BaseFolderSchema,StringField,StringWidget
from Products.CMFCore import permissions
from config import PROJECTNAME
from config import ADD_CONTENT_PERMISSION
import time
from Products.ATContentTypes.content.folder import ATFolder
import MapServerTemplates
import StringIO
import logging

logger = logging.getLogger("Organization")
hdlr = logging.FileHandler('Organization.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)


extra_schema = getattr(ATFolder,'schema',Schema(()))


class Organization(BaseFolder): 
    '''Organization for CoGIS'''    
    schema = BaseFolderSchema

    schema = BaseSchema + Schema([
        StringField('description',
                     required=False,                            
                     searchable = 1,                     
                     widget=StringWidget(label='Description',description="Enter organization description")), 
                      ]) 
                      
#    actions = ({'id': 'pingServer',
#              'name': 'Ping Server',
#              'action': 'string:${object_url}/Map_Server_PingServer',
#              'permissions': (CMFCorePermissions.ViewManagementScreens,)},              
#              
#              {'id': 'licenseAgreement',
#              'name': 'License Agreement',
#              'action': 'string:${object_url}/Map_Server_LicenseAgreement_Edit',
#              'permissions': (CMFCorePermissions.ViewManagementScreens,)},              
#                                                   
#                )   

    #schema = schema + extra_schema 
    content_icon = "organization.gif"  
    security = ClassSecurityInfo()      
    
    archetype_name             = 'Organization'
    meta_type                  = 'Organization'
    portal_type                = 'Organization'
    allowed_content_types      = [] #['MapServer'] 
    filter_content_types       = 1
    global_allow               = 0
    allow_discussion           = 0
    content_icon = "organization.gif"       


    def __init__(self, id,title=''):
        '''Initialize an instance of the class'''            
        self.id=id
        if title == '':
            self.title = id   
        else:
            self.title = title  
            
        self.organization = ""          
    
    def getDetails(self):
        """
        """
        return self.id + " : " + self.organization + "  :  " + self.title        
    
    security.declarePublic('userIsOwner')
    def userIsOwner(self):
        """
        @summary: this is a zope specific method to get logged in user name
        @return: boolean, true if logged in user is the owner
        """                         
        try:
            ownerName = self.owner_info()['id']
            member =  self.portal_membership.getAuthenticatedMember()  
            userName = member.getUserName()      
            if userName == ownerName:
                return True
            else:
                return False             
        except:
            logger.exception('error')

registerType(Organization,PROJECTNAME)


