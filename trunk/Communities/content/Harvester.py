
__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ZMetadata.config import *
import Global
from FTPTransport import FTPTransport
from HTTPTransport import HTTPTransport
from CSWTransport import CSWTransport
import time
from Products.ZMetadata.Metadata import Metadata
from ZipUtil import ZipUtil
import traceback
import sys
from xml.dom import minidom
from StringIO import StringIO
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.CMFCore import permissions

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='standard',        
        widget=SelectionWidget
        (
            label='Standard',
            label_msgid='ZMetadata_label_standard',
            i18n_domain='ZMetadata',
        ),
        vocabulary=Global.config.getMetadataTypes()
    ),

    StringField(
        name='transport',
        required=1,
        widget=SelectionWidget
        (
            label='Transport',
            label_msgid='ZMetadata_label_transport',
            i18n_domain='ZMetadata',
        ),
        vocabulary=['CSW','HTTP','FTP']
    ),

    StringField(
        name='url',
        required=1,
        widget=StringWidget(
            label='Url',
            label_msgid='ZMetadata_label_url',
            i18n_domain='ZMetadata',
        ),
        validators=('isURL',)
    ),

    StringField(
        name='updatefrequency',
        required=1,
        widget=SelectionWidget
        (
            label='Update Frequency',
            label_msgid='ZMetadata_label_updatefrequency',
            i18n_domain='ZMetadata',
        ),
        vocabulary=['Never','12 Hours','1 Days','2 Days','7 Days','14 Days', '30 Days', '6 Months', '12 Months']        
    ),
    
    StringField(
        name='username',
        widget=StringWidget(
            label='Username (if required)',
            label_msgid='ZMetadata_label_username',
            i18n_domain='ZMetadata',
        ),        
    ),
    
    StringField(
        name='password',
        widget=PasswordWidget(
            label='Password (if required)',
            label_msgid='ZMetadata_label_password',
            i18n_domain='ZMetadata',
        ),        
    ),
    
    StringField(
        name='publishharvested',
        required=1,
        default = 'No',
        widget=SelectionWidget
        (
            label='Publish Harvested Metadata',            
        ),
        vocabulary=['Yes','No']
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

#Harvester_schema = BaseSchema.copy() + schema.copy()
Harvester_schema = ATContentTypeSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Harvester(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Harvester'

    meta_type = 'Harvester'
    portal_type = 'Harvester'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    content_icon = 'harvester.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Harvester"
    typeDescMsgId = 'description_edit_harvester'
    
    actions =  (
       {'action': "string:${object_url}/harvest_view",
        'category': "metadata",
        'id': 'harvest',
        'name': 'Harvest',
        'permissions': (permissions.ViewManagementScreens,),
        'condition': 'python:1'
       },
    )
    
    _at_rename_after_creation = True

    schema = Harvester_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    def __init__(self,id, title="Harvester"):
        """
        """        
        self.id = id;
        self.title = title;
        self.lastUpdateDate = time.time() #seconds from epoc
        
    def getMetadataCollectionFolder(self):
        """
        @summary: returns the metadatacollection container for the current harvester instance
        """
        return self.aq_parent.getMetadataCollectionFolder()
    
    def getSecondsFromString(self, stringTime):
        """
        @summary: converts string time into milliseconds
        @param stringTime: in the format 5 Days, 1 Hours, 2 Months
        """
        hour = 60 * 60
        day = hour * 24
        month = day * 30
        year = month * 12        
        
        parts = stringTime.split(" ")
        amount = int(parts[0])
        unit = parts[1].lower()
        
        if unit == "hours":
            return amount * hour
        if unit == "days":
            return amount * day
        if unit == "months":
            return amount * month        
        return 0
            
    def getUpdatefrequency(self):
        """
        @summary: returns the current updateFrequency string
        """
        return self.updatefrequency    
    
    def mustUpdate(self):
        """
        @summary: checks if the harvester is due to harvest the source
                  it checks the lastUpdateTime against the current time to check if it is larger than the update frequency
        """
        if self.getUpdatefrequency() == "Never":
            return False
        
        last = self.lastUpdateDate
        current = time.time()
        
        diff = current - last;
        updateSeconds = self.getSecondsFromString(self.getUpdatefrequency())
        if diff >= updateSeconds:
            return True  
        else:
            return False
    
    def getMetadataByURI(self, uri):
        """
        @summary: looks for metadata in the metadatacollection with the given uri
        @param uri: the uri to look for in the metadata in the metadatacollection
        @return: metadata object        """
        # XXX fix to look in folder
        container = self.getMetadataCollectionFolder()        
        items = container.objectItems()        
        
        for item in items:
            if item[1].meta_type == 'MetadataContainer':
                containerData = item[1].objectItems()
                for data in containerData:
                    if data[1].meta_type == 'Metadata':                
                        if data[1].uri == uri:
                            return data[1]            
            if item[1].meta_type == 'Metadata':                
                if item[1].uri == uri:
                    return item[1]       
        return None  
    
    def uriExists(self, uri):
        """
        @summary: checks if the given uri exists in the metadacollection
        """
        # XXX fix to look in folder
        container = self.getMetadataCollectionFolder()        
        items = container.objectItems()
        for item in items:
            if item[1].meta_type == 'MetadataContainer':
                containerData = item[1].objectItems()
                for data in containerData:
                    if data[1].meta_type == 'Metadata':                
                        if data[1].uri == uri:
                            return True            
            if item[1].meta_type == 'Metadata':                
                if item[1].uri == uri:
                    return True       
        return False  
    
    def checkXmlStructure(self, xml):
        """
        @summary: checks the structure of the xml to check if it is valid xml
        @param xml: xml can be an xml string or an xml file or a zip file
        """        
        try:
            if type(xml) == str:
                d = minidom.parseString(xml)                                           
            else:
                fileType = xml.filename[-3:]
                if fileType.lower() == "zip":
                    pass
                elif fileType.lower() == "xml":
                    xmlData = xml.read()    
                    xml.seek(0)
                    d = minidom.parseString(xmlData)                
            return True
        except:
            return False           
        
    def createNewMetadata(self,xml, uri):
        """
        @summary: create a new metadata document in the metadatacollection container of the current custodian
        @param: the xml data to put in the new metadata object
        """
        try:
            fails = 0
            valid = self.checkXmlStructure(xml)
            if not valid:
                fails += 1
                self.aq_parent.addLog("Xml structure not valid", "Xml structure for document is not valid. " + uri, type="Error")
                return fails        
        
            moved = None
            hasURI = self.uriExists(uri)
            if hasURI:
                meta = self.getMetadataByURI(uri)
                
                if meta.xml == xml:
                    print "=============its the same document============="
                    self.aq_parent.addLog("Duplicate document ignored", "Ignored document during harvest. Xml is identical to " + str(meta.title) +" . " + uri, type="Info")
                    return 0
#                else:           
#                    moved = meta.makeACopyToArchive()
#                    self.aq_parent.addLog("Archived Document", "Updated and archived document. " + uri + "\n With id: " + str(moved.id), type="Info")
            else:        
                collection = self.getMetadataCollectionFolder()
                id = "meta"+str(time.time()).replace(".","")    
                collection._setObject(id,Metadata(id,id))        
                meta = getattr(collection,id)
                meta.setURI(uri) 
            meta.setXml(xml)            
            meta.setMetadatatype(meta.guessMetadataType(xml))
            if meta.mTitle.strip() != "": # set the metadata object title to that of the metadata document title
                meta.title = meta.mTitle
                meta.reindexObject()                
            
            self.aq_parent.addLog("Create Document from harvest", "Create document from harvest. " + uri + "\n With id: " + str(meta.title), type="Info")
            if self.getPublishharvested() == "Yes":
                self.portal_workflow.doActionFor(meta, 'publish')
                print "published metadata : " + str(meta.getURI())                
            return fails
        except:
            io = StringIO()
            traceback.print_exc(file=io)
            io.seek(0)            
            trace = io.read()
            print trace
            self.aq_parent.addLog("Error during document creation : " + uri,trace,type="Error")            
            return fails
    
    def harvest(self):
        """
        @summary: does the harvesting for the given type and url
        """
        try:
            warnings = 0
            self.lastUpdateDate = time.time()
            if self.getTransport() == "FTP":
                ftp = FTPTransport(self.getUrl(), self.getUsername(), self.getPassword())                
                if ftp.message:
                    raise ftp.message
                files = ftp.getFiles()            
                for file in files.keys():
                    ext = files[file]                
#                    if ext[-3:] == "zip":
#                        util = ZipUtil(file)
#                        contents = util.getFileContentWithExtension("xml")
#                        for part in contents:
#                            self.createNewMetadata(part[1], ext +"/"+part[0])
                    if ext[-3:] == "xml":
                        warnings += self.createNewMetadata(file, ext)
            
            if self.getTransport() == "CSW":
                csw = CSWTransport(self.getUrl(), "")            
                if csw.message:
                    raise csw.message
                files = csw.getRecords()
                for file in files.keys():                    
                    warnings += self.createNewMetadata(file, files[file])            
                        
            if self.getTransport() == "HTTP":
                print '>2'
                http = HTTPTransport(self.getUrl())
                print '>2!'
                if http.message:
                    print 'Exit message'
                    raise '%s\n%s' % (http.message, self.getUrl())
                
                print 'Creating Metadata documents.'
                files = http.files
                for file in files.keys():
                    warnings += self.createNewMetadata(file, files[file])
            if warnings:
                return warnings
            else:
                return -1        
        except:
            io = StringIO()
            traceback.print_exc(file=io)
            io.seek(0)            
            trace = io.read()
            print trace
            self.aq_parent.addLog("Error during harvesting from : " + self.getUrl(),trace,type="Error")
            return 1

registerType(Harvester, PROJECTNAME)
# end of class Harvester

##code-section module-footer #fill in your manual code here
##/code-section module-footer



