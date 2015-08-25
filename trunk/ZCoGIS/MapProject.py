import Globals
import AccessControl
from AccessControl import ClassSecurityInfo
import AccessControl.SecurityManagement, AccessControl.User
import Acquisition
from Products.CMFCore.CMFCatalogAware import CMFCatalogAware
from Products.CMFDefault.DublinCore import DefaultDublinCoreImpl
from Products.ATContentTypes.types.ATImage import ATImage
from Products.ATContentTypes.types.ATDocument import ATDocument
import urllib
import binascii
import MapServerTemplates
import transaction
from SecurityUtil import Login

from Products.Archetypes.public import registerType,BaseContent,StringField,StringWidget
from Products.CMFCore import permissions
from config import PROJECTNAME
from config import ADD_CONTENT_PERMISSION
from xml.dom import minidom
import cStringIO
import StringIO
import logging
import time
import SecurityUtils
from Products.Archetypes.atapi import *
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin


# Zope imports
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Acquisition import aq_base

# CMF imports
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import ReferenceField
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFCore.permissions import ModifyPortalContent
from Products.ATContentTypes import ATCTMessageFactory as _



logger = logging.getLogger("MapProject")
hdlr = logging.FileHandler('MapProject.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

class MapProject(BaseContent): 
    '''Map Project for CoGIS'''    
        
    schema = BaseSchema + Schema([
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
    )])
    meta_type = 'MapProject'
    actions = ({'id': 'view',
              'name': 'View',
              'action': 'string:${object_url}/MapProject_View',
              'permissions': (permissions.View,)}, 
              {'id': 'edit',
              'name': 'Edit',
              'action': 'string:${object_url}/MapProject_Edit',
              'permissions': (permissions.ViewManagementScreens,)},
              {'id': 'manage',
              'name': 'Manage',
              'action': 'string:${object_url}/Project_Edit',
              'permissions': (permissions.ViewManagementScreens,)}, 
              {'id': 'search',
              'name': 'Search',
              'action': 'string:${object_url}/LayerSearch',
              'permissions': (permissions.ViewManagementScreens,)},                                         
              ) 
    
    aliases = {
        '(Default)'  : 'MapProject_View',
        'view'       : 'base_view',
        'edit'       : 'base_edit',
        'properties' : 'base_metadata',
        'sharing'    : 'folder_localrole_form'            
        }  

    content_icon = "project_icon.gif"  
    security = ClassSecurityInfo()     

    def __init__(self, id,mapServerFacade='',title="MapProject",description=''):
        '''Initialize an instance of the class'''            
        try:
            self.id=id
            self.mapServerFacadeId = mapServerFacade
            self.title = title
            self.description = description
            self.layerList = []  
            self.wmsGetCapabilitiesLayerList = []   
            self.wfsGetCapabilitiesDict = {}
            self._layerRegistryStructure = [] 
            self.reindexObject()
            self._p_changed = 1 
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read() 
            logger.exception('Map Project Init failed')     
        
    def manage_afterAdd(self,item, container):
        """
        """                   
        self.manage_permission("Copy or Move", roles=["Owner"], acquire=False)      
        self.manage_permission("Delete objects", roles=["Owner"], acquire=False)      
        self.manage_permission("Modify portal content", roles=["Owner"], acquire=False)      
        self.manage_permission("Take ownership", roles=["Owner"], acquire=False)      
        self.manage_permission("View management screens", roles=["Owner"], acquire=False)      
        
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
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()            
            logger.exception('failed user is owner')     
        
    def _layerContainsKeyword(self,layer,keyword):
        """
        @summary: Checks the layers text attributes for a partial match with the keyword given        
        @param keyword: the string keyword too look for
        @param layer: the zope layer object to search attributes
        @return: boolean
        """
        try:
            if layer['abstract'].lower().find(keyword.lower()) != -1:           
                return True
            if layer['keywords'].lower().find(keyword.lower()) != -1:            
                return True
            if layer['uniqueName'].lower().find(keyword.lower()) != -1:            
                return True
            if layer['title'].lower().find(keyword.lower()) != -1:            
                return True    
            if layer['geometryField'].lower().find(keyword.lower()) != -1:            
                return True  
            return False
        except:
            logger.exception('error')
    
    def _getLayerFromRegistryStructure(self,name):
        """
        @summary: returns a layer with given name from the local copy of the layer registry
        @param name: the uniqueName of the layer
        @return: returns a dict with layer attributes as keys for the given name
        """
        try:
            for layer in self._layerRegistryStructure:
                if layer['uniqueName'] == name:
                    return layer        
            return None        
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read() 
            logger.exception('failed get layer from registry structure')     
    
    def addLayer(self,name,title,env,REQUEST=None):
        """
        @summary: Adds a new layer to the project, duplicate layers are ignored
        @return: 1, because method is called from an xml-rpc javascipt client and None is not valid return type
        @param name: the unique name of the layer as listed in the mapserver facade
        @param title: the title of the layer to add
        @param env: the envelope of the layer to be added
        """
        
        try:
            nameList = []
            for l in self.layerList:
                nameList.append(l['name'])         
            if not name in nameList:  
                layer = {'name':name,'title':title,'env':env}            
                self.layerList.append(layer)  
                self.commitTransaction()
            return 1
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read() 
            logger.exception('failed addLayer')     
    
    def saveURLContentAsDocument(self,docTitle,url,REQUEST=None):
        """
        @summary: reads te url content and stores it in a new document
        @param docTitle: the title to give the new document        
        """      
