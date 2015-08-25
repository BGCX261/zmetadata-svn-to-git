import AccessControl.SecurityManagement, AccessControl.User
from AccessControl import ClassSecurityInfo
from AccessControl.Permission import Permission
from AccessControl.unauthorized import Unauthorized
from Acquisition import aq_base, aq_inner, ImplicitAcquisitionWrapper
import Globals
from Globals import InitializeClass
from OFS import SimpleItem
from ZODB.PersistentMapping import PersistentMapping
from ZODB.PersistentList import PersistentList

from Products.Archetypes.public import Schema, BaseSchema, registerType,BaseContent,BaseFolder, BaseFolderSchema,StringField,StringWidget

from Products.CMFCore import permissions
from config import PROJECTNAME,ADD_CONTENT_PERMISSION
import time
import MapServerTemplates
from MapServer import MapServer
from MapLayer import MapLayer
from LayerField import LayerField
import binascii
from xml.dom import minidom
import string
import logging
import StringIO
import cStringIO
import urllib
from PIL import Image
from Products.ATContentTypes.content.folder import ATFolder
import transaction
import traceback
import SLDTemplates

from CoGIS.UniversalMapServer import UniversalMapServer
from CoGIS.LayerRegistry import LayerRegistry
from CoGIS.RequestResponseTranslator import RequestResponseTranslator 
from CoGIS.SecurityManager import SecurityManager

from Organization import Organization
from MapServer import MapServer
from MapLayer import MapLayer
from LayerField import LayerField


