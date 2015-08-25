

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ZMetadata.config import *
from Globals import package_home
from XMLTransform import XMLTransform
from XMLValidate import XMLValidate
import Global
import traceback
import sys
from StringIO import StringIO
from XMLValidator import XMLValidator
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
import os

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='xsd',
        widget=FileWidget
        (
            label='Xsd',
            label_msgid='ZMetadata_label_xsd',
            i18n_domain='ZMetadata',
        )
    ),

    StringField(
        name='xsl',
        widget=FileWidget
        (
            label='Xsl',
            label_msgid='ZMetadata_label_xsl',
            i18n_domain='ZMetadata',
        )
    ),

    StringField(
        name='name',
        widget=StringWidget(
            label='Name',
            label_msgid='ZMetadata_label_name',
            i18n_domain='ZMetadata',
        )
    ),

    StringField(
        name='type',
        widget=SelectionWidget
        (
            label='Type',
            label_msgid='ZMetadata_label_type',
            i18n_domain='ZMetadata',
        ),
        vocabulary=Global.config.getMetadataTypes()
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

#Standard_schema = BaseSchema.copy() + schema.copy()
Standard_schema = ATContentTypeSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Standard(ATCTContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(ATCTContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Standard'

    meta_type = 'Standard'
    portal_type = 'Standard'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    content_icon = 'standard.gif'
    #immediate_view = 'base_view'
    #default_view = 'base_view'
    #suppl_views = ()
    typeDescription = "Standard"
    typeDescMsgId = 'description_edit_standard'

    _at_rename_after_creation = True

    schema = Standard_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    
    def __init__(self,id, title="Standard"):
        """
        """
        self.id = id;
        self.title = title;
        self.name = id;
        self.xsd = "";
        self.xsl = "";
        self.name = "";
        self.type = "OTHER";        

    def setName(self, name):
        ""
        self.name = name
    
    def getName(self):
        ""
        return self.name
    
    def setType(self, type):
        ""
        self.type = type;
        
    def getType(self):
        ""
        return self.type        
    
    def setXsd(self,filePath):
        ""        
        self.xsd = filePath
        
    def getXsd(self):
        ""
        return self.xsd
        
    def setXsl(self,filePath):
        """
        """        
        self.xsl = filePath
        
    def getXsl(self):
        """
        """
        return self.xsl
    
    def getProductPath(self):
        ""        
        return package_home(product_globals)
    
    security.declarePublic('editXML')
    def editXML(self,xml):
        ""
        pass
    
    def getBasePathForXSD(self):
        """
        @summary: returns a base path for the current xsd document to use in xsds with multiple includes
        @return: base xsd path
        """
        i = self.xsd.rfind("/") + 1
        return self.xsd[0:i]
    
    def getBasePathForXSL(self):
        """
        @summary: returns a base path for the current xsd document to use in xsds with multiple includes
        @return: base xsd path
        """
        i = self.xsl.rfind("/") + 1
        return self.xsl[0:i]        

    security.declarePublic('validateXML')
    def validateXML(self,xml):
        """
        @summary: validate passed xml against the standards xsd document
        @param xml: xml for validation
        @return: a tuple (Boolean, "Message from validation") e.g (True, "Valid")
        """
        try:   
            separator = ";"
            if os.name.lower() == "nt":
                separator = ";"
            else:
                separator = ":"
            
                     
            jarPath = self.getProductPath() + "/XMLValidator.jar" + separator + self.getProductPath() + "/xercesImpl.jar" + separator + self.getProductPath() + "/xml-apis.jar";
            validator = XMLValidator("java", jarPath)
            result = validator.validate(xml, self.xsd)
            
            print 'self.xsd '*20
            print self.xsd
            print '.'*20
            
            
            #print result
            #if result.lower().find("file is invalid") != -1 or result.lower().find("error") != -1:
            #    return [False,result]
            #else:
            #    return [True,result]
            return [result['valid'], '\n'.join(result['messages'])]
        except:
            traceback.print_exc(file=sys.stdout)
            return [False, "Error occured while validating file"]   
        
    def extractBBox(self,xml):
        """
        """        
        #print "Common BBox : " + self.getBasePathForXSD() + "extract_bbox.xsl"
        f = file(self.getBasePathForXSD() + "extract_bbox.xsl", "r")
        xsl = f.read()
        f.close() 
        trans = XMLTransform()
        return trans.transform(xml, xsl,base_url=self.getBasePathForXSL())
        
    def extractCommonFields(self,xml):
        """
        """
        try:
            #print "Common XSL : " + self.getBasePathForXSD() + "extract_common_fields.xsl"
            f = file(self.getBasePathForXSD() + "extract_common_fields.xsl", "r")
            print 'USING XSL:', self.getBasePathForXSD() + "extract_common_fields.xsl"
            xsl = f.read()
            f.close()   
            trans = XMLTransform()        
            return trans.transform(xml, xsl,base_url=self.getBasePathForXSL())    
        except:
            io = StringIO()
            traceback.print_exc(file=io)
            io.seek(0)            
            trace = io.read()
            print trace    
            return ""   

    security.declarePublic('transform')
    def transformXML(self,xml):
        """
        @summary: transforms passed xml with standards xsl document
        @param xml: xml to use in transform, passed as string
        @return: string after transform
        """
        f = file(self.xsl, "r")
        xsl = f.read()
        f.close()
        trans = XMLTransform()
        return trans.transform(xml, xsl,base_url=self.getBasePathForXSL())

registerType(Standard, PROJECTNAME)
# end of class Standard

##code-section module-footer #fill in your manual code here
##/code-section module-footer