#        print "==========================================================="  
#        print docTitle
#        print url
#        print "==========================================================="
        member = "Anonymous" 
        try:
            tmpMember =  self.portal_membership.getAuthenticatedMember()            
            member = tmpMember.getRoles()[0]
        except:
            member = "Anonymous"   
        
        if member == "Anonymous":
            return 2        
        res = urllib.urlopen(url)        
        fObject = StringIO.StringIO(res.read())
        fObject.seek(0)
        folder = self.portal_membership.getHomeFolder()
        
        try:
            tName = str(time.time()).replace(".","")  
            folder._setObject(tName,ATImage(tName,title=docTitle,content_type='image/png'))
            img = getattr(folder,tName)               
            img.cmf_edit('',file=fObject,title=docTitle)            
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()             
            logger.exception('Could not saveURLContentAsDocument')                    
        
        # use data to create a new document in the user folder
        return 1
    
    def getGeometryColumnForLayerName(self,layerName,REQUEST=None):
        """
        @summary: Calls the facade objects identical method for getting the geometry column
        @param layerName: the name of the layer to get the geometry column for
        @return: str geometry column for the layer name given
        """         
        return self.getProjectFacadeObject().getGeometryColumnForLayerName(layerName)        
    
    def getLayerMetadata(self,uniqueLayerName, REQUEST=None):
        """
        @summary: returns the metadata view for the given layer name in the project
        @param uniqueLayerName: unique layer name to get metadata view for 
        @return: html metadata view for the give n layer name
        """       
         
        try:
            resList = self.getProjectFacadeObject().getLayerByName(uniqueLayerName)
            if resList:
                layer = resList[0]
                return layer.getMetadata()
            else:
                return 0        
        except:
            logger.exception('error')
    
    def commitTransaction(self):
        """
        @summary: Triggers zope to store any changes to the object
        """        
        self._p_changed = 1   
        transaction.savepoint(True)                      
    
    def mmanage_AddMapProject(self,REQUEST=None):
        """
        @summary:creates a new instance of the map project
        @param title: a title for the project object
        @param description: a description for the project
        @param the id of the mapserver facade to associate with the project
        @return: the mapProject_View page template
        """        
         
        try:
            title = REQUEST['title']
            facadeId = REQUEST['mapServerFacade']
            description = REQUEST['description']            
            
            self.title = title
            self.mapServerFacadeId = facadeId
            self.description = description  
            self.reindexObject()
            self._p_changed = 1      
            return REQUEST.RESPONSE.redirect(self.absolute_url())       
        except:
            logger.exception('error')
    
    def moveLayerTop(self,name):
        """
        @summary: Move a layer with the given name to the top of the layerList
        @param name: the name of the layer to move 
        @return: 1
        """
        try:
            
            tmpList = [x for x in self.layerList if x['name'] == name]        
            theLayer = tmpList[0]        
            index = self.layerList.index(theLayer)        
            if index == 0:
                return 1           
            if index > 0:
                self.layerList.remove(theLayer)
                self.layerList.insert(0,theLayer)       
            return 1        
        except:
            logger.exception('error')
    
    def moveLayerBottom(self,name):
        """
        @summary: Move a layer with the given name to the bottom of the layerList
        @param name: the name of the layer to move 
        @return: 1
        """            
        try:           
            tmpList = [x for x in self.layerList if x['name'] == name]        
            theLayer = tmpList[0]           
            self.layerList.remove(theLayer)
            self.layerList.append(theLayer)        
            return 1  
        except:
            logger.exception('error')
    
    def moveLayerUp(self,name):
        """
        @summary: move the given layer up in the list order
        @param name: passed as a REQUEST variable, and is the uniqueName of the layer 
        @return: 1 so that xml-rpc call does not fail
        """    
          
        try:
            tmpList = [x for x in self.layerList if x['name'] == name]        
            theLayer = tmpList[0]        
            index = self.layerList.index(theLayer)        
            
            if index > 0:
                self.layerList.remove(theLayer)
                self.layerList.insert(index-1,theLayer)       
            return 1
        except:
            logger.exception('error')
    
    def moveLayerDown(self,name):
        """
        @summary: move the given layer down in the list order
        @param name: passed as a REQUEST variable, and is the uniqueName of the layer 
        @return: 1 so that xml-rpc call does not fail
        """
        try:            
            tmpList = [x for x in self.layerList if x['name'] == name]   
            theLayer = tmpList[0]
            index = self.layerList.index(theLayer) 
            
            if index < len(self.layerList):
                self.layerList.remove(theLayer)
                self.layerList.insert(index+1,theLayer)         
            return 1   
        except:
            logger.exception('error')
    
    def getOrganizationNames(self):
        """
        @summary: return a list of organization names
        """   
        #authMember = self.portal_membership.getAuthenticatedMember()                
        #nLogin = Login();
        #nLogin.loginAsManager()   
        try:
            facade = self.getProjectFacadeObject()        
            items =  facade.objectItems()
            organizationNameList = []
            for i in items:
                if i[1].meta_type == 'Organization':                                   
                    if i[1].organization not in organizationNameList: 
                        pass                        
                    organizationNameList.append(i[1].id)       
        except:            
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read() 
            logger.exception('failed getOrganizationNames')   
        #nLogin.loginAsUser(authMember)             
        return organizationNameList
    
    def getServerNamesForOrganization(self, organization,REQUEST=None):
        """
        @summary: return a list of organization names
        """        
        serverNameList = []
        try:            
            tmpList = self.getMapServers()
            
            for server in tmpList:
                if server.organization == organization:
                    serverNameList.append(server.title)
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()            
            logger.exception('failed getServerNamesForOrganization')     
        
