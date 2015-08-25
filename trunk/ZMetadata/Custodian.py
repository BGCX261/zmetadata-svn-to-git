

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ZMetadata.config import *
from Products.Communities.content.MetadataCollection import MetadataCollection
from Products.ZMetadata.Logs import Logs
from Products.ZMetadata.Archive import Archive
import time
import sys
import traceback
from Products.ATContentTypes.content.schemata import ATContentTypeSchema


##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

##    StringField(
##        name='name',
##        widget=StringWidget(
##            label='Name',
##            label_msgid='ZMetadata_label_name',
##            i18n_domain='ZMetadata',
##        )
##    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

#Custodian_schema = BaseFolderSchema.copy() +  schema.copy()
Custodian_schema = ATContentTypeSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Custodian(BaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Custodian'

    meta_type = 'Custodian'
    portal_type = 'Custodian'
    allowed_content_types = ['Harvester', 'Window']
    filter_content_types = 1
    global_allow = 1
    content_icon = 'custodian.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Custodian"
    typeDescMsgId = 'description_edit_custodian'

    _at_rename_after_creation = True

    schema = Custodian_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    
    def __init__(self,id,title="Custodian"):
        ""
        self.id = id;
        self.title = title;
        
    def _renameAfterCreation(self,check_auto_id=True):
        ""             
        self._setObject(self.getId()+"-Logs", Logs(self.getId()+"-Logs"))
        self._setObject(self.getId()+"-MetadataCollection",MetadataCollection(self.getId()+"-MetadataCollection"))   
        metaCol = getattr(self,self.getId() + "-MetadataCollection")
        #exec("metaCol = self." + self.getId() + "-MetadataCollection")   
        #self._setObject(self.getId()+"-Archive", Folder(self.getId()+"-Archive","Archive"))
        #metaCol._setObject(metaCol.getId()+"-Archive", Folder(metaCol.getId()+"-Archive"))     
        #self.invokeFactory(id=self.getId() + "-Archive" ,type_name="Folder", title="Archive")
        
        metaCol._setObject(metaCol.getId()+"-Archive", Archive(metaCol.getId()+"-Archive", "Archive"))
        metaCol._renameAfterCreation(check_auto_id)
        #metaCol.invokeFactory(id=metaCol.getId()+"-Archive" ,type_name="Archive", title="Archive")
    
##    def manage_afterAdd(self,item, container):
##        """
##        """                        
##        pass

    
    def getMetadataCollectionFolder(self):
        """
        @summary:
        @return:
        """
        items = self.objectItems()
        for item in items:            
            if (item[1].meta_type == "MetadataCollection"): 
                return item[1]
        return None        
    
    def getLogsFolder(self):
        """
        @summary: 
        @return: the logs folder for the current custodian
        """
        items = self.objectItems()
        for item in items:            
            if (item[1].title == "Logs") and (item[1].meta_type == "Logs"): 
                return item[1]
        return None
    
    def getHarvesters(self):
        """
        @summary: returns a list of harvesters
        """
        retList = []
        items = self.objectItems()
        for item in items:            
            if item[1].meta_type == "Harvester": 
                retList.append(item[1])        
        return retList
    
    def addLog(self,title,message,type="Error"):
        """
        @summary: convenience for creating new log messages 
        @param title: the title to the new log
        @param message: the message to set in the log
        """        
        newId = "log" + str(time.time()).replace(".","")
        logs = self.getLogsFolder()
        logs.invokeFactory(id=newId ,type_name="Log", title=title)   
        log = getattr(logs, newId)
        log.setMessage(message)   
        log.setLogtype(type)       
    
    def test(self):
        """
        """
        print "================================="
        from Globals import package_home
        product_path = package_home(product_globals)
        print product_path
        print "================================="

registerType(Custodian, PROJECTNAME)
# end of class Custodian

##code-section module-footer #fill in your manual code here
##/code-section module-footer



