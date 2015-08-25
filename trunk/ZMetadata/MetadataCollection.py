

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ZMetadata.config import *
from Globals import package_home

print "PACKAGE!!!!!!!", package_home

import Global
from Products.ZMetadata.Metadata import Metadata
from Products.ZMetadata.MetadataContainer import MetadataContainer
import time
from datetime import datetime
from Products.ATContentTypes.content.folder import ATFolder
from OFS.Folder import Folder
import sys
import traceback
from Products.ATContentTypes.content.schemata import ATContentTypeSchema

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

#MetadataCollection_schema = BaseFolderSchema.copy() + schema.copy()
MetadataCollection_schema = ATContentTypeSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class MetadataCollection(BaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'MetadataCollection'

    meta_type = 'MetadataCollection'
    portal_type = 'MetadataCollection'
    allowed_content_types = ['Metadata',"MetadataContainer", "Topic"]
    filter_content_types = 1
    global_allow = 0
    content_icon = 'metadatacollection.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "MetadataCollection"
    typeDescMsgId = 'description_edit_metadatacollection'

    actions =  (
       {'action': "string:${object_url}/new_metadata_from_template",
        'category': "object",
        'id': 'newFromTemplate',
        'name': 'New From Template',
        'permissions': ("View",),
        'condition': 'python:1'
       },
       )

    _at_rename_after_creation = True

    schema = MetadataCollection_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    def __init__(self,id,title="MetadataCollection"):
        ""
        self.id = id;
        self.title = title;        
        
    def makeAllPrivate(self):
        ""
        #workflowTool = getToolByName(context, "portal_workflow")
        #workflowTool.doActionFor(portal.sampleProperty, "submit")        
        pass
    
    def createNewContainer(self):
        """
        @summary: create a new folder and return the folder instance
        """
        d = datetime.now()
        title = d.ctime()
        id = "MetadataContainer_" + str(time.time()).replace(".","")
        self._setObject(id, MetadataContainer(id,title))
        #metaCol._setObject(metaCol.getId()+"-Archive", Archive(metaCol.getId()+"-Archive", "Archive"))        
        return getattr(self,id)  
        
    def checkMetadataMove(self):
        """
        """        
        count = self.getLocalMetadataRecordCount()
        if count > Global.config.getRecordsPerFolder():
            moveFolder = self.getMoveContainer()
            # move all local metadata to moveFolder
            
            recs = self.getLocalMetadataRecords()
            # split list into lists of RecordsPerFolder size
            recsList = []
            current = 0
            for x in range(len(recs) / Global.config.getRecordsPerFolder()):
                tmp = recs[current:current+Global.config.getRecordsPerFolder()]
                current += Global.config.getRecordsPerFolder()
                recsList.append(tmp)    
                
            for recList in recsList:
                moveFolder = self.getMoveContainer()
                for rec in recList:
                    try:
                        rec.backupOnDelete = False
                        moveFolder.manage_pasteObjects(self.manage_cutObjects([rec.getId()]))
                        rec.backupOnDelete = True
                    except:
                        traceback.print_exc(file=sys.stdout)
                        print "Could not move " + str(rec.getId()) + " to folder : " + str(moveFolder.id)
                                                    
    def getMoveContainer(self):
        """
        @summary: get the next folder to create metadata in        
        """
        # look for folder with latest creation date
        items = self.objectItems()
        for item in items:            
            if item[1].meta_type == "MetadataContainer": 
                theFolder = item[1]
                if len(theFolder.objectItems()) < Global.config.getRecordsPerFolder():
                    return theFolder
        # if all folders are full then create a new folder
        return self.createNewContainer() 
    
    def getLocalMetadataRecordIds(self):
        """
        """
        ids = []
        items = self.objectItems()
        for item in items:            
            if item[1].meta_type == "Metadata":
                ids.append(item[1].id)             
        return ids
    
    def getLocalMetadataRecords(self):
        """
        """
        records = []
        items = self.objectItems()
        for item in items:            
            if item[1].meta_type == "Metadata":
                records.append(item[1])             
        return records
    
    def getLocalMetadataRecordCount(self):
        """
        @summary: returns the number of records in the metadata collection that is not in a folder
        """
        count = 0
        items = self.objectItems()
        for item in items:            
            if item[1].meta_type == "Metadata":
                count +=1                
        return count
    
    def getMetadataTypes(self):
        """
        @summary: returns a comma seperated list of metadata types for creation        
        @return: a comma seperated list of metadata types available for creation
        """
        return Global.config.getMetadataTypes()               
    
    def getProductPath(self):
        ""        
        return package_home(product_globals)
    
    def createNewFromTemplate(self,title,type):
        """
        @summary: creates a new metadata document from a blank template
        @param title: string, the title of the new document
        @param type: string, the metadata template to use for new document
        """     
        path = self.getProductPath()
        
        #SANS1878
        if type == "SANS1878":
            templatePath = path + "/templates/iso_19139_master.xml"
        
        if type == "ISO19115":            
            templatePath = path + "/templates/iso_19139_master.xml"
            
        if type == "ISO19139":            
            templatePath = path + "/templates/iso_19139_master.xml"
            
        if type == "ISO19115p2":            
            templatePath = path + "/templates/iso_19139_master.xml"
            
        if type == "DublinCore":            
            templatePath = path + "/templates/new_dublincore.xml"
            
        if type == "FGDC":            
            templatePath = path + "/templates/new_fgdc.xml"
            
        if type == "EML":            
            templatePath = path + "/templates/new_eml.xml"
                
        f = file(templatePath,"r")
        xml = f.read()
        f.close()
        
        id = ss = "meta"+str(time.time()).replace(".","")        
        self._setObject(id,Metadata(id,title))        
        meta = getattr(self,id)
        meta.setXml(xml) 
        meta.setMetadatatype(type)
        #meta.setType(type)
        return 1        
    

registerType(MetadataCollection, PROJECTNAME)
# end of class MetadataCollection

##code-section module-footer #fill in your manual code here
##/code-section module-footer