#        facade = self.getProjectFacadeObject()        
#        items =  facade.objectItems()
#        serverNameList = []
#        for i in items:
#            if i[1].meta_type == 'Organization':  
#                if i[1].id == organizationName:  
#                    serverNameList.append(i[1].id)
        return serverNameList
    
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
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read() 
            logger.exception('failed getMapServers')     
    
#    def getServerNames(self,REQUEST=None):
#        """
#        @summary: returns a list of server names associated with the project facade object
#        @return: a list
#        """
#         
#        facade = self.getProjectFacadeObject()        
#        items =  facade.objectItems()
#        serverNameList = []
#        for i in items:
#            if i[1].meta_type == 'MapServer':    
#                serverNameList.append(i[1].title)            
#        return serverNameList
    
    def checkAgreements(self,REQUEST=None):
        """
        @summary: check if the current user has accepted all license agreements for the data        
        """            
        try:
            redirectURL = self.absolute_url() + "/MapProject_View"        
                    
            for layer in self.getLayerList():  
                name = layer['name']
                hasAccepted = self.getProjectFacadeObject().userHasAcceptedAgeement(name)
                if not hasAccepted:                
                    path = self.getProjectFacadeObject().absolute_url() + "/getAgreementForServerWithLayer?layerName=" + name + "&redirectURL=" + redirectURL
                    
                    REQUEST.RESPONSE.redirect(path) 
                    #return path      
            return ""
        except:
            logger.exception('error')
        
    def getLayerList(self,REQUEST=None):
        """
        @summary: returns the current layerList
        @return: returns the project layer list, which is a list of dictionary objects containing name,title and envelope
        """  
                
        try:
            
            self._checkLayerAvailability()  
            layerNames = [x['name'] for x in self.layerList]
            layerStructure = self.getProjectFacadeObject().getLayerStructure(layerNames=layerNames)
            
            if not layerStructure:
                return []
