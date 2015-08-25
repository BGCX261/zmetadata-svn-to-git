import time
import traceback
from StringIO import StringIO
import sys
import urllib
import urllib2
import base64
from urlparse import urlparse
from ZipUtil import ZipUtil


class HTTPTransport:
    def __init__(self, url,username="", password=""):
        """
        """
        if url.lower().startswith('http://'):
            parts = url[7:].split('/')
            if not parts[1].startswith(':'):
                url = 'http://%s:80/%s' %(parts[0], '/'.join(parts[1:]))
            else:
                url = 'http://%s/%s' %(parts[0], '/'.join(parts[1:]))
        self.url = url
        self.username = username
        self.password = password   
        self.contentType = "" 
        self.message = ""
        
        self.files = self.getFile()
    
    def getFile(self):
        """
        @summary: a dict with file data as key and file path as value
        """  
        try: 
            if (self.username == "") and (self.password == ""):
                res = urllib.urlopen(self.url)
                self.contentType = res.info()["Content-Type"]
                print 'Get HTTP File anonymously.'
            else:
                req = urllib2.Request(self.url)
                base64string = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
                authheader =  "Basic %s" % base64string
                req.add_header("Authorization", authheader)
                res = urllib2.urlopen(req)
                self.contentType = res.info()["Content-Type"]
                print 'Get Authenticated File.'
            print 'self.contentType', self.contentType
            if self.contentType.lower().find("zip") != -1:
                tDict = {}
                f = StringIO()
                f.write(res.read())
                util = ZipUtil(f)
                theFiles = util.getFileContentWithExtension("xml")
                for f in theFiles:
                    tDict[f[1]] = self.url +"/"+ f[0]
                return tDict
            elif self.contentType.lower().find("xml") != -1:
                return {res.read():self.url}
            else:
                print 'Return unknown.'
                result = res.read()
                return {result:self.url}
            self.message = "Invalid URL or Wrong Content Type"
            return {}
        except:
            traceback.print_exc(file=sys.stdout)
            io = StringIO()
            traceback.print_exc(file=io)
            io.seek(0)            
            trace = io.read()
            self.message = trace            
            return {}
    
if __name__ == "__main__":    
    trans = HTTPTransport("http://127.0.0.1/test/Provinces.xml","","")
    print trans.message
    #trans.getFile()
    #print trans.contentType
    #print trans.message
    #trans = HTTPTransport("http://127.0.0.1/test/xml_to_load.zip","","")
    #print trans.getFile()
    
    
    

