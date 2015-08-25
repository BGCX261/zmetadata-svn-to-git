import MapServerTemplates
import logging
import cStringIO

logger = logging.getLogger("LayerRegistry")
#hdlr = logging.FileHandler('./Logs/LayerRegistry.log')
hdlr = logging.FileHandler('LayerRegistry.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

class LayerRegistry:
    """
    All layers returned from the discovery process will be listed here
    with the relevant metadata such as source,type,scale,fields and format
    """
    def __init__(self, facade):
        self.facade = facade                       
    
    # ==================================================================
    # Public interface
    # ==================================================================       
    
    def describeFeatureType(self,typeName):
        """
        @summary: Is called from the RequestResponseTranslator
        @param typeName: the wfsName of the layer to describe
        @return: an xml string containing describeFeatureType response
        """        
        try:
            #layer = self._getLayerByWFSName(typeName)  
            layer = self._getLayerByUniqueName(typeName)                             
            if not layer:
                return MapServerTemplates.ogcServiceException %("Layer %s could not be found in mapfile" %(typeName))               
            orgCleanName = layer.wfsName.split(":")[-1]
            newCleanName = typeName.split(':')[-1]
            res = layer.describeFeatureResponse.replace(orgCleanName,newCleanName)                                   
            logger.info("describeFeatureType %s" %typeName)
            return res
 
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not describeFeatureType')
            return MapServerTemplates.ogcServiceException %("Exception occured with describeFeatureType request, check log for details %s" %trace)    
    
    def getCapabilities(self,service,facadeURL):
        """
        @summary: Is called from the RequestResponseTranslator
        @param service: service denotes which type of capabilities should be returned wms or wfs
        @param facadeURL: the url to the MapServerFacade posting entry point
        @return: a GetCapabilities xml response string
        """ 
        try:          
            logger.info("getCapabilities %s" %service)
            if service.lower() == 'wms':
                res = self._getWMSCapabilities()      
                res = res.replace("FACADE_URL",facadeURL)      
                return res
            if service.lower() == 'wfs':           
                res = self._getWFSCapabilities()
                res = res.replace("FACADE_URL",facadeURL)      
                return res
            return MapServerTemplates.ogcServiceException %("%s is not a valid service request" %service)         
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not getCapabilities')
            return MapServerTemplates.ogcServiceException %("Exception occured with getCapabilities request, check log for details %s" %trace)    
    
    def getLayersForOrganization(self, layerList, organization):
        """
        @summary: layerList is a list of dicts that needs to be filtered according to organization given
        @param layerList: a list of dicts to be filtered on organization
        @param organization: the name of the organization to filter on
        @return: a filtered list of dicts 
        """        
        newList = []        
        for layer in layerList:
            if layer.organization == organization:
                newList.append(layer)        
        return newList 
    
    def getLayersForWmsSource(self, layerList, wmsSource):
        """
        @summary: layerList is a list of Layer that needs to be filtered according to wmsSource given
        @param layerList: a list of Layer to be filtered on organization
        @param organization: the name of the wmsSource to filter on
        @return: a filtered list of dicts 
        """        
        newList = []        
        for layer in layerList:
            if layer.source[1] == wmsSource:
                newList.append(layer)        
        return newList   
    
    def getLayersForLayerNames(self, layerList, layerNames):
        """
        @summary: layerList is a list of Layer that needs to be filtered according to layernames given
        @param layerList: a list of Layer to be filtered on layer names
        @param layerNames: is a list of layerNames to filter on
        @return: a filtered list of dicts 
        """        
        newList = []        
        for layer in layerList:
            if layer.uniqueName in layerNames:
                newList.append(layer)        
        return newList        
    
    def getLayerStructure(self,layerNames=None,wmsSource=None, organization=None):
        """
        @summary: returns the xmlStructure that was given with the updateLayers call
        @param layerNames: a list of the uniqueName of the layers in the layer structure to return (optional)        
        @param wmsSource: only return layers from the given wmsSource url        
        @return: xmlrpc xml structure of layers 
        """        
        try:              
            if not layerNames and not wmsSource and not organization:
                layers = []
                for layer in self.facade.layerStructure:
                    layers.append(layer.dict)                            
                return layers
            
            if layerNames and wmsSource and organization:
                tmpList = self.getLayersForOrganization(self.facade.layerStructure, organization)
                tmpList = self.getLayersForWmsSource(tmpList, wmsSource)
                tmpList = self.getLayersForLayerNames(tmpList, layerNames)                
                layers = []
                for layer in tmpList:
                    layers.append(layer.dict)                
                return layers
            
            if organization and wmsSource:
                tmpList = self.getLayersForOrganization(self.facade.layerStructure, organization)
                tmpList = self.getLayersForWmsSource(tmpList, wmsSource)                
                layers = []
                for layer in tmpList:
                    layers.append(layer.dict)                
                return layers
            
            if layerNames and not organization and not wmsSource:
                tmpList = self.getLayersForLayerNames(self.facade.layerStructure, layerNames)                
                layers = []
                for layer in tmpList:
                    layers.append(layer.dict)
                return layers                    

        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()            
            logger.exception('Could not getLayerStructure')
            return MapServerTemplates.ogcServiceException %("Exception occured with getLayerStructure request, check log for details %s" %trace)    
            
    def getGeometryColumnForLayerName(self,layerName):
        """
        @summary: gets the geometry column for the layer name given
        @param layerName: the layer name to get the geometry column for
        @return: the name of the geometry column for the given layer name
        """          
        try:
            for layer in self.facade.layerStructure:
                if (layer.uniqueName == layerName) or (layer.uniqueName == layerName): # changed to uniqueName to find in registry
                    return layer.geometryField                            
            return MapServerTemplates.ogcServiceException %("Layer Registry does not contain a layer by the name: %s" %layerName)
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not getGeometryColumnForLayerName')
            return MapServerTemplates.ogcServiceException %("Exception occured with getGeometryColumnForLayerName request, check log for details %s" %trace)                
    
    def setLayerList(self,layerList): 
        """
        @summary:
        @param xmlStructure: as generated by the discoverLayers method from the universalMapServer
        @return: 1 or an exception string if an error occurs
        """
        try:  
            #if not layerList:
            #    return                              
            tmpStruct = layerList  
            self.facade.layerStructure = []
            layerCount = len(tmpStruct)
            for x in range(layerCount):                
                l = Layer()
                l.fromDict(tmpStruct[x])                                 
                self.facade.layerStructure.append(l)
            return 1
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not updateLayers')
            return MapServerTemplates.ogcServiceException %("Exception occured with updateLayers request, check log for details %s" %trace) 
    
    def updateLayers(self,layerList):
        """
        @summary: Called from the MapServerFacade after calling updateLayer on UniversalMapServer         
        @param xmlStructure: the map layers metadata represented in xml structure
        @return: 1 or an exception string if an error occurs
        """        
        try:              
            if not layerList:                
                return                     
            tmpStruct = layerList          
            layerCount = len(tmpStruct)
            uniqueNames = self._getUniqueNames()            
            for x in range(layerCount):
                if tmpStruct[x].has_key('uniqueName'):
                    if not tmpStruct[x]['uniqueName'] in uniqueNames:                                    
                        l = Layer()
                        l.fromDict(tmpStruct[x])                               
                        self.facade.layerStructure.append(l) 
            logger.info("updateLayers " )            
            return 1
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()            
            logger.exception('Could not updateLayers')
            return MapServerTemplates.ogcServiceException %("Exception occured with updateLayers request, check log for details %s" %trace)  
    # =====================================================================
    # Protected Interface
    # =====================================================================
    
    def _getNameAndSourceList(self):
        """
        @summary: builds a list of lists with each list containing the layer name and it's source
        @return: a list of lists
        """
        nameList = []
        sourceList = []
        for layer in self.facade.layerStructure:
            nameList.append(layer.wmsName)
            sourceList.append(layer.source)            
        return [nameList,sourceList]
    
    def _getWMSCapabilities(self):
        """
        @summary: generates a wms getcapabilities from the current layerStructure
        @return: an xml string containing getcapabilities response
        """        
        lStr = ''
        for layer in self.facade.layerStructure:   
            
            if layer.error:                  
                continue            
            #if layer.wmsQueryable == "":
            #    continue
            lStr += MapServerTemplates.wmsCapabilitiesTemplate %(layer.wmsQueryable,layer.uniqueName,layer.uniqueName,layer.abstract,
                                                                layer.keywords,layer.wmsSRS,layer.wfsBoundingBox[0],
                                                                layer.wfsBoundingBox[1],layer.wfsBoundingBox[2],layer.wfsBoundingBox[3],
                                                                layer.wmsStyleName,layer.wmsStyleName)            
        
        response = MapServerTemplates.wmsCapabilitiesBodyTemplate %lStr
        return response                 
        
    def _getWFSCapabilities(self):
        """
        @summary: generates a wfs getcapabilities from the current layerStructure
        @return: the wfs getcapabilities xml string
        """
        lStr = ''
        
        for layer in self.facade.layerStructure:            
            if layer.error:                
                continue 
            if layer.hasWFSLayer == True:
                lStr += MapServerTemplates.wfsCapabilities %(layer.uniqueName,layer.uniqueName,layer.abstract,layer.keywords, layer.wfsSRS,
                                                        layer.wfsBoundingBox[0],layer.wfsBoundingBox[1],layer.wfsBoundingBox[2],layer.wfsBoundingBox[3])
                        
        return MapServerTemplates.wfsCapabilitiesBody %(lStr)  
    
    def _getLayerByWFSName(self,wfsName):
        """
        @summary: gets the layer dict that has the given wfsName
        @param wfsName: the wfsName of the layer to search for
        @return: return the layer object with the wfsName,and None if layer not found
        """        
        for layer in self.facade.layerStructure:
            if layer.wfsName == wfsName:
                return layer
            
        return None 
    
    def _getUniqueNames(self):
        """
        """
        layers = []
        for layer in self.facade.layerStructure:
            layers.append(layer.uniqueName)
        return layers
    
    def _getLayerByUniqueName(self,name):
        """
        @summary: to access a layer by its unique name
        @param name: the name of the layer to get
        @return: the layer structure for the unique name given
        """
        for layer in self.facade.layerStructure:
            if layer.uniqueName == name:
                return layer            
        return None            
    
    def _setLayerStructure(self, layers):
        """
        @summary: Set layer structure from python structure
        @param layers: list of layer dicts
        """
        self.facade.layerStructure = []
        for layerDict in layers:
            layer = Layer()
            layer.fromDict(layerDict)
            self.facade.layerStructure.append(layer)        
            
class Layer:
    '''Class representing a layer'''
    def __init__(self):
        self.wmsName = ''
        self.wfsName = ''
        self.title = ''
        self.wfsBoundingBox = []
        self.abstract = ''
        self.wmsTitle = ''
        self.wmsQueryable = 0
        self.source = []
        self.geometryType = ''
        self.error = ''
        self.hasWFSLayer = False
        self.keywords = ''
        self.wfsSRS = ''
        self.wmsSRS = ''
        self.wmsBoundingBox = []
        self.geometryField = ''
        self.attributes = []
        self.error = ''        
        self.dict = {}
        self.wmsXML = ""
        self.wfsXML = ""
        self.organization = ""
    
    def fromDict(self, dict):
        """
        @summary: Set layer object from dict keys and values
        """
        self.dict = dict
        for k in dict.keys():            
            if k == 'fields':
                continue
            if k == 'describeFeatureResponse':
                self.describeFeatureResponse = dict['describeFeatureResponse']                
                continue
    
            if type(dict[k]) == list:            
                exec('''self.%s = %s''' %(k,dict[k]))
            else:
                exec("""self.%s = '%s'""" %(str(k),str(dict[k]).replace("\r","").replace("\n","").replace("\t","")))                
                
        if dict.has_key('fields'):
            fields = dict['fields']
            for k in fields.keys():
                theAttr = Attribute(k,fields[k])
                self.attributes.append(theAttr)        
                       
        
class Attribute:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        
    def fromDict(self, dict):
        self.name = dict['name']
        self.type = dict['type']        
        
if __name__ == "__main__":
    pass
    
        
        
        
        
        
        
        
        
        