logger = logging.getLogger("MapServerFacade")
hdlr = logging.FileHandler('MapServerFacade.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

messagesAlreadySent = {}

WFS_CAPABILITIES_EXTENSION = "version=1.0.0&request=getcapabilities&service=WFS"
WMS_CAPABILITIES_EXTENSION = "version=1.0.0&request=getcapabilities&service=WMS"
WFS_DESCRIBEFEATURETYPE_EXTENSION = "version=1.0.0&request=DescribeFeatureType&service=WFS"
WFS_GETFEAURE_EXTENSION = "version=1.0.0&service=WFS&request=GetFeature"
WMS_GETMAP_EXTENSION = "version=1.0.0&request=GetMap&service=WMS"


extra_schema = getattr(ATFolder,'schema',Schema(()))


class MapServerFacade(BaseFolder):
    '''A class containing various handy functions'''    
    #schema = BaseSchema    
    security = ClassSecurityInfo()      
    
    archetype_name             = 'MapServerFacade'
    meta_type                  = 'MapServerFacade'
    portal_type                = 'MapServerFacade'
    allowed_content_types      = [] #['Organization'] 
    filter_content_types       = 1
    global_allow               = 1
    allow_discussion           = 0
    content_icon               = 'facade_small.gif'  
    
    
    schema = BaseFolderSchema 
        
    actions = ({'id': 'view',
              'name': 'View',
              'action': 'string:${object_url}/MapServerFacade_View',
              'permissions': (permissions.View,)},              
              {'id': 'status',
              'name': 'Status',
              'action': 'string:${object_url}/MapServerFacade_Status',
              'permissions': (permissions.ViewManagementScreens,)},              
              {'id': 'manageSources',
              'name': 'Current Sources',
              'action': 'string:${object_url}/MapServerFacade_ManageSources',
              'permissions': (permissions.ViewManagementScreens,)},
              {'id': 'addSource',
              'name': 'Add Sources',
              'action': 'string:${object_url}/MapServerFacade_AddSource',
              'permissions': (permissions.ViewManagementScreens,)},     
              {'id': 'currentLayers',
              'name': 'Layers',
              'action': 'string:${object_url}/MapServerFacade_CurrentLayers',
              'permissions': (permissions.ViewManagementScreens,)},              
              {'id': 'tests',
              'name': 'Tests',
              'action': 'string:${object_url}/MapServerFacade_Tests',
              'permissions': (permissions.ViewManagementScreens,)},
              
              {'id': 'pingLayers',
              'name': 'Ping All Layers',
              'action': 'string:${object_url}/MapServerFacade_PingAllLayers',
              'permissions': (permissions.ViewManagementScreens,)},             
                                         
                )
    
    def __init__(self,id):        
        self.id = id   
        self.title = id     
        # keeps a list of the last 30 requests of each type made and times
        self._requests = PersistentMapping()           
        # from SecurityManager
        self.securityDefinitions = PersistentMapping()        
        self.layerStructure = PersistentList()        
        self.sources = PersistentList() # is a list of tuples (wfsSource, wmsSource,organization)                 
        self.layerList = PersistentList() 
        self.timeouts = PersistentMapping()        
        
        self.ums = UniversalMapServer(self)        
        self.lr = LayerRegistry(self)
        self.sm = SecurityManager(self)        
        self.rrt = RequestResponseTranslator(self, self.lr, self.sm, self.ums) 
        self.dummySLDFile = ""
    
    def hasTimeout(self, source):
        """
        """        
        return self.timeouts.has_key(source)    
    
    def getTimeout(self, source):
        """
        """
        return self.timeouts[source]    
    
    def userHasAcceptedAgeement(self, layerName):
        """
        @summary: checks if the current user has accepted the license agreement for the layer and server
        @return: boolean
        """           
        try:
            userName = self.getAuthneticatedUserName()  
            # get the server for the layername and check if username is in acceptedlist
            layer = self.getLayerByName2(layerName)[0]
            if not layer.aq_parent.enableLicenseAgreement:
                return True
            if userName in layer.aq_parent.acceptedUserNames:
                return True
            else:
                return False
        except:
            logger.exception('Error')
        
    def acceptAgreementForLayer(self,layerName):
        """
        """                
        try:
            userName = self.getAuthneticatedUserName()
            layer = self.getLayerByName2(layerName)[0]
            layer.aq_parent.acceptedUserNames.append(userName)
            layer.aq_parent._p_changed = 1               
            transaction.savepoint(True)              
            return 1
        except:
            logger.exception('Error')
        
    def getAgreementForServerWithLayer(self, layerName, redirectURL,REQUEST=None):
        """
        @returns the agreement for the server with the given layer
        """        
        try:
            layer = self.getLayerByName2(layerName)[0]
            agreementtext = layer.aq_parent.licenseAgreement        
            return self.LegalDocument(layerName=layerName,license=agreementtext, redirectURL = redirectURL)
        except:
            logger.exception('Error')
    
    def getAuthneticatedUserName(self):    
        """
        @summary: returns the currently logged in username
        """        
        member =  self.portal_membership.getAuthenticatedMember()   
        return member.getUserName()                 

    def setOwnerPermissions(self):
        """
        """
        self.manage_permission("Copy or Move", roles=["Owner"], acquire=False)   
        self.manage_permission("Delete objects", roles=["Owner"], acquire=False)
        self.manage_permission("Take ownership", roles=["Owner"], acquire=False)
        return 1   
    
    def _buildServerLayerStructure(self,struct):
        """
        @summary: Uses the response from the universal mapserver's updateLayer to construct a server and layer structure in plone
        @param struct: the layer structure as gotten from the Universal MapServer's updateLayers method
        """        
        
        try:            
            sources = [x['source'] for x in struct]
            tmpDict = {}
            for source in sources:
                tmpDict[source[0] + source[1] + source[2]] = source
            sources = tmpDict.values()            
            
            for source in sources:
                # check if the organization exist            
                if not hasattr(self,source[2]):
                    self._setObject(source[2],Organization(source[2]))
                    
                organizationFolder = getattr(self,source[2])  
                organizationFolder.organization = source[2]
                # id is the wms source url combined with the organization
                id = source[2] + "__" + source[1].replace(':','_').replace('/','_').replace('&','').replace('?','').replace(' ','_').replace("="," ")
                # create the server folder
                if hasattr(organizationFolder,id):                     
                    organizationFolder.manage_delObjects([id])
                
                # XXX check if the organization exists
                organizationFolder._setObject(id, MapServer(id))
                
                server = getattr(organizationFolder,id)  
                server.manage_permission("View", roles=["Owner"], acquire=False)
                server.manage_permission("List folder contents", roles=["Owner"], acquire=False)
                
                logger.info("Create server : " + id)
                
                server.wmsSource = source[1]   
                server.wfsSource = source[0]       
                server.organization = source[2]
                
                for layer in struct:                    
                    if layer['source'][1] == source[1] and layer['source'][0] == source[0] and layer['source'][2] == source[2]:   
                        if not layer.has_key('uniqueName'):
                            continue                 
                        uniqueName = str(layer['uniqueName'])                        
                        server._setObject(uniqueName, MapLayer(uniqueName))
                        
                        logger.info("Create MapLayer : " + uniqueName)
                        tmpLayer = getattr(server,uniqueName)  
                        tmpLayer.manage_permission("View", roles=["Owner"], acquire=False)
                        tmpLayer.manage_permission("List folder contents", roles=["Owner"], acquire=False)
                        tmpLayer.sampleImage = layer['sampleImage']
                        tmpLayer.abstract = layer['abstract']
                        tmpLayer.keywords = layer['keywords']
                        tmpLayer.uniqueName = layer['uniqueName']
                        tmpLayer.geometryField = layer['geometryField']
                        tmpLayer.geometryType = layer['geometryType']
                        tmpLayer.title = layer['title']
                        tmpLayer.wfsSRS = layer['wfsSRS']
                        tmpLayer.wmsStyleName = layer['wmsStyleName']
                        tmpLayer.wfsBoundingBox = layer['wfsBoundingBox']
                        tmpLayer.fields = layer['fields']
                        tmpLayer.source = layer['source']
                        tmpLayer.error = layer['error']
                        tmpLayer.wmsQueryable = layer['wmsQueryable']
                        tmpLayer.wmsName = layer['wmsName']
                        tmpLayer.wfsName = layer['wfsName']
                        tmpLayer.wmsSRS = layer['wmsSRS']
                        tmpLayer.wmsTitle = layer['wmsTitle']
                        tmpLayer.wmsBoundingBox = layer['wmsBoundingBox']
                        tmpLayer.describeFeatureResponse = layer['describeFeatureResponse']    
                        tmpLayer.hasWFSLayer = layer['hasWFSLayer']    
                        tmpLayer.wmsXML = layer['wmsXML']
                        tmpLayer.wfsXML = layer['wfsXML']
                        tmpLayer.organization = layer['organization']                                    
                        
                        fieldDict = layer['fields']                    
                        for k in fieldDict.keys():
                            name = k
                            fieldType = fieldDict[k]                            
                            tmpLayer._setObject("gis_field_"+name, LayerField("gis_field_"+name))
                            
                            fieldObj = getattr(tmpLayer,"gis_field_" + name)                        
                            fieldObj.type = fieldType  
                            fieldObj.manage_permission("View", roles=["Owner"], acquire=False)                 
        except:            
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()            
            logger.exception('Error')
            

    def _fixSourceURL(self,source):
        """
        @summary: This is a utility method for cleaning up the source urls and changing forward slashes to back slashes
                    that are usually given in mapserver sources
        @param source: the gis resource url to clean
        @return: The slash converted url source
        """
        try:
            if source:            
                source = source.replace("\\","/")
                source = source.replace("?&","?")
                source = source.replace("&&","&")
                if source[-1] != '&' or source[-1] != '?':
                    if source.find('?') == -1:
                        source = source + "?"
                    else:
                        source = source + "&"     
            return source  
        except:
            logger.exception('Error')
            
            
    def clearSources(self):
        """
        @summary: deletes all the current sources
        """
        self.layerList = []
        self.sources = []
    
    security.declarePublic('addSource')
    def addSource(self,wfsResource,wmsResource, organization,REQUEST=None):
        """
        @summary: appends the given sources to the universal mapserver's sources
        @param wfsResource: the wfs url to the source
        @param wmsResource: the wms url to the source
        @return: status message if succeeds or a service exception if there was a failure
        """       
                   
        wfsResource = self._fixSourceURL(wfsResource)
        wmsResource = self._fixSourceURL(wmsResource)
        
        for source in self.sources:
            if (wfsResource, wmsResource, organization) == source:                    
                return
        self.sources.append((wfsResource, wmsResource, organization))    
        
        self._p_changed = 1               
        transaction.savepoint(True)
                
        return "Sources have been added"     
          
        
    def getSingleLegendGraphic(self,layers="",REQUEST=None):
        """
        @summary: Does a getLegendRequest for each of the layers and returns a single legend image for all
        @param layers: a pipe delimited list of layer names e.g city|river|country
        @return: a binary string containing the image data
        """        
        try:
            imgDataList = []
            layerList = layers.split("|")           
            if not layerList:
                return MapServerTemplates.ogcServiceException %("Exception occured with getSingleLegendGraphic request, No layer names given")       
            
            for layer in layerList:
                imgData = self.getLegendGraphic(layer,format="image/jpeg",width=20,height=20)
                if imgData.find("ServiceException") != -1:                
                    continue
                fCreate = StringIO.StringIO(imgData)
                tmpImg = Image.open(fCreate)
                fNew = StringIO.StringIO('')
                tmpImg.save(fNew,"PNG")            
                imgDataList.append(fNew.getvalue())            
            if not imgDataList:
                return MapServerTemplates.ogcServiceException %("Exception occured with getSingleLegendGraphic request, No legends could be retrieved")       
            
            compImg = self.getCompositeLegend(imgDataList)  
            if REQUEST:
                REQUEST.RESPONSE.setHeader("Content-type","image/png")  
            return compImg
        except:
            logger.exception('Error')
    
    def getCompositeLegend(self, imageDataList, x1 = None, x2 = None):
        '''
        Composes a legend image from several images. Using the images in
        imageDataList, they are cropped of "blank" pixels from the bottom up.
        The method then returns a composed legend image.
        '''
        try:
            images = []
            height = 0
            bottom = 0
            # get the largest with
            width = 1
            for image in imageDataList:
                img = Image.open(StringIO.StringIO(image))
                box = img.getbbox()
                if box[2] > width:
                    width = box[2] 
                     
            for image in imageDataList:
                img = Image.open(StringIO.StringIO(image))
                box = img.getbbox()
                bottom = self._findLastPixel(img, x1, x2) 
                if bottom:                    
                    img = img.crop((0,0,box[2],bottom))
                    tmpImg = Image.new("RGB",(width,bottom),(255,255,255))
                    tmpImg.paste(img,(0,0,box[2],bottom))                
                    images += [tmpImg]
                    height += img.size[1]            
            legend = Image.new('RGB', (width, height),(255,255,255))
            top = 0
            for image in images:
                legend.paste(image, (0, top, width, top+image.size[1]))
                top += image.size[1] 
            tmpIO = StringIO.StringIO('')
            legend.save(tmpIO,"PNG")
            resData = tmpIO.getvalue()            
            return resData
            
        except:            
            sio = StringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not get composite legend')            
            return MapServerTemplates.ogcServiceException %("Exception occured with getCompositeLegend request, check log for details %s" %trace)             
        return ''
    
    def _findLastPixel(self,img, x1 = None, x2 = None):
        box = img.getbbox()
        if box is None:
            box = (0,0,img.size[0],img.size[1])
        if not x1:
            x1 = 0
        if not x2:
            x2 = box[2]
        #use LL corner pixel as blank color
        blank = img.getpixel((0, box[3]-1))
        
        for y in range(box[3]-1, 0, -1):
            for x in range(x1, x2):
                if img.getpixel((x, y)) != blank:
                    return y
        return None
    
    def getLayerByName2(self,layerName):
        """
        """        
        try:            
            items =  self.objectItems()
            for i in items:
                if i[1].meta_type == 'Organization':
                    mapservers = i[1].objectItems()                
                    for mapserver in mapservers:
                        if mapserver[1].meta_type == 'MapServer':                
                            layerItems = mapserver[1].objectItems()
                            for layerItem in layerItems:
                                if layerItem[1].meta_type == 'MapLayer':  
                                    if layerItem[1].id == layerName:
                                        return [layerItem[1]]
            return [] 
#            mapServers = self.getMapServers()
#            #items =  self.objectItems()
#            for server in mapServers:
#                serverLayers = server.objectItems()
#                for lItem in serverLayers:
#                    if lItem[1].meta_type == 'MapLayer':  
#                        if lItem[1].id == layerName:
#                            return [lItem[1]]
#            return []    
        except:
            logger.exception('Error')
        
#        for i in items:
#            if i[1].meta_type == 'MapServer':                
#                serverItems= i[1].objectItems()
#                for sItem in serverItems:
#                    if sItem[1].meta_type == 'MapLayer':  
#                        if sItem[1].id == layerName:
#                            return [sItem[1]]
#        return []    
    
    def getLayerByName(self,layerName):
        """
        @summary:
        @param: the layer name/ id to search for
        @return: a list with result objects
        """        
        try:
            resList = []
            
            results = self.portal_catalog.searchResults(meta_type = "MapLayer", id = layerName)          
            for result in results: 
                layer = result.getObject()                
                resList.append(layer)            
            return resList 
        except:
            logger.exception('Error')
    
    def updateSecurityForSingleLayer(self,layerName):
        """
        @param layerName: the name of the layer to update
        """        
        try:
            resList = self.getLayerByName(layerName)
            if resList:
                layer = resList[0]
                securityDef = layer.security
                
                fieldDict = {}
                for f in layer.objectItems():
                    if f[1].meta_type == 'LayerField':
                        fName = f[1].id
                        fieldDict[fName] = dict(f[1].security)
                        
                securityDef['fields'] = fieldDict                
                self.sm.setSecurityDefinition(securityDef,singleSource=1,name=layerName)                
                return 1         
            else:
                return 0  
        except:
            logger.exception('Error')    
        
    def getServerPingResults(self):
        """
        @summary: sends ping requests to all the servers and layers in the sub structure
        """
        
        try:
            results = {}   # too keep the results of each of the sub servers
            
            items =  self.objectItems()
            for i in items:
                if i[1].meta_type == 'Organization':
                    organizationItems = i[1].objectItems()
                    for organizationItem in organizationItems:
                        if organizationItem[1].meta_type == 'MapServer':
                            server = organizationItem[1]       
                            serverPingRes = server.pingServer()
                            if serverPingRes[1].find("Server Unavailable") != -1:
                                results[organizationItem[1].title] = {'Server':['Server not available','Server not available']}                 
                            else:
                                resDict = server.pingAllLayers()
                                results[organizationItem[1].title] = resDict                    
            return results          
        except:
            logger.exception('Error')
    
         
    
    def getSecurityStructureCount(self):
        """
        @summary: gets the number of layers in the security manager security structure
        @return: the number of layers in the security manager's security structure
        """        
        try:            
            res = self.sm.getSecurityDefinitionCount()
            return res
        except:
            logger.exception('Error')
            return 0
    
    def checkComponentStatuses(self):
        """
        @summary: Checks that all the components are running e.g [1,0,0,1]
        The sequence is [universalMapServer,LayerRegistry,SecurityManager,RequestresponseTranslator]
        @return: a list with a 1 or a 0 defining if the soap service is running or not. 1 is for running.
        """
        responseList = [1,1,1,1]
        return responseList     
    
    def deleteSourceViaURL(self, wms, wfs, organization, REQUEST=None):
        """
        @summary:
        @param wms:
        @param wfs:
        @param organization:
        @param REQUEST:
        @return:
        """      
        self.deleteSource(source=[wfs,wms,organization])        
        
        return 1
    
    def printLayerStructure(self,REQUEST=None):
        """
        """        
                
        return 1        
    
    def getMapServers(self):
        """
        @summary: searches and returns all MapServer objects         
        @return: a list with result objects
        """        
        try:
            resList = []        
            results = self.portal_catalog.searchResults(meta_type = "MapServer")          
            for result in results: 
                mapServer = result.getObject()                
                resList.append(mapServer)            
            return resList 
        except:
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()            
            logger.exception('Error')
    
    def deleteSource(self,source):
        """
        @summary: this will call updateLayers on the LayerRegistry after removing all layers from the given source.
                Called from the mapserver facade plone interface.
        @param source: a list containing [wfsSource,wmsSource], this list is considered a source        
        @return: the mapserver facade manage sources interface page template
        """    

        try:
            mapServers = self.getMapServers()
            
            for mapServer in mapServers:            
                layerItems = mapServer.objectItems()
                
                for layerItem in layerItems:
                    if layerItem[1].meta_type == 'MapLayer':     
                        layer = layerItem[1]     
                        if (layer.source[1] == source[1]) and (layer.source[0] == source[0]) and (layer.source[2] == source[2]):
                            parent = mapServer.aq_parent
                            parent.manage_delObjects([mapServer.id])                          
                            break      
            
            layerList = self.getLayerStructureFromFacadeObjects()           
             
            self.ums.deleteSource(source)     
            self.ums.setLayerList(layerList)               
            self.lr.setLayerList(layerList)   
            logger.info("Delete Source")
            return 1  
        except:
            logger.exception('Error')
    
    security.declarePublic('describeFeatureType')
    def describeFeatureType(self,layerName):
        """
        @summary: WFS describeFeatureType is called on the RequestResponseTranslator. This request was forwarded from the 
        wfswms entry point on the mapserver facade.
        @param layerName: the name of the layer to be described
        @return: xml schema describing the layer. In case of an error a service exception xml will be returned.      
        """ 
        try:
            userName = self.getAuthenticatedUser()            
            response = self.rrt.describeFeatureType(userName, layerName) 
            return response            
        except:           
            sio = StringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not describeFeatureType')            
            return MapServerTemplates.ogcServiceException %("Exception occured with describeFeatureType request, check log for details %s" %trace) 
    
    
    security.declarePublic('getCurrentLayerRegistryLayers')
    def getCurrentLayerRegistryLayers(self):
        """
        @summary: call getLayerStructure on the layerRegistry SOAP Service to get an xml string off all layers in the layer regsitry.
                This is used from the mapserver facade management interface.
        @return: returns a dict with source url as key and layer names for that source as a list of names values
        """        
        try:
            layerStructure = self.getLayerStructure(unfiltered=1)    
            if not type(layerStructure) == list:
                if (layerStructure.find("ServiceException") != -1) or (layerStructure.strip() == ''):
                    if (layerStructure.find("describeFeatureResponse") == -1) or (layerStructure.strip() == ''):
                        return {}
                #return {'No Sources/Layers':['Please call update layers on Layer Registry']}
            struct = layerStructure
            layerDict = {}        
            for layer in struct:
                source = layer['source'][1]            
                if layer['error']:
                    name = layer['error']
                    if layerDict.has_key(source):
                        layerDict[source].append(name)  
                    else:
                        layerDict[source] = [name]   
                else:
                    name = layer['wmsName']
                    if layerDict.has_key(source):
                        layerDict[source].append(name)  
                    else:
                        layerDict[source] = [name]
            return layerDict
        except:
            logger.exception('Error')
       
    security.declarePublic('getServerStatus')
    def getServerStatus(self):
        """
        @summary: This checks that the urls given at creation is valid or that all servers are running.
                This is called from the status tab of the mapserver facade.
                The request times for each of the status requests are recorded and used as ping times
        @return: a dict with a list containing status and ping time as value
        """            
        struct = {}
        struct['univeralMapServer'] = ['Running','0']    
        struct['layerregistry'] = ['Running','0']    
        struct['securityManager'] = ['Running','0']        
        struct['requestResponseTranslator'] = ['Running','0']                           
        return struct 
    
    def getLayerCount(self):
        """
        @summary: Does a call on the layer registry to get the number of layer that are in it.
        @return: a number count of the layers in the layer registry.
        """                             
        count = len(self.layerStructure)    
        return count    
    
    def getLayerStructureFromFacadeObjects(self,serverName=None):
        """
        @summary: builds the layerList from the server and layer objects in plone in the sub structure of the map server facade
        @return: a list of dict objects each containing layer info.
        """        
        try:
            layerList = []        
            #items =  self.objectItems()
            items = self.getMapServers()        
            for i in items:
                if i.meta_type == 'MapServer':                
                    serverItems= i.objectItems()
                    for sItem in serverItems:
                        if sItem[1].meta_type == 'MapLayer':  
                            l = sItem[1]
                            layerStructure = {'uniqueName': l.uniqueName ,'geometryField':l.geometryField ,
                                'geometryType':l.geometryType ,'wfsName':l.wfsName ,
                                'title':l.title ,'abstract':l.abstract ,'keywords':l.keywords ,'wfsSRS':l.wfsSRS ,'wmsStyleName':l.wmsStyleName ,
                                'wfsBoundingBox':l.wfsBoundingBox ,'fields':l.fields ,'source':l.source ,'error':l.error,
                                'wmsQueryable':l.wmsQueryable ,'wmsName':l.wmsName ,'wmsSRS':l.wmsSRS ,'wmsTitle':l.wmsTitle ,
                                'wmsBoundingBox':l.wmsBoundingBox ,'describeFeatureResponse':l.describeFeatureResponse ,
                                'sampleImage':l.sampleImage,'hasWFSLayer':l.hasWFSLayer,'wmsXML':l.wmsXML,'wfsXML':l.wfsXML, 'organization':l.organization}                            
                        layerList.append(layerStructure) 
                  
            return layerList 
        except:
            logger.exception('Error')
    
    def getFacadeLayerCount(self):
        """
        @summary: Loops through facade structure and counts the amount of map layers
        @return: number of layers in facade
        """
        try:
            count = 0
            items =  self.objectItems()
            for i in items:
                if i[1].meta_type == 'Organization':
                    organization = i[1]
                    organizationItems = organization.objectItems() 
                    for organizationItem in organizationItems:                    
                        if organizationItem[1].meta_type == 'MapServer':                
                            serverItems= organizationItem[1].objectItems()
                            for sItem in serverItems:
                                if sItem[1].meta_type == 'MapLayer':  
                                    count += 1               
            return count 
        except:            
            sio = StringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()    
            logger.exception('Error')
            return count
        
    def updatePloneLayersSecurityFromSecurityManager(self):
        """
        """
        try:            
            securityStruct = self.sm.getSecurityDefinition()                        
            # update layers and fields wityh security from the securityManager
            items =  self.objectItems()
            for i in items:
                if i[1].meta_type == 'MapServer':                
                    serverItems= i[1].objectItems()
                    for sItem in serverItems:
                        if sItem[1].meta_type == 'MapLayer':  
                            l = sItem[1]                            
                            if securityStruct.has_key(l.uniqueName):                            
                                l.setSecurityVarOnly(securityStruct[l.uniqueName])                                
        except:
            logger.exception('Error')
    
    def updateSecurityManager(self):
        """
        @summary:
        @return:
        """          
        try:
            secStruct = {}
            items =  self.objectItems()
            for i in items:
                if i[1].meta_type == 'MapServer':                
                    serverItems= i[1].objectItems()
                    for sItem in serverItems:
                        if sItem[1].meta_type == 'MapLayer':  
                            l = sItem[1]
                            secStruct[l.uniqueName] = dict(l.security)
                            secStruct[l.uniqueName]['fields'] = []
                            
                            fieldDict = {}
                            for f in l.objectItems():
                                if f[1].meta_type == 'LayerField':
                                    fName = f[1].id
                                    fieldDict[fName] = dict(f[1].security)
                                    
                            secStruct[l.uniqueName]['fields'] = fieldDict                                
            
            secStruct = dict(secStruct)            
            self.sm.setSecurityDefinition(secStruct)
            return self.MapServerFacade_Status(self)       
        except:
            logger.exception('Error')
        
    security.declarePublic('getSources')
    def getSources(self):
        """                
        """
        return self.sources
    
    def getTimeoutStructure(self):
        """        
        """
        return self.timeouts    
    
    security.declarePublic('getFilteredSourceStructure')
    def getFilteredSourceStructure(self):
        """
        @summary: calls getSources on universal mapserver and converts the xml to a python structure
        @return: list of tuples containing wms and wfs server sources
        """         
        returnStructure = [] 
        try:            
            tmpStruct = self.sources   
            # loop through the servers and remove servers from list that are not owned by current user
            serverList = []
            serverWMSSourceList = []
            #items =  self.objectItems()
            items =  self.getMapServers()
            for i in items:
                if i.meta_type == 'MapServer':                    
                    server = i         
                    serverList.append(server)
            
            for server in serverList:
                serverWMSSourceList.append(server.wmsSource.lower().strip())                
                    
            for serv in serverList:                
                for source in tmpStruct:                    
                    if serv.wmsSource.lower().strip() == source[1].lower().strip():
                        if serv.userIsOwner():  
                            if source not in returnStructure:                                                          
                                returnStructure.append(source)   
                    if source[1].lower().strip() not in serverWMSSourceList:
                        returnStructure.append(source) 
                        
            if not serverList:                
                return tmpStruct                        
                      
            logger.info("getSourceStructure")
            return returnStructure
            
        except:
            logger.exception('Error')            
            sio = StringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()  
            return [['Universal Map Server is not running.','%s.' %trace]]    
        
    security.declarePublic('getLayerStructure')
    def getLayerStructure(self,unfiltered=0,wmsSource=None,layerNames=None, organization=None):
        """        
        """  
        try:     
            userName = self.getAuthenticatedUser()
            layerStructure = self.rrt.getLayerStructure(userName,unfiltered,wmsSource=wmsSource,layerNames=layerNames,organization=organization)       
            return layerStructure    
        except:            
            sio = StringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()            
            logger.exception('Could not getLayerStructure')
            return MapServerTemplates.ogcServiceException %("Exception occured with getLayerStructure request, check log for details %s" %trace)
    
    security.declarePublic('getSecurityDefinition')
    def getSecurityDefinition(self,REQUEST=None):
        """        
        """     
        return self.securityDefinitions
    
    security.declarePublic('getLegendGraphic')
    def getLegendGraphic(self,layer,format="image/png",width=20,height=20,sld="",sld_body=""):
        """
        @summary: does a wms getLegendGraphic request for the given layerName 
                  and returns the image data
        @return: the legend image data or a service exception if an error occurs
        @param layer: the name of the layer to get the legend image for
        @param format: the image format in which the legend image must be (gif,png,bmp,jpg)
        @param width: int defining the width of the legend image
        @param height: int defining the height of the legend image
        @param sld: the url to the sld for the layer
        @param sld_body : the fisical sld document string
        """     
        try:   
            userName = self.getAuthenticatedUser()        
            paramDict = {'layer':layer,'width':width,'height':height,
                        'format':format,'sld':sld,'sld_body':sld_body}
            
            response = self.rrt.getLegendGraphic(userName, paramDict)
            if response.find("ServiceException") != -1:
                return response
            else:
                return binascii.a2b_base64(response)              
        except:            
            sio = StringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not getLegendGraphic')
            return MapServerTemplates.ogcServiceException %("Exception occured with getLegendGraphic request, check log for details %s" %trace)
    
    security.declarePublic('getAuthenticatedUser')
    def getAuthenticatedUser(self):
        """
        @summary: this is a zope specific method to get logged in user name
        @return: a list of roles for the current logged in user
        """        
        try:
            member =  self.portal_membership.getAuthenticatedMember()            
            return member.getRoles()
        except:
            return 
        return "Anonymous"
    
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
            logger.exception('Error')
            return False    

    security.declarePublic('getMap')
    def getMap(self,layers,width="400",height="400",transparent="true",styles="",srs="EPSG:4269",
                bbox="-180,-90,180,90",format="image/png",bgcolor="0xFFFFFF",exceptions="XML",time="",elevation="",sld="",sld_body="",REQUEST=None):
        """
        @summary: getMap is called on the RequestResponseTranslator
        @param layers: is a string of comma separated layer names
        @param width: the width of the map to draw
        @param height: the height of the map to draw
        @param transparent: to make the background color transparent or not
        @param styles: a comma separated list of styles to draw the layers in
        @param srs: the spatial reference system to use for map
        @param bbox: the extent of the map to draw
        @param format: the format to return the image in
        @param bgcolor: the background color of the image
        @param exceptions: the format in which to return exception info
        @param time: time info for the layer
        @param elevation: elevation info for the layer
        @param sld: the layer style descriptor to use (url to the for the sld)
        @param sld_body: the sld document body
        
        """        
        try:            
            userName = self.getAuthenticatedUser()            
            paramDict = {'layers':layers,'width':width,'height':height,'transparent':transparent,
                        'styles':styles,'srs':srs,'bbox':bbox,'format':format,'bgcolor':bgcolor,
                        'exceptions':exceptions,'time':time,'elevation':elevation,'sld':sld,'sld_body':sld_body}            
             
            mapData = self.rrt.getMap(userName, paramDict)
            if mapData.find("ServiceException") == -1:           
                mapData = binascii.a2b_base64(mapData)
            else:
                return mapData                
            return mapData        
        except:            
            sio = StringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not getMap')
            return MapServerTemplates.ogcServiceException %("Exception occured with getMap request, check log for details %s" %trace)
            
    security.declarePublic('getCapabilities')
    def getCapabilities(self,service,version="1.0.0",updatesequence="empty"):
        """ 
        @summary: getCapabilities is called on the RequestResponseTranslator 
        @param service: can be wms of wfs    
        @param version: any valid version for the given wms or wfs service
        @param updatesequence: not currently used
        @return: gml xml string describing the service or a service exception if an error occurs
        """
        try:
            facadeURL = self.absolute_url() + "/wfswms?"
            userName = self.getAuthenticatedUser()             
            response = self.rrt.getCapabilities(userName, service, facadeURL)
            return response        
        except:            
            sio = StringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not getCapabilities')
            return MapServerTemplates.ogcServiceException %("Exception occured with getCapabilities request, check log for details %s" %trace)
    
    security.declarePublic('getFeatureInfo')
    def getFeatureInfo(self,query_layers,x,y,width,height,bbox,layers,srs,format,styles='',
                        version="1.0.0",info_format="text/xml",feature_count=5,x2=None,y2=None):
        """
            @summary: A WMS getFeature request. getFeatureInfo is called on the RequestResponseTranslator
            @param request: will always be GetFeatureInfo  
            @param query_layers: a comma separated string of layer names to be queried
            @param width: the width of the map being idetified on
            @param height: the height in pixels of the map being identified on
            @param bbox: the current extent of the map being identified on e.g "-180,-90,180,90"
            @param layers: the current visible layers in the map being identified on e.g "city,county,rails"
            @param srs: the current spatial reference system the map is in e.g "EPSG:4269"
            @param format: the format the current map is in e.g "image/png"
            @param styles: the styles for each layers that was rendered on the map image
            @param version: the version of the wms service used
            @param info_format: the format in which results must be returned
            @param feature_count: the number of results to return
            @return: an xml getFeatureInfo response from the requestResponseTranslator or a service exception if an error occurs
        """
        try:
            userName = self.getAuthenticatedUser()
            params = {'queryLayers':query_layers.split(","),'i':x,'j':y,'feature_count':feature_count,'width':width,'height':height,
                        'bbox':bbox.split(","),'layers':layers,'srs':srs,'format':format,'styles':styles,'version':version,'info_format':info_format}
            
            if (x2 != None) and (y2 != None):
                params['x2'] = x2
                params['y2'] = y2                
             
            response = self.rrt.getFeatureInfo(userName,params)
            return response        
        except:            
            sio = StringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not getFeatureInfo')
            return MapServerTemplates.ogcServiceException %("Exception occured with getFeatureInfo request, check log for details %s" %trace)
    
    security.declarePublic('getFeature')
    def getFeature(self,**kwargs):
        """
        @summary: getFeature is called on the RequestResponseTranslator and does a wfs getFeature request
        @param kwargs: can contain 'propertyname','featureversion','maxfeatures','typename','featureid','filter','bbox','service' 
        depending on the type of getfeature request that is being done.
        @param propertyname: used in a attribute query to define which property too search
        @param featureversion: optional, tells the server which version of the feature to return
        @param maxfeatures: defines the max number of features to return
        @param typename: the name of the layer to search on
        @param featureid: the feature's id to search for
        @param filter: a filter string defining search parameters
        @param bbox: the extent of the layer to search, is used with filter
        @param service: service will always be "wfs"        
        @return: a gml string with search results or a service exception if a error occurs        
        """
        try:
            userName = self.getAuthenticatedUser()                      
            #params = {'maxfeatures':20}
            params = {}
            params.update(kwargs)
            data = self.rrt.getFeature(userName,params)  
            
            tmpDom = minidom.parseString(data)
            elms = tmpDom.getElementsByTagName('wfs:FeatureCollection')             
            if elms:                    
                resource = elms[0].getAttribute('xsi:schemaLocation')
                resourceList = resource.split(" ")
                newResourceList = []
                for resource in resourceList:
                    if resource.find('DescribeFeatureType') != -1:
                        path =  self.absolute_url() + '/wfswms?'   
                        tmpResource = path + WFS_DESCRIBEFEATURETYPE_EXTENSION + '&typename=' + params['typename']
                        newResourceList.append(tmpResource)
                    else:
                        newResourceList.append(resource)                        
                elms[0].setAttribute('xsi:schemaLocation',string.join(newResourceList,' ')) 
                data = str(tmpDom.toxml())
            
            return data
        except:           
            sio = StringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not getFeature')
            return MapServerTemplates.ogcServiceException %("Exception occured with getFeature request, check log for details %s" %trace)
        
    def getLayerRegistryLayerNames(self):
        """
        @summary: does a call to the layer registry to get the layer structure and build a list of layer names from that structure
        @return: a list of layer names in the layer registry, the wmsName is used as layer name and not he unique name.
                a service exception is returned if an error occurs.
        """
        try:
            struct = self.getLayerStructure()
            if type(struct) != list:        
                if struct.find("ServiceException") != -1: 
                    if struct.find("describeFeatureResponse") == -1:
                        return struct              
            layerList = []        
            for layer in struct:                
                name = layer['wmsName']
                layerList.append(name)        
            return layerList 
        except:
            logger.exception('Error')
    
    def getLayerRegistryUniqueNames(self):
        """
        @summary: does a call to the layer registry to get the structure and build a list of unique layer names in the structure
        @return: a list of unique layer names in the layer registry. or a service exception if an error occurs
        """
        try:
            struct = self.getLayerStructure()     
            if type(struct) != list: 
                if struct.find("ServiceException") != -1:   
                    if struct.find("describeFeatureResponse") == -1:
                        return struct       
            
            layerList = []        
            for layer in struct:
                name = layer['uniqueName']
                layerList.append(name)        
            return layerList 
        except:
            logger.exception('Error')
    
    def getGeometryColumnForLayerName(self,layerName):
        """
        @summary:
        @param layerName: the name of the layer to get the geometry column for
        @return: str geometry column for the layer name given
        """        
        colName = self.lr.getGeometryColumnForLayerName(layerName)        
        return colName                
    
    def getFirstLayerFromLayerRegistry(self):
        """
        @summary: This will do a request to the layer registry and get the first layer in the structure and return it
        @return: Returns the first layer structure found in the layer registry layer structure. or a service exception if an error occurs
        """
        try:
            struct = self.getLayerStructure()        
            if type(struct) != list:
                if struct.find("ServiceException") != -1: 
                    if struct.find("describeFeatureResponse") == -1:
                        return struct              
            if struct:
                return struct[0][0]
            else:
                return None 
        except:
            logger.exception('Error')
      
    
    security.declarePublic('setSecurityDefinition')
    def setSecurityDefinition(self,definition):
        """
        @summary: setSecurityDefinition is called on the SecurityManager
        @param definition: is a xml string defining the security structure        
        """
        
        self.securityDefinitions = definition           
    
    security.declarePublic('setSources')
    def setSources(self,sources):
        """
        @summary: value is set on the universal mapserver
        @param sourcesXML: an xml string in xmlrpc format that describes a list of tuples containing wfs and wms server resources        
        """
        self.sources = sources
    
    def testWMSGetCapabilities(self,REQUEST=None):
        """
        @summary: this is a test method uised in the test tab of the mapserver facade and
        calls self.getCapabilities
        @return: a wms getCapabilities xml reponse string
        """ 
        REQUEST.RESPONSE.setHeader("Content-type","text/xml")
        xmlStr = '''<?xml version='1.0' encoding="ISO-8859-1" standalone="no" ?>
<!DOCTYPE WMT_MS_Capabilities SYSTEM "http://schemas.opengeospatial.net/wms/1.0.0/capabilities_1_0_0.dtd"> \n\n'''        
        
        res = self.getCapabilities("wms")        
        index = res.find('<WMT_MS_Capabilities version="1.1.1">')
        if index != -1:
            res = res[index:]
            res = xmlStr + res
            return res                
        else:
            return res        
    
    def testWFSCapabilities(self,REQUEST=None):
        """
        @summary: this is a test method uised in the test tab of the mapserver facade and
        calls self.getCapabilities with a wfs service
        @return: a wfs getCapabilities xml reponse string
        """
        REQUEST.RESPONSE.setHeader("Content-type","text/xml")        
        res = self.getCapabilities("wfs")
        return res         
    
    def testGetMap(self,REQUEST=None):
        """
        @summary: this is a test method uised in the test tab of the mapserver facade and
        calls self.getMap with the first 10 layers from the layer registry
        @return: a png image binary data, or a service exception if an error occurs
        """
        names = self.getLayerRegistryUniqueNames()        
        REQUEST.RESPONSE.setHeader("Content-type","text/xml")
        if type(names) == list and names:
            if len(names) > 10:
                names = names[0:10]
            REQUEST.RESPONSE.setHeader("Content-type","image/png")
            layers = string.join(names,',') 
            return self.getMap(layers)                     
        else: 
            REQUEST.RESPONSE.setHeader("Content-type","text/xml") 
            return names 
    
    def testLegendGraphic(self,REQUEST=None):
        """
        @summary: this is a test method uised in the test tab of the mapserver facade and
        calls self.getLegendGraphic with the first layer from the layer registry
        @return: a png image binary data, or a service exception if an error occurs
        """        
        #names = self.getLayerRegistryLayerNames()
        names = self.getLayerRegistryUniqueNames()
        if type(names) == list and names:
            REQUEST.RESPONSE.setHeader("Content-type","image/png")
            return self.getLegendGraphic(names[0])         
        else:
            REQUEST.RESPONSE.setHeader("Content-type","text/xml") 
            return names           
        
    def testGetFeature(self,REQUEST=None):
        """
        @summary: this is a test method uised in the test tab of the mapserver facade and
        calls self.getFeature with the first layer from the layer registry
        @return: an xml getfeature response string, or a service exception if an error occurs
        """
        names = self.getLayerRegistryUniqueNames()
        #names = self.getLayerRegistryLayerNames()
        REQUEST.RESPONSE.setHeader("Content-type","text/xml")
        if type(names) == list and names:            
            colName = self.lr.getGeometryColumnForLayerName(names[0])
            if colName.find("ServiceException") != -1:
                return colName                
            
            filter = '<ogc:Filter xmlns:ogc="http://ogc.org" xmlns:gml="http://www.opengis.net/gml"><ogc:BBOX><ogc:PropertyName>%s</ogc:PropertyName><gml:Box srsName="http://www.opengis.net/gml/srs/epsg.xml"><gml:coordinates>-180,-90 180,90</gml:coordinates></gml:Box></ogc:BBOX></ogc:Filter>' %colName
            filter = urllib.quote(filter)
            params = {'filter':filter,'typename':names[0],'maxfeatures':1}
            #res = self.getFeature(typeName=names[0],filter,maxFeatures=1)
            res = self.getFeature(**params)
            return res
        else:             
            return names               
    
    def testDescribeFeatureType(self,REQUEST=None):
        """
        @summary: this is a test method uised in the test tab of the mapserver facade and
        calls self.describeFeatureType with the first layer from the layer registry
        @return: a wfs descridefeatureType xml response
        """
        #names = self.getLayerRegistryLayerNames()
        names = self.getLayerRegistryUniqueNames()
        REQUEST.RESPONSE.setHeader("Content-type","text/xml")
        if type(names) == list and names:
            res = self.describeFeatureType(names[0])        
            return res                 
        else:            
            return names   
        
    def testDescribeFeatureTypeForLayerName(self,REQUEST=None):
        """
        @summary: this is called from the layers tab in the facade interface and does 
        a DescribeFeatureType request for the given layer name.
        @param name: passed in the REQUEST parameter, the name of the layer in the describefeaturetype request
        @return: a describefeaturetype response xml string for the given layer name
        """
        
        name = ""
        if REQUEST:
            if REQUEST.form.has_key('name'):                
                REQUEST.RESPONSE.setHeader("Content-type","text/xml")
                layers = self.getLayerStructure()                
                for layer in layers:
                    #if layer['wmsName'] == REQUEST['name']:
                    if layer['wfsName'] == REQUEST['name']:
                        name = layer['uniqueName']        
                        break
                
                if name == "":
                    return MapServerTemplates.ogcServiceException %("You do not have permissions to view the requested layer")                    
                res = self.describeFeatureType(name)        
                return res         
        return name       
    
    def testGetLegendGraphicForLayerName(self,REQUEST=None):
        """
        @summary: this is called from the layers tab in the facade interface and does 
        a GetLegendGraphic request for the given layer name.
        @param name: passed in the REQUEST parameter, the name of the layer in the GetLegendGraphic request
        @return: a GetLegendGraphic response xml string for the given layer name
        """
        name = ""
        if REQUEST:
            if REQUEST.form.has_key('name'):
                layerStructure = self.getLayerStructure()
                layers = layerStructure
                for layer in layers:
                    if layer['wmsName'] == REQUEST['name']:
                        name = layer['uniqueName']   
                        break
                REQUEST.RESPONSE.setHeader("Content-type","image/png")             
                if name == "":
                    return MapServerTemplates.ogcServiceException %("You do not have permissions to view the requested layer")                    
                return self.getLegendGraphic(name) 
        return 1
    
    def testGetFeatureInfo(self,REQUEST=None):
        """
        @summary: Does a getFeatureInfo request on the first layer found in the layerRegistry layer structure.
        Called from the test tab on the facade interface.
        @return: a getFeatureInfo xml response string
        """
        #get the first layer in the layer structure of the layerRegistry
        #get attributes from that layer
        #getFeatureInfo(self,query_layers,x,y,width,height,bbox,layers,srs,format,styles='',version="1.0.0",info_format="text/xml",feature_count=5)
        REQUEST.RESPONSE.setHeader("Content-type","text/xml")
        fLayer = self.getFirstLayerFromLayerRegistry()
        if fLayer == None:
            return MapServerTemplates.ogcServiceException %("Could not find a layer in the layer registry \n or the layer registry is not running.")
        layerName = fLayer['uniqueName']
        extent = fLayer['wmsBoundingBox']
        x = 100
        y = 100
        width = 300
        height = 300
        bbox = str(extent[0]) + ',' + str(extent[1]) + ',' + str(extent[2]) + ',' + str(extent[3])
        layers = layerName
        srs = fLayer['wmsSRS']
        format = 'image/png'        
        res = self.getFeatureInfo(layerName,x,y,width,height,bbox,layers,srs,format)            
        return res   
    
    def updateSingleSource(self, wfs, wms, organization, REQUEST=None):
        """
        @summary:
        @param wfs: the url for the wfs source
        @param wms: the url for the wms source
        @param REQUEST: zope request object dict
        @return: 1 if there were no errors or a traceback in case of failure
        """       
        
        res = self.updateLayers(singleSource=[wfs,wms,organization])
        return res      
    
    security.declarePublic('updateLayers')
    def updateLayers(self,singleSource=None,REQUEST=None):
        """
        @summary: triggeres a request to all sources to update/reload/create layers.
        updateLayers is called on the universal mapserver which returns the xml structure for the layers which
        is used to update the layer registry with.
        This method is also used to trigger the building of the plone/zope server and layer structure.
        @param singleSource: a list containing [wfsSource,wmsSource]. This is optional
        If a value is given then only the source given wil be updated, else all sources will be updated.
        @return: returns to the calling web page. Returns an xml service exception if an error occurs.
        """            
        try: 
            if singleSource: 
                layerList = self.ums.updateLayers(singleSource)                              
            else:
                layerList = self.ums.updateLayers() 
            # use reponse to generate the servers and its layers in facade folder
            if type(layerList) != list:
                if (layerList.find('ServiceException') != -1) and (layerList.find('describeFeatureResponse') == -1):
                    return layerList               
            
            self._buildServerLayerStructure(layerList)    
            self.lr.updateLayers(layerList)
            logger.info("updateLayers" )
            return 1
        except:            
            sio = StringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not updateLayers')
            return MapServerTemplates.ogcServiceException %("Exception occured with updateLayers request, check log for details %s" %trace)
        
    def _getFilterFromGetFeatureXML(self,xml):    
        d = minidom.parseString(xml)
        elms = d.getElementsByTagName('ogc:Filter')
        if not elms:
            elms = d.getElementsByTagName('ogc:filter')
        if not elms:
            elms = d.getElementsByTagName('Filter')
        if not elms:
            elms = d.getElementsByTagName('filter')
        if not elms:    
            return ''        
        return elms[0].toxml()
    
    def _getTypeNameFromGetFeatureXML(self,xml):
        """
        """            
        try:
            xml = xml.replace("\n","").replace("\r","")          
            tIndex = xml.find('typename="')
            if tIndex == -1:
                tIndex = xml.find('typeName="')
            if tIndex == -1:
                tIndex = xml.find('TYPENAME="')        
            if tIndex == -1:
                return ''    
            tmpXML = xml[tIndex+10:]
            qindex = tmpXML.find('"')
            typeName = tmpXML[0:qindex]  
            return typeName      
        except:
            logger.exception('Error')
    

    def checkSyncState(self):
        """
        """
        
        try:
            statusDict = self.getServerStatus()
            for status in statusDict.values():
                if status[0].find("Not Running") != -1:
                    return
                
            layerRegistryCount = self.getLayerRegistryLayerCount()            
            securityStructureCount = self.getSecurityStructureCount()            
            layerRegistryCount = self.getLayerRegistryLayerCount()
            # check the security layer count
            
            if layerRegistryCount != securityStructureCount:
                self.updateSecurityManager()        
    
            return 1    
        except:
            logger.exception('Error')
            
            
    def dummySLD(self,REQUEST=None):
        """
        """                  
            
        return SLDTemplates.dummySLD  

    security.declarePublic('wfswms')
    def wfswms(self,REQUEST=None):
        """
        @summary: This is the global entry point for all the ogc requests
                  All requests will be forwarded to the correct methods.
                  If no valid request type is found in the request parameters the 
                  method will return a service exception xml string
        @return: the response to the type of request passed
        @param REQUEST: the REQUEST parameter can contain any valid OGC wfs and wms request paramete pairs.
        The only types catered for are:
            WMS: getMap,getCapabilities,getFeatureInfo,getLegendGraphic
            WFS: getCapabilities,getFeature,DescribeFeatureType
        """       
        
        try:                        
            content = ""
            fDict = REQUEST.form          
            fKeys = fDict.keys()
            for k in fKeys:
                if k.lower().find("getfeature") != -1:
                    content = k +"="+ REQUEST.form[k]         
            
            if content:            
                typeName = self._getTypeNameFromGetFeatureXML(content)
                if typeName == None:
                    return 'Type Name was None'
                filter = self._getFilterFromGetFeatureXML(content)            
                REQUEST.form['typename'] = typeName
                REQUEST.form['service'] = 'wfs'
                REQUEST.form['request'] = 'getfeature'
                REQUEST.form['version'] = '1.0.0'
                REQUEST.form['filter'] = filter            
            
            getMapParamList = ['width','height','transparent','styles','srs','bbox','format','bgcolor','exceptions','time','elevation','sld']
            getLegendGraphicParamList = ['format','width','height','sld','sld_body']                 
            
            # lower the request 
            if REQUEST == None:  
                REQUEST.RESPONSE.setHeader("Content-type","text/xml")      
                return MapServerTemplates.ogcServiceException %'Nothing valid found in request'            
            
            formDict = REQUEST.form
            newRequest = {}
            for k in formDict.keys():
                try:
                    if type(k) == str:
                        lowerKey = k.lower()
                        value = formDict[k]
                        if lowerKey == 'request' and type(value) in [type([]),type(())]:
                            #TODO: some clients passes multiple values for request - check this ???
                            value = value[0]
                        newRequest[lowerKey] = value
                except:
                    pass       
                       
            requestType = ''
            if newRequest.has_key('request'):            
                requestType = newRequest['request'].lower()         
           
            #wms requests
            if requestType == 'getmap':            
                layers = newRequest['layers']            
                for k in newRequest.keys():
                    if not k in getMapParamList:
                        del newRequest[k]      # only include valid params 
                
                data = self.getMap(layers,**newRequest)  
                return data            
            
            if requestType == 'getfeatureinfo':
                paramList = ['query_layers','x','y','width','height','bbox','layers','srs','format']#,'styles']
                paramListAll = ['query_layers','x','y','x2','y2','width','height','bbox','layers','srs','format','styles','version','info_format','feature_count']
                # filter the request keys to valid getFeatureInfo parameters
                for k in newRequest.keys():
                    if not k in paramListAll:
                        del newRequest[k]
               
                # check for all the requered parameters in the request
                tmpRequest = {} # dict for the kwargs
                for k in newRequest.keys():
                    if not k in paramList:
                        tmpRequest[k] = newRequest[k]  
                
                for param in paramList:
                    if not param in newRequest.keys():
                        REQUEST.RESPONSE.setHeader("Content-type","text/xml")
                        return MapServerTemplates.ogcServiceException %("Invalid getFeatureInfo Request. Parameter %s was not passed" %param)    
                            
                res = self.getFeatureInfo(newRequest['query_layers'],newRequest['x'],newRequest['y'],newRequest['width'],newRequest['height'],newRequest['bbox'],newRequest['layers'],newRequest['srs'],newRequest['format'],**tmpRequest)                            
                return res
                                    
            if requestType == 'getlegendgraphic':
                paramList = ['layer']
                for param in paramList:
                    if not param in newRequest.keys():
                        REQUEST.RESPONSE.setHeader("Content-type","text/xml")
                        return MapServerTemplates.ogcServiceException %("%s not found in request parameters." %(param))
                layerName = newRequest['layer']
                for k in newRequest.keys():                
                    if not k in getLegendGraphicParamList:
                        del newRequest[k]            
                return self.getLegendGraphic(layerName,**newRequest)                    
            
            # wfs requests
            if requestType == 'getfeature':
                paramList = ['service','typename']
                allParamList = ['propertyname','featureversion','maxfeatures','typename','featureid','filter','version',
                                'bbox','service']
                for param in paramList:
                    if not param in newRequest.keys():
                        REQUEST.RESPONSE.setHeader("Content-type","text/xml")
                        return MapServerTemplates.ogcServiceException %("%s not found in request parameters." %(param))
                
                for k in newRequest.keys():
                    if not k in allParamList:
                        del newRequest[k]            
                
                data = self.getFeature(**newRequest)
                return data
                
            if requestType == 'describefeaturetype': 
                paramList = ['typename','service']   
                for param in paramList:
                    if not param in newRequest.keys():
                        REQUEST.RESPONSE.setHeader("Content-type","text/xml")
                        return MapServerTemplates.ogcServiceException %("%s not found in request parameters." %(param))
                res = self.describeFeatureType(newRequest['typename']) 
                REQUEST.RESPONSE.setHeader("Content-type","text/xml")           
                return res            
            
            # mixed
            if requestType.find('capabilities') != -1:
                if newRequest.has_key('service'):
                    service = newRequest['service']
                    res = self.getCapabilities(service)  
                    REQUEST.RESPONSE.setHeader("Content-type","text/xml")
                    res = res.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="UTF-8"?>')                   
                    return res
                else:
                    REQUEST.RESPONSE.setHeader("Content-type","text/xml")
                    return MapServerTemplates.ogcServiceException %("Service parameter was not passed for the getcapabilities requests")        
            
            
            REQUEST.RESPONSE.setHeader("Content-type","text/xml")
            return MapServerTemplates.ogcServiceException %('Nothing valid found in request parameter')           
        except:
            logger.exception('Error')
              

registerType(MapServerFacade,PROJECTNAME)
InitializeClass(MapServerFacade)      

# ums                  : http://localhost:8081/
# layerRegistry        : http://localhost:8082/
# securityManager      : http://localhost:8085/
# RRTranslator         : http://localhost:8084/

# Test URLs for MapServerFacade

# GetMap Test
# http://teora:7070/plone/mapserverfacade.2005-11-18.9864375225/wfswms?bbox=-180,-90,180,90&styles=&Format=image/png&request=GetMap&layers=REGIONS,LOCAL_MUNICIPALITIES_STATS_SA&width=550&height=250&srs=EPSG:4269

# DescribeFeatureType Test
# http://teora:7070/plone/mapserverfacade.2005-11-18.9864375225/wfswms?version=1.0.0&request=DescribeFeatureType&service=WFS&typename=REGIONS

# GetLegendGraphic Test
# http://teora:7070/plone/mapserverfacade.2005-11-18.9864375225/wfswms?VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=topp:states&request=getlegendgraphic

# GetCapabilities Test
# http://teora:7070/plone/mapserverfacade.2005-11-18.9864375225/wfswms?version=1.0.0&service=WMS&request=GetCapabilities 
# http://teora:7070/plone/mapserverfacade.2005-11-18.9864375225/wfswms?version=1.0.0&service=WFS&request=GetCapabilities

# GetFeatureInfo
# http://teora:7070/plone/mapserverfacade.2005-11-18.9864375225/wfswms?bbox=-180,-90,90,180&styles=&format=jpeg&info_format=text/plain&request=GetFeatureInfo&layers=topp:biketrailsarc&query_layers=topp:biketrailsarc&width=550&height=250&x=170&y=160&srs=EPSG:4269
#

# GetFeEature
# http://teora:7070/plone/mapserverfacade.2005-11-18.9864375225/wfswms?request=getfeature&service=wfs&version=1.0.0&maxfeatures=1&typename=REGIONS&filter=<ogc:Filter xmlns:ogc="http://ogc.org" xmlns:gml="http://www.opengis.net/gml"><ogc:BBOX><ogc:PropertyName>the_geom</ogc:PropertyName><gml:Box srsName="http://www.opengis.net/gml/srs/epsg.xml"><gml:coordinates>-180,-90 180,90</gml:coordinates></gml:Box></ogc:BBOX></ogc:Filter>
#

# ARCIMS Server
#http://libcwms.gov.bc.ca/wmsconnector/com.esri.wsit.WMSServlet/ogc_layer_service?REQUEST=GetCapabilities&VERSION=1
#http://libcwms.gov.bc.ca/wfsconnector/com.esri.wsit.WFSServlet/ogc_layer_service?REQUEST=GetCapabilities&VERSION=1



            





