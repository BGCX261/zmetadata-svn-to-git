"""
RequestResponseTranslator Module
"""
import SecurityFilter
import WMSWFSMapper
from xml.dom import minidom
import MapServerTemplates
import logging
import cStringIO
import string
#import hotshot, hotshot.stats
import time

logger = logging.getLogger("RequestResponseTranslator")
hdlr = logging.FileHandler('RequestResponseTranslator.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

##FILTER_TEMPLATE = """
##<Filter>
##    <BBOX>
##        <PropertyName>Geometry</PropertyName>
##            <gml:Envelope srsName="http://www.opengis.net/gml/srs/epsg.xml#%(srs)s">
##                <gml:lowerCorner>%(minx)f %(miny)f</gml:lowerCorner>
##                <gml:upperCorner>%(maxx)f %(maxy)f</gml:upperCorner>
##            </gml:Envelope>
##    </BBOX>
##</Filter>
##"""

FILTER_TEMPLATE = """
<ogc:Filter xmlns:ogc="http://ogc.org" xmlns:gml="http://www.opengis.net/gml">
    <ogc:BBOX>
    <ogc:PropertyName>%(geoColumn)s</ogc:PropertyName>
        <gml:Box srsName="http://www.opengis.net/gml/srs/epsg.xml">
            <gml:coordinates>%(minx)s,%(miny)s %(maxx)s,%(maxy)s</gml:coordinates>
        </gml:Box>
    </ogc:BBOX>
</ogc:Filter>
"""

class RequestResponseTranslator:
    def __init__(self, facade, layerRegistry, securityManager, universalMapServer):
        """
        Set up the connections to external objects
        """
        self.facade = facade
        self._layerRegistry = layerRegistry
        self._securityFilter = SecurityFilter.SecurityFilter()
        self._securityManager = securityManager
        self._universalMapServer = universalMapServer
        self._wmswfsMapper = WMSWFSMapper.WMSWFSMapper()
    
    # ==================================================================
    # Public interface
    # ==================================================================
    def describeFeatureType(self, userName, typeName):
        """
        @summary: WFS describeFeatureType
        @param xml: xml request Record
            Record <list>: userName, typeName
        """
        try:                        
            params = {'typeName':typeName}
            layerNames = [typeName]
            permissions = self._securityManager.getUserPermissions(userName,layerNames=layerNames)
            self._securityFilter.filter(params, permissions,type='describefeaturetype')   
            if params['typeName'] == '':
                return MapServerTemplates.ogcServiceException %("You do not have permissions to view the requested layer") 
           
            response = self._layerRegistry.describeFeatureType(typeName)
            dom = self._toDOM(response)
            self._securityFilter.filter(dom, permissions,type='describefeaturetyperesponse') 
            response = self._toXML(dom)
            logger.info("describeFeatureType" )
            return str(response)
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not describeFeatureType')
            return MapServerTemplates.ogcServiceException %("Exception occured with describeFeatureType request, check log for details %s" %trace)
    
    def getMap(self, userName, paramsDict):
        """
        Called from MapServerFacade
        a wms request
        @param xml: xml document containing getMap Record
                Record <list>: userName, Params
                Params <mapping>: layers, width, height, transparent, styles, srs, bbox, format, bgcolor, sld, sld_body
        @return: base64 encoded data string map image
        """
        try:
            startTime = time.time()
            
            layerNames = paramsDict['layers'].split(",")
            permissions = self._securityManager.getUserPermissions(userName,layerNames=layerNames)            
            self._securityFilter.filter(paramsDict, permissions,type='getmap')             
            
            if paramsDict['layers'] == '':
                return MapServerTemplates.ogcServiceException %("You do not have permissions to view the requested layers")                 
            
            params = (paramsDict['layers'], paramsDict['width'], paramsDict['height'], 
                       paramsDict['transparent'], paramsDict['styles'], 
                       paramsDict['srs'], paramsDict['bbox'], paramsDict['format'], 
                       paramsDict['bgcolor'],paramsDict['exceptions'],paramsDict['time'],
                       paramsDict['elevation'],paramsDict['sld'],paramsDict['sld_body'])
            
            response = self._universalMapServer.getMap(*params)            
            endTime = time.time()
            logger.info("The getmap took: %s" %str(endTime - startTime)) 
            return str(response)
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not getMap')
            return MapServerTemplates.ogcServiceException %("Exception occured with getMap request, check log for details %s" %trace)
    
    def getLegendGraphic(self,userName, paramDict):
        """        
        @summary: applies security to the request and forwards the request to the universalMapServer
        @param: Record <list>: userName, Params
                Params <mapping>: layer, width, height,format
        @return: base64 encoded binary data
        """        
        try:            
            layerNames = paramDict['layer'].split(",")
            permissions = self._securityManager.getUserPermissions(userName,layerNames=layerNames)
                        
            self._securityFilter.filter(paramDict, permissions,type='getlegendgraphic')
            if paramDict['layer'] == '':
                return MapServerTemplates.ogcServiceException %("You do not have permissions to view the requested layer") 
                  
            imgData = self._universalMapServer.getLegendGraphic(paramDict['layer'],paramDict['format'],paramDict['width'],paramDict['height'],paramDict['sld'],paramDict['sld_body'])
            
            return imgData        
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not getLegendGraphic')
            return MapServerTemplates.ogcServiceException %("Exception occured with getLegendGraphic request, check log for details %s" %trace)
    
    def getCapabilities(self, userName, serviceType, facadeURL):
        """
        @summary: WMS or WFS getCapabilities
        @param xml: xml request Record
            Record <list>: userName, serviceType, facadeURL
        @return: a getCapabilities xml response or an error xml string
        """
        try:                    
            xml = self._layerRegistry.getCapabilities(serviceType,facadeURL)
            dom = self._toDOM(xml)            
            permissions = self._securityManager.getUserPermissions(userName)
            self._securityFilter.filter(dom, permissions)            
            response = self._toXML(dom)
            logger.info("getCapabilities" )
            return str(response)
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not getCapabilities')
            return MapServerTemplates.ogcServiceException %("Exception occured with getCapabilities request, check log for details %s" %trace)
    
    def getFeatureInfo(self, userName,params):
        """
        @summary: WMF Feature info request
        @param xml: xml request Record
            Record <list>: userName, Params
            Params <mapping>: queryLayers, i, j, width, height, bbox
            queryLayers <list>: layerName
            bbox <list>: xmin,ymin,xmax,ymax
        @return: a getfeature response string or xml error message
        """
        try:
            logger.info("getFeatureInfo" )                        
            params['srs'] = params['srs'].split(":")[-1]  
            
            layerNames = params['queryLayers']
            permissions = self._securityManager.getUserPermissions(userName,layerNames=layerNames)
            
            self._securityFilter.filter(params, permissions,type='getfeatureinfo')   
            
            if (params['layers'] == '') or (params['queryLayers'] == []) :
                return MapServerTemplates.ogcServiceException %("You do not have permissions to view the requested layers")
            
            # if one of the layers in query_layers does not have a wfsSource then
            # a getFeatureInfo in done instead of a getfeature            
            layerNames = params['queryLayers']
            layerStructure = self._layerRegistry.getLayerStructure(layerNames=layerNames)
            doGetFeatureInfo = False
            for layer in layerStructure:                
                if not layer['hasWFSLayer']:
                    doGetFeatureInfo = True
                    break
            if doGetFeatureInfo:                
                tmpParams = params
                tmpParams['query_layers'] = string.join(params['queryLayers'],',')
                del tmpParams['queryLayers']
                tmpParams['bbox'] = string.join(params['bbox'],',')
                res = self._universalMapServer.getFeatureInfo(**tmpParams)                
                return str(res)                        
                     
            self._translateWMSToWFS(params)
            responseDom = self._getFeatureInfoWithWMS(params)                     
            if responseDom is None:
                return ''
            else:
                self._securityFilter.filter(responseDom, permissions,type='getfeatureresponse')
                responseDom = self._stripGMLCoordinates(responseDom)
                response = self._toXML(responseDom)
                return str(response)   
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not getFeatureInfo')
            return MapServerTemplates.ogcServiceException %("Exception occured with getFeatureInfo request, check log for details %s" %trace)
      
    def getLayerStructure(self,userName,unfiltered=0,wmsSource=None,layerNames=None, organization=None):
        """
        @summary: called from mapserver facade. This function gets the layer structure from the layer registry and
        applies the security filter to the structure and returns the result.
        @param userName: plain text string defining the user name to filter on
        @param unfiltered: 0 or 1 defining whether security should be applied
        @param wmsSource: only return layers from the given wmsSource url
        @param layerNames: only return layers in the layerNames list
        @return: xml string containing layer structure that has been filtered by the security
        """
        layerStructure = self._layerRegistry.getLayerStructure(wmsSource=wmsSource,layerNames=layerNames, organization=organization)  
        if unfiltered == 1:             
            return layerStructure        
        else:          
            permissions = self._securityManager.getUserPermissions(userName)            
            filteredLayers = []
            for layer in layerStructure:
                if layer['uniqueName'] in permissions.keys():
                    filteredLayers.append(layer) 
            return filteredLayers           
        
    def getFeature(self, userName,paramsDict):
        """
        @summary: WMS getFeature request
        @param xml: xml request Record
            Record <list>: userName, Params
            Params Required <mapping>: typeName
            Optional Params <mapping>: 'propertyname','featureversion','maxfeatures','typename','featureid','filter','bbox','service'
        @return: an getfeature response string or an xml error message
        """
        try:
            logger.info("getFeature" )            
            layerNames = paramsDict['typename'].split(",")
            permissions = self._securityManager.getUserPermissions(userName,layerNames=layerNames)  
            
            self._securityFilter.filter(paramsDict, permissions,type='getfeaturerequest')             
            params = paramsDict 
            if paramsDict['typename'] == '':
                return MapServerTemplates.ogcServiceException %("You do not have permissions to view the requested layer ")                      
            response = self._universalMapServer.getFeature(**params)   
            
            dom = self._toDOM(response)
            self._securityFilter.filter(dom, permissions,type='getfeatureresponse')   
            response = self._toXML(dom)                      
            return str(response)
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not getFeature')
            return MapServerTemplates.ogcServiceException %("Exception occured with getFeature request, check log for details %s" %trace)
            
    # =====================================================================
    # Protected Interface
    # =====================================================================
    def _stripGMLCoordinates(self,dom):
        """
        @summary: called by getFeatureInfo to strip the gml coordinates from the xml dom returned from the getfeature request
        @param dom: dom instance containing xml structure from getfeature request
        @return: an xml dom instance
        """        
        remList = ['gml:lineStringProperty','gml:pointProperty','gml:polygonProperty','gml:MultiPolygon','gml:Polygon']
        for i in remList:
            elms = dom.getElementsByTagName(i)
            for elm in elms:
                parent = elm.parentNode.removeChild(elm)        
        return dom 
    
    def _getFeatureInfoWithWMS(self, params):   
        """
        @summary: translates wms getfeatureinfo params to a wfs getfeature request
        @param params: standard wms getfeatureinfo parameters
        @return: a xml dom containing getfeature results
        """     
        layerNames = params['queryLayers']        
        # transform the "pick point" from screen to map coords
        mapCoord2 = None
        imageSize = map(int,(params['width'],params['height']))
        boundingBox = map(float, params['bbox'])
        pickCoord = map(int,(params['i'],params['j']))
        if (params.has_key('x2')) and (params.has_key('y2')):
            pickCoord2 = map(int,(params['x2'],params['y2']))
            mapCoord2 = self._screenToMapCoords(boundingBox, imageSize, pickCoord2)
        mapCoord = self._screenToMapCoords(boundingBox, imageSize, pickCoord)
        
        responseDom = None
        featureCollection = None
        
        for layerName in layerNames:             
            geometryColumn = self._layerRegistry.getGeometryColumnForLayerName(layerName)
            if geometryColumn.find('ServiceException') != -1:
                return minidom.parseString(geometryColumn)
                         
            filter = self._createGetFeatureInfoFilter(boundingBox, mapCoord,geometryColumn,coord2=mapCoord2)            
            # do a getFeature WFS request
            paramDict = {'typename':layerName,'filter':filter}
            currentResponse = self._universalMapServer.getFeature(**paramDict)  
            
            #currentResponse = self._universalMapServer.getFeature(layerName, filter)
            
            currentDOM = self._toDOM(currentResponse)            
            if responseDom is None:
                try:
                    featureCollection = currentDOM.getElementsByTagName('wfs:FeatureCollection')[0]
                    responseDom = currentDOM
                except IndexError:
                    #not a valid response
                    featureCollection = None
#            else:
#                # extract the featureMembers and add them to the existing dom
#                for fm in d.getElementsByTagName('gml:featureMember'):
#                    featureCollection.appendChild(fm)
                    
        return responseDom
    
    def _screenToMapCoords(self, boundingBox, imageSize, coord):
        """
        @summary: Convert pixel coords to map coords
        @param boundingBox: map bounding box in map coordinates (minx,miny,maxx,maxy)
        @param imageSize: image size in pixels (width, height)
        @param coord: the coordinate to transform (x,y)
        @return: the transformed coord (x,y)
        """
        minx,miny,maxx,maxy = boundingBox
        width,height = imageSize
        x,y = coord
        
        mapWidth = maxx-minx
        mapHeight = maxy-miny
        
        xf = mapWidth / float(width)
        yf = mapHeight / float(height)
        
        mx = minx + xf*x
        my = maxy - yf*y
        
        return (mx,my)
        
    def _createGetFeatureInfoFilter(self, boundingBox, coord, geometryColumn, percentage=3,coord2=None):
        """
        @summary: Create a "pick box" filter element for a getFeatureInfo request
        @param boundingBox: the map bounding box (minx,miny,maxx,maxy)
        @param coord: the "pick" coordinate in map coordinates (x,y)
        @param percentage: the bounding box will be this percentage of total map size
        @param srs: the spatial reference system to use for request
        @return: a string containing the xml filter fragment
        """
        d = {}
        minx,miny,maxx,maxy = boundingBox
        x,y = coord
        
        boxWidth = ((maxx-minx) * (percentage / 100.0)) / 2.0
        boxHeight = ((maxy-miny) * (percentage / 100.0)) / 2.0
        
        if coord2:            
            d['minx'],d['miny'],d['maxx'],d['maxy'] = (coord[0],coord[1],coord2[0],coord2[1])
        else:
            d['minx'],d['miny'],d['maxx'],d['maxy'] = (x-boxWidth,y-boxHeight,x+boxWidth,y+boxHeight)
        d['geoColumn'] = geometryColumn 
        filter = FILTER_TEMPLATE %d        
        return filter    
    
    def _toDOM(self, xml):
        """
        @summary: Convert WMS/WFS xml to a DOM object
        @param: valid xml string
        @return: the xml string converted into a dom object
        """        
##        index = xml.find("</wfs:FeatureCollection>")
##        if index != -1:
##            xml = xml[0:index + 24]
        xml = xml.replace('xmlns:=""',"")
        xml = xml.replace("&"," ")
        return minidom.parseString(xml.strip())
        
    def _toXML(self, dom):
        """
        @summary: Convert WMS/WFS DOM to XML
        @param: a dom object
        @return: an xml string
        """
        return dom.toxml()
        
    def _translateWMSToWFS(self,dom):
        """
        @summary:translates the wms request parameters into the equivelant wfs request
        @param dom: a dom object
        """
        self._wmswfsMapper.toWFS(dom)
    
    def _translateWFSToWMS(self,dom):
        """
        @summary: translates wfs getfeature response into a wms getfeatureInfo response
        @param: a dom object
        """
        self._wmswfsMapper.toWMS(dom)
        
if __name__ == "__main__":
    pass
    
        
