import urllib
import unittest

requestBase = "http://teora:7070/plone/mapserverfacade.2005-11-18.9864375225/wfswms?"
getMapURL_PNG = "bbox=-180,-90,180,90&styles=&Format=image/png&request=GetMap&layers=topp:country&width=550&height=250&srs=EPSG:4326"
getMapURL_JPEG = "bbox=-180,-90,180,90&styles=&Format=image/jpeg&request=GetMap&layers=topp:country&width=550&height=250&srs=EPSG:4326"
getLegendGraphic = "request=getlegendgraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=topp:country"
getCapabilitiesWMSURL = "service=wms&request=getcapabilities"
getCapabilitiesWFSURL = "service=wfs&request=getcapabilities"

filter = '<ogc:Filter xmlns:ogc="http://ogc.org" xmlns:gml="http://www.opengis.net/gml"><ogc:BBOX><ogc:PropertyName>the_geom</ogc:PropertyName><gml:Box srsName="http://www.opengis.net/gml/srs/epsg.xml"><gml:coordinates>-180,-90 180,90</gml:coordinates></gml:Box></ogc:BBOX></ogc:Filter>'
getFeatureURL = 'request=getfeature&service=wfs&version=1.0.0&maxfeatures=1&typename=topp:states&filter='
getFeatureURLInvalid = 'request=getfeature&service=wfs&version=1.0.0&maxfeatures=1&typename=topp:states1234&filter='

getFeatureInfoURL = "bbox=-180,-90,90,180&styles=&format=jpeg&info_format=text/plain&request=GetFeatureInfo&layers=topp:country&query_layers=topp:country&width=550&height=250&x=225&y=125&srs=EPSG:4326"
getFeatureInfoURLInvalid = "bbox=-180,-90,90,180&styles=&format=jpeg&info_format=text/plain&request=GetFeatureInfo&layers=topp:country&query_layers=topp:country11&width=550&height=250&x=225&y=125&srs=EPSG:4326"

describeFeatureType = "request=DescribeFeatureType&service=wfs&typename=topp:states"
describeFeatureTypeInvalid = "request=DescribeFeatureType&service=wfs&typename=topp:states12"

#http://teora:7070/plone/mapserverfacade.2005-11-18.9864375225/wfswms?bbox=-180,-90,90,180&styles=&format=jpeg&info_format=text/plain&request=GetFeatureInfo&layers=topp:country12&query_layers=topp:country11&width=550&height=250&x=225&y=125&srs=EPSG:4326

class MapServerFacadeTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def testGetMap(self):
        res = urllib.urlopen(requestBase + getMapURL_PNG)
        data = res.read() 
        self.failIf(data.find("ServiceException") != -1)   
        f = open("d:/temp/!pngImage.png","wb")
        f.write(data)
        f.close()
        
        res = urllib.urlopen(requestBase + getMapURL_JPEG)
        data = res.read() 
        self.failIf(data.find("ServiceException") != -1) 
        f = open("d:/temp/!pngImage.jpeg","wb")
        f.write(data)
        f.close()  
    
    def testGetLegendGraphic(self):
        res = urllib.urlopen(requestBase + getLegendGraphic)
        data = res.read()  
        self.failIf(data.find("ServiceException") != -1)         
    
    def testWMSGetCapabilities(self):
        res = urllib.urlopen(requestBase + getCapabilitiesWMSURL)
        data = res.read()  
        self.failIf(data.find("ServiceException") != -1)         
    
    def testWFSGetCapabilities(self):
        res = urllib.urlopen(requestBase + getCapabilitiesWFSURL)
        data = res.read()        
        self.failIf(data.find("ServiceException") != -1)   
    
    def testGetFeature(self):
        theFilter = '<ogc:Filter xmlns:ogc="http://ogc.org" xmlns:gml="http://www.opengis.net/gml"><ogc:BBOX><ogc:PropertyName>the_geom</ogc:PropertyName><gml:Box srsName="http://www.opengis.net/gml/srs/epsg.xml"><gml:coordinates>-180,-90 180,90</gml:coordinates></gml:Box></ogc:BBOX></ogc:Filter>'
        filter = urllib.quote(theFilter)  
        res = urllib.urlopen(requestBase + getFeatureURL + filter)
        data = res.read()        
        self.failIf(data.find("ServiceException") != -1)   
        
        res = urllib.urlopen(requestBase + getFeatureURLInvalid + filter)
        data = res.read()           
        val = data.find("ServiceException") > 0         
        self.failUnless(val) 
    
    def testGetFeatureInfo(self):
        res = urllib.urlopen(requestBase + getFeatureInfoURL)
        data = res.read()
        self.failIf(data.find("ServiceException") != -1)     
        
        res = urllib.urlopen(requestBase + getFeatureInfoURLInvalid)
        data = res.read()
        self.failIf(data.find("ServiceException") == -1)           
    
    def testDescribeFeatureType(self):
        res = urllib.urlopen(requestBase + describeFeatureType)
        data = res.read()
        self.failIf(data.find("ServiceException") != -1)    
        
        res = urllib.urlopen(requestBase + describeFeatureTypeInvalid)
        data = res.read()
        self.failIf(data.find("ServiceException") == -1)                  
    
if __name__ == "__main__":
    unittest.main() 

