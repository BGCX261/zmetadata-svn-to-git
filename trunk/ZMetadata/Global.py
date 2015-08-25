from Products.Archetypes.atapi import *
from Products.ZMetadata.config import *
from Globals import package_home
from xml.dom import minidom
from Products.CMFCore.utils import getToolByName

class GlobalConfig:
    def __init__(self,path):
        """
        @param configPath: the path the the zmetadata config file
        """                       
        self.metadataCategories = []
        self.maplayers = []
        self.mapserver = ""
        self.recordsPerFolder = 25
        self.metadataTypes = []
        self.mapExtent = []
        self.showUploadTab = ""
        self.showSpatialSearchLink = ""
        self.searchResultTemplate = ""
        self.resultsPerPage = 10
        self.maxSearchResults = 1000
        
        self.configFilePath = path + "/config/zmetadata_config.xml"
        f = open(self.configFilePath,"r")
        data = f.read()
        f.close()
        self.doc = minidom.parseString(data) 
    
    def getMaxSearchResults(self):
        elms = self.doc.getElementsByTagName("max_search_results")
        if elms:
            elm = elms[0]
            val = elm.firstChild.nodeValue
            self.maxSearchResults = int(val)             
        return self.maxSearchResults
    
    def getResultsPerPage(self):
        """
        """
        
        elms = self.doc.getElementsByTagName("results_per_page")
        if elms:
            elm = elms[0]
            val = elm.firstChild.nodeValue
            self.resultsPerPage = int(val)             
        return self.resultsPerPage        
        
    def getShowUploadTab(self):
        """
        """        
        elms = self.doc.getElementsByTagName("upload_metadata_action")
        if elms:
            elm = elms[0]
            val = elm.firstChild.nodeValue
            if str(val) == "1":                
                self.showUploadTab = True;
            if str(val) == "0":
                self.showUploadTab = False;  
        return self.showUploadTab
    
    def getShowSpatialSearchLink(self):
        """
        """        
        elms = self.doc.getElementsByTagName("show_spatial_search_link")
        if elms:
            elm = elms[0]
            val = elm.firstChild.nodeValue
            if str(val) == "1":                
                self.showSpatialSearchLink = True;
            if str(val) == "0":
                self.showSpatialSearchLink = False;  
        return self.showSpatialSearchLink    
        
    def getMapServer(self):
        """
        """        
        if not self.mapserver:
            elms = self.doc.getElementsByTagName("address")
            if elms:
                elm = elms[0]
                self.mapserver = elm.firstChild.nodeValue        
        return self.mapserver
    
    def getMapLayers(self):
        """
        """        
        if not self.maplayers:        
            elms = self.doc.getElementsByTagName("layers")
            if elms:
                for elm in elms:
                    nodes = elm.childNodes
                    for node in nodes:
                        if node.firstChild:
                            self.maplayers.append(str(node.firstChild.nodeValue))        
        return self.maplayers
        
    def getMapExtent(self):
        """
        """        
        if not self.mapExtent:        
            elms = self.doc.getElementsByTagName("mapextent")
            mapExtentElm = elms[0]            
            minxNodes = mapExtentElm.getElementsByTagName("minx")[0].childNodes
            minyNodes = mapExtentElm.getElementsByTagName("miny")[0].childNodes
            maxxNodes = mapExtentElm.getElementsByTagName("maxx")[0].childNodes
            maxyNodes = mapExtentElm.getElementsByTagName("maxy")[0].childNodes
            
            self.mapExtent.append(str(minxNodes[0].nodeValue))
            self.mapExtent.append(str(minyNodes[0].nodeValue))    
            self.mapExtent.append(str(maxxNodes[0].nodeValue))    
            self.mapExtent.append(str(maxyNodes[0].nodeValue))
            
        return self.mapExtent
    
    def getRecordsPerFolder(self):
        """
        """
        elms = self.doc.getElementsByTagName("recordsperfolder")
        if elms:
            return int(str(elms[0].firstChild.nodeValue))
        else:            
            return 25
    
    def getMetadataCategories(self):
        """
        """        
        if not self.metadataCategories:        
            elms = self.doc.getElementsByTagName("metadatacategories")
            if elms:
                elm = elms[0]
                nodes = elm.childNodes
                for node in nodes:
                    if node.firstChild:
                        self.metadataCategories.append(str(node.firstChild.nodeValue))        
        return self.metadataCategories
    
    def getMetadataTypes(self):
        """
        """        
        if not self.metadataTypes:
            elms = self.doc.getElementsByTagName("standards")
            if elms:
                elm = elms[0]
                nodes = elm.childNodes
                for node in nodes:
                    if node.firstChild:
                        self.metadataTypes.append(str(node.firstChild.nodeValue))        
        return self.metadataTypes
    
    def getSearchResultTemplateName(self):
        """
        @summary: reads the template name to use for search results from the config file
        """        
        elms = self.doc.getElementsByTagName("search_result_template")
        if elms:
            self.searchResultTemplate = str(elms[0].firstChild.nodeValue)            
        return self.searchResultTemplate       

path = package_home(product_globals)

config = GlobalConfig(path)


#def getConfig(siteName):
#    """
#    @summary:
#    @param siteName: the name of the plone site to get configuration file for
#    """
#    configFilePath = path + "/config/zmetadata_config.xml"
#    config = GlobalConfig(configFilePath)
#    return config
    
    