#            if xmlStr.find("ServiceException") != -1:
#                if xmlStr.find("describeFeatureResponse") == -1:
#                    return [] 
            self._layerRegistryStructure = layerStructure   
            uniqueNames = [x['uniqueName'] for x in self._layerRegistryStructure]     
            
            roleFilteredList = [x for x in self.layerList if x['name'] in uniqueNames]  
            return roleFilteredList  
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read() 
            logger.exception('failed getLayerList')     
    
    def _checkLayerAvailability(self, REQUEST=None):
        """
        @summary: Goes through each layer in the layer list and checks that all the layers a still available,
        If layer is not available then it is removed
        """           
        try:  
            statusList = self.getProjectFacadeObject().checkComponentStatuses()            
            for status in statusList:
                if not status:
                    return # if a component is not running then return  
                    
            layerNames = [x['name'] for x in self.layerList]           
            layerStructure = self.getProjectFacadeObject().getLayerStructure(unfiltered=1,layerNames=layerNames)            
            if not layerStructure:
                return 
              
            self._layerRegistryStructure = layerStructure   
            uniqueNames = [x['uniqueName'] for x in self._layerRegistryStructure]   
            tmpList = [x for x in self.layerList if x['name'] in uniqueNames]            
            self.layerList = tmpList              
        except:   
            logger.exception('Could not saveURLContentAsDocument')            
    
    def getMapServerFacadeList(self,REQUEST=None):
        """
        @summary:Does a catalog search for all the mapserver facades and returns their names and ids.
        @return: a list of tuples with mapserverfacade [(name,id),..]
        """  
