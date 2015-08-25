import os
import urllib
import urllib2

class XMLValidator:

    def __init__(self, javaPath, jarPath):
        self.javaPath = javaPath
        self.jarPath = jarPath

    def validate(self, xmlString, xsdFilePath):
        open('/tmp/debug-cogis.xml', 'w').write(
            xmlString
        )
        command = "%s -cp \"%s\" business.XMLValidate piped" %(self.javaPath, self.jarPath)
        print 'xsdFilePath', xsdFilePath 
        #p = os.popen3(command)
        #p[0].write(xmlString)
        #p[0].write("\0")
        #p[0].write(xsdFilePath)
        #p[0].write("\0")
        #p[0].close()
        
        #resultLength = int(p[1].readline().split("\n")[0])
        #result = p[1].read(resultLength)
        # 
        url = 'http://localhost:8081/XMLValidator/services/validator/validateXMLMulti'
        paths = [xsdFilePath]
        data = urllib.urlencode({'xml': xmlString, 'xsdPaths': {'paths':paths}})
        headers =  {'User-agent' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko/2009032711 Ubuntu/8.10 (intrepid) Firefox/3.0.8', 'Content-Type': 'application/json'}
        print 'url', url
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        page = response.read()
        result = eval(page.replace('true', 'True').replace('false', 'False'))
        print "validated document:", result['valid']
        
        if not result['valid']:
            print 'trying bruteforce validation'
            deprecated = '/deprecated_'
            count = 1
            folder, filename = os.path.split(xsdFilePath)
            standard = folder.split('/')[1]
            
            newPath = folder + deprecated + str(count) + '/' + filename
            print '??', newPath, '<<'
            while os.path.exists(newPath):
                print 'using', newPath
                paths = [newPath]
                data = urllib.urlencode({'xml': xmlString, 'xsdPaths': {'paths':paths}})
                req = urllib2.Request(url, data, headers)
                response = urllib2.urlopen(req)
                page = response.read()
                result2 = eval(page.replace('true', 'True').replace('false', 'False'))
                if result2['valid']:
                    print 'valid'
                    result = result2
                    newPath = ''
                else:
                    print 'invalid', result2
                    count += 1
                    newPath = folder + deprecated + str(count) + '/' + filename
                    result['messages'] += result2['messages']
        
        return result 
        
if __name__ == "__main__":
    #xsdFilePath=r"c:/Plone3_Instance4080/Products/ZMetadata/standards/dublin-core/dc.xsd"
    xsdFilePath=r"c:\ProgramFiles\Plone3\parts\instance\Products\ZMetadata\standards\eml\eml.xsd"    
    #xmlFilePath=r"c:/temp/iso_19139_master.xml"
    #xmlFilePath=r"c:/temp/fgdc/veg-model-metadata.xml"
    #xmlFilePath=r"c:/temp/sample_metadata/test_dc.xml"
    xmlFilePath=r"c:\ProgramFiles\Plone3\parts\instance\Products\ZMetadata\templates\new_eml.xml"

    # load the test xml file
    xmlFile = file(xmlFilePath)
    xmlFile.seek(0,2)
    xmlFileSize = xmlFile.tell()
    xmlFile.seek(0)
    xmlString = xmlFile.read(xmlFileSize)
    xmlFile.close()
    classpath = r"c:/ProgramFiles/Plone3/parts/instance/Products/ZMetadata/xercesImpl.jar;c:/ProgramFiles/Plone3/parts/instance/Products/ZMetadata/xml-apis.jar;c:/ProgramFiles/Plone3/parts/instance/Products/ZMetadata/XMLValidator.jar;"
    #classpath = r"c:/Plone3_Instance4080/Products/ZMetadata/XMLValidator.jar;c:/Plone3_Instance4080/Products/ZMetadata/XMLValidator.jar;"
    validator = XMLValidator("java", classpath)
    result = validator.validate(xmlString, xsdFilePath)
    print result





