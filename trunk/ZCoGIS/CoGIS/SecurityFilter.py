from xml import xpath
from xml.dom import minidom
import string
import cStringIO
import MapServerTemplates
import logging
import time

logger = logging.getLogger("SecurityFilter")
hdlr = logging.FileHandler('SecurityFilter.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)


"""
SecurityFilter Module
"""

class SecurityFilter:
    """
    SecurityFilter class
    """
    def __init__(self):
        """
        @summary: Initializer
        """       
        self.nameSpace = ""
        
        
    def filter(self,dom,permissions,type=""):
        """
        @summary:Filter a dom according to permissions, dom is filtered in-place
        @param dom: the xml dom object to be filtered
        @param permissions: the permission tructure to filter the dom with
        @param type: the type of request to be filtered
        @return: 1 or an xml error message
        """ 
        
        try:                   
            if type == 'getmap':
                self._filterGetMapRequest(dom,permissions)
                return
            if type == 'getlegendgraphic':
                self._filterGetLegendGraphic(dom,permissions)            
                return 
            if type == 'getfeaturerequest':
                self._filterGetFeatureRequest(dom,permissions)            
                return
            if type == 'getfeatureinfo':
                self._filterGetFeatureInfo(dom,permissions)
                return
            if type == 'describefeaturetype':
                self._filterDescribeFeatureType(dom,permissions)
                return             
                            
            rootName = dom.documentElement.tagName        
            res = rootName.split(":")
            if len(rootName.split(":")) == 1:
                self.nameSpace = ""
            else:
                self.nameSpace = rootName.split(":")[0]   
            
            if type == 'describefeaturetyperesponse':
                self._filterDescribeFeatureTypeReponse(dom,permissions)
                return 1
            
            if type == 'getfeatureresponse':
                self._filterGetFeatureResponse(dom,permissions)
                return 1
            
            if len(dom.getElementsByTagName("WMT_MS_Capabilities")) != 0:
                self._filterWMSGetCapabilities(dom,permissions)  
                return 1         
                
            if len(dom.getElementsByTagName("WFS_Capabilities")) != 0:
                # wfs getCapabilities
                self._filterWFSGetCapabilities(dom,permissions)
                return 1       
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()            
            return MapServerTemplates.ogcServiceException %("Exception occured with security filter , check log for details %s" %trace)
    
    def _filterGetMapRequest(self,params,permissions):
        """
        @summary: Filters the getmap request with given permissions
        @param params: standard wms getmap params
        @param permissions: the permission structure used to filter the request   
        """           
        try:
            strLayerNames = params['layers']
            layerNames = strLayerNames.split(",")
            filteredNames = [name for name in layerNames if name in permissions.keys()]
            if filteredNames:
                params['layers'] = string.join(filteredNames,",")            
            else:
                params['layers'] = ''
        except:
            logger.exception('error')
            
    def _filterGetLegendGraphic(self,params,permissions):
        """
        @summary: Filters the getLegendGraphic request
        @param params: standard wms getLegendGraphic parameters
        @param permissions: the permission structure used to filter the request   
        """               
        try:
            layerName = params['layer']        
            if layerName in permissions.keys():
                pass
            else:
                params['layer'] = ''        
        except:
            logger.exception('error')
    
    def _filterWMSGetCapabilities(self,dom,permissions):
        """
        @summary: filter a wms getCapabilities response
        @param dom: the DOM document object to be filtered.
        @param permissions: dic containing permissions for layers and fields to filter the dom by
        @return: a filtered DOM document instance
        """
        try:
            if dom.toxml().find("ServiceException") != -1:
                return
            tmpLayerElms = dom.getElementsByTagName('Layer')        
            tmpLayerElm = tmpLayerElms[0]
            layerElms = tmpLayerElm.getElementsByTagName("Layer")     
            
            for layer in layerElms:
                name = layer.getElementsByTagName("Name")[0].firstChild.nodeValue
                if not name in permissions.keys():
                    tmpLayerElm.removeChild(layer)           
        except:
            logger.exception('error')
    
    def _filterWFSGetCapabilities(self,dom,permissions):
        """
        @summary: filter a wfs getCapabilities response
        @param dom: the DOM document object to be filtered.
        @param permissions: dic containing permissions for layers and fields to filter the dom by
        @return: a filtered DOM document instance
        """
        try:
            if dom.toxml().find("ServiceException") != -1:
                return
            
            featureTypeListElm = dom.getElementsByTagName("FeatureTypeList")[0]
            
            featureTypeElms = dom.getElementsByTagName("FeatureType")
            for feature in featureTypeElms:
                name = feature.getElementsByTagName("Name")[0].firstChild.nodeValue
                if not name in permissions.keys():
                    featureTypeListElm.removeChild(feature)        
        except:
            logger.exception('error')
    
    def _filterGetFeatureRequest(self,dom,permissions):
        """
        @summary: filter a wfs getFeature request
        @param dom: the DOM document object to be filtered.
        @param permissions: dic containing permissions for layers and fields to filter the dom by
        @return: a filtered DOM document instance
        """        
        try:
            layerName = dom['typename']        
            if not layerName in permissions.keys():
                dom['typename'] = ''         
        except:
            logger.exception('error')
    
    
    def _filterGetFeatureResponse(self,dom,permissions):
        """
        @summary: filter a wfs getFeature response
        @param dom: the DOM document object to be filtered.
        @param permissions: dic containing permissions for layers and fields to filter the dom by
        @return: a filtered DOM document instance
        """
        try:
            if dom.toxml().find("ServiceException") != -1:
                return
            
            elms = dom.getElementsByTagName('gml:featureMember')
            if elms:               
                for elm in elms: 
                    try:                       
                        tName = elm.childNodes[1].tagName            
                    except:
                        continue
                    parts = tName.split(':')
                    if len(parts) == 1:
                        nameSpace = ""
                    else:
                        nameSpace = parts[0]
                        
                    layerName = tName.replace(":","").replace(nameSpace,"")
                    fields = [x.replace("gis_field_","") for x in permissions[layerName]]                             
                    for node in elm.childNodes[1].childNodes:
                        if hasattr(node,'tagName'):                    
                            tagName = node.tagName                    
                            if nameSpace == "":
                                if not tagName in fields:
                                    pNode = node.parentNode
                                    pNode.removeChild(node)
                            else:
                                tmpTag = tagName.replace(nameSpace+":","")                            
                                if not tmpTag in fields:
                                    pNode = node.parentNode
                                    pNode.removeChild(node)  
        except:
            logger.exception('error')
    
    def _filterDescribeFeatureType(self,params,permissions):
        """
        @summary: filter a describeFeatureType request
        @param dom: the DOM document object to be filtered.
        @param permissions: dic containing permissions for layers and fields to filter the dom by
        @return: a filtered DOM document instance
        """        
        try:
            layerName = params['typeName']
            if not layerName in permissions.keys():
                params['typeName'] = ''  
        except:
            logger.exception('error')
            
    def _filterDescribeFeatureTypeReponse(self,dom,permissions):
        """
        @summary: filter a describeFeatureType reposnse
        @param dom: the DOM document object to be filtered.
        @param permissions: dic containing permissions for layers and fields to filter the dom by
        @return: a filtered DOM document instance
        """      
        try:
            if dom.toxml().find("ServiceException") != -1:
                return
              
            if self.nameSpace == "":
                eElms = dom.getElementsByTagName("element")
            else:
                eElms = dom.getElementsByTagName(self.nameSpace + ":element" )
                
            layerName = ""
            for elm in eElms:
                if elm.hasAttribute("name"):
                    name = elm.getAttribute("name")
                    if name in permissions.keys():
                        layerName = name                    
            
            if layerName != "":
                fields = [x.replace("gis_field_","") for x in permissions[layerName]]             
                for elm in eElms:
                    if elm.hasAttribute('name'):
                        if elm.getAttribute('name') != layerName:                        
                            if not elm.getAttribute('name') in fields:                            
                                pNode = elm.parentNode
                                pNode.removeChild(elm)        
        except:
            logger.exception('error')
    
    def _filterGetFeatureInfo(self,params,permissions):
        """
        @summary: filter a getFeatureInfo reponse
        @param dom: the DOM document object to be filtered.
        @param permissions: dic containing permissions for layers and fields to filter the dom by
        @return: a filtered DOM document instance
        """
        try:
            strLayerNames = params['layers']
            queryLayers = params['queryLayers']
            layerNames = strLayerNames.split(",")
            filteredNames = [name for name in layerNames if name in permissions.keys()]
            filteredQNames = [name for name in queryLayers if name in permissions.keys()]
            if filteredNames:
                params['layers'] = string.join(filteredNames,",")  
                params['queryLayers'] = filteredQNames          
            else:
                params['layers'] = '' 
                params['queryLayers'] = []
        except:
            logger.exception('error')
    
    
        
