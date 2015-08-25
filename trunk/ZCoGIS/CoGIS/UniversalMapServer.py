from ImageUtil import ImageUtil
import urllib
import os
from os import path
import time
from xml.dom import minidom
import cStringIO
import MapServerTemplates
import string
#import mapscript
import StringIO
import binascii
import logging
import httplib
from PIL import Image
from PIL import ImageDraw
import traceback

logger = logging.getLogger("UniversalMapServer")
#hdlr = logging.FileHandler('./Logs/UniversalMapServer.log')
hdlr = logging.FileHandler('UniversalMapServer.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)


# Constants
WFS_CAPABILITIES_EXTENSION = "version=1.0.0&request=getcapabilities&service=WFS"
WMS_CAPABILITIES_EXTENSION = "version=1.0.0&request=getcapabilities&service=WMS"
WFS_DESCRIBEFEATURETYPE_EXTENSION = "version=1.0.0&request=DescribeFeatureType&service=WFS"
WFS_GETFEAURE_EXTENSION = "version=1.0.0&service=WFS&request=GetFeature"
WMS_GETMAP_EXTENSION = "version=1.0.0&request=GetMap&service=WMS"
invalidChars = [':','?','<','>','{','}','[',']','!','@','#','$','%','^','&','*','(',')','+','=','|',',','/','\\']  

#==========================================================================
# Super Important NOTE: All WMS layers MUST have the same projection !!!!!!
#==========================================================================
GLOBAL_SRS = "EPSG:4326"

class UniversalMapServer:
    soapServer = None
    def __init__(self,facade):
        """
        @param mapFilePath: the phisical disk path of the mapfile, the mapfile is used to initialize the server. 
        @param sources: a list of sources in the format [("http://wfsSource?","http://wmsSource?")]
        @param soapHost: the hostname of the soap server
        @param soapPort: the port for the soap server to serve on
        """
        self.facade = facade       
        self.cleanup_counter = 0
        
#===========================================================
#   Public Methods
#===========================================================
        
    def _deleteLayersWithSource(self,source):
        """
        @summary: deletes all layers with the given source
        @param: a tuple source structure e.g (wfsSource,wmsSource)
        """
        tmpList = []     
        for layer in self.facade.layerList:         
            if (layer['source'][1].lower() != source[1].lower()) or (layer['source'][0].lower() != source[0].lower()) or (layer['source'][2].lower() != source[2].lower()):                              
                tmpList.append(layer)   
        self.facade.layerList = tmpList 
            
    def discoverLayers(self,singleSource=None):
        """
        @summary: this will send GetCapabilities and describeFeatureType requests to all the sources
        The structure returned is a list of dict objects that contain layer info
        """   
        try:
            if not self.facade.sources:                
                return MapServerTemplates.ogcServiceException %("No sources have been set in the Universal Map Server")      
            
            if singleSource:     
                tmpSource = singleSource
                theSources = [tmpSource]   
            else:
                self.facade.layerList = [] 
                theSources = self.facade.sources               
            
            for source in theSources:
                self._deleteLayersWithSource(source)
                wfsURL = source[0] + WFS_CAPABILITIES_EXTENSION
                wmsURL = source[1] + WMS_CAPABILITIES_EXTENSION    
                
                organization = source[2]              
                if source[0].strip() == "":
                    hasWFS = False
                else:
                    try:                        
                        hasWFS = True
                        data = self._getURLContent(wfsURL)   
                        self.facade.timeouts[source[0]] = ""   
                        
                        if data.find("ServiceExceptionReport") != -1:
                            if data.find("Operation timed out") != -1:                                      
                                self.facade.timeouts[source[0]] = "Operation timed out"  
                                continue
                        if data.find("Operation timed out") != -1:                    
                            self.facade.timeouts[source[0]] = "Operation timed out"
                            continue 
                                            
                        if data.find(" 404 ") != -1:
                            self.facade.timeouts[source[0]] = "Resource is not available or does not exist"                        
                            continue  
                        
                        if data.lower().find("wfs_capabilities") == -1:
                            self.facade.timeouts[source[0]] = MapServerTemplates.ogcServiceException %("WFS Source given is not a valid wfs source")                         
                            continue  
                        
                        data = self._removeHTMLComments(data)
                        wfsDom = minidom.parseString(data) 
                        wfsNameElms = wfsDom.getElementsByTagName("Name")
                        wfsFeatureElms = wfsDom.getElementsByTagName("FeatureType")
                        wfsLayerNames = [x.firstChild.nodeValue for x in wfsNameElms]
                        
                    except:
                        logger.exception('Error parsing XML results (WFS):\n%s' %(data))                        
                        sio = cStringIO.StringIO()
                        traceback.print_exc(file=sio)
                        sio.seek(0)
                        trace = sio.read()
                        self.facade.layerList.append({'source':source,'error':trace})                        
                        continue                    
                
                wmsData = self._getURLContent(wmsURL)                 
                wmsData = self._removeHTMLComments(wmsData)
                try:      
                    self.facade.timeouts[source[1]] = ""   
                    if wmsData.find("ServiceExceptionReport") != -1:
                        if wmsData.find("Operation timed out") != -1:                                       
                            self.facade.timeouts[source[1]] = "Operation timed out" 
                            continue
                    if wmsData.find("Operation timed out") != -1:                    
                        self.facade.timeouts[source[1]] = "Operation timed out"
                        continue 
                    
                    if wmsData.find(" 404 ") != -1:
                        self.facade.timeouts[source[1]] = "Resource is not available or does not exist"
                        continue
                    
                    if wmsData.lower().find("wmt_ms_capabilities") == -1:
                        self.facade.timeouts[source[0]] = wmsData                        
                        continue
                         
                    wmsDom = minidom.parseString(wmsData)
                except:
                    logger.exception('Error parsing XML results (WMS):\n%s' %(wmsData))                    
                    sio = cStringIO.StringIO()
                    traceback.print_exc(file=sio)
                    sio.seek(0)
                    trace = sio.read()  
                    self.facade.layerList.append({'source':source,'error':trace})
                    
                    continue
                # parse the wms response
                try:
                    wmsDom.getElementsByTagName("Layer")[0] 
                except:
                    logger.exception('Error parsing XML results (WMS):\n%s' %(wmsData))                    
                    sio = cStringIO.StringIO()
                    traceback.print_exc(file=sio)
                    sio.seek(0)
                    trace = sio.read()                    
                    self.facade.layerList.append({'source':source,'error':trace})                    
                    continue                
                    
                wmsLayersContainer = wmsDom.getElementsByTagName("Layer")[0] 
                wmsLayers = wmsLayersContainer.getElementsByTagName("Layer")      
                                
#                onlineResourceList = wmsDom.getElementsByTagName("OnlineResource")              
#                if onlineResourceList:
#                    onlineResource = onlineResourceList[0].getAttribute("xlink:href")
                for wmsLayer in wmsLayers: 
                    wmsQueryable = wmsLayer.getAttribute('queryable')
                    wmsName = wmsLayer.getElementsByTagName('Name')[0].firstChild.nodeValue               
                    
                    wmsSRSElms = wmsLayer.getElementsByTagName('SRS')
                    if wmsSRSElms:                            
                        wmsSRS = wmsLayer.getElementsByTagName('SRS')[0].firstChild.nodeValue
                    else:
                        wmsSRS = GLOBAL_SRS
                    wmsStyleElms = wmsLayer.getElementsByTagName('Style')
                    if wmsStyleElms:                    
                        nameElms = wmsLayer.getElementsByTagName('Style')[0].getElementsByTagName('Name')
                        if nameElms:
                            if wmsLayer.getElementsByTagName('Style')[0].getElementsByTagName('Name')[0].firstChild:
                                wmsStyleName = wmsLayer.getElementsByTagName('Style')[0].getElementsByTagName('Name')[0].firstChild.nodeValue                                            
                            else:
                                wmsStyleName = "default"
                        else:
                            wmsStyleName = "default"
                    else:
                        wmsStyleName = "default"
                    
                    wmsTitleElms = wmsLayer.getElementsByTagName('Title')
                    if wmsTitleElms:                        
                        wmsTitle = wmsTitleElms[0].firstChild.nodeValue
                    else:
                        wmsTitle = wmsName
                    
                    abstractElms = wmsLayer.getElementsByTagName('Abstract')
                    if abstractElms:
                        abstract = abstractElms[0].firstChild.nodeValue
                    else:
                        abstract = ""                    
                    
                    keywordElms = wmsLayer.getElementsByTagName('Keyword')
                    if keywordElms:
                        keyword = keywordElms[0].firstChild.nodeValue                    
                    else:
                        keyword = ""
                    
                    elmsLatLon = wmsLayer.getElementsByTagName('LatLonBoundingBox')
                    if not elmsLatLon:
                        minx = -180
                        miny = -90
                        maxx = 180
                        maxy = 90
                    else:
                        minx = wmsLayer.getElementsByTagName('LatLonBoundingBox')[0].getAttribute('minx')
                        miny = wmsLayer.getElementsByTagName('LatLonBoundingBox')[0].getAttribute('miny')
                        maxx = wmsLayer.getElementsByTagName('LatLonBoundingBox')[0].getAttribute('maxx')
                        maxy = wmsLayer.getElementsByTagName('LatLonBoundingBox')[0].getAttribute('maxy')
                    wmsBoundingBox = [minx,miny,maxx,maxy]  
                    
                    img = self._getSampleImage(wmsName,source[1],wmsBoundingBox)                
                    
                    wmsXML = wmsLayer.toxml().replace("\r","").replace("\n","")                
                    
                    geometryType = ""
                    geometryField = ""
                    layerFields = {}
                    describeFeatureTypeResponse = ""
                    
                    wfsXML = ""
                    wfsName = ""
                    hasWFSLayer = False
                                        
                    if hasWFS:                          
                        nameIndex = self._wmsNameinWfsNames(wmsName,wfsLayerNames)                  
                        #if wmsName in wfsLayerNames:                         
                        if nameIndex != -1:                              
                            wfsName = wfsLayerNames[nameIndex]                                    
                            #wfsNameIndex = wfsLayerNames.index(wmsName)
                            #wfsFeatureElm = wfsFeatureElms[nameIndex - 1 ] # changed for arcims services with wfs
                            wfsFeatureElm = wfsFeatureElms[nameIndex-1]
                            wfsXML = wfsFeatureElm.toxml().replace("\r","").replace("\n","")                            
                            hasWFSLayer = True                  
                            #layerFields,describeFeatureTypeResponse = self._getFieldsForLayer(wmsName,source[0])  
                            layerFields,describeFeatureTypeResponse = self._getFieldsForLayer(wfsName,source[0])  
                            geometryField,geometryType = self._getGeometryTypeFromFields(layerFields)                          
                            if not geometryField:
                                geometryField = self._determineGeometryField(layerFields.keys())   
                        else:
                            pass                            
                        
                    else:
                        layerFields = {}
                        describeFeatureTypeResponse = MapServerTemplates.ogcServiceException %("WFS Source was not given for this layer")
                        geometryField = ""
                        geometryType = ""                
                                  
                    if not geometryType:        
                        geometryType = self._getGeometryTypeFromMap(wmsName,source[1]) 
                        if geometryType == "RASTER":
                            hasWFSLayer = True  
                    uniqueName = self._getIncrementedName(wmsName) 
                                       
                    wmsXML = wmsXML.replace(wmsName,uniqueName)                
                    wfsXML = wfsXML.replace(wfsName,uniqueName)
                    
                    if not geometryType: # or (not geometryField):
                        layerStructure = {'uniqueName': uniqueName,'geometryField':geometryField,'geometryType':geometryType,'wfsName':wfsName,
                                    'title':wmsTitle,'abstract':abstract,'keywords':keyword,'wfsSRS':wmsSRS,'wmsStyleName':wmsStyleName,
                                    'wfsBoundingBox':wmsBoundingBox,'fields':layerFields,'source':source,'error':'Could not determine the type of the layer',
                                    'wmsQueryable':wmsQueryable,'wmsName':wmsName,'wmsSRS':wmsSRS,'wmsTitle':wmsTitle,
                                    'wmsBoundingBox':wmsBoundingBox,'describeFeatureResponse':describeFeatureTypeResponse,
                                    'sampleImage':img,'hasWFSLayer':hasWFSLayer,'wmsXML':wmsXML, 'wfsXML':wfsXML, 'organization':organization}
                        self.facade.layerList.append(layerStructure)                    
                        continue   
                    
                    layerStructure = {'uniqueName': uniqueName,'geometryField':geometryField,'geometryType':geometryType,'wfsName':wfsName,
                                    'title':wmsTitle,'abstract':abstract,'keywords':keyword,'wfsSRS':wmsSRS,'wmsStyleName':wmsStyleName,
                                    'wfsBoundingBox':wmsBoundingBox,'fields':layerFields,'source':source,'error':'',
                                    'wmsQueryable':wmsQueryable,'wmsName':wmsName,'wmsSRS':wmsSRS,'wmsTitle':wmsTitle,
                                    'wmsBoundingBox':wmsBoundingBox,'describeFeatureResponse':describeFeatureTypeResponse,
                                    'sampleImage':img,'hasWFSLayer':hasWFSLayer,'wmsXML':wmsXML, 'wfsXML':wfsXML, 'organization':organization}
                    self.facade.layerList.append(layerStructure) 
            
            if singleSource:
                # only return layers from the source that was passed as single source
                retList = []
                for layer in self.facade.layerList:                
                    if (layer['source'][1] == tmpSource[1]) and (layer['source'][0] == tmpSource[0]) and (layer['source'][2] == tmpSource[2]):
                        retList.append(layer)                            
            else:
                retList = self.facade.layerList            
            return retList
        except:
            logger.exception('Error with discovers')            
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            return MapServerTemplates.ogcServiceException %("Exception with discover layers: %s" %trace)         
    
    def _wmsNameinWfsNames(self,wmsName,wfsNames):
        """
        @summary: get the list index for the wms name that matched a part of a wfs name
        returns -1 if no match was found
        @param wmsName: the wms name to look for in wfsNames
        @param wfsNames: a list if wfs names
        """
        if wmsName in wfsNames:
            index = wfsNames.index(wmsName)
            return index
        
        # filter for arcims matching
        count = 0
        for name in wfsNames:
            tmpName = name.split("-")[0]            
            if wmsName.lower() == tmpName.lower():
                return count
            count += 1        
        return -1;        
        
    def _getSampleImage(self,layerName,source,extent):
        """
        @summary: does a getmap request on the layer source and returns the image data
        @param layerName: the name of the layer to get the map for. The wmsName from the getCapabilities request
        @param source: the url source of the server where the layer resides
        @param extent: the bounding box or envelope of the map to retrieve
        @return: an ascii hex string containing the image data
        """
        try:
            layerName = layerName.replace(" ","%20")
            strEnv = "%s,%s,%s,%s" %(extent[0],extent[1],extent[2],extent[3])
            theURL = source + WMS_GETMAP_EXTENSION + "&bbox=%s&styles=&Format=image/png&width=150&height=150&srs=EPSG:4326&layers=%s" %(strEnv,layerName) #"&request=GetLegendGraphic&version=1.0.0&format=%s&width=%s&height=%s&layer=%s" %(format,width,height,layer['wmsName'])        
            data = self._getURLContent(theURL,{})           
            asciiData = binascii.b2a_hex(data)   
            self.cleanup_counter += 1          
            return asciiData             
        except:            
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not get _getSampleImage')
            return MapServerTemplates.ogcServiceException %("Exception occured with _getSampleImage request, check log for details %s" %trace)             
    
    def getLegendGraphic(self,layerName,format="image/png",width=20,height=20,sld="",sld_body=""):
        """
            @summary: retrieves the legend graphic for the given layer name            
            @param layerName: the name of the layer to retrieve the legend image for
            @param format: the format in which to return the image
            @param width: the width of the image to return
            @param height: the height of the image to return
            @return: returns the legend graphic data for the image in a base64 encoding, or a service exception if an error occurs
        """        
        try:
            if (not self.facade.layerList):
                return MapServerTemplates.ogcServiceException %("discoverLayers has not been called, mapfile is empty")
            
            if not layerName:
                return MapServerTemplates.ogcServiceException %("No layers given for GetLegendGraphic") 
            
            self.cleanup_counter += 1
            sourceURL = ""          
            for layer in self.facade.layerList:                 
                if layer.has_key('uniqueName') and layer['uniqueName'] == layerName:
                    sourceURL = layer['source'][1]
                    theURL = sourceURL + "&request=GetLegendGraphic&version=1.0.0&format=%s&width=%s&height=%s&layer=%s" %(format,width,height,layer['wmsName'].replace(" ","%20"))
                    if sld.strip() != "":
                        theURL += '&sld=' + sld
                    if sld_body.strip() != "":
                        theURL += '&sld_body=' + sld_body
                    try:
                        data = self._getURLContent(theURL,{})                      
                        if (data.find("ServiceException") != -1):
                            return data
                        else:
                            return binascii.b2a_base64(data)                                      
                    except:                        
                        sio = cStringIO.StringIO()
                        traceback.print_exc(file=sio)
                        sio.seek(0)
                        trace = sio.read()
                        logger.exception('Could not get getLegendGraphic') 
                        return ""         
            
            return MapServerTemplates.ogcServiceException %("%s is not a valid layer name for GetLegendGraphic request" %layerName) 
        except:            
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not get getLegendGraphic')
            return MapServerTemplates.ogcServiceException %("Exception occured with getLegendGraphic request, check log for details %s" %trace)
    
    def getLayerByName(self,layerName):
        """
        @summary: retieves the layer dict from the layerList with the given name
        @param layerName: unique layer name
        @return: dictionary object containing layer information
        """
        for layer in self.facade.layerList:
            if layer['uniqueName'] == layerName:
                return layer        
        return None 
    
    def _getInvalidSources(self):
        """
        @summary: does a url open on each of the sources and checkes if the url is still active
        @return: a list of sources that can not be opened
        """
        invalidSources = {}
        for source in self.facade.sources:
            part = source[1]            
            if part.strip() != '':
                try:
                    res = urllib.urlopen(part)
                    data = res.read()
                    data = data.lower()
                    if (data.find("html") != -1) or (data.find("serviceexception") != -1 or data.strip() == ''):                            
                        pass
                    else:                            
                        invalidSources[part] = ''
                except:
                    invalidSources[part] = ''
        return invalidSources.keys()
    
    def _getTextImage(self,text,width=400,height=400):
        """
        @summary:
        @return:
        @param text:
        @param width:
        @param height:
        """        
        tmpImg = Image.new("RGB",(width,height),(33,73,115))    
        draw = ImageDraw.Draw(tmpImg)
        draw.text((0,0),text)
        
        text = text.replace(".","\n").replace(",","\n").replace(":","\n")
        tList = text.split("\n")
        yPos = 0
        for i in tList:    
            draw.text((0,yPos),i)
            yPos += 10        
        
        del draw  
        tmpIO = StringIO.StringIO('')
        tmpImg.save(tmpIO,"PNG")
        resData = tmpIO.getvalue() 
        return resData   
    
    def getImageTypeFromString(self, formatString):
        """
        @summary: get the image format from the format string e.g "image/png"
        """
        formats = ["PNG","JPEG","GIF"]
        type = "PNG"
        parts = formatString.split("/")
        if len(parts) > 1:
            fmt = parts[1]
            if fmt.strip().upper() in formats:
                return fmt.upper()        
        return type         
    
    def getMap(self,layers,width="400",height="400",transparent="true",styles="",srs="EPSG:4326",
                bbox="-180,-90,180,90",format="image/png",bgcolor="0xFFFFFF",exceptions="XML",Time="",elevation="",sld="",sld_body=""):
                
        try:
            srs="EPSG:4326"   
            localFormat = "image/gif"
            dataTemplate = "layers=%(layers)s&width=%(width)s&height=%(height)s&transparent=%(transparent)s&styles=%(styles)s&srs=%(srs)s&bbox=%(bbox)s&format=%(format)s&bgcolor=%(bgcolor)s&exceptions=%(exceptions)s&Time=%(Time)s&elevation=%(elevation)s&sld=%(sld)s&sld_body=%(sld_body)s"
            getMapStub = "request=getmap&version=1.0.0&"
            
            imgUtil = ImageUtil()
            layers = layers.split(",")    
            imageList = []
            for layer in layers:  
                layerDict = self.getLayerByName(layer)
                wfsSource = layerDict['source'][0]
                wmsSource = layerDict['source'][1]            
                theURL = wmsSource      
                # get the layer image and merge it with the other images
                data = {"layers":layer,"width":width, "height":height, "transparent":transparent, "styles":styles, "srs":srs, "bbox":bbox,
                        "format":localFormat, "bgcolor":bgcolor , "exceptions":exceptions , "Time":Time , "elevation":elevation, "sld": sld,"sld_body":sld_body}
                dataStr = dataTemplate %data       
                all = theURL + getMapStub + dataStr
                res = imgUtil.getURLContent(all, {})        
                imageList.append(imgUtil.getPILImageFromData(res))
        
            # build a composite of the images
            res = imgUtil.mergeImageList(imageList)
                        
            f = StringIO.StringIO()
            res.save(f, self.getImageTypeFromString(format))
            f.seek(0)
            data = f.read()
            f.close()                                                
            data = binascii.b2a_base64(data)
            return data            
        except:
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()   
            logger.exception('Could not get getMap %s' %str(trace))           
    
    
#    def getMapOrg(self,layers,width="400",height="400",transparent="true",styles="",srs="EPSG:4326",
#                bbox="-180,-90,180,90",format="image/png",bgcolor="0xFFFFFF",exceptions="XML",Time="",elevation="",sld="",sld_body=""):
#        """
#        called from the RequestResponseTranslator
#        @summary: does a GetMap request via mapscript nad returns the base64 encoded binary data string        
#        @param layers: a comma separated list of layer names to display, defaults to all
#        @param width: the width of the map to draw
#        @param height: the height of the map to draw
#        @param transparent: string being true or false, sets background color transparent
#        @param styles: sld styles to use to render layers
#        @param srs: the spatial reference system to use for rendering
#        @param bbox: the envelope of the map to render
#        @param format: the output format of the image being requested
#        @param bgcolor: the image background color in hex
#        @param exceptions: the format in which excdeptions are returned SE_XML
#        @param Time: time value of the desired layer
#        @param elevation: the elevation of the layer
#        @param sld: the url to the sld for the layer
#        @param sld_body : the fisical sld document string
#        @return: Image data is returned in base64 encoded ascii string, or a service exception if an error occurs
#        """    
#                
#        self.cleanup_counter += 1
#        srs="EPSG:4326"               
#        try:
#            if (not self.facade.layerList):
#                return MapServerTemplates.ogcServiceException %("discoverLayers has not been called, mapfile is empty")   
#                      
#            layerList = layers.split(",")
#            tmpMapFile = self._getTempMapFile(self.facade.layerList, layerList)
#            
#            tmpName = "tmp_" + str(time.time()).replace(".","") + ".map"    
#            f = open(tmpName,"w")            
#            f.write(tmpMapFile)
#            f.close()   
#            
#            map = mapscript.mapObj(tmpName)   
#            tmpMap = map.clone()             
#            
#            tmpLayerList = []
#            for l in layerList:
#                layer = tmpMap.getLayerByName(l)                
#                if layer:                    
#                    tmpLayerList.append(layer.name)
#                # check that layer is valid name
#            if not tmpLayerList:
#                return MapServerTemplates.ogcServiceException %("No valid layers found in WMS GetMap request.") 
#            
#            invalidLayers = []
#            invalidSources = self._getInvalidSources()            
#            if invalidSources:
#                for layer in tmpLayerList:
#                    layerDict = self.getLayerByName(layer)
#                    wfsSource = layerDict['source'][0]
#                    wmsSource = layerDict['source'][1]
#                    if (wfsSource in invalidSources) or (wmsSource in invalidSources):
#                        invalidLayers.append(layer)                              
#            
#            validLayerList = [x for x in tmpLayerList if x not in invalidLayers]
#            layers = string.join(validLayerList,",")    
#            
#            if not layers:
#                pass            
#                   
#            wmsRequest = mapscript.OWSRequest()         
#            wmsRequest.setParameter("layers", layers)           
#            wmsRequest.setParameter("width", width)           
#            wmsRequest.setParameter("height", height)           
#            wmsRequest.setParameter("transparent", transparent)           
#            wmsRequest.setParameter("styles", styles)           
#            wmsRequest.setParameter("srs", srs)           
#            wmsRequest.setParameter("bbox", bbox)           
#            wmsRequest.setParameter("format", format)           
#            wmsRequest.setParameter("bgcolor", bgcolor)  
#            wmsRequest.setParameter("sld", sld)                 
#            if sld_body:
#                wmsRequest.setParameter("sld_body", sld_body)                 
#            
#            layerNames = layers.split(",")         
#            for layerName in layerNames:            
#                layer = tmpMap.getLayerByName(layerName)
#                if layer:
#                    layer.status = 1                                 
#            
#            tmpMap.loadOWSParameters(wmsRequest,'1.0.0')
#            fileHandle = StringIO.StringIO()          
#            
#            image = tmpMap.draw()
#            image.write(fileHandle) 
#            
#            fileHandle.seek(0)
#            data = fileHandle.read()
#            fileHandle.close() 
#            
#            if self.cleanup_counter > 100:
#                self.cleanup_counter = 0
#                self._cleanUpTempFiles()            
#                self._deleteTempMapFile(tmpName)                   
#            
#            data = binascii.b2a_base64(data)                 
#            return data 
#        except:  
#            sio = cStringIO.StringIO()
#            traceback.print_exc(file=sio)
#            sio.seek(0)
#            trace = sio.read()            
#            trace = trace.replace("\n","").replace("\r","")            
#                        
#            params = {'layers':layers ,'width':width ,'height':height ,'transparent':transparent ,'styles':styles,
#            'srs':srs ,'bbox':bbox ,'format':format ,'bgcolor': bgcolor,'time':time,'sld':sld}
#            
#            logger.exception('Could not get getMap %s' %str(params))
#            return trace
#            return binascii.b2a_base64(self._getTextImage(trace,int(width),int(height)))            
#            #return MapServerTemplates.ogcServiceException %("Exception occured with getMap request, check log for details. %s" %trace )     
#    
    
    def getFeatureInfo(self,**kwargs):
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
            kwargs['format'] = 'image/png'     
            kwargs['info_format'] = 'text/plain'      
            #kwargs['info_format']  
            if (not self.facade.layerList):
                return "discoverLayers has not been called, mapfile is empty"  
            sourceURL = ""      
            
            allData = ''
            passedLayerList = kwargs['query_layers'].split(",")   
            for layer in self.facade.layerList:            
                if layer['uniqueName'] in passedLayerList: 
                    sourceURL = layer['source'][1]                    
                    wmsName = layer['wmsName']  
                    
                    params = {'query_layers':wmsName,'x':kwargs['i'],'y':kwargs['j'],'feature_count':kwargs['feature_count'],'width':kwargs['width'],'height':kwargs['height'],
                        'bbox':kwargs['bbox'],'layers':wmsName,'srs':'EPSG:'+kwargs['srs'],'styles':kwargs['styles'],'version':kwargs['version'],'format':kwargs['format'],'info_format':kwargs['info_format']}
                    
                    urlQuoted = sourceURL + 'request=getfeatureinfo&service=wms'
                    for k in params.keys():
                        urlQuoted += '&' +k+ '=' + str(params[k])                     
                    data = self._getURLContent(urlQuoted,{})        
                    try:
                        data = str(data)
                    except:
                        data = 'Layer %s Returned an Error' %layer['uniqueName']
                    allData += data
            return allData
        except:           
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()            
            logger.exception('Could not getFeatureInfo')
            return MapServerTemplates.ogcServiceException %("Exception occured with getFeatureInfo request, check log for details %s" %trace)
    
        
        return ""    
    
    def getFeature(self,maxFeatures=50,**kwargs):
        """  
        @summary: does a getfeature request via url get 
        @param maxFeatures: the max number of results to request
        @param kwargs: can contain 'propertyname','featureversion','maxfeatures','typename','featureid','filter','bbox','service'
        @return: a xml gml response from a getfeature request
        """          
        try:
            if (not self.facade.layerList):
                return "discoverLayers has not been called, mapfile is empty"            
            
            sourceURL = ""
            if not kwargs.has_key('maxfeatures'):
                kwargs['maxfeatures'] = maxFeatures
            
            typeName = kwargs['typename']              
            for layer in self.facade.layerList:            
                if (layer.has_key('uniqueName')) and (layer['uniqueName'] == typeName):                    
                    if not layer['hasWFSLayer']:
                        return MapServerTemplates.ogcServiceException %("WFS Source not given for layer %s" %(typeName))
                    sourceURL = layer['source'][0]                    
                    wfsName = layer['wfsName']                    
            if not sourceURL:
                return MapServerTemplates.ogcServiceException %("Layer %s could not be found in mapfile" %(typeName))                   
            
            # XXX remove this if it brakes the getfeature of mapserver and geoserver
            # XXX  arcims does not accept the url params in a post request
            postURL = sourceURL #+ "service=WFS&version=1.0.0&request=getfeature&typename="+wfsName            
            
            if kwargs.has_key('filter'):
                kwargs['filter'] = urllib.unquote(kwargs['filter'])
                gml = 'xmlns:gml="http://www.opengis.net/gml"'
                wfs = 'xmlns:wfs="http://www.opengis.net/wfs"'
                ogc = 'xmlns:ogc="http://ogc.org"' 
                
                esri = 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'     
                esriComplete = '<host_name>:<port_number>/<path>'
                esriPort = '<port_number>'
                esriHost = '<host_name>'
                esripath = '<path>'   
                   
                kwargs['filter'] = kwargs['filter'].replace(gml,"").replace(wfs,"").replace(ogc,"").replace(esri,"").replace(esriComplete,"").replace(esriPort,"").replace(esriHost,"").replace(esripath,"")     
                postString = MapServerTemplates.getFeatureQueryTemplate %(kwargs['maxfeatures'],wfsName,kwargs['filter'])              
                                
                postString = postString.replace("\n","").replace("\r","")                
                
                data = self._getPostContent(postURL,postString)  
            else:
                del kwargs['typename']
                urlQuoted = sourceURL + 'request=getfeature&service=wfs&version=1.0.0&typename=%s' %wfsName
                for k in kwargs.keys():
                    urlQuoted += '&' +k+ '=' + str(kwargs[k])                
                data = self._getURLContent(urlQuoted,{})                
            try:       
                if (data.find("ServiceException") != -1)  or (data.find("ServiceExceptionReport") != -1):# or (data.find("gml:boundedBy") == -1):                
                    pass                 
                if data == "":
                    return ""                   
                orgCleanName = wfsName.split(":")[-1]
                newCleanName = typeName.split(':')[-1] 
                data = data.replace(orgCleanName,newCleanName)   
                data = data.replace(typeName,typeName.replace(" ",""))  
                data = data.replace(esriComplete,"").replace(esriPort,"").replace(esriHost,"").replace(esripath,"")    
                return data               
            except:                
                sio = cStringIO.StringIO()
                traceback.print_exc(file=sio)
                sio.seek(0)
                trace = sio.read()  
                logger.exception('Could not getFeature')            
                return trace  
        except:            
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not getFeature')
            return MapServerTemplates.ogcServiceException %("Exception occured with getFeature request, check log for details %s" %trace)
        
    def hasSource(self):
        """
        @summary: checks if the ums has sources
        @return: a boolean stating whether the ums has sources
        """
        if self.facade.sources:
            return True
        return False             
    
    def updateLayers(self,singleSource=None):
        """
        @summary: Is called from the MapServerFacade and response is used to update the layer registry
        @return: an xml structure that contains the layer attributes or a service exception if an error occurs
        """  
        try:      
            layerList = self.discoverLayers(singleSource)            
            return layerList 
        except:            
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()            
            logger.exception('Could not updateLayers')
            return MapServerTemplates.ogcServiceException %("Exception occured with updateLayers request, check log for details %s" %trace) 
    
    def setLayerList(self,layerList):
        """
        @summary: This method is used to set the state for the ums and build the map file for doing GetMap Requests
        @param layerListXML: is an xml representation of "self.layerList" that is used to initialize the UMS and build the map file
        """
        try:
            self.facade.layerList = []
            self.facade.sources = [] # XXX remove this line if update gives errors             
            self.facade.layerList = layerList
            
            for layer in self.facade.layerList:
                source = layer['source']
                if not source in self.facade.sources:
                    self.facade.sources.append(source)              
        except:            
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not setLayerList ' + trace)                    
    
    def deleteSource(self,source):
        """
        @summary: deletes a given source from the source list given the source xml structure
        @param: source is a tuple containing the wfs and wms source to be removed e.g (wfs,wms) in xml format with dumps
        @return: 1 or an xml error message
        """
        try:
            if not source:
                return 
            
            struct = source
            wmsSource = struct[1]           
            if struct:
                self.facade.sources = [x for x in self.facade.sources if (x[1] != wmsSource) or (x[1].find(wmsSource) == -1 )]                   
                self._deleteLayersWithSource(struct)  
            self.changed = True;  
            return 1
        except:           
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not deleteSource')
            return MapServerTemplates.ogcServiceException %("Exception occured with setSources request, check log for details %s" %trace)             
    
    
       
#===========================================================
#   Private Methods
#===========================================================

    def _getIncrementedName(self,name):
        """
        @summary: checks that the layer name is unique, else increments it. Also replaces invalid chars with "_" so that name can be used as a plone id
        @param name: the layer name to be incremented by one if it already exists in the layer structure of the ums
        @return: the incremented layer name 
        """   
        for c in invalidChars:
            name = name.replace(c,'_')          
        checkList = [x['uniqueName'] for x in self.facade.layerList]  
                      
        counter = 1
        tmpName = name
        if tmpName in checkList:           
            while tmpName in checkList:
                tmpName = name + str(counter)
                counter +=1            
            return tmpName            
        else:            
            return name      
    
    def _getParametersFromUrl(self,url):
        """
        @summary: this will parse the url parameters into a dict
        @param url: the url with parameters to parse into a dict
        @return: a dict of url parameters
        """      
        paramPart = url.split("?")[-1]
        paramParts = paramPart.split("&")
        paramDict = {}
        for param in paramParts:
            paramDict[param.split("=")[0]] = param.split("=")[1]        
        return paramDict
        
    
    def _getPostContent(self,url,data=''):
        """
        """
        if url[len(url)-1] == '&':
            url = url[0:len(url)-1]
        url = url.replace("http://",'')
        url = url.replace("HTTP://",'')
        index = url.find("/")
        hostname = url[0:index]
        server = url[index:]        
        
        h = httplib.HTTP(hostname)
        h.putrequest("POST", server)
        h.putheader("Content-type", "text/xml")
        h.putheader("Content-length", "%d" % len(data))
        h.putheader("Accept", "text/xml")
        h.putheader('Host', hostname)
        h.endheaders()
        h.send(data)
        reply, msg, hdrs = h.getreply()   
        data = h.getfile().read()        
        return data     
    
    def _getURLContent(self,url,data={}):
        """
        @summary: retrieves the content of the given url
        @param url: the url's content to return 
        @param data: the data to pass to the url        
        @return: the data string read from the response
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
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception("Error in get url content") 
            return MapServerTemplates.ogcServiceException %("Exception occured getURLContent request, check log for details %s" %trace) 
            
    
    def _getURLFileObject(self,url,data={}):
        """
        @summary: retrieves the document/ file related to the given url
        @param url: the url to get file object for
        @param data: the data to pass to the url
        @return: the file object associated with the url        
        """
        try:
            if data:
                params = urllib.urlencode(data)
                f = urllib.urlopen(url,params)   
            else:
                f = urllib.urlopen(url)      
             
            return f.fp
        except:            
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()            
            sio.seek(0) 
            logger.exception("Error in get url file object " + trace) 
            return sio
        
    def _cleanUpTempFiles(self):
        """
        @summary: checks the current directory for any files with the "*.img.tmp" extention
        or files starting with"_tmp" and tries to delete the file.
        All tmp map files older than 5 min are deleted
        """
        try:
            compareTime = time.time()
            files = os.listdir("")
            for file in files:
                if (file.find(".img.tmp") != -1) or file.find("tmp_") != -1 or file.find(".sld.xml") != -1:
                    creation = path.getctime(file)
                    diff = compareTime - creation
                    if (diff / 60) > 5:
                        os.remove(file)                
        except:            
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not clean old images ' + trace)            
    
    def _deleteTempMapFile(self,name):
        """
        @summary: This will delete the temp map file
        @param name: the name of the file to delete
        """
        try:            
            os.remove(name) # do cleanup
        except:
            logger.exception('Could not delete tmp files')      
    
    def _getGeometryTypeFromFields(self,layerFields):
        """
        @summary: this will check if the geometry type has been deifned in the DescribeFeatureType response
        If the type cannot be found in this reponse then a getfeature request is sent to determine the type
        If type cannot be determined then the layer is not used
        @param layerFields: a dictionary of fields contained in the layer
        @return: a string being empty, 'POLYGON','POINT' or LINE
        """  
        if layerFields.has_key('ref'):
            refVal = layerFields['ref']
            if refVal.lower().find("polygon") != -1:
                return ("the_geom",'POLYGON') 
            if refVal.lower().find("point") != -1:
                return ("the_geom",'POINT')
            if refVal.lower().find("line") != -1:
                return ("the_geom",'LINE')             
              
        for k in layerFields:            
            if layerFields[k].lower().find("polygon") != -1:
                return (k,'POLYGON') 
            if layerFields[k].lower().find("point") != -1:
                return (k,'POINT')
            if layerFields[k].lower().find("line") != -1:
                return (k,'LINE') 
            
        for k in layerFields:            
            if k.lower().find("polygon") != -1:
                return (k,'POLYGON') 
            if k.lower().find("point") != -1:
                return (k,'POINT')
            if k.lower().lower().find("line") != -1:
                return (k,'LINE') 
               
        return ("","")
    
    def _getGeometryTypeFromMap(self,wmsName,connectionString):
        """
        @summary: tries to get an 2*2 image for each of the types in the gTypes list
        @param wmsName: the wms layer name
        @param connectionString: the online resource for the given layer name
        @return: POLYGON or LINE or POINT or RASTER 
        """
        gTypes = ['POLYGON','LINE','POINT','RASTER']
        for gType in gTypes:
            try:
                tmpName = "tmp_" + str(time.time()).replace(".","") + ".map"    
                #map = MapServerTemplates.discoveryMap %(gType,connectionString,wmsName)
                #f = open(tmpName,"w")
                #f.write(map)
                #f.close()
                #theMap = mapscript.mapObj(tmpName)
                #myImg = theMap.draw()                
                return gType
            except:                
                sio = cStringIO.StringIO()
                traceback.print_exc(file=sio)
                sio.seek(0)
                trace = sio.read()   
                logger.exception('Could not _getGeometryTypeFromMap ' + trace) 
                continue
            
        return "POLYGON"        
    
    def _getGeometryType(self,source,layerName,geometryColumn,bounds):
        """
        @param source: The online resource of the service
        @param layerName: the name of the layer to query
        @param geometryColumn: The column to query
        @param bounds: the envelope of the layer
        @summary: Does a getFeature request on the given source and layer to determine 
        if the layer is a line,point or polygon
        """
        #strBounds = "%s,%s %s,%s" %(bounds[0],bounds[1],bounds[2],bounds[3])
        #filterRequest = MapServerTemplates.getFeatureTemplate %(geometryColumn,strBounds)
        filterRequest = MapServerTemplates.getFeatureTemplate %(geometryColumn,"-180,-90 180,90")
        qFilterRequest = urllib.quote(filterRequest)     
        
        try:            
            url = source + 'request=getfeature&service=wfs&version=1.0.0&maxfeatures=1&typename='+layerName+ '&filter='+filterRequest                            
            url2 = source + 'request=getfeature&service=wfs&version=1.0.0&maxfeatures=1&typename='+layerName+ '&filter='+qFilterRequest                
            data = self._getURLContent(url2,{})  
            if (data.find("ServiceException") != -1)  or (data.find("ServiceExceptionReport") != -1) or (data.find("gml:boundedBy") == -1):                
                data = self._getURLContent(url,{})   
            if data == "":
                return ""                     
        except:            
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could _getGeometryType ' + trace) 
        try:               
            dom = minidom.parseString(data)
        except:            
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()   
            logger.exception('Could not _getGeometryType ' + trace)                    
            return ""
        
        memberElms = dom.getElementsByTagName("gml:featureMember")        
        if memberElms:            
            if memberElms[0].getElementsByTagName("gml:Polygon"):
                return "POLYGON"
            if memberElms[0].getElementsByTagName("gml:LineString"):
                return "LINE"                
            if memberElms[0].getElementsByTagName("gml:Point"):
                return "POINT"  
               
        return ""             
        
    def _getFieldsForLayer(self,name,source):
        """        
        @param name: the name of the layer to retrieve fields for
        @param source: the url source for the layer (as set in self.sources)
        @return: a tuple with a list of layer fields and a string with describefeaturetype response for the layer
        """
        
        data = ''
        baseURL = source + WFS_DESCRIBEFEATURETYPE_EXTENSION
        fieldDict = {}        
        baseURL += "&typename=" + name.replace(" ","%20")
        data = self._getURLContent(baseURL)  
        
        try:  
            dom = minidom.parseString(data)   
            elements = dom.getElementsByTagName("xs:element")
            if not elements:
                elements = dom.getElementsByTagName("element")
            if not elements:
                elements = dom.getElementsByTagName("xsd:element")
            for element in elements:
                if element.hasAttribute('name'):
                    elmName = element.getAttribute('name')
                    elmType = element.getAttribute('type')  
                    fieldDict[str(elmName)] = str(elmType)
                if element.hasAttribute('ref'):
                    elmRef = element.getAttribute('ref')    
                    fieldDict['ref'] = str(elmRef)                    
        except:            
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()   
            logger.exception('Could not _getFieldsForLayer : ' + trace)             
            return (fieldDict,data)         
            
        return (fieldDict,data) 
    
    def _determineGeometryField(self,fieldList):
        """
            @summary: method must determine which field is the geometry field
            This is not an exact science
            @param fieldList: a list of field names
            @return: fieldName that is closest match to the common names used for the geometry column
        """
        
        fieldList2 = [x.lower() for x in fieldList]
        for field,fieldOrg in zip(fieldList2,fieldList):
            if field == 'msgeometry':
                return fieldOrg
            if field == 'the_geom':
                return fieldOrg
            if field == 'geometry':
                return fieldOrg
            if field.find("geometry") != -1:
                return fieldOrg
            if field.find("_geom") != -1:
                return fieldOrg
            if field.find("geom") != -1:
                return fieldOrg
            if field.find("latlong") != -1:
                return fieldOrg            
        return ""             
    
    def _getTempMapFile(self,layerStructure, requestLayers=[]):
        """        
        @summary: build a temp map file for get map requests
        @param layerStructure: as built by discoverLayers
        @return: a string containing the mapfile (generated with mapscript)
        """        
        layersString = ""        
        extentList = []
        for layer in layerStructure:            
            if not layer['uniqueName'] in requestLayers:
                # only include layers for the given request
                continue
            
            if not layer['error']:
                layersString += MapServerTemplates.layerTemplate %(layer['geometryType'],layer['uniqueName'],layer['source'][1],layer['source'][0],layer['source'][1],
                                layer['wmsName'],layer['wfsName'],layer['wmsName'],GLOBAL_SRS,GLOBAL_SRS,layer['wmsName'],GLOBAL_SRS)                                
                                      
                extentList.append(layer['wfsBoundingBox'])             
        if not extentList:
            return
        # calc the extent of the map
        minx = 99e99
        miny = 99e99
        maxx = -99e99
        maxy = -99e99
        for extent in extentList:
            if float(extent[0]) < minx:
                minx = float(extent[0])
            if float(extent[0]) < miny:
                miny = float(extent[1])
            if float(extent[2]) > maxx:
                maxx = float(extent[2])
            if float(extent[3]) > maxy:
                maxy = float(extent[3])
        mapExtent = "%s %s %s %s" %(minx,miny,maxx,maxy)         
        
        tmpMap = MapServerTemplates.mapBaseTemplate %(mapExtent,GLOBAL_SRS,"./","./",GLOBAL_SRS,GLOBAL_SRS,GLOBAL_SRS,layersString)          
        return tmpMap    
    
##    def _buildMapFile(self,layerStructure):
##        """        
##        @summary: this will build a MapServer MapFile from the response of the discover layers 
##        @param layerStructure: as built by discoverLayers
##        @return: a string containing the mapfile (generated with mapscript)
##        """        
##        layersString = ""        
##        extentList = []
##        for layer in layerStructure:
##            # all layers in the map must have the same projection, else the gemap request will fail
##            if not layer['error']: 
##                box = "%s %s %s %s" %(layer['wfsBoundingBox'][0],layer['wfsBoundingBox'][1],layer['wfsBoundingBox'][2],layer['wfsBoundingBox'][3])
##                layersString += MapServerTemplates.layerTemplate %(layer['geometryType'],layer['uniqueName'],layer['source'][1],layer['source'][0],layer['source'][1],
##                                layer['wmsName'],layer['wfsName'],layer['wmsName'],GLOBAL_SRS,GLOBAL_SRS,layer['wmsName'],GLOBAL_SRS)                                
##                                      
##                extentList.append(layer['wfsBoundingBox'])             
##        if not extentList:
##            return
##        # calc the extent of the map
##        minx = 99e99
##        miny = 99e99
##        maxx = -99e99
##        maxy = -99e99
##        for extent in extentList:
##            if float(extent[0]) < minx:
##                minx = float(extent[0])
##            if float(extent[0]) < miny:
##                miny = float(extent[1])
##            if float(extent[2]) > maxx:
##                maxx = float(extent[2])
##            if float(extent[3]) > maxy:
##                maxy = float(extent[3])
##        mapExtent = "%s %s %s %s" %(minx,miny,maxx,maxy)         
##        self.mapFile = MapServerTemplates.mapBaseTemplate %(mapExtent,GLOBAL_SRS,"./","./",GLOBAL_SRS,GLOBAL_SRS,GLOBAL_SRS,layersString)  
                
    def _removeHTMLComments(self,theString):
        """
        @summary: 
        @param theString: the string containing the html comments to be strinpped out
        @return: returns a decommented string
        """  
        
        while theString.find("<!--") != -1:
            startPos = theString.find("<!--")
            endPos = theString.find("-->")
            remString = theString[startPos:endPos+3]
            theString = theString.replace(remString,'')
            
        return theString    
    
    
    def _validateBoundingBox(self,minx,miny,maxx,maxy):
        """
        @summary: This checks that the coords are in degrees and that they are within 
        the world scope of (-180,-90,180,90) and no bigger
        @return: a boolean that states whether coords are valid
        """
        if float(maxx) < float(minx):
            return False
        if float(maxy) < float(miny):
            return False        
        if float(minx) == float(maxx):
            return False
        if float(miny) == float(maxy):
            return False
        
        if float(minx) < -180:
            return False
        if float(miny) < -90:
            return False
        if float(maxx) > 180:
            return False
        if float(maxy) > 90:
            return False        
        return True         
    
##    def _writeMapFile(self):
##        """
##        @summary: writes the current mapFile variable to a file
##        """
##        f = open("map.map","w")
##        f.write(self.mapFile)
##        f.close()  
        
class Mapper:
    """
    usage:
        #m = Mapper()
        #d = unicode(trace,'utf')
        #trace = d.translate(m)        
    """
    def __getitem__(self, key):
        if chr(key) in ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~':
            return key
        else:
            return ord('?') 
    
if __name__ == "__main__":
    pass



    
    
    
    
    
    
    
    
    
    
