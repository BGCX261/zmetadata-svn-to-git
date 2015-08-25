# -*- coding: utf-8 -*-
#
# File: MetadataCollection.py
#
# Copyright (c) 2009 by []
# Generator: ArchGenXML Version 2.3
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Globals import package_home
import time
from datetime import datetime
from Products.ZMetadata.Metadata import Metadata
from Products.ZMetadata.MetadataContainer import MetadataContainer


from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.Communities.config import *
from Products.ZMetadata import Global

##code-section module-header #fill in your manual code here
from Products.ATContentTypes.content.topic import ATTopic
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

MetadataCollection_schema = ATFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class MetadataCollection(ATFolder):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IMetadataCollection)

    meta_type = 'MetadataCollection'
    _at_rename_after_creation = True

    schema = MetadataCollection_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
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
        return meta.absolute_url()
        return 1
    
    security.declarePublic('_renameAfterCreation')
    def _renameAfterCreation(self, check_auto_id=True):
        """"""
        self._setObject("content", ATTopic("content"))
        self['content'].setTitle("Content")
        self['content'].addCriterion('Type', 'ATPortalTypeCriterion')
        self['content'].crit__Type_ATPortalTypeCriterion.setValue(['Metadata', 'MetadataContainer'])
        self['content'].addCriterion('path', 'ATRelativePathCriterion')
        self['content'].setCustomView(True)
        self['content'].setCustomViewFields(['Title', 'ModificationDate', 'review_state', 'CreationDate', 'Type'])
        self.portal_workflow.doActionFor(self['content'], "publish", comment="")        
        self.setDefaultPage('content')
    

registerType(MetadataCollection, PROJECTNAME)
# end of class MetadataCollection

##code-section module-footer #fill in your manual code here
##/code-section module-footer



