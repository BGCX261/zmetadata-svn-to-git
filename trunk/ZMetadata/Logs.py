

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ZMetadata.config import *
from datetime import datetime
from Products.ZMetadata.LogContainer import LogContainer
import sys
import traceback
import time
from StringIO import StringIO
import Global
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.CMFCore import permissions

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

#Logs_schema = BaseFolderSchema.copy() + schema.copy()
Logs_schema = ATContentTypeSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Logs(BaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Logs'

    meta_type = 'Logs'
    portal_type = 'Logs'
    allowed_content_types = ['LogContainer','Log']
    filter_content_types = 1
    global_allow = 0
    content_icon = 'logs.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Logs"
    typeDescMsgId = 'description_edit_logs'


    actions =  (
       {'action': "string:${object_url}/search_logs",
        'category': "metadata",
        'id': 'search',
        'name': 'Search',
        'permissions': (permissions.ViewManagementScreens,),
        'condition': 'python:1'
       },
    )

    _at_rename_after_creation = True

    schema = Logs_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    
    def __init__(self,id,title="Logs"):
        ""
        self.id = id;
        self.title = title;
        
    def manage_afterAdd(self,item, container):
        """
        """                   
        self.manage_permission("List folder contents", roles=["Manager"], acquire=False)      
        self.manage_permission("Access contents information", roles=["Manager"], acquire=False)
        self.manage_permission("View", roles=["Manager"], acquire=False)
        
    def search(self,REQUEST=None):
        """
        """
        # clear the session        
        s = REQUEST.SESSION
        s["logSearchResults"] = []
        
        #anytext abstract keywords title scale fromdate todate category spatialtype extent
        
        keyword = ""
        fromDate = ""
        toDate = ""
        logType = ""
        
        f = REQUEST.form        
        
        if f.has_key("keyword"):
            keyword = f["keyword"]        
        if f.has_key("logType"):
            logType = f["logType"]   
            if logType == '-Any-':
                logType = ""  
        if f.has_key("fromDate"):
            fromDate = f["fromDate"]
            parts = fromDate.split("-")
            fromDate = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
        if f.has_key("toDate"):
            toDate = f["toDate"]
            parts = toDate.split("-")
            toDate = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
        
        #review_state = "published",SearchableText = "Plone",sort_order="Date"
        # , path = self.absolute_url()
        results = self.portal_catalog.searchResults(meta_type = "Log")        
        obResults = [x.getObject() for x in results]        
        
        if keyword:            
            obResults = [x for x in obResults if x.message.lower().find(keyword.lower()) != -1]        
        if fromDate:            
            obResults = [x for x in obResults if x.getDate() >= fromDate]
        if toDate:            
            obResults = [x for x in obResults if x.getDate() <= toDate]
        if logType:            
            obResults = [x for x in obResults if x.getLogtype() == logType]            
        
        count = len(obResults) 
        
        if count == 0:
            return "No matches found"
        else:     
            tmpResList = []
            for ob in obResults:
                tmpDict = {}
                tmpDict["type"] = ob.getLogtype();
                tmpDict["date"] = ob.getDate();
                tmpDict["url"] = ob.absolute_url();
                tmpResList.append(tmpDict) 
                   
            s = REQUEST.SESSION            
            s["logSearchResults"] = tmpResList                        
            return 1   
    
    def checkLogMove(self):
        """
        """        
        count = self.getLocalLogRecordCount()
        if count > Global.config.getRecordsPerFolder():
            moveFolder = self.getMoveContainer()
            # move all local metadata to moveFolder
            
            recs = self.getLocalLogs()
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
                        moveFolder.manage_pasteObjects(self.manage_cutObjects([rec.getId()]))                        
                    except:
                        traceback.print_exc(file=sys.stdout)
                        print "Could not move " + str(rec.getId()) + " to folder : " + str(moveFolder.id)
    
    def getLocalLogs(self):
        """
        """
        records = []
        items = self.objectItems()
        for item in items:            
            if item[1].meta_type == "Log":
                records.append(item[1])             
        return records
    
    def getMoveContainer(self):
        """
        @summary: get the next folder to create metadata in        
        """
        # look for folder with latest creation date
        items = self.objectItems()
        for item in items:            
            if item[1].meta_type == "LogContainer": 
                theFolder = item[1]
                if len(theFolder.objectItems()) < Global.config.getRecordsPerFolder():
                    return theFolder
        # if all folders are full then create a new folder
        return self.createNewContainer() 
    
    def createNewContainer(self):
        """
        @summary: create a new folder and return the folder instance
        """
        d = datetime.now()
        title = d.ctime()
        id = "LogContainer_" + str(time.time()).replace(".","")
        self._setObject(id, LogContainer(id,title))                
        return getattr(self,id)  
    
    def getLocalLogRecordCount(self):
        """
        @summary: returns the number of records in the metadata collection that is not in a folder
        """
        count = 0
        items = self.objectItems()
        for item in items:            
            if item[1].meta_type == "Log":
                count +=1                
        return count  
        

registerType(Logs, PROJECTNAME)
# end of class Logs

##code-section module-footer #fill in your manual code here
##/code-section module-footer



