from StringIO import StringIO
import sys
import traceback
from Ft.Xml.Xslt import Processor
from Ft.Xml import InputSource

class XMLTransform:
    def __init__(self):
        ""
        pass
    
    def transform(self, xmlData, xslData, base_url=""):
        """
        @param xmlData: the xml data to transform
        @param styleData: the xsl style sheet data to use in transform
        @return: a string version of the transformed document
        """
        try:
            processor = Processor.Processor()
            transform = InputSource.DefaultFactory.fromString(xslData, "http://spam.com/identity.xslt")
            source = InputSource.DefaultFactory.fromString(xmlData, "http://spam.com/doc.xml")
            processor.appendStylesheet(transform)
            result = processor.run(source)
            return result
        except:
            traceback.print_exc(file=sys.stdout)    
            return ""
        
    def transformFromFile(self, xmlFile, xslFile, base_url=""):
        """
        @param xmlData: the xml file to transform
        @param styleData: the xsl style sheet file to use in transform
        @return: a string version of the transformed document
        """        
        xmlF = file(xmlFile,"r")
        xmlData = xmlF.read()
        xmlF.close()
        
        xslF = file(xslFile,"r")
        xslData = xslF.read()
        xslF.close()        
        return self.transform(xmlData, xslData, base_url=base_url)                
    
if __name__ == "__main__":
    
    transform = XMLTransform()
    #print transform.transformFromFile(r"c:\!Projects\NSIF\docs\metadata\iso19115\schema.xsd", r"c:\!Projects\Python\XmlHtmlUtil\xsd2html.xsl")
    #print transform.transformFromFile(r"c:\temp\Provinces.xml", r"c:\temp\my_generic.xsl","c:/temp/")
    
    # dc    
    #print transform.transformFromFile(r"c:\temp\sample metadata\testqualifieddc_dc.xml", r"c:\Program Files\geonetwork\web\geonetwork\xsl\main-page.xsl","c:/Program Files/geonetwork/web/geonetwork/xsl/")
    # iso 19115
    #print transform.transformFromFile(r"c:\temp\sample metadata\SampleFile_19115.xml", r"c:\Plone3_Instance4080\Products\ZMetadata\standards\dublin-core\extract_bbox.xsl","c:/temp/sample metadata/")
    # iso 19139
    print transform.transformFromFile(r"c:\temp\sample metadata\ex3.xml", r"c:\Plone3_Instance4080\Products\ZMetadata\standards\iso19139\extract_common_fields.xsl","c:/temp/sample metadata/")
    # fgdc
    #print transform.transformFromFile(r"c:\temp\sample metadata\esvp200m_fgdc.xml", r"c:\Plone3_Instance4080\Products\ZMetadata\standards\dublin-core\extract_bbox.xsl","c:/temp/sample metadata/")
    # eml
    #print transform.transformFromFile(r"c:\temp\sample metadata\EML_arc.1596.2.xml", r"c:\Plone3_Instance4080\Products\ZMetadata\standards\eml\extract_common_fields.xsl","c:/temp/sample metadata/")
    
    
    
    
    