#        try:
#            resList = []
#            id = self.getProjectFacadeObject().id
#            name = self.getProjectFacadeObject().title
#            resList.append((name,id))   
#            return resList   
#        except:
#            logger.exception('failed getMapServerFacadeList')
            
        # get logged in user and store to relogin later
        
        # get a user with manager permissions and login as that user
        #authMember = self.portal_membership.getAuthenticatedMember()                
        #nLogin = Login();
        #nLogin.loginAsManager()
        
        resList = []
        results = self.portal_catalog.searchResults(meta_type = "MapServerFacade")          
        for result in results:            
            name = result.getObject().title
            id = result.getRID()            
            resList.append((name,id))            
        
        #nLogin.loginAsUser(authMember)
        
        return resList     
    
    def getCapabilities(self,service):
        """
        @summary: generates a getcapabilities request for the current project layers
        @param service: service can be wfs or wms
        @return: the getcapabilities response in xml for the given service type
        """        
        try:
            if service == 'wms':        
                tmpXML = ''
                for layer in self.getLayerList():#self.layerList:
                    name = layer['name']                        
                    tmpList = [x for x in self.wmsGetCapabilitiesLayerList if x['name'] == name]                
                    xml = tmpList[0]['xml']            
                    tmpXML += xml            
                return MapServerTemplates.wmsCapabilitiesBodyTemplate %(tmpXML)
            
            if service == 'wfs':
                tmpXML = ''
                for layer in self.layerList:
                    name = layer['name']
                    layerXML = self.wfsGetCapabilitiesDict[name]
                    tmpXML += layerXML
                return MapServerTemplates.wfsCapabilitiesBody %(tmpXML)
        except:
            logger.exception('failed getCapabilities')
    
    
    def getLayersForWMSSource(self,serverTitle,organization,REQUEST=None):
        """
        @summary: returns a list of layer from the given wms source
        @param wmsSource: the wmsSource to return layers for
        @return: returns a list of layer from the given wms source
        """     
         
        try:            
            # get the wmsSource for the server name/title given            
            wmsSource = ""
            mapServers = self.getMapServers()
            for server in mapServers:
                if server.title == serverTitle and server.organization == organization:
                    wmsSource = server.wmsSource            
            
            layerStructure = self.getProjectFacadeObject().getLayerStructure(wmsSource=wmsSource,organization=organization)   
            self._layerRegistryStructure = layerStructure     
            retList = []
            for layer in self._layerRegistryStructure:            
                name = layer['uniqueName']
                title = layer['wmsTitle']
                abstract = layer['abstract']
                srs = layer['wmsSRS']
                minx = layer['wmsBoundingBox'][0]
                miny = layer['wmsBoundingBox'][1]
                maxx = layer['wmsBoundingBox'][2]
                maxy = layer['wmsBoundingBox'][3]
                env = layer['wmsBoundingBox']
                type = layer['geometryType']
                wmsXML = layer['wmsXML']
                wfsXML = layer['wfsXML']           
                
                tmpDict = {'name':name,'title':title,'abstract':abstract,'srs':srs,'env':env,'type':type,'xml':wmsXML}                
                retList.append(tmpDict)
                
                layerNames = [x['name'] for x in self.wmsGetCapabilitiesLayerList]
                if not name in layerNames:                
                    self.wmsGetCapabilitiesLayerList.append(tmpDict)            
                self.wfsGetCapabilitiesDict[name] = wfsXML           
            return retList
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()   
            logger.exception('Could not getLayersForWMSSource')         
            return MapServerTemplates.ogcServiceException %("Exception occured with getLayersForWMSSource, check log for details %s" %trace)  
                
    
    def getAllFacadeLayers(self,REQUEST=None):
        """
        @summary: Does a getCapabilities request on the mapserver facade to get all the map layers
        @return: returns a list if dictionaries that each represent a map layer 
        """                
         
        try:
            
            self.wmsGetCapabilitiesLayerList = []
            layerStructure = self.getProjectFacadeObject().getLayerStructure()   
            self._layerRegistryStructure = layerStructure       
            
            for layer in self._layerRegistryStructure:            
                name = layer['uniqueName']
                title = layer['wmsTitle']
                abstract = layer['abstract']
                srs = layer['wmsSRS']
                minx = layer['wmsBoundingBox'][0]
                miny = layer['wmsBoundingBox'][1]
                maxx = layer['wmsBoundingBox'][2]
                maxy = layer['wmsBoundingBox'][3]
                env = layer['wmsBoundingBox']
                type = layer['geometryType']
                wmsXML = layer['wmsXML']
                wfsXML = layer['wfsXML']           
                
                tmpDict = {'name':name,'title':title,'abstract':abstract,'srs':srs,'env':env,'type':type,'xml':wmsXML}
                #tmpDict = {'name':name,'title':title,'abstract':abstract,'srs':srs,'env':env,'type':type,'xml':layer.toxml()}
                self.wmsGetCapabilitiesLayerList.append(tmpDict)            
                self.wfsGetCapabilitiesDict[name] = wfsXML  
            
            return self.wmsGetCapabilitiesLayerList  
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()   
            logger.exception('Could not getAllFacadeLayers')                
            return MapServerTemplates.ogcServiceException %("Exception occured with getAllFacadeLayers, check log for details %s" %trace)  
            
    
    def getLayerSampleImage(self,REQUEST=None):
        """  
        @param name: passed as a REQUEST variable, and is the uniqueName of the layer      
        @summary: 
        @return: the sample image for the given layer name
        """
         
        try:
            name = REQUEST.form['name']
            layer = self._getLayerFromRegistryStructure(name)
            imgData = layer['sampleImage']           
            data = binascii.a2b_hex(imgData) 
            REQUEST.RESPONSE.setHeader("Content-type","image/png")
            return data
        except:
            logger.exception('getLayerSampleImage')
    
    def getSearchResults(self,keyword,minx='',miny='',maxx='',maxy='', REQUEST=None):
        """
        @summary: Does a search for all the layers in the facade structure that match the search criteria
        @param minx: minx element of the layer envelope
        @param miny: miny element of the layer envelope
        @param maxx: maxx element of the layer envelope
        @param maxy: maxy element of the layer envelope
        @param keyword: the text keyword too search for in all text attributes of the layer
        @return: a list of dict objects containing attribute info about the layer
        """ 
        try:
            resultList = []
            facade = self.getProjectFacadeObject()        
            
            layerStructure = facade.getLayerStructure() #sampleImage
            if type(layerStructure) != list:
                if (layerStructure.find("ServiceException") != -1) and (layerStructure.find("sampleImage") == -1):            
                    return []
            if not layerStructure:
                return []
            
            layerList = layerStructure
            #results = self.portal_catalog.searchResults(meta_type = "MapLayer", path=searchPath)  
                
            for layer in layerList:            
                if self._layerContainsKeyword(layer,keyword):                
                    if minx != '':
                        if (not float(minx) >= float(layer['wmsBoundingBox'][0])):
                            continue                    
                    if miny != '':
                        if (not float(miny) >= float(layer['wmsBoundingBox'][1])):
                            continue
                    if maxx != '':
                        if (not float(maxx) >= float(layer['wmsBoundingBox'][2])):
                            continue
                    if maxy != '':
                        if (not float(maxy) >= float(layer['wmsBoundingBox'][3])):
                            continue                
                    resultList.append(layer) 
            tmpLayers = []             
            for layer in resultList:
                tmpDict = {}
                tmpDict['name'] = layer['uniqueName']
                tmpDict['title'] = layer['title']
                tmpDict['env'] = layer['wmsBoundingBox']
                tmpDict['srs'] = layer['wmsSRS']
                tmpDict['type'] = layer['geometryType']
                tmpLayers.append(tmpDict)   
            return tmpLayers              
        except:
            logger.exception('getSearchResults')
    
    security.declarePublic('getProjectFacadeObject')
    def getProjectFacadeObject(self,REQUEST=None):
        """
        @summary: does a catalog search for a mapserver facade object with a certain id
        @return: the zope mapserverFacade object associated with this project object
        """            
