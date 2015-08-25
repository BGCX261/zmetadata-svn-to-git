
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
import transaction

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
        name='email',
        required=1,
        widget=StringWidget(
            label='Results Email',
            label_msgid='ZMetadata_label_email',
            i18n_domain='ZMetadata',
        ),
        validators=('isEmail',)
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
            fails = []
            #valid = self.checkXmlStructure(xml)
            #if not valid:
            #    fails += 1
            #    self.aq_parent.addLog("Xml structure not valid", "Xml structure for document is not valid. " + uri, type="Error")
            #    return fails        
            moved = None
            hasURI = self.uriExists(uri)
            if hasURI:
                meta = self.getMetadataByURI(uri)
                
                if meta.xml == xml:
                    self.aq_parent.addLog("Duplicate document ignored", "Ignored document during harvest. Xml is identical to " + str(meta.title) +" . " + uri, type="Info")
                    return 0, meta.absolute_url()
#                else:           
#                    moved = meta.makeACopyToArchive()
#                    self.aq_parent.addLog("Archived Document", "Updated and archived document. " + uri + "\n With id: " + str(moved.id), type="Info")
            else:        
                collection = self.getMetadataCollectionFolder()
                id = "meta"+str(time.time()).replace(".","")    
                collection._setObject(id,Metadata(id,id))        
                meta = getattr(collection,id)
                meta.setURI(uri) 
            meta.setMetadatatype(self.standard)
            meta.setXml(xml, ignoreValid=True)
            url = meta.absolute_url()
            #meta.setMetadatatype(meta.guessMetadataType(xml))
            if meta.mTitle.strip() != "": # set the metadata object title to that of the metadata document title
                meta.title = meta.mTitle
                meta.reindexObject()                
            
            self.aq_parent.addLog("Create Document from harvest", "Create document from harvest. " + uri + "\n With id: " + str(meta.title), type="Info")
            if self.getPublishharvested() == "Yes":
                #if not valid:
                #    fails += 1
                #    self.aq_parent.addLog("Xml structure not valid", "Xml structure for document is not valid. " + uri, type="Error")
                #    return fails
                try:
                    self.portal_workflow.doActionFor(meta, 'publish')
                except Exception, e:
                    try:
                        self.portal_workflow.doActionFor(meta, 'publish_provisionally')
                    except:
                        pass
                    fails += ["Document %s could not publish due to '%s' but was published provisionally." % (url, str(e))]
            return fails, url
        except:
            io = StringIO()
            traceback.print_exc(file=io)
            io.seek(0)
            trace = io.read()
            print trace
            self.aq_parent.addLog("Error during document creation : " + uri,trace,type="Error")
            url = meta.absolute_url()
            return ["Error during document creation : %s, %s, %s" % (uri,str(trace), "Error")], url
    
    def harvest(self):
        """
        @summary: does the harvesting for the given type and url
        """
        try:
            
            harvestStart = time.strftime("%H:%M %y-%m-%d")
            print 'Harvesting', self.getUrl()
            mTo = self.getEmail()
            mFrom = 'hermangeldenhuys@fusemail.com'
            mSubjTemplate = 'Harvester "%s" progress report (from %s to %s) '
            obj_url = self.absolute_url() 
            messageTemplate = """From: CoGIS Portal <%s>
Subject: %s
To: <%s>
Content-Type: text/plain;\n\n"""
            warnings = []
            self.lastUpdateDate = time.time()
            start = time.time()
            avgStats = []
            processed = []

            if self.getTransport() == "FTP":
                ftp = FTPTransport(self.getUrl(), self.getUsername(), self.getPassword())                
                if ftp.message:
                    raise '%s\n%s' % (ftp.message, self.getUrl())
                files = ftp.getFiles()
            
            if self.getTransport() == "CSW":
                csw = CSWTransport(self.getUrl(), "")            
                if csw.message:
                    raise '%s\n%s' % (csw.message, self.getUrl())
                files = csw.getRecords()

            if self.getTransport() == "HTTP":
                http = HTTPTransport(self.getUrl())
                if http.message:
                    raise '%s\n%s' % (http.message, self.getUrl())
                
                files = http.files
            
            total = len(files)
            count = 0
            total = len(files)
            
            for file in files.keys():
                start = time.time()
                count += 1
                newwarnings, url = self.createNewMetadata(file, files[file])
                print 'newwarnings', newwarnings
                warnings += newwarnings
                processed += [url]
                end = time.time()
                timeTaken = end-start
                avg = end-start
                avgStats += [avg]
                
                print '>>', count, 'of', total, 'and', timeTaken, 'seconds. AVG:', avg
                if count % 10 == 0:
                    avg = 0
                    for i in avgStats:
                        avg += i
                    avg = avg / ((count / 10)*10+1)
                    
                    mSubj = mSubjTemplate % (self.title_or_id(), str((count / 10 - 1)*10+1), str((count / 10)*10))
                    mSubj += 'of %s documents.' % `total`
                    message = messageTemplate % (mFrom, mSubj, mTo)
                    if warnings:
                        message += "The following errors occurred, please se the Harvester logs for further details: \n" + str(warnings)
                    else:
                        message += "The Harvest didn't run into any problems yet.: %s \n" % self.absolute_url()
                    message += "Processed the following urls:\n%s\n" % '\n\t'.join(processed)
                    message += "\nThe average processing time was: %s\n" % (avg,)
                    processed = []
                    warnings = []
                    transaction.commit()
                    self.sendemail(mSubj, self.absolute_url(), message)
                    
            harvestEnd = time.strftime("%H:%M %y-%m-%d");
            
            mSubj = mSubjTemplate % (self.title_or_id(), harvestStart, harvestEnd)
            message = messageTemplate % (mFrom, mSubj, mTo)
            
            if warnings:
                #return warnings
                message += "The following errors occurred, please se the Harvester logs for further details: \n" + str('\n'.join(warnings))
            else:
                message += "The Harvest was successful: %s \n" % self.absolute_url()
            
            self.sendemail(mSubj, self.absolute_url(), message)
        except:
            io = StringIO()
            traceback.print_exc(file=io)
            io.seek(0)            
            trace = io.read()
            print trace
            self.aq_parent.addLog("Error during harvesting from : " + self.getUrl(),trace,type="Error")
            return 1
    def sendemail(self, subject, url, message):
        """
        """
        try:
            mTo = self.getEmail()
            mFrom = 'hermangeldenhuys@fusemail.com'
            self.MailHost.send(message, mTo, mFrom, subject)
        except Exception, e:
            print e

registerType(Harvester, PROJECTNAME)
# end of class Harvester

##code-section module-footer #fill in your manual code here
##/code-section module-footer



