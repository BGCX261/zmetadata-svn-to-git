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
import binascii
import MapServerTemplates
import cStringIO
import StringIO
import time
import logging
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.base import ATCTFolder
from Products.ATContentTypes.content.base import ATCTContent
from ZODB.PersistentMapping import PersistentMapping
from Products.Archetypes.atapi import ReferenceField
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFCore.permissions import ModifyPortalContent
from Products.ATContentTypes import ATCTMessageFactory as _


logger = logging.getLogger("MapLayer")
hdlr = logging.FileHandler('MapLayer.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)


WMS_GETMAP_EXTENSION = "version=1.0.0&request=GetMap&service=WMS"
WFS_DESCRIBEFEATURETYPE_EXTENSION = "version=1.0.0&request=DescribeFeatureType&service=WFS"
WFS_GETFEAURE_EXTENSION = "version=1.0.0&service=WFS&request=GetFeature"

#extra_schema = getattr(ATFolder,'schema',Schema(()))
#extra_schema = getattr(BaseFolder,'schema',Schema(()))
extra_schema = getattr(ATCTContent,'schema',Schema(()))
#extra_schema.update(BaseFolderSchema)

class MapLayer(BaseFolder):#(BaseFolder): 
    '''Map Layer for CoGIS'''    
    #schema = extra_schema#BaseFolderSchema
    #schema = BaseFolderSchema
    
    actions = ({'id': 'details',
              'name': 'Details',
              'action': 'string:${object_url}/MapLayer_Details',
              'permissions': (permissions.ViewManagementScreens,)},   
              {'id': 'security',
              'name': 'Security',
              'action': 'string:${object_url}/Map_Layer_Security',
              'permissions': (permissions.ViewManagementScreens,)}, 
              {'id': 'pingLayer',
              'name': 'Ping Layer',
              'action': 'string:${object_url}/Map_Layer_Ping',
              'permissions': (permissions.ViewManagementScreens,)}, 
                                          
                )

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
      
                      ]) 

    #schema = schema + extra_schema 
    security = ClassSecurityInfo()      
    
    archetype_name             = 'MapLayer'
    meta_type                  = 'MapLayer'
    portal_type                = 'MapLayer'
    allowed_content_types      = [] #['LayerField'] 
    filter_content_types       = 1
    global_allow               = 0
    allow_discussion           = 0
    content_icon = "mapService_icon.gif"     

    def __init__(self, id,title=''):
        '''Initialize an instance of the class'''            
        self.id=id            
        self.sampleImage = ''
        self.abstract = ''
        self.keywords = ''        
        self.uniqueName = ''
        self.geometryField = ''
        self.geometryType = ''
        self.title = id
        self.wfsSRS = ''
        self.wmsStyleName = ''
        self.wfsBoundingBox = ''
        self.fields = ''
        self.source = ''
        self.error = ''
        self.wmsQueryable = ''
        self.wmsName = ''
        self.wfsName = ''
        self.wmsSRS = ''
        self.wmsTitle = ''
        self.hasWFSLayer = False
        self.wmsBoundingBox = ''
        self.describeFeatureResponse = ''
        self.availablePermissions = ['Render','Extract']
        self.security = PersistentMapping() # e.g {'Manager':{'Render':0,'Extract':1}}        
        self.wmsXML = ""
        self.wfsXML = ""
        self.organization = ""
        self.reindexObject()
        self._p_changed = 1
        
          
        
