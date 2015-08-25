import string
import urllib2
import urllib
import cgi
import httplib
import datetime
import time
from xml.dom import minidom
import random
from StringIO import StringIO
import sys
import traceback

recordCountTemaple = """<?xml version="1.0" encoding="UTF-8"?>
<csw:GetRecords xmlns:csw="http://www.opengis.net/cat/csw" service="CSW" version="2.0.1" resultType="hits">
  <csw:Query>
    <csw:Constraint version="1.1.0">
      <Filter xmlns="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml">
        <PropertyIsNotEqualTo>
          <PropertyName>title</PropertyName>
          <Literal>aaaaaa-9999999</Literal>
        </PropertyIsNotEqualTo>
      </Filter>
    </csw:Constraint>
  </csw:Query>
</csw:GetRecords>
"""

recordByIdTemplate = """<?xml version="1.0" encoding="UTF-8"?>
<csw:GetRecordById xmlns:csw="http://www.opengis.net/cat/csw" service="CSW" version="2.0.1">
  <csw:Id>%s</csw:Id>
</csw:GetRecordById>"""

recordIdTemplate = """<?xml version="1.0" encoding="UTF-8"?>
<csw:GetRecords xmlns:csw="http://www.opengis.net/cat/csw" service="CSW" version="2.0.1" resultType="results" outputSchema="csw:Record">
  <csw:Query typeNames="application service datasetcollection dataset">
    <csw:ElementSetName>brief</csw:ElementSetName>
    <csw:Constraint version="1.1.0">
      <Filter xmlns="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml">
        <PropertyIsNotEqualTo>
          <PropertyName>title</PropertyName>
          <Literal>aaaaaa-9999999</Literal>
        </PropertyIsNotEqualTo>
      </Filter>
    </csw:Constraint>
  </csw:Query>
</csw:GetRecords>"""


recordResultsTemplateISO = """<?xml version="1.0" encoding="UTF-8"?>
<csw:GetRecords xmlns:csw="http://www.opengis.net/cat/csw" service="CSW" version="2.0.1" resultType="results" outputSchema="csw:IsoRecord" startPosition="%s" maxRecords="%s">
  <csw:Query>
    <csw:ElementSetName>full</csw:ElementSetName>
    <csw:Constraint version="1.1.0">
      <Filter xmlns="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml">
        <PropertyIsNotEqualTo>
          <PropertyName>title</PropertyName>
          <Literal>aaaaaa-9999999</Literal>
        </PropertyIsNotEqualTo>
      </Filter>
    </csw:Constraint>
  </csw:Query>
</csw:GetRecords>
"""

recordResultsTemapleRecord = """<?xml version="1.0" encoding="UTF-8"?>
<csw:GetRecords xmlns:csw="http://www.opengis.net/cat/csw" service="CSW" version="2.0.1" resultType="results" outputSchema="csw:Record" startPosition="%s" maxRecords="%s">
  <csw:Query>
    <csw:ElementSetName>full</csw:ElementSetName>
    <csw:Constraint version="1.1.0">
      <Filter xmlns="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml">
        <PropertyIsNotEqualTo>
          <PropertyName>title</PropertyName>
          <Literal>aaaaaa-9999999</Literal>
        </PropertyIsNotEqualTo>
      </Filter>
    </csw:Constraint>
  </csw:Query>
</csw:GetRecords>
"""

xmlHeader = """<?xml version="1.0" encoding="UTF-8"?>"""

class CSWTransport:
    """
    """    
    
    def __init__(self, url, xmlDumpPath):
        self.url = url;
        self.path = xmlDumpPath;
        self.message = ""
        #self.getPostContent(self.url, "")
            
    def getRecords(self):
        """
        @summary: requests all the xml metadata from the given CSW site url and returns the records
        @return: a dict with file data as key and record id as value
        """  
        ids = self.getAllRecordIds()
        retDict = {}
        for id in ids:
            xmlRes = self.getPostContent(self.url, recordByIdTemplate % id)            
            tDom = minidom.parseString(xmlRes)
            elms = tDom.getElementsByTagName("csw:GetRecordByIdResponse")           
            
            for node in elms[0].childNodes:                
                if node.nodeType != node.TEXT_NODE:
                    tRes = node.toxml()
                    break
            retDict[str(tRes)] = id           
        return retDict
            
    def getRecordForId(self,recordId):
        """
        @summary: get the metadata for the given record id
        @param recordId: record id to get metadata for
        """
        return self.getPostContent(self.url, recordByIdTemplate % id)
                    
    def getAllRecordIds(self):
        """
        @return: returns a list of metadata record ids from the csw service
        """
        resXml = self.getPostContent(self.url, recordIdTemplate)        
        d = minidom.parseString(resXml)
        retList = []
        elms = d.getElementsByTagName("dc:identifier")        
        for elm in elms:
            retList.append(elm.firstChild.nodeValue)
        return retList   

    def getRecordCountForServer(self):
        """
        @summary: queries the CSW service for a count of records on the server exposed to the csw service
        @return: the count of records returned from the query
        """
        resXml = self.getPostContent(self.url, recordCountTemaple)
        d = minidom.parseString(resXml)
        elm = d.getElementsByTagName("csw:SearchResults")[0]
        matched = elm.getAttribute("numberOfRecordsMatched")
        return matched    

    def getPostContent(self,url,data=''):    
        """
        @summary: does a post to the url with the given data and returns the result
        @param url: the url to post to
        @param data: the data to post to the url
        """
        try:
            if url[len(url)-1] == '&':
                url = url[0:len(url)-1]
            url = url.replace("http://",'')
            url = url.replace("HTTP://",'')
            print 'url', url
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
            print 'data1', data
            reply, msg, hdrs = h.getreply()
            print 'reply, msg, hdrs', reply, msg, hdrs
            data = h.getfile().read()
            print 'data2', data
            return data
        except:
            traceback.print_exc(file=sys.stdout)
            io = StringIO()
            traceback.print_exc(file=io)
            io.seek(0)            
            trace = io.read()
            self.message = trace  
            #return ""
    
    def _getTimestampName(self):
        """
        @summary: generates a random/unique name and returns the name
        @return: a name for an xml file
        """
        tNum = random.randint(1, 99999)
        return str(time.time()).replace(".","") + str(tNum) + ".xml"    
    
    def getAllRecordAndWriteToFile(self):
        """
        @summary: does a query to the CSW service for all records and writes the results to file
        """
        recs = self.getRecords()
        print 'recs', recs
        for rec in recs.keys():            
            f = file(self.path + "/" + self._getTimestampName(),"w")
            f.write(rec)
            f.close()
        

if __name__ == "__main__":    
    postUrl = "http://www.saeonocean.co.za/geonetwork/srv/en/csw?"
    #postUrl = "http://delta.icc.es/indicio/csw?"
    #proxies = {'http': 'http://10.50.130.26:8080'}

    h = CSWTransport(postUrl, "c:/temp/xml")
    #h.getAllRecordAndWriteToFile()    
    print "========================="
    print h.getAllRecordAndWriteToFile()
    #count = h.getRecordCountForServer(postUrl);
    #h.harvest()  
    



