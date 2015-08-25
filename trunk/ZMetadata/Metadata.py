__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ZMetadata.config import *
from XMLTransform import XMLTransform
from XMLValidate import XMLValidate
from XmlHTMLConvert import Convert
import Global
from Products.validation.validators.ExpressionValidator import ExpressionValidator
from ZipUtil import ZipUtil
import time
import random
import transaction
from Globals import package_home
from datetime import datetime
import sys
import re
import traceback
import urllib
from xml.dom import minidom
from xml.xpath.Context import Context as ContextNew
from xml.xpath import Evaluate as EvaluateNew
from Products.CMFCore.utils import getToolByName 
from BeautifulSoup import BeautifulSoup
import smtplib, MimeWriter, base64, os, string
from StringIO import StringIO 
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
import XPathConfig
from Products.CMFPlone import PloneMessageFactory
from OrderedDict import OrderedDict
from Products.PythonScripts.standard import html_quote    

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='xml',
        required=1,
        searchable=1,
        validators = ( ExpressionValidator('python: here.isValidXML(value)'), ),
        widget=FileWidget
        (
            label='Xml',
            label_msgid='ZMetadata_label_xml',
            i18n_domain='ZMetadata',
        )
    ),
    
    StringField(
        name='metadatatype',
        required=1,
        searchable=1,
        default = '',
        widget=SelectionWidget
        (
            label='Metadata Type',
            label_msgid='ZMetadata_label_metadatatype',
            i18n_domain='ZMetadata',
        ),
        vocabulary=Global.config.getMetadataTypes()        
    ),
    
    StringField(
        name='metadatacategory',
        required=0,
        default = '',
        searchable=1,        
        widget=SelectionWidget
        (
            label='Metadata Category',
            label_msgid='ZMetadata_label_metadatacategory',
            i18n_domain='ZMetadata',
        ),
        vocabulary=Global.config.getMetadataCategories()
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Metadata_schema = ATContentTypeSchema.copy() + schema.copy()
#Metadata_schema = BaseSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
Metadata_schema['relatedItems'].widget.visible = {'edit':'invisible', 'view':'visible'}
##/code-section after-schema

class Metadata(ATCTContent): #(BaseContent):
    """
    """
    security = ClassSecurityInfo()    
    __implements__ = (getattr(ATCTContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Metadata'

    meta_type = 'Metadata'
    portal_type = 'Metadata'    
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    content_icon = 'metadata.gif'    
    typeDescription = "Metadata"
    typeDescMsgId = 'description_edit_metadata'
    searchable_type = 1
    searchable = 1    

    actions =  (
#        {'action': "string:${object_url}/view_metadata_default",
#        'category': "object",
#        'id': 'view',
#        'name': 'View',
#        'permissions': (permissions.View,)        
#       },

       {'action': "string:${object_url}/edit_metadata",
        'category': "metadata",
        'id': 'edit_metadata',
        'name': 'Edit Metadata',
        'permissions': (permissions.ViewManagementScreens,)        
       },

       {'action': "string:${object_url}/view_metadata",
        'category': "metadata",
        'id': 'view_metadata',
        'name': 'View Metadata',
        'permissions': (permissions.View,)        
       },
       
       {'action': "string:${object_url}/export_metadata",
        'category': "metadata",
        'id': 'export_metadata',
        'name': 'Export Metadata',
        'permissions': (permissions.View,)        
       },
       
       # {'action': "string:${object_url}/view_metadata_summary",
       #  'category': "metadata",
       #  'id': 'view_metadata_summary',
       #  'name': 'Summary',
       #  'permissions': (permissions.View,)        
       # },
       {'action': "string:${object_url}/generic_corefields_editor",  #edit_metadata_core_fields
        'category': "metadata",
        'id': 'edit_metadata_core_fields',
        'name': 'Edit Core Fields',
        'permissions': (permissions.ViewManagementScreens,),
        'condition': 'python: here.showCoreFieldsTab()',
       },
       {'action': "string:${object_url}/generic_corefields_view",  #view_metadata_core_fields
        'category': "metadata",
        'id': 'view_metadata_core_fields',
        'name': 'View Core Fields',
        'permissions': (permissions.View,),
        'condition': 'python: here.showCoreFieldsTab()',
       },
       
    )
    
    aliases = {
        '(Default)'  : 'view_metadata_summary',
        'view'       : 'view_metadata_summary',
        'edit'       : 'base_edit',
        'properties' : 'base_metadata',
        'sharing'    : 'folder_localrole_form'            
        }


    _at_rename_after_creation = True

    schema = Metadata_schema
    
    messageTemplate = '''<dl class="portalMessage %s" id="kssPortalMessage" style="display:none">
                            <dt>%s</dt><dd></dd></dl><dl class="portalMessage %s">
                            <dt>%s</dt><dd>%s</dd></dl>'''

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    
    def __init__(self,id,title="Metadata"):
        super(Metadata, self).__init__(id)
        self.id = id;
        self.title = title
        self.uri = ""        
        
        self.mBounds = []
        self.mOnlineResource = [];  
        self.mAbstract = "";
        self.mTitle = "";
        self.mDate = "";
        self.mKeywords = "";
        self.mDescription = ""; 
        self.mScale = "";
        self.mOrganization = "";
        self.mMapSmall = "";
        self.mMapLarge = "";
        self.mLanguage = "";
        self.mOwner = "";
        
        # status flags
        self.backupOnDelete = True
            
    def showCoreFieldsTab(self):
        """
        """
        if self.getMetadatatype() in ["ISO19115","ISO19115p2","ISO19139","SANS1878","DublinCore","EML"]:
            return True
        else:
            return False
        
    def isValidXML(self,value):
        """
        @param value: a HTTPRequest.FileUpload instance
        """
        print "====in isValidXML==="
        try:
            if value == "":
                return True 
            if type(value) == str: # its a string
                xmlData = value
            else:                  # its a file
                fileType = value.filename[-3:]
                if fileType.lower() == "zip":
                    return True
                xmlData = value.read()
                value.seek(0)
            if xmlData.strip() == "":
                return True
            d = minidom.parseString(xmlData)            
            return True
        except:
            traceback.print_exc(file=sys.stdout)            
            print "return string from validator"
            return 0 #"Uploaded xml document is not a valid xml document"                
            
    def getLoggedInUserEmail(self):
        """
        """
        try:
            user = self.portal_membership.getAuthenticatedMember()        
            email = user.getProperty('email')
            return email
        except:
            return ""
        
    def emailXMLDocument(self,address,REQUEST=None):
        """
        @summary: email the xml to the given address
        """        
        try:
            message = StringIO()
            writer = MimeWriter.MimeWriter(message)
            writer.addheader('MIME-Version', '1.0')
            writer.addheader('Subject', 'Metadata Document')
            
            writer.addheader('To', address )
            # get ready to send attachment
            writer.startmultipartbody('mixed')
            # start off with a text/plain part
            part = writer.nextpart()
            body = part.startbody('text/plain')
            body.write('Metadata document mailed from Metadata portal.\n')
            body.write('\nSee attached')
            # ............................
            # add XML attachment
            # ............................
            part = writer.nextpart()
            #part.addheader('Content-Transfer-Encoding', 'base64')
            part.addheader('Content-Transfer-Encoding', 'text')
            fileName =  str(self.id) +".xml"
            body = part.startbody('text/xml; name=%s' % fileName)
            # XML file
            body.write(self.xml)
            # finish off
            writer.lastpart()
    
            # ..................................................
            # send the mail
            # . if user supplied userid/password then deal w/it
            # ..................................................
            self.MailHost.send(message.getvalue(), address, address, 'Metadata Document')
            
            # smtp = smtplib.SMTP(self.MailHost.smtp_host)
            # if self.MailHost.smtp_userid:
            #    smtp.ehlo()
            #    smtp_userid64 = base64.encodestring(self.MailHost.smtp_userid)
            #    smtp.docmd("auth", "login " + smtp_userid64[:-1])
            #    if self.MailHost.smtp_pass:
            #       smtp_pass64 = base64.encodestring( self.MailHost.smtp_pass)
            #       smtp.docmd(smtp_pass64[:-1])
            #        #smtp.sendmail( from address, to address, message body)
            # smtp.sendmail(address, address, message.getvalue())
            # smtp.quit()
            return 1  
        except:
            #traceback.
            traceback.print_exc(file=sys.stdout)            
            return 0              
    def metadataTitle(self):
        return self.mTitle
    def metadataAbstract(self):
        return self.mAbstract
    def metadataKeywords(self):
        return self.mKeywords

    def metadataMinXExtent(self):
        if len(self.mBounds) == 4:
            return float(self.mBounds[0])
    def metadataMinYExtent(self):
        if len(self.mBounds) == 4:
            return float(self.mBounds[1])
    def metadataMaxXExtent(self):
        if len(self.mBounds) == 4:
            return float(self.mBounds[2])
    def metadataMaxYExtent(self):
        if len(self.mBounds) == 4:
            return float(self.mBounds[3])
    #def metadatatype(self):
    #    """
    #    """
    #    return self.getMetadatatype()

    def getProductPath(self):
        ""        
        return package_home(product_globals)
    
    def getMapSmall(self, REQUEST=None):
        """
        """                   
        if REQUEST:
            REQUEST.RESPONSE.setHeader("Content-type","image/png")
        return self.mMapSmall 
    
    def getMapLarge(self, REQUEST=None):
        """
        """
        if REQUEST:
            REQUEST.RESPONSE.setHeader("Content-type","image/png")
        return self.mMapLarge        
    
    def getSampleImageForBounds(self,width, height):
        """
        """  
        print "-----getSampleImageForBounds---"
        
        minWidthDD = 90
        minHeightDD = 45
              
        if not self.mBounds:
            return ""
        
        if self.mBounds:
            # check that the bounding box is valid
            x1 = self.mBounds[0]
            y1 = self.mBounds[1]
            x2 = self.mBounds[2]
            y2 = self.mBounds[3]  
            if x1 < -200 or x2 > 200 or y1 < -120 or y2 > 120:
                return []                   
            if x1 > x2:
                return []
            if y1 > y2:
                return []
        
        # calc map extent
        minx = self.mBounds[0]
        maxx = self.mBounds[2]
        miny = self.mBounds[1]
        maxy = self.mBounds[3]
        
        if minx < -200:
            minx = -200.0
        if maxx > 200:
            maxx = 200
        if miny < -120:
            miny = -120.0
        if maxy > 120:
            maxy = 120
            
        xDiff = abs(maxx - minx)
        yDiff = abs(maxy - miny)
        
        if xDiff < minWidthDD:   
            tDiffx = minWidthDD - xDiff;
            minx = minx - (tDiffx/2)
            maxx = maxx + (tDiffx/2)                    
        else:
            minx = minx - 4
            maxx = maxx + 4            
        
        if yDiff < minHeightDD:
            tDiffy = minHeightDD - yDiff;
            miny = miny - (tDiffy/2)
            maxy = maxy + (tDiffy/2)  
        else:
            miny = miny - 2
            maxy = maxy + 2
                
        url = Global.config.getMapServer()
        url += "&mode=map"
        url += "&map_size=%s+%s" %(width,height)
#        url += "&map_myrect_feature=new"
        url += "&mapext=%s+%s+%s+%s" %(minx,miny,maxx,maxy)
                
        d = {"x1": self.mBounds[0], "y1": self.mBounds[1], "x2": self.mBounds[2], "y2": self.mBounds[3]}
        rectTemplate = "%(x1)s+%(y1)s+%(x2)s+%(y1)s+%(x2)s+%(y2)s+%(x1)s+%(y2)s+%(x1)s+%(y1)s"
        rect = rectTemplate %(d)
#        url += "&map_myrect_feature_points=" + rect
        
        url += "&map.layer[myrect]=FEATURE+POINTS+" + rect + "+END+END"
        
        for layer in Global.config.getMapLayers():
            url+="&layer="+layer

        print 'THE MAP URL:', url   

        res = urllib.urlopen(url.replace('geoportal.csir.co.za', 'localhost'))
        data = res.read()
        
        #print len(data)        
        #x1+y1+x2+y1+x2+y2+x1+y2+x1+y1
        #http://127.0.0.1/cgi-bin/mapserv.exe?MAP=c:/ms4w/apps/wms_client.map&mode=map
        #layer=Country&map_size=800+400&map_myrect_feature=new&
        #map_myrect_feature_points=-100+-50+100+-50+100+50+-100+50-100+-50&layer=myrect&mapext=-120+-70+120+70
        return data      
        
    def getExtractedInfo(self):
        """
        """
        d = {"bounds": self.mBounds, "online": self.mOnlineResource, "abstract": self.mAbstract,
              "title" : self.mTitle, "date" : self.mDate, "keywords": self.mKeywords, "description" : self.mDescription,
              "scale" : self.mScale, "organization" : self.mOrganization, "language" : self.mLanguage}
        
        return d
    
    def parseDateFromMetadata(self,stringDate):
        """
        @summary: parse the stringdate to a datetime object
        @param stringDate: the date string to parse to a datetime object
        @return: returns blank string if stringDate is not a valid date, or a datetime object if the date is valid  
        """
        try:
            # cater for following formats 1980, 20030914, 2004-03-12, 2008-08-27T07:50:00
            if len(stringDate) == 4: #1980
                if stringDate.isdigit():
                    date = datetime(int(stringDate),1,1)
                    return date
            
            if len(stringDate) == 8: #20030914
                if stringDate.isdigit():                
                    date = datetime(int(stringDate[0:4]), int(stringDate[4:6]), int(stringDate[6:8]))
                    return date
            
            if len(stringDate) == 10: #2004-03-12
                parts = stringDate.split("-")
                if len(parts) == 3:
                    if str(parts[0]).isdigit() and str(parts[1]).isdigit() and str(parts[2]).isdigit(): 
                        date = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
                        return date
                   
            if len(stringDate) == 19: #2008-08-27T07:50:00 
                parts = stringDate.split("-")
                if len(parts) == 3:
                    if str(parts[0]).isdigit() and str(parts[1]).isdigit() and str(parts[2][0:2]).isdigit():
                        date = datetime(int(parts[0]), int(parts[1]), int(parts[2][0:2])) 
                        return date
        except:
            traceback.print_exc(file=sys.stdout)
            print stringDate
            return ""
        
        return ""
       
    def _renameAfterCreation(self,check_auto_id=True):
        """
        @summary: called after the object is added and atributes have been set
        """
        print '::RENAME BEFORE CREATE::', self.getMetadatatype() 
        self.checkExtract()
        print '::RENAME AFTER CREATE::', self.getMetadatatype() 
                
    def guessMetadataType(self,data):
        """
        @param: the data to search for type
        @return: the type of metadata guessed
        """
        
        # look for dublic core
        if "DublinCore" in Global.config.getMetadataTypes():
            if data.lower().find("xmlns:dc") != -1 or data.lower().find("xmlns:dct") != -1 or data.lower().find("dublincore") != -1:
                return "DublinCore"        
        
        # look for fgdc 
        if "FGDC" in Global.config.getMetadataTypes():
            if data.lower().find("<metadata") != -1 and data.lower().find("idinfo") != -1:
                return "FGDC"
        
        # look for iso19139        
        if "ISO19139" in Global.config.getMetadataTypes():
            if (data.lower().find("gmd:MD_Metadata") != -1 or data.lower().find("xmlns:gmd") != -1) and (data.lower().find("19139") != -1):
                return "ISO19139"
                
        if "ISO19139" in Global.config.getMetadataTypes():        
            if data.lower().find("gmd:MD_Metadata") != -1 or data.lower().find("xmlns:gmd") != -1:
                return "ISO19139"        
        
        # look for iso19115
        if "ISO19115" in Global.config.getMetadataTypes():
            if data.lower().find("idCitation") != -1  and data.lower().find("metadata") != -1 :
                return "ISO19115"
        
        # look for eml
        if "EML" in Global.config.getMetadataTypes():
            if data.lower().find("<eml:") != -1:
                return "EML"   
        
        return "ISO19139"    
    
    def setURI(self, uri):
        """
        """
        self.uri = uri
        
    def getURI(self):
        """
        """
        return self.uri
    
    def getArchiveFolder(self):
        """
        """
        items = self.getMetadataCollection().objectItems()
        for item in items:            
            if item[1].title == "Archive": 
                archiveFolder = item[1]
                return archiveFolder
        return None
    
    def manage_beforeDelete(self, item, container):
        """
        """                 
        if not self.backupOnDelete or True:
            print "don't backup"            
        else:        
            if self.aq_parent.meta_type != "Archive" or self.aq_parent.aq_parent.meta_type != "Archive" :                
                if self.aq_parent.meta_type == "MetadataContainer" or self.aq_parent.meta_type == "MetadataCollection":                          
                    archiveFolder = self.getArchiveFolder()
                    if archiveFolder:
                        try:
                            print "copy to archive"
                            archiveFolder.manage_pasteObjects(container.manage_copyObjects([self.id])) 
                        except Exception, e:
                            print "copy to archive failed", e
            
        super(Metadata, self).manage_beforeDelete(item, container)                     
    
    def makeACopyToArchive(self):
        """
        @summary: copies a copy of the metadata to the archive folder
        @return: the copied metadata element that is now in the archive folder
        """                 
        
        if self.aq_parent.meta_type != "Archive" or self.aq_parent.aq_parent.meta_type != "Archive" :                
            if self.aq_parent.meta_type == "MetadataContainer" or self.aq_parent.meta_type == "MetadataCollection":        
                archiveFolder = self.getArchiveFolder()
                if archiveFolder:
                    copied =  self.aq_parent.manage_copyObjects([self.id])                        
                    pasted = archiveFolder.manage_pasteObjects(copied)
                    moved = getattr(archiveFolder,pasted[0]["new_id"])
                    #moved.makePrivate() # retract the moved/archived document
                    d = datetime.now()
                    changeDateTitle = str(d.year) + "-" + str(d.month) + "-" + str(d.day) + " " + str(d.hour) + ":" + str(d.minute) + ":" + str(d.second)
                    moved.setTitle(moved.title + " " +changeDateTitle)                                                 
                    rItems = self.getRelatedItems()                                                
                    rItems.append(moved)                        
                    self.setRelatedItems(rItems)
                    # get current object state and make the moved object the same state
                    portal_workflow = self.portal_workflow
                    state = portal_workflow.getInfoFor(self, "review_state")                    
                    if state=="published":            
                        moved.makePublished()
                    
                return moved                  
        return None
        
    def getMetadataCollection(self):
        """
        @summary: returns the metadata's metadata collection object
        """        
        if self.aq_parent.meta_type == 'MetadataCollection':
            return self.aq_parent
        if self.aq_parent.aq_parent.meta_type == 'MetadataCollection':
            return self.aq_parent.aq_parent
        return None
    
    def getCustodian(self):
        """
        @summary: returns the metadata's custodian object
        """        
        if self.getMetadataCollection():
            return self.getMetadataCollection().aq_parent
        else:
            return None
        
    def makePrivate(self):
        """
        @summary: retract a published metadata document
        """                
        portal_workflow = self.portal_workflow
        state = portal_workflow.getInfoFor(self, "review_state")                    
        if state=="published":            
            wfcontext=self.portal_workflow.doActionFor(self,"retract",  comment="" )
        #self.portal_workflow.doActionFor(self, 'publish')
        
    def hasValidBounds(self):
        """
        """
        if not self.mBounds:
            return False
        
        if len(self.mBounds) < 4:
            return False
        
        minx = float(self.mBounds[0])
        miny = float(self.mBounds[1])
        maxx = float(self.mBounds[2])
        maxy = float(self.mBounds[3])
        
        #if minx >= maxx:
        if minx > maxx:
            return False
        #if miny >= maxy:
        if miny > maxy:
            return False;
        
        return True
        
    def makePublished(self):
        """
        """
        portal_workflow = self.portal_workflow
        state = portal_workflow.getInfoFor(self, "review_state")                    
        if state!="published":            
            wfcontext=self.portal_workflow.doActionFor(self,"publish",  comment="" )        
    
    def getMetadata(self):
        """
        """        
        return self.metadata_tool
            
    def getMetadataManager(self):
        """
        @summary: returns the metadata's metadata manager
        """        
        return self.metadata_tool
    
    def getStandard(self):
        """
        @summary: returns the standard for the current metadata object
        """
        items = self.getMetadataManager().objectItems()     
        
        for item in items:                        
            if item[1].meta_type == 'Standard':                
                if item[1].title == self.getMetadatatype():                    
                    return item[1]
        return None
    
    security.declarePublic('getHTMLView')
    def getHTMLView(self):
        """
        @summary: 
        """              
        try:
            c = Convert()
            html = c.convertToHTMLView(self.xml)        
            return html        
        except Exception, e:
            error = str(e)
            traceback.print_exc()
            return "An error occurred rendering the document contents: %(error)s." % locals()
            
        #standard = self.getStandard()                
        #return standard.transformXML(self.xml)                
    
    security.declarePublic('getHTMLEdit')
    def getHTMLEdit(self):
        """
        @summary: generates an xml editor for the xml attribute from the xml attribute
        """
        try:
            c = Convert()
            html = c.convertToHTML(self.xml)
            return html
        except Exception, e:
            error = str(e)
            traceback.print_exc()
            return "An error occurred rendering the document contents: %(error)s." % locals()
    
    def makeXHTML(self, html):
        """
        @summary: fix xhtml formatting broken by browser
        @param html: the html to fix
        """
        data = html.replace("<br>","")
        data = data.replace("<BR>","")
        data = data.replace('type="hidden">','type="hidden"/>')
        data = data.replace('type="hidden">','type="hidden"/>')
        data = data.replace('type="text">','type="text"/>')
        data = data.replace('type="button">','type="button"></input>')
        return data
    
    def generateURI(self):
        """
        @summary: generate a uri for metadata loaded from xml string
        """
        s = str(time.time()).replace(".","")
        s += str(random.randint(1, 9999))        
        return s  
    
    def getSummaryHTML(self):
        """
        """        
        #return self.catalogue_part(self)
        return self.summary_part(self)       
    
    def getModalSummaryHTML(self, fieldName, recordType):
        """
        """        
        #return self.catalogue_part(self)
        return self.modal_summary_part(self, fieldName=fieldName, recordType=recordType)       

    def extractBBox(self, xml):
        """
        """
        self.mBounds = []           
        try:
            res = self.getStandard().extractBBox(xml)
            parts = res.split("|")
            if len(parts) >= 4:
                parts = parts[0:4]
                if len(res.replace(" ","")) == 3:
                    self.mBounds = []
                self.mBounds = [float(x) for x in parts]
            if self.hasValidBounds():
                self.mMapSmall = self.getSampleImageForBounds(200,200)
                self.mMapLarge = self.mMapSmall#self.getSampleImageForBounds(640,480)            
        except:
            pass
            
    def extractCommonValuesFromMetadata(self,xml):
        """        
        """     
        self.mBounds = []
        self.mOnlineResource = [];  
        self.mAbstract = "";
        self.mTitle = "";
        self.mDate = "";
        self.mKeywords = "";
        self.mDescription = ""; 
        self.mScale = "";
        self.mOrganization = "";
        self.mMapSmall = ""
        self.mMapLarge = ""    
        self.mLanguage = "";  
        self.mOwner = "";  
                   
        res = self.getStandard().extractCommonFields(xml)
        parts = res.split("|")
        secondowner = ''
        for part in parts:
            print 'part', part
            attributes = part.split("=")
            if attributes[0] == "title":
                self.mTitle = attributes[1]
            if attributes[0] == "date":
                self.mDate = self.parseDateFromMetadata(attributes[1])
                #self.mDate = attributes[1]
            if attributes[0] == "keywords":
                self.mKeywords += attributes[1] + "\n"
            if attributes[0] == "abstract":
                self.mAbstract += attributes[1] + " "
            if attributes[0] == "online":
                self.mOnlineResource.append(attributes[1])
            if attributes[0] == "organization":
                self.mOrganization += attributes[1] + " "
            if attributes[0] == "scale":
                self.mScale = attributes[1]
            if attributes[0] == "language":
                self.mLanguage = attributes[1]
            if attributes[0] == "owner":
                self.mOwner = attributes[1]
            if attributes[0] == "secondowner":
                secondowner = attributes[1]
        if not self.mOwner:
            self.mOwner = secondowner
            
        related = self.getRelatedItems()
        if related:
            for object in related:
                if object.portal_type not in ['Metadata']:
                    self.setOnlineURL(object.absolute_url())
                    break
                    
        # self.Schema()['title'].set(self, self.mTitle)
        # self.Schema()['subject'].set(self, self.mKeywords.split(' '))
        # self.Schema()['description'].set(self, self.mDescription)
        self.setTitle(self.mTitle)
        self.setSubject(self.mKeywords.split(' '))
        self.setDescription(self.mDescription)
        self.reindexObject()

        return res
    
    def setXml(self, xml, ignoreValid=False):
        """
        """            
        try:
            if type(xml) == str:                
                if self.xml.strip() != "" and self.xml != xml:
                    moved = self.makeACopyToArchive()                     
                    if moved:
                        self.getCustodian().addLog("Archived Document", "Updated and archived document. " + self.uri + "\n With id: " + str(moved.id), type="Info")
                self.xml = xml
                if self.uri == "":
                    self.uri = self.generateURI()

                if not self.getStandard():
                    return
                if not ignoreValid:
                    valid = self.getStandard().validateXML(xml)[0]

                    if (not valid):
                        print "XML is not valid"
                        plone_utils = getToolByName(self, 'plone_utils')
                        contentEditSuccess=0
                        new_context = self.portal_factory.doCreate(self)
                        portal_workflow=new_context.portal_workflow
                        state = portal_workflow.getInfoFor(self, "review_state")
                        print "State is %s" %state 

                        if state=="published":
                            wfcontext=new_context.portal_workflow.doActionFor(self,"retract",
                                                               comment="Validation failed, auto retracting" )
                            plone_utils.addPortalMessage('XML Fails validation, this item has been auto-retracted.', 'warning')

            else:                            
                fileType = xml.filename[-3:]
                if fileType.lower() == "zip":
                    print ":ZIP FILE:"
                    # read zipfile and create metadata objects
                    util = ZipUtil(xml)
                    contents = util.getFileContentWithExtension("xml")
                    if len(contents) > 1:
                        #use first to create current metadata and the rest to build more
                        self.xml = contents[0][1]     
                        fName = contents[0][0]                                   
                        parent = self.aq_parent                    
                        for part in contents[1:]:
                            id = ss = "meta"+str(time.time()).replace(".","")        
                            parent._setObject(id,Metadata(id,part[0]))        
                            meta = getattr(parent,id)
                            meta.uri = xml.filename + "/" + part[0]
                            meta.setXml(part[1], ignoreValid)
                            meta.setMetadatatype(self.guessMetadataType(part[1]))
                    else:
                        self.xml = '''<?xml version="1.0" encoding="UTF-8"?><none></none>'''                

                elif fileType.lower() == "xml":                    
                    print ":XML FILE:"
                    if self.uri == "":                
                        self.uri = xml.filename                    
                    self.setXml(str(xml.read()))
                    return
                else:
                    raise "Unknown File type"

            if self.getMetadatatype() <> "":
                 self.checkExtract()
        except:
            io = StringIO()
            traceback.print_exc(file=io)
            io.seek(0)            
            trace = io.read()
            print trace
            if self.getCustodian():
                self.getCustodian().addLog("Error setting xml",trace,type="Error")
    

    def setMetadatatype(self, metadatatype):
        ""
        self.metadatatype = metadatatype
        if self.getMetadatatype() <> "":
             self.checkExtract()
        
    def checkExtract(self):
        """
        """
        #print 'self.getXml', self.getXml()
        #print '='*80
        if self.getXml() == "":
            return
        if self.getStandard() == None:
            return           
        self.extractCommonValuesFromMetadata(self.getXml())
        self.extractBBox(self.getXml())  
        
    def setOnlineURL(self, url):
        """
        """     
        
        doc = minidom.parseString(self.xml)        
        allStandards = XPathConfig.getMergedStandards();
        if self.getMetadatatype() in ["ISO19115","ISO19115p2","ISO19139","SANS1878"]:
            results = self.getExpressionResults(allStandards["sans1878_SpatialOnlineResourceURL"], doc)                        
        elif self.getMetadatatype() in ["EML"]:
            results = self.getExpressionResults("//distribution/online/url", doc)
        elif self.getMetadatatype() in ["FGDC"]:
            results = self.getExpressionResults("//citation/citeinfo/onlink", doc) 
        elif self.getMetadatatype() in ["DublinCore"]:
            results = self.getExpressionResults("//rdf:Description/@rdf:about", doc)   
            #//rdf:Description/@rdf:about
        else:
            print 'UNSUPPORTED METADATA', self.getMetadatatype()
            return
        if results:
            result = results[0]
            self.setValueOnNode(result, url)                
            self.xml = str(doc.toxml())
            self.mOnlineResource = [url]
         
    def createOnlineURLForISO(self, url):
        """
        XXX not tested: Do not use 
        """
        if not self.getMetadatatype() in ["ISO19115","ISO19115p2","ISO19139","SANS1878"]:
            return
        doc = minidom.parseString(self.xml)
                
        elms = doc.getElementsByTagName("gmd:CI_OnlineResource")
        if elms:
            elms2 = elms[0].getElementsByTagName("gmd:linkage")
            if not elms2:
                linkageElm = doc.createElement("gmd:linkage")
                elms[0].appendChild(linkageElm)
                
                urlElm = doc.createElement("gmd:URL")
                urlElm.nodeValue = url
                linkageElm.appendChild(urlElm)
                self.xml = str(doc.toxml())   
    
    def createOnlineURLForFGDC(self, url):
        """
        XXX not tested: Do not use
        """
        if self.getMetadatatype()  != "FGDC":
            return
        doc = minidom.parseString(self.xml)
                
        elms = doc.getElementsByTagName("citeinfo")
        if elms:
            elm = elms[0]
            linkElms = elm.getElementsByTagName("onlink")
            if not linkElms:
                linkElm = doc.createElement("onlink")
                linkElm.nodeValue = url
                elm.appendChild(linkElm)
                self.xml(str(doc.toxml()))
    
    def createOnlineURLForEML(self):
        """
        XXX not tested: Do not use
        """
        
        pass
         
    def fixIEQuotes(self,html):
        """
        """        
        sString = '(\s[a-zA-Z]+=)([^\s"><]+)'       
        
        p = re.compile(sString)
        return p.sub(r'\1"\2"', html)   
    
    def upperAllTags(self,html):
        """
        """        
        html = html.replace("<span","<SPAN")
        html = html.replace("</span","</SPAN")
        html = html.replace("<div","<DIV")
        html = html.replace("</div","</DIV")
        html = html.replace("<input","<INPUT")
        html = html.replace("input/>","INPUT/>")
        html = html.replace("<form","<FORM")
        html = html.replace("</form","</FORM")
        html = html.replace("label>","LABEL>")
        html = html.replace("<fieldset","<FIELDSET")
        html = html.replace("</fieldset>","</FIELDSET>")
        html = html.replace("legend>","LEGEND>")
        #html = html.replace("\r","")
        #html = html.replace("\n","")        
        return html             
    
    def updateXMLFromHTML(self, html=""):
        """
        @summary: updates the current xml attribute from the passed html
        @param html: the html to parse to xml and update the current xml attribute
        """
        try:
            html = self.fixIEQuotes(html)
            html = self.makeXHTML(html)
            #html = self.upperAllTags(html)
            #print "DEBUG***************", "upperAllTags"
            if html == "":            
                return self.messageTemplate %("warning", "Warning", "warning", "Warning", "Error saving XML")
      
            c = Convert()
            
            html = BeautifulSoup(html).prettify()
            open('/tmp/debug.html', 'w').write(html)
            
            xml = c.convertToXML(html)
            self.setXml(str(xml))        
            self.commitMe()
            return self.messageTemplate %("info", "Info", "info", "Info", "Document saved")
            #return 1
        except Exception, e:
            import traceback
            traceback.print_exc()
            
            errMsg = str(e)
            
            errText = ''
            
            #Try establishing line number to extract error in XML Document.
            try:
                
                line = int(errMsg.split('line ')[1].split(',')[0]) - 1
                data = str(html).split('\n')
                length = len(data)
                
                start = line
                end = line
                
                while start and (start >= line - 6):
                    start -= 1
                while (end < length) and (end <= line + 6):
                    end += 1
                
                for x in range(start, end):
                    nr = x + 1
                    lineText = html_quote(data[x])
                    if x == line:
                        errText += '<b><span style="color:blue;">..  #%(nr)d</span>  %(lineText)s</b><br/>' % locals()
                    else:
                        errText += '<span style="color:blue;">..  #%(nr)d</span>  %(lineText)s<br/>' % locals()
            except Exception, e:
                import traceback
                traceback.print_exc()
                errText = "Unable to display error in file: " + str(e)
            
            return self.messageTemplate %("error", "Error", "error", "Error", "An error occurred: %(errMsg)s<br/><br/><br/><br/>%(errText)s" % locals())
    
    def commitMe(self):
        """
        """
        self._p_changed = 1   
        transaction.savepoint(True)
        
    def downloadXML(self,REQUEST=None):
        """
        @summary: download xml document
        """        
        REQUEST.RESPONSE.setHeader("Content-type","text/xml")  
        REQUEST.RESPONSE.setHeader("Content-type","application/force-download")  
        REQUEST.RESPONSE.setHeader("Content-disposition","iattachment; filename=" + str(self.id) +".xml")  
        return self.xml.replace('><', '>\n<') 
    
    def downloadXMLPlain(self,REQUEST=None):
        """
        @summary: download xml document
        """        
        return self.xml 
    
    def hasGenericCoreFields(self):
        """
        """
        errorList = []
        coreFields = self.getGenericCoreFields()
        for key in coreFields.keys():
            if coreFields[key] == None:
                errorList.append(key)
        if errorList:            
            return [False,errorList]
        if len(coreFields) == 0:
            return [False,["All Fields"]]
        return [True,[]]

    def hasCoreFields(self):
        """
        """
        errorList = []
        coreFields = self.getCoreFields()
        for key in coreFields.keys():
            if coreFields[key] == None:
                errorList.append(key)
        if errorList:
            return [False,errorList]
        if len(coreFields) == 0:
            return [False,["All Fields"]]
        return [True,[]]
    
    def getGenericCoreFieldsOrder(self):
        """
        """
        currentStd = XPathConfig.STANDARD_TO_XPATH[self.getMetadatatype()]
        allStandards = XPathConfig.getMergedStandards();
        res = []
        for k in allStandards.keys():
            if k.startswith(currentStd):
                res.append(k)
        return res
    
    def getGenericCoreFields(self):
        """
        """
        currentStd = XPathConfig.STANDARD_TO_XPATH[self.getMetadatatype()]
        doc = minidom.parseString(self.xml)
        allStandards = XPathConfig.getMergedStandards();
        res = {}#OrderedDict()
        for k in allStandards.keys():
            if k.startswith(currentStd):
                hit = self.getFirstExpressionResult(allStandards[k], doc)
                if hit:
                    res[k] = hit
        return res
        
    def getFirstExpressionResult(self, xpath, documentObject): 
        """
        @summary: returns the first result of the expression, else empty string
        @param xpath: the expression to evaluate
        @param documentObject: sax document object to evaluate the xpath against
        @param ns: dict with namespace declarations to use in xpath evaluation
        @return: first result in xpath results or empty string
        """
        try:
            ns = self.getNamespaceDict(documentObject)
            con = ContextNew(documentObject, 1, 1, processorNss=ns)
            res = EvaluateNew(xpath, context=con)
            if res:
                r = res[0]
                if r.ATTRIBUTE_NODE != r.nodeType:
                    return r.toxml()
                if r.ATTRIBUTE_NODE == r.nodeType:
                    return r.value
        except:
            io = StringIO()
            traceback.print_exc(file=io)
            io.seek(0)
            trace = io.read()
            print trace
        return None
        
    def getExpressionResults(self, xpath, documentObject):
        """
        @summary: returns the results of the expression, else empty list
        @param xpath: the expression to evaluate
        @param documentObject: sax document object to evaluate the xpath against
        @param ns: dict with namespace declarations to use in xpath evaluation
        @return: list with xpath results
        """
        try:
            ns = self.getNamespaceDict(documentObject)
            con = ContextNew(documentObject, 1, 1, processorNss=ns)        
            result = EvaluateNew(xpath, context=con)
            return result
        except:
            io = StringIO()
            traceback.print_exc(file=io)
            io.seek(0)            
            trace = io.read()
            print trace
        return []   
    
    def updateGenericCoreFields(self,REQUEST=None):
        """
        @summary: update the core fields for the current doc standard
        """
        print 'Getting core fields..'
        if REQUEST == None:
            return 0          
        f = REQUEST.form     
        doc = minidom.parseString(self.xml) 
        allStandards = XPathConfig.getMergedStandards();   
        
        for k in allStandards.keys():
            if f.has_key(k):
                print '..', k, f[k]
                val = f[k]                
                self.setValueOnNode(self.getExpressionResults(allStandards[k], doc)[0], val)
                
        self.setXml(str(doc.toxml()))        
        self.reindexObject()
        return self.generic_corefields_editor(self)
    
        
    def setValueOnNode(self,node,value):
        """
        @summary: node can be a textnode or an attribute of an element
        @param node: the node to set the value on
        @param value: the value to set on the node
        """
        node.value = value
        node.data = value                
        
    def getNamespaceDict(self, doc):
        """
        """     
        attributes = doc.documentElement.attributes
        ns = {}
        for k in attributes.keys():    
            ns[k.replace("xmlns:","")] = attributes[k].firstChild.nodeValue
        return ns   
                            
    def getValidationResults(self):
        """
        @summary: validates document xml and returns the validation results
        """        
        res = self.getStandard().validateXML(self.xml)
        return res  
    
    def getFormatedValidationMessage(self):
        """
        """
        try:
            res = self.getValidationResults()
            if res[0] == True:
                return self.messageTemplate %("info", "Info", "info", "Info", "Document is valid") 
            else:
                tmpRes = res[1].replace("ERROR : ", "<br>ERROR : ")
                
                if tmpRes.count('file:/'):
                    start = tmpRes.find('file:/')
                    path = 'file:/' + tmpRes.split('file:/')[1].split("'")[0]

                    tmpRes = tmpRes.replace("'%(path)s'" % locals(), '')

                return self.messageTemplate %("warning", "Warning", "warning", "Warning", "Document is not valid.  \n "+ tmpRes)
        except Exception, e:
            import traceback
            traceback.print_exc()

            errMsg = str(e)

            errText = ''

            #Try establishing line number to extract error in XML Document.
            try:

                line = int(errMsg.split('line ')[1].split(',')[0]) - 1
                data = str(html).split('\n')
                length = len(data)

                start = line
                end = line

                while start and (start >= line - 2):
                    start -= 1
                while (end < length) and (end <= line + 3):
                    end += 1

                for x in range(start, end):
                    nr = x + 1
                    lineText = html_quote(data[x])
                    if x == line:
                        errText += '<b><span style="color:blue;">..  #%(nr)d</span>  %(lineText)s</b><br/>' % locals()
                    else:
                        errText += '<span style="color:blue;">..  #%(nr)d</span>  %(lineText)s<br/>' % locals()
            except Exception, e:
                import traceback
                traceback.print_exc()
                errText = "Unable to display error in file: " + str(e)
            return self.messageTemplate %("error", "Error", "error", "Error", "An error occurred: %(errMsg)s<br/><br/><br/><br/>%(errText)s" % locals())
            
    
    def validateXMLFromHTML(self, html):
        """
        @summary: validate the data from html
        @param html: the html to convert to xml for validation
        """
        try:
            html = self.fixIEQuotes(html)     
            html = self.makeXHTML(html) 
            #html = self.upperAllTags(html)
            html = BeautifulSoup(html).prettify()
            c = Convert()
            xml = c.convertToXML(html)        
            res = self.getStandard().validateXML(xml)
        
            if res[0] == True:
                #return "Document is valid"
                return self.messageTemplate %("info", "Info", "info", "Info", "Document is valid") 
            else:
                #return res[1]   
                # format the error result
                tmpRes = res[1].replace("ERROR : ", "<br>ERROR : ")
                return self.messageTemplate %("warning", "Warning", "warning", "Warning", "Document is not valid.  \n "+ tmpRes)
                #return messageTemplate %(res[1])
        except Exception, e:
            import traceback
            traceback.print_exc()

            errMsg = str(e)

            errText = ''

            #Try establishing line number to extract error in XML Document.
            try:

                line = int(errMsg.split('line ')[1].split(',')[0]) - 1
                data = str(html).split('\n')
                length = len(data)

                start = line
                end = line

                while start and (start >= line - 2):
                    start -= 1
                while (end < length) and (end <= line + 3):
                    end += 1

                for x in range(start, end):
                    nr = x + 1
                    lineText = html_quote(data[x])
                    if x == line:
                        errText += '<b><span style="color:blue;">..  #%(nr)d</span>  %(lineText)s</b><br/>' % locals()
                    else:
                        errText += '<span style="color:blue;">..  #%(nr)d</span>  %(lineText)s<br/>' % locals()
            except Exception, e:
                import traceback
                traceback.print_exc()
                errText = "Unable to display error in file: " + str(e)

            return self.messageTemplate %("error", "Error", "error", "Error", "An error occurred: %(errMsg)s<br/><br/><br/><br/>%(errText)s" % locals())

registerType(Metadata, PROJECTNAME)
# end of class Metadata

##code-section module-footer #fill in your manual code here
##/code-section module-footer