##    def manage_afterAdd(self,item, container):
##        """
##        """      
##        self.manage_permission("View", roles=["Owner"], acquire=False)  
##        self.manage_permission("List folder contents", roles=["Owner"], acquire=False)  

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
    
    def getSecurity(self):
        """
        @summary: returns the current security definitions dict
        @return: dict containing security info for roles defined in plone
        """            
        return dict(self.security)
    
    def getMetadata(self):
        """
        @summary: gets the metadata template for the layer
        @return: an html interface with metadata information
        """        
        return self.Map_Layer_Details_Stripped(self)
    
    def setSecurityVarOnly(self,securityDict):
        """
        """
        try:
            tmpDict = {}           
            for k in securityDict.keys():
                if k == 'fields':
                    continue
                
                cDict = {}
                if securityDict[k]['Render'] in ['false',0]:
                    cDict['Render'] = 0                
                if securityDict[k]['Render'] in ['true',1]:
                    cDict['Render'] = 1                
                if securityDict[k]['Extract'] in ['false',0]:
                    cDict['Extract'] = 0 
                if securityDict[k]['Extract'] in ['true',1]:
                    cDict['Extract'] = 1
                tmpDict[k] = cDict                
            
            # get a diff between current security settings and the passed security settings
            changed = {}
            for k in tmpDict.keys():
                if not k in self.security.keys():
                    changed[k] = tmpDict[k]   # its a new key
                if k in self.security.keys():
                    if self.security[k]['Render'] != tmpDict[k]['Render']:
                        changed[k] = tmpDict[k]        
            
            self.security = tmpDict        
            # only let the changes be propagated to children 
            
            # get all fields
            fields = []
            items =  self.objectItems()        
            for i in items:
                if i[1].meta_type == 'LayerField':                                
                    fields.append(i[1])                        
            
            for field in fields:
                tmpSec = field.getSecurity()             
                for k in changed.keys():
                    if not tmpSec.has_key(k):
                        tmpSec[k] = {'Render':0}  # add the key if it does not exist
                    tmpSec[k]['Render'] = changed[k]['Render']              
                field.setSecurityVarOnly(tmpSec)          
            return 1
        except:
            logger.exception('error')
    
    def setSecurity(self,securityDict):
        """
        @summary:
        @param securityDict: a dictionary containing permissions defined for certain roles defined in plone 
        """         
        try:
            tmpDict = {}           
            for k in securityDict.keys():
                if k == 'fields':
                    continue
                
                cDict = {}
                if securityDict[k]['Render'] in ['false',0]:
                    cDict['Render'] = 0                
                if securityDict[k]['Render'] in ['true',1]:
                    cDict['Render'] = 1                
                if securityDict[k]['Extract'] in ['false',0]:
                    cDict['Extract'] = 0 
                if securityDict[k]['Extract'] in ['true',1]:
                    cDict['Extract'] = 1
                tmpDict[k] = cDict                
            
            # get a diff between current security settings and the passed security settings
            changed = {}
            for k in tmpDict.keys():
                if not k in self.security.keys():
                    changed[k] = tmpDict[k]   # its a new key
                if k in self.security.keys():
                    if self.security[k]['Render'] != tmpDict[k]['Render']:
                        changed[k] = tmpDict[k]        
            
            self.security = tmpDict        
            # only let the changes be propagated to children 
            
            # get all fields
            fields = []
            items =  self.objectItems()        
            for i in items:
                if i[1].meta_type == 'LayerField':                                
                    fields.append(i[1])                        
            
            for field in fields:
                tmpSec = field.getSecurity()             
                for k in changed.keys():
                    if not tmpSec.has_key(k):
                        tmpSec[k] = {'Render':0}  # add the key if it does not exist
                    tmpSec[k]['Render'] = changed[k]['Render']              
                field.setSecurity(tmpSec)        
            
            self.aq_parent.updateSecurityForSingleLayer(self.uniqueName)        
            return 1        
        except:
            logger.exception('error')
    
    def getSampleImage(self,REQUEST=None):
        """
        @summary: converts the hex encoded image to binary
        @return: sample image in binary format
        """
        try:
            data = binascii.a2b_hex(self.sampleImage) 
            REQUEST.RESPONSE.setHeader("Content-type","image/png")
    
            return data      
        except:
            logger.exception('error')
    
    def pingWMSLayer(self,extent=['23.00','23.00','23.01','23.01']):
        """ 
        """        
        try:
            startTime = time.time()
            layerName = self.wmsName
            source = self.source[1]
            
            layerName = layerName.replace(" ","%20")
            strEnv = "%s,%s,%s,%s" %(extent[0],extent[1],extent[2],extent[3])
            theURL = source + WMS_GETMAP_EXTENSION + "&bbox=%s&styles=&Format=image/png&width=2&height=2&srs=EPSG:4326&layers=%s" %(strEnv,layerName) #"&request=GetLegendGraphic&version=1.0.0&format=%s&width=%s&height=%s&layer=%s" %(format,width,height,layer['wmsName'])        
            data = self._getURLContent(theURL,{})           
            
            if data.find("ServiceExceptionReport") != -1:
                return "Layer Unavailable"
            endTime = time.time()
            return str(endTime - startTime)
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()            
            logger.exception('error')
            return MapServerTemplates.ogcServiceException %("Exception occured with _getSampleImage request, check log for details %s" %trace)                            

    def pingWFSLayer(self):
        """
        """        
        if self.hasWFSLayer:
            try:
                startTime = time.time()
                layerName = self.wfsName
                source = self.source[0]                 
                baseURL = source + WFS_DESCRIBEFEATURETYPE_EXTENSION   
                baseURL += "&typename=" + layerName.replace(" ","%20")                 
                data = self._getURLContent(baseURL)    
                
                if (data.find("ServiceException") != -1) or (data.find("ServiceExceptionReport") != -1) or (data.strip() == ""):     
                    return  "Layer Unavailable"  
                
                endTime = time.time()
                return str(endTime - startTime)
            
            except:
                import traceback
                sio = cStringIO.StringIO()
                traceback.print_exc(file=sio)
                sio.seek(0)
                trace = sio.read()
                logger.exception('error')
                return MapServerTemplates.ogcServiceException %("Exception occured with pingWFSLayer request, check log for details %s" %trace)                                   
            
        else:
            return "No WFS Source given."
        
##        if self.hasWFSLayer:
##            try:
##                startTime = time.time()
##                layerName = self.wfsName
##                source = self.source[0]                
##                data = ''
##                baseURL = source + WFS_DESCRIBEFEATURETYPE_EXTENSION
##                baseURL += "&typename=" + layerName.replace(" ","%20") 
##                data = self._getURLContent(baseURL)  
##                if data.find("ServiceExceptionReport") != -1:
##                    return "Layer Unavailable"
##                
##                endTime = time.time()
##                return str(endTime - startTime)
##            except:
##                import traceback
##                sio = cStringIO.StringIO()
##                traceback.print_exc(file=sio)
##                sio.seek(0)
##                trace = sio.read()
##                
##                return MapServerTemplates.ogcServiceException %("Exception occured with pingWFSLayer request, check log for details %s" %trace)                            
##                    
##        else:
##            return "No WFS Source given."
##        
##        return 1
    
    
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
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('error')             
            return MapServerTemplates.ogcServiceException %("Exception occured getURLContent request, check log for details %s" %trace) 
       
    
registerType(MapLayer,PROJECTNAME)


