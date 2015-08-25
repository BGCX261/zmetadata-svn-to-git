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
import logging
import MapServerTemplates
import StringIO
import transaction
from Products.Archetypes.atapi import ReferenceField
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFCore.permissions import ModifyPortalContent
from Products.ATContentTypes import ATCTMessageFactory as _



logger = logging.getLogger("MapServer")
hdlr = logging.FileHandler('MapServer.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

extra_schema = getattr(ATFolder,'schema',Schema(()))


class MapServer(BaseFolder): 
    '''Map Server for CoGIS'''    
    schema = BaseFolderSchema

    schema = BaseSchema + Schema([
        StringField('description',
                     required=False,                            
                     searchable = 1,                     
                     widget=StringWidget(label='Description',description="Enter project description")), 
        ReferenceField(
                     'relatedItems', 
                     relationship = 'relatesTo', 
                     multiValued = True, 
                     isMetadata = True, 
                     languageIndependent = False, 
                     index = 'KeywordIndex', 
                     write_permission = ModifyPortalContent, 
                     widget = ReferenceBrowserWidget( allow_search = True, 
                                                      allow_browse = True, 
                                                      show_indexes = False, 
                                                      force_close_on_insert = True, 
                                                      label = _(u'label_related_items', default=u'Related Items'), 
                                                      description = '', 
                                                      visible = {'edit' : 'visible', 'view' : 'invisible' } 
                                                      )
                      )
        ],
        ) 
                      
    actions = ({'id': 'publish',
              'name': 'Publish',
              'action': 'string:${object_url}/Map_Server_PublishAll',
              'permissions': (permissions.ViewManagementScreens,)},
              
              {'id': 'pingServer',
              'name': 'Ping Server',
              'action': 'string:${object_url}/Map_Server_PingServer',
              'permissions': (permissions.ViewManagementScreens,)},              
              
              {'id': 'licenseAgreement',
              'name': 'License Agreement',
              'action': 'string:${object_url}/Map_Server_LicenseAgreement_Edit',
              'permissions': (permissions.ViewManagementScreens,)},              
                                                   
                )   

    #schema = schema + extra_schema 
    content_icon = "mapServer.gif"  
    security = ClassSecurityInfo()      
    
    archetype_name             = 'MapServer'
    meta_type                  = 'MapServer'
    portal_type                = 'MapServer'
    allowed_content_types      = [] #['MapLayer'] 
    filter_content_types       = 1
    global_allow               = 0
    allow_discussion           = 0
    content_icon = "mapServer.gif"       


    def __init__(self, id,title=''):
        '''Initialize an instance of the class'''            
        self.id=id
        if title == '':
            self.title = id   
        else:
            self.title = title  
            
        self.organization = ""
        self.wmsSource = ""
        self.wfsSource = ""
        self.enableLicenseAgreement = False
        # licenseAgreent is the text to display in the tbx
        self.licenseAgreement = "Put the license text here \nPlease read license before publishing"        
        # its a list of usernames that have accepted the license agreement
        self.acceptedUserNames = []    
    
    def dummyTest(self):
        """
        """        
        return dir(self) 
        
    def updateLicenseAgreement(self,REQUEST=None):
        """
        @summary: udpate the server license agreement and disables/enables the agreement
        """
        try:
            self.acceptedUserNames = []         
                            
            if REQUEST.has_key('enableIt'):
                enable = True
            else:
                enable = False
                    
            licenseText = REQUEST.form['licenseText'];
               
            self.enableLicenseAgreement = enable       
            self.licenseAgreement = licenseText       
            
            self._p_changed = 1   
            transaction.savepoint(True)      
                    
            status_message = "License Agreement Updated"
            
            REQUEST.RESPONSE.redirect( "%s/Map_Server_LicenseAgreement_Edit?portal_status_message=%s" %(self.absolute_url(), status_message))      
        except:
            logger.exception('failed updateLicenseAgreement')
        
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
            logger.exception('failed user is owner')
        
    def publishLayersForRoles(self,rolesToPublish):
        """
        @summary : publishes layer for the given roles passed
        @param   : a list of roles to publish layers for
        """
        
        try:
            items =  self.objectItems()
            for i in items:            
                if i[1].meta_type == 'MapLayer':  
                    l = i[1]
                    secStruct = l.setSecurity(self.getPublishedStructureForRoles(rolesToPublish))                
            return 1        
        except:
            logger.exception('failed publishLayersForRoles')
    
    def publishAllLayers(self):
        """
        @summary: this will publish all the layers in the server
        @return: 1
        """
        
        try:
            items =  self.objectItems()
            for i in items:            
                if i[1].meta_type == 'MapLayer':  
                    l = i[1]
                    secStruct = l.setSecurity(self.getPublishedSecurityStructure())                
            return 1
        except:
            logger.exception('failed publishAllLayers')
    
    def retractAllLayers(self):
        """
        @summary: this will retract all the layers in the server
        @return: 1
        """
        
        try:
            items =  self.objectItems()
            for i in items:            
                if i[1].meta_type == 'MapLayer':  
                    l = i[1]
                    secStruct = l.setSecurity(self.getRetractedSecurityStructure())                
            return 1
        except:
            logger.exception('failed retractAllLayers')
    
    def pingServer(self):
        """
        """
        try:
            startTime = time.time()
            wmsPingRes = self._getURLContent(self.wmsSource)    
            endTime = time.time()
            wmsTime = endTime - startTime
            if wmsPingRes.find("Exception occured") != -1:
                wmsTime = "Server Unavailable"
            
            
            startTime = time.time()
            wfsPingRes = self._getURLContent(self.wfsSource)
            endTime = time.time()        
            wfsTime = endTime - startTime   
            if wfsPingRes.find("Exception occured") != -1:
                wfsTime = "Server Unavailable"     
            
            return [str(wfsTime), str(wmsTime)]        
        except:
            logger.exception('failed pingServer')
    
    def pingAllLayers(self):
        """
        """
        try:
            results = {}
            items =  self.objectItems()
            for i in items:   
                layer = i[1]
                pingResWMS = layer.pingWMSLayer() 
                pingResWFS = layer.pingWFSLayer() 
                results[layer.uniqueName] = [pingResWFS,pingResWMS]            
            return results   
        except:
            logger.exception('error')
                
    def getPublishedSecurityStructure(self):
        """
        @summary: builds a security structure that will expose all layers
        @return: a dictionary with all the roles as keys and another dict as value
        """
        try:
            roles = self.validRoles()        
            tmpDict = {}
            for role in roles:
                tmpDict[role] = {'Render':1,'Extract':1}          
            return tmpDict
        except:
            logger.exception('failed getPublishedSercurityStructure')
    
    def getPublishedStructureForRoles(self,theRoles):
        """
        """        
        try:
            roles = self.validRoles()        
            tmpDict = {}
            for role in roles:
                if role in theRoles:
                    tmpDict[role] = {'Render':1,'Extract':1}    
                else:
                    tmpDict[role] = {'Render':0,'Extract':0}                          
            return tmpDict
        except:
            logger.exception('Error')
    
    def getRetractedSecurityStructure(self):
        """
        @summary: builds a security structure that will expose all layers
        @return: a dictionary with all the roles as keys and another dict as value
        """
        try:
            roles = self.validRoles()        
            tmpDict = {}
            for role in roles:
                tmpDict[role] = {'Render':0,'Extract':0}          
            return tmpDict
        except:
            logger.exception('Error')
    
    def _getURLContent(self,url,data={}):
        """        
        """        
        try:             
            if data:
                if type(data) == unicode:                    
                    data = str(urllib.unquote(data))                                
                if type(data) == str:                    
                    f = urllib.urlopen(url,data)  
                else:
                    params = urllib.urlencode(data)
                    f = urllib.urlopen(url,params) 
            else:
                f = urllib.urlopen(url)        
            data = f.read()
            f.close()        
            return data
        except:
            import traceback
            sio = StringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()    
            logger.exception('Error')        
            return MapServerTemplates.ogcServiceException %("Exception occured getURLContent request, check log for details %s" %trace) 
                       

registerType(MapServer,PROJECTNAME)


