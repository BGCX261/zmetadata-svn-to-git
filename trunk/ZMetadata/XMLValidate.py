from StringIO import StringIO
from XMLValidator import XMLValidator

class XMLValidate:    
    def __init__(self):
        """
        @summary: XMLvalidate is a class for validating xml documents against xsd and dtd schemas
        """
        pass
    
    def validateXMLForXSD(self, xmlData, xsdData, base_url=""):
        """
        @param xmlData: string containing xml data
        @param xsdData: string containing xml schema definition
        @return: tuple with boolean as first elm and error log as second elm (False, "Error message")
        """   
        validator = XMLValidator("java", "c:\\temp\\XMLValidator.jar")
        result = validator.validate(xmlData, xsdFilePath)         
        print result
#        xsdFile = StringIO(xsdData)
#        xmlSchemaDoc = etree.parse(xsdFile,base_url=base_url)        
#        
#        xmlSchema = etree.XMLSchema(xmlSchemaDoc)
#        
#        # create an xml document to validate
#        docFile = StringIO(xmlData)
#        doc = etree.parse(docFile)
#        
#        # validate the xml against the xsd file
#        res = xmlSchema.validate(doc)        
#        if res == True:
#            return (res,xmlSchema.error_log)
#        else:
#            return (False, self.getFriendlyMessage(str(xmlSchema.error_log)))
        
    def getFriendlyMessage(self, errorMsg):
        """
        """
        parts = errorMsg.split(":")
        line = parts[1]
        element = parts[2]
        
        s = " ".join(parts[6:])
        return "Line " + line + " Element " + element + ".\n" + s
    
#    def validateXMLForXSDFromFile(self, xmlFileName, xsdFileName, base_url=""):
#        """
#        @param xmlFileName: path of xml file to validate
#        @param xsdFileName: path of xsd file to validate
#        @return: tuple with boolean as first elm and error log as second elm (False, "Error message")
#        """        
#        xmlFile = file(xmlFileName)
#        xmlData = xmlFile.read()
#        xmlFile.close()
#        
#        xsdFile = file(xsdFileName)
#        xsdData = xsdFile.read()
#        xsdFile.close()
#        
#        return self.validateXMLForXSD(xmlData, xsdData, base_url)  
            
    def validateXMLForXSDFromFile(self, xmlFileName, xsdFileName, base_url=""):
        """
        @param xmlFileName: path of xml file to validate
        @param xsdFileName: path of dtd file to validate
        @return: tuple with boolean as first elm and error log as second elm (False, "Error message")
        """        
        xmlFile = file(xmlFileName)
        xmlData = xmlFile.read()
        xmlFile.close()
        
        xsdFile = file(xsdFileName)
        xsdData = xsdFile.read()
        xsdFile.close()
        
        return self.validateXMLForXSD(xmlData, xsdData, base_url)           

if __name__ == '__main__':
    
    xmlValidate = XMLValidate()
    #xmlValidate.validateXMLForXSDFromFile(r"c:\!Projects\Python\CSW\2008-08-18 16_04_56_577000.xml", r"c:\!Projects\NSIF\docs\metadata\iso19115\schema.xsd")   
    #print xmlValidate.validateXMLForXSDFromFile("c:/!Projects/NSIF/docs/metadata/eml/eml-2.0.1/eml-2.0.1/edit_template.xml", "c:/!Projects/NSIF/docs/metadata/eml/eml-2.0.1/eml-2.0.1/eml.xsd", "c:/!Projects/NSIF/docs/metadata/eml/eml-2.0.1/eml-2.0.1/")   
    #print xmlValidate.validateXMLForXSDFromFile(r"c:\temp\test_fgdc.xml", r"c:\!Projects\NSIF\docs\metadata\fgdc-std\schema.xsd", "c:/!Projects/NSIF/docs/metadata/fgdc-std/")   

    #print xmlValidate.validateXMLForXSDFromFile(r"c:/ftproot/xml/iso_19139_sample8.xml", "c:/temp/work/19139/19139.xsd", "c:/temp/work/19139/")

    print xmlValidate.validateXMLForXSDFromFile(r"c:\ftproot\xml\iso19139\iso_19139_sample0.xml", "c:/Plone3_Instance4080/Products/ZMetadata/standards/iso19139/gmd/gmd.xsd", "c:/Plone3_Instance4080/Products/ZMetadata/standards/iso19139/gmd/")   
    
    