#        return self.MapServer  
        authMember = self.portal_membership.getAuthenticatedMember()                
        nLogin = Login();
        nLogin.loginAsManager()
                       
        results = self.portal_catalog.searchResults(meta_type = "MapServerFacade")          
        for result in results:   
            id = result.getRID()            
            if str(id) == str(self.mapServerFacadeId):
                #nLogin.loginAsUser(authMember)
                return result.getObject() 
        nLogin.loginAsUser(authMember)    
        return None 
    
    def removeLayer(self,name,REQUEST=None):
        """
        @summary: Removed the layer with the given unique name from the layer list
        @param name: the unique name of the layer to remove
        @return: 1, because method is called from an xml-rpc javascipt client and None is not valid return types        
        """       
        try:
            for layer in self.layerList:
                if name == layer['name']:
                    self.layerList.remove(layer)
                    self.commitTransaction()
                    break            
            return 1    
        except:
            logger.exception('error')
    
    def removeAllLayers(self,REQUEST=None):
        """
        @summary: deletes all the layersfrom the project
        @return: 1, because method is called from an xml-rpc javascipt client and None is not valid return types   
        """
        self.layerList = []
        return 1
    
    def getSingleLegendGraphic(self,layers="",REQUEST=None):
        """
        @summary: Does a getLegendRequest for each of the layers and returns a single legend image for all
        @param layers: a pipe delimited list of layer names e.g city|river|country
        @return: a binary string containing the image data
        """       
         
        try:
            data = self.getProjectFacadeObject().getSingleLegendGraphic(layers)
            if REQUEST:
                REQUEST.RESPONSE.setHeader("Content-type","image/png")  
            return data
        except:
            logger.exception('error')
    
    def wfswms(self,REQUEST=None):
        """
        @summary: this acts as a dummy MapServerFacade and routes the requests to the projects alocated facade
        @return: the response to the type of request passed
        @param REQUEST: the REQUEST parameter can contain any valid OGC wfs and wms request paramete pairs.
        The only types catered for are:
            WMS: getMap,getCapabilities,getFeatureInfo,getLegendGraphic
            WFS: getCapabilities,getFeature,DescribeFeatureType
        """        
        try:
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
                    import traceback
                    sio = cStringIO.StringIO()
                    traceback.print_exc(file=sio)
                    sio.seek(0)
                    trace = sio.read()                       
                    logger.exception('Could not wfswms')
                           
                       
            requestType = ''
            if newRequest.has_key('request'):            
                requestType = newRequest['request'].lower()        
                
            if requestType.find('capabilities') != -1:
                if newRequest.has_key('service'):
                    service = newRequest['service']
                    
                    if (service.lower() == 'wms') or (service.lower() == 'wfs'):                    
                        REQUEST.RESPONSE.setHeader("Content-type","text/xml")
                        res = self.getCapabilities(service.lower())                            
                        res = res.replace('http://10.50.130.45:9080/geoserver/wms?',self.absolute_url() + '/wfswms?')
                        res = res.replace('http://10.50.130.45:9080/geoserver/wfs?',self.absolute_url() + '/wfswms?')
                        res = res.replace(self.getProjectFacadeObject().absolute_url() + '/wfswms',self.absolute_url() + '/wfswms?')
                        res = res.strip()
                        return res
            
            res = self.getProjectFacadeObject().wfswms(REQUEST)            
            return res 
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('wfswms failed')
    
                

registerType(MapProject,PROJECTNAME)


