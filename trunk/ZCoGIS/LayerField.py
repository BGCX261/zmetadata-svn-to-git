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
from ZODB.PersistentMapping import PersistentMapping
import logging

logger = logging.getLogger("LayerField")
hdlr = logging.FileHandler('LayerField.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)


class LayerField(BaseContent): 
    '''Layer Field for CoGIS'''    
    schema = BaseSchema
    actions = ({'id': 'security',
              'name': 'Security',
              'action': 'string:${object_url}/Layer_Field_Security',
              'permissions': (permissions.ViewManagementScreens,)},                                  
                )

    schema = BaseSchema + Schema([
        StringField('description',
                     required=True,                            
                     searchable = 1,                     
                     widget=StringWidget(label='Description',description="Enter project description")),        
                      ])    

    
    security = ClassSecurityInfo()     
    
    archetype_name             = 'LayerField'
    meta_type                  = 'LayerField'
    portal_type                = 'LayerField'
    allowed_content_types      = [] 
    filter_content_types       = 1
    global_allow               = 0
    allow_discussion           = 0
    content_icon = "layer_icon.gif"     
    

    def __init__(self, id,title=''):
        '''Initialize an instance of the class'''            
        self.id= id
        if title == '':
            self.title = id   
        else:
            self.title = title  
        self.type = ''        
        
        self.availablePermissions = ['Render']
        self.security = PersistentMapping() #  e.g {'Manager':{'Render':0}}
        self.reindexObject()
        self._p_changed = 1  
        
##    def manage_afterAdd(self,item, container):
##        """
##        """  
##        self.manage_permission("View", roles=["Owner"], acquire=False)      
##        #self.manage_permission("List folder contents", roles=["Owner"], acquire=False)  

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
            return False    
        
    def getParentSecurity(self):
        """
        @summary: returns the security structure for the parent object
        @retrun: the security definition for the parent layer
        """        
        return self.aq_parent.getSecurity()        
        
    def getSecurity(self):
        """
        @summary: returns the current security definitions dict
        @return: dict containing security info for roles defined in plone
        """        
        return dict(self.security)
    
    def setSecurityVarOnly(self,securityDict):
        """
        """
        try:
            tmpDict = {}   
            for k in securityDict.keys():
                cDict = {}
                if securityDict[k]['Render'] in ['false',0]:
                    cDict['Render'] = 0                
                if securityDict[k]['Render'] in ['true',1]:
                    cDict['Render'] = 1               
                tmpDict[k] = cDict
            self.security = tmpDict     
            return 1
        except:
            logger.exception('error')
        
    
    def setSecurity(self,securityDict):
        """
        @summary: sets the security structure with the given dict object
        @param securityDict: a dictionary containing permissions defined for certain roles defined in plone 
        @return: 1
        """         
        try:
            tmpDict = {}   
            for k in securityDict.keys():
                cDict = {}
                if securityDict[k]['Render'] in ['false',0]:
                    cDict['Render'] = 0                
                if securityDict[k]['Render'] in ['true',1]:
                    cDict['Render'] = 1               
                tmpDict[k] = cDict
            self.security = tmpDict        
            
            self.aq_parent.aq_parent.updateSecurityForSingleLayer(self.aq_parent.uniqueName)
            
            return 1
        except:
            logger.exception('error')

registerType(LayerField,PROJECTNAME)


