

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from Globals import package_home
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ZMetadata.config import *
import time
import Global
from Products.ZMetadata.Standard import Standard
from Products.ZMetadata.Metadata import Metadata
from Products.Communities.content.MetadataContainer import MetadataContainer
from datetime import datetime
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from shapely.geometry import Polygon
import string
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from datetime import date
from xml.dom import minidom
import XPathConfig
from multiPing import MultiPinger
from StringIO import StringIO
import traceback
import urlparse
import FieldsConfig
import urllib
from ZipUtil import ZipUtil



##code-section module-header #fill in your manual code here
from Products.CMFPlone import PloneMessageFactory as _
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

#MetadataManager_schema =  BaseFolderSchema.copy() +  schema.copy()
MetadataManager_schema =  ATContentTypeSchema.copy() +  schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class MetadataManager(BaseFolder):
    """
    """
    
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'MetadataManager'

    meta_type = 'MetadataManager'
    portal_type = 'MetadataManager'
    allowed_content_types = ["Standard"]
    filter_content_types = 1
    global_allow = 0
    content_icon = 'metadatamanager.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "MetadataManager"
    typeDescMsgId = 'description_edit_metadatamanager'


    actions =  (
       {'action': "string:${object_url}/search_metadata",
        'category': "metadata",
        'id': 'search',
        'name': 'Search',
        'permissions': (permissions.View,),
        'condition': 'python:1'
       },
       {'action': "string:${object_url}/metadata_reports",
        'category': "metadata",
        'id': 'reports',
        'name': 'Reports',
        'permissions': (permissions.ViewManagementScreens,),
        'condition': 'python:1'
       },
       {'action': "string:${object_url}/metadata_harvester_admin",
        'category': "metadata",
        'id': 'harvesteradmin',
        'name': 'Harvester Admin',
        'permissions': (permissions.ViewManagementScreens,),
        'condition': 'python:1'
       },

    )

    _at_rename_after_creation = True

    schema = MetadataManager_schema
    
    _v_multiPing = MultiPinger([])
    
    def __init__(self,id, title="Metadata"):
        """
        """        
        self.id = id;
        self.title = title;   
        
    def getMetadataTypes(self):
        """
        """  
        metadataTypes = Global.config.getMetadataTypes()
        return metadataTypes 
        
    def getProductPath(self):
        ""        
        return package_home(product_globals)
    
    def getFieldAliases(self):
        """
        """
        return FieldsConfig.fieldAliases    
    
    def getFieldValues(self):
        """
        """
        return FieldsConfig.fieldValues
    
    def getDateFields(self):
        """
        """
        return FieldsConfig.dateFields  
    
    def zipMetadata(self, REQUEST=None):
        """
        @summary: gets an id of a metadatacollection or metadatacontainer and zips the content and returns the zip file
        """        
        url = REQUEST.id        
        parts = url.split("/")
        theId = parts[-1]
                
        results = self.portal_catalog.searchResults(id = theId)
        obj = results[0].getObject()
        
        if obj.portal_type in ['Topic']:
            obj = obj.aq_parent
        print obj
        
        zipData = {}
        items = obj.objectItems()
        for i in items:
            if i[1].meta_type == "Metadata":
                #print i[1].title 
                zipData[i[1].id + ".xml"] = i[1].xml 
        
        sIO = StringIO("")
        z = ZipUtil(sIO, mode="w")       
        z.writeData(zipData)
        
        if REQUEST:
            REQUEST.RESPONSE.setHeader("Content-type","application/zip")
        return z.getZipFileData()
    
    def createNewFromTemplate(self,REQUEST=None):
        """
            string:${portal_url}/metadata_tool/metadata_from_template?id=${object_url}
        """   
        
        metaTitle = REQUEST.form["tbxTitle"]
        type = REQUEST.form["cbxType"]        
        parentUrl = REQUEST.form["tbxParentUrl"]
               
        parts = parentUrl.split("/")
        theId = parts[-1]
                
        results = self.portal_catalog.searchResults(id = theId)
        obj = results[0].getObject()  
        path = self.getProductPath()
        
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
        
        id =  "meta"+str(time.time()).replace(".","")  
        if metaTitle == "":
            metaTitle = id
          
        if hasattr(obj, "_setObject"):
            obj._setObject(id,Metadata(id,metaTitle))
            meta = getattr(obj,id)
        else: # add it to the parent
            parent = obj.aq_parent
            parent._setObject(id,Metadata(id,metaTitle))
            meta = getattr(parent,id)            
       # meta = getattr(obj,id)
        meta.setXml(xml)
        meta.setMetadatatype(type)
        if type in ["DublinCore","DublinCore","EML"]:
            return meta.view_metadata_summary(meta)
        else:
            return meta.edit_metadata_core_fields(meta)
                                       
        
    def getMetadataHarvestedInDateRange(self,REQUEST=None):
        """
        """
        hour = 60 * 60
        day = 24 * hour
        week = day * 7 
        month = 30 * day 
        year = 365 * day      
        
        currentSecs = time.time()
        currentDate = datetime.now()
        fromDate = currentDate
        toDate = currentDate
        timeOperation = ""
        
        if REQUEST.has_key("time_operation"):
            timeOperation = REQUEST["time_operation"] 
            if timeOperation == "Today":
                fromDate = datetime(currentDate.year, currentDate.month, currentDate.day, hour=1, minute=1, second=1)
                toDate = datetime(currentDate.year, currentDate.month, currentDate.day, hour=23, minute=59, second=59)
            if timeOperation == "Week":
                fromDateStruct = time.localtime(currentSecs)
                toDateStruct = time.localtime(currentSecs - week)
                fromDate = datetime(fromDateStruct[0],fromDateStruct[1],fromDateStruct[2] ,hour=fromDateStruct[3], minute=fromDateStruct[4], second=fromDateStruct[5])
                toDate = datetime(toDateStruct[0],toDateStruct[1],toDateStruct[2] ,hour=toDateStruct[3], minute=toDateStruct[4], second=toDateStruct[5])                
            if timeOperation == "Month":
                fromDateStruct = time.localtime(currentSecs)
                toDateStruct = time.localtime(currentSecs - month)
                fromDate = datetime(fromDateStruct[0],fromDateStruct[1],fromDateStruct[2] ,hour=fromDateStruct[3], minute=fromDateStruct[4], second=fromDateStruct[5])
                toDate = datetime(toDateStruct[0],toDateStruct[1],toDateStruct[2] ,hour=toDateStruct[3], minute=toDateStruct[4], second=toDateStruct[5])    
            if timeOperation == "Year":
                fromDateStruct = time.localtime(currentSecs)
                toDateStruct = time.localtime(currentSecs - year)
                fromDate = datetime(fromDateStruct[0],fromDateStruct[1],fromDateStruct[2] ,hour=fromDateStruct[3], minute=fromDateStruct[4], second=fromDateStruct[5])
                toDate = datetime(toDateStruct[0],toDateStruct[1],toDateStruct[2] ,hour=toDateStruct[3], minute=toDateStruct[4], second=toDateStruct[5])                    
            
        if  REQUEST.has_key("from_date") and REQUEST.has_key("to_date"):
            sFromDate = REQUEST["from_date"]
            sToDate = REQUEST["to_date"]
            fromDate = datetime(int(sFromDate.split("-")[0]),int(sFromDate.split("-")[1]),int(sFromDate.split("-")[2]))
            toDate = datetime(int(sToDate.split("-")[0]),int(sToDate.split("-")[1]),int(sToDate.split("-")[2]))
                         
            
        results = self.portal_catalog.searchResults(Type="Metadata", created = {"query": [fromDate,toDate], "range": "minmax"})        
        records = [x.getObject() for x in results]
        # this will exclude archived metdata 
        records = [x for x in records if x.aq_parent.meta_type != "Archive"]
        
        total = len(records)
        return self.metadata_harvested_from_to(self,fromDate=fromDate, toDate=toDate, total=total)
                
        
    def getMetadataCountPerCustodian(self,REQUEST=None):
        """
        """
        countPerCustodian = {}
        # get all custodians 
        results = self.portal_catalog.searchResults(meta_type = "Custodian")        
        custodians = [x.getObject() for x in results]
        for custodian in custodians:
            cusName = custodian.title            
            countPerCustodian[cusName] = 0
            collection = custodian.getMetadataCollectionFolder()
            
            items = collection.objectItems()
            for item in items:            
                if item[1].meta_type == "Metadata":
                    countPerCustodian[cusName] = countPerCustodian[cusName] + 1 
                if item[1].meta_type == "MetadataContainer":
                    containerItems = item[1].objectItems()
                    for containerItem in containerItems:
                        if containerItem[1].meta_type == "Metadata":
                            countPerCustodian[cusName] = countPerCustodian[cusName] + 1
                            
        vals = countPerCustodian.values()
        total = 0
        for val in vals:
            total += val   
        return self.metadata_count_per_custodian(self,data=countPerCustodian, total=total)
        
        # get all metadata records in the metadata collection       
        #REQUEST.RESPONSE.redirect()
        
    def hasPermission(self, object, permission = "View"):
        """
        """
        mtool = self.portal_membership
        checkPermission = mtool.checkPermission
        return checkPermission(permission, object)
        
    def getAllMyMetadataLocations(self):
        """
        """
        results = self.portal_catalog.searchResults(meta_type = "MetadataCollection")
        collections = []
        
        for x in results:
            try:
                collections += [x.getObject()]
            except:
                #For broken catalogs
                pass
        
        collections = [collection for collection in collections if self.hasPermission(collection, 'Add portal content')]
        
        custodians = {}
        for collection in collections:
            if not custodians.has_key(collection.aq_parent):
                custodians[collection.aq_parent] = []
            custodians[collection.aq_parent] += [collection]
        
        return custodians
        
    def getMetadataCustodian(self, metadata):
        """
        """        
        try:
            object = metadata
            while object.meta_type != 'Custodian':                
                object = object.aq_parent
            return object
        except Exception, e:
            print e
            return None
        
        
    def uploadMetadataFromPortalAction(self, id, collectionLocation=None, containerName=None, REQUEST=None):
        """
        """
        #parts = id.split("/")
        #theId = parts[-1]
        #path = '/'.join(parts[3:])
        if not collectionLocation:
            contextPath = REQUEST.environ["HTTP_REFERER"]
            #portal_url = getToolByName(self, 'portal_url')
            REQUEST.RESPONSE.redirect('pick-custodian?id=%(id)s' % locals())
            return
        
        catalog = getToolByName(self, 'portal_catalog')
        data = catalog(UID=id)[0].getObject()
        collection = catalog(UID=collectionLocation)[0].getObject()
        theId = data.getId()
        
        #data = self.portal_url.getPortalObject().restrictedTraverse(id)
        #collection = self.portal_url.getPortalObject().restrictedTraverse(collectionLocation)

        print 'data', data.getId(), data.absolute_url()
        print 'collection', collection.getId(), collection.absolute_url()

        
        if data.UID() not in collection.objectIds():
            collection._setObject(data.UID(), MetadataContainer(data.UID()))
        container = collection[data.UID()]
        container.setTitle(containerName)
        #container._renameAfterCreation(True)
        print 'container', container.getId(), container.absolute_url()
        
        
        newId = "meta"+str(time.time()).replace(".","")
        container._setObject(newId, Metadata(newId,"New Metadata For " + theId))
        
        # set object related items
        metadata = getattr(container,newId)
        relatedItems = [x for x in data.getRelatedItems() if x]
        relatedItems.append(metadata)
        data.setRelatedItems(relatedItems)
        # set metadata related item to obj
        metadataRelatedItems = [x for x in metadata.getRelatedItems() if x]
        metadataRelatedItems.append(data)
        metadata.setRelatedItems(metadataRelatedItems)
        REQUEST.RESPONSE.redirect(metadata.absolute_url() + "/edit")
        return
        
        #results = self.portal_catalog.searchResults(id = theId)
        #obj = results[0].getObject()    
        
        # get the logged in users user folder and create metadata there
        #homeFolder = self.portal_membership.getHomeFolder()
        #print homeFolder
        
        #if homeFolder:
        #    # check if metadata folder exists, else create it
        #    hasFolder = False
        #    items = homeFolder.objectItems()
        #    for item in items:            
        #        print item[1].meta_type
        #        if item[1].meta_type == "ATFolder":
        #            if item[1].id == "Metadata":
        #                hasFolder = True            
        #    if not hasFolder:
        #        homeFolder.invokeFactory('Folder',"Metadata")
        #    parent = getattr(homeFolder, "Metadata")            
        #else:         
        #    parent = obj.aq_parent   
                
        newId = "meta"+str(time.time()).replace(".","")
        parent._setObject(newId,Metadata(newId,"New Metadata For " + theId))
        metadata = getattr(parent,newId)
        # set object related items
        relatedItems = [x for x in obj.getRelatedItems() if x]
        relatedItems.append(metadata)
        obj.setRelatedItems(relatedItems)
        # set metadata related item to obj
        metadataRelatedItems = [x for x in metadata.getRelatedItems() if x]
        metadataRelatedItems.append(obj)
        metadata.setRelatedItems(metadataRelatedItems)
        
        REQUEST.RESPONSE.redirect(metadata.absolute_url() + "/edit")
    
    def getMapLayers(self):
        """
        """  
        layers = Global.config.getMapLayers()
        return string.join(layers,",")
    
    def getMapserverUrl(self):
        """
        """
        return Global.config.getMapServer() 
    
    def getMapExtent(self):
        """
        """
        extent = Global.config.getMapExtent()        
        return extent
        
    def doSavedSearch(self, REQUEST=None):
        """
        """
        self.doSearch(REQUEST)
        REQUEST.RESPONSE.redirect("/spatial_results")
    
    def doDiagSearch(self, REQUEST=None):
        """
        """
        self.doSearch(REQUEST)
        REQUEST.RESPONSE.redirect("/resultIds_diag")
        
    def doSearch(self, REQUEST=None):
        """
        @summary: do the search from the advanced search interface
        """
        # clear the session
        import time
        startTime = time.time()
        s = REQUEST.SESSION
        s["searchResults"] = []
        
        #anytext abstract keywords title scale fromdate todate category spatialtype extent
        anytext = ""
        abstract = ""
        title = ""
        keywords = ""
        scale = ""
        fromdate = ""
        todate = ""
        category = ""
        extent = ""
        spatialtype = ""
        
        f = dict(REQUEST.form)
        modal = f.has_key('modal')
        print 'modal', modal
        if modal:
            fieldName = f['fieldName']
            recordType = f['recordType']
            del f['modal']
            del f['fieldName']
        else:
            fieldName = ''
            recordType = ''


        if f.has_key("extent"):
            if f.has_key("spatialtype"):
                extent = f["extent"]
                tmpExtent = extent.split(",")
                extent = [float(x) for x in tmpExtent]
                spatialtype = f["spatialtype"]  
        if f.has_key("title"):
            title = f["title"]
        if f.has_key("abstract"):
            abstract = f["abstract"]
        if f.has_key("keywords"):
            keywords = f["keywords"]
        if f.has_key("scale"):
            scale = f["scale"]
            scale = int(scale)
        if f.has_key("anytext"):
            anytext = f["anytext"]
        if f.has_key("category"):
            category = f["category"]
        if f.has_key("fromdate"):
            fromdate = f["fromdate"]
            parts = fromdate.split("-")
            fromdate = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
        if f.has_key("todate"):
            todate = f["todate"]
            parts = todate.split("-")
            todate = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
        
        #review_state = "published",SearchableText = "Plone",sort_order="Date"
        if keywords:
            if recordType:
                results = self.portal_catalog.searchResults(meta_type = "Metadata", metadatatype = recordType, Subject = keywords.split())
                print 'metadatatype', recordType
            else:
                results = self.portal_catalog.searchResults(meta_type = "Metadata", Subject = keywords.split())
        else:
            if recordType:
                results = self.portal_catalog.searchResults(meta_type = "Metadata", metadatatype = recordType)
                print 'metadatatype', recordType
            else:
                results = self.portal_catalog.searchResults(meta_type = "Metadata")
        print "Searching " + str(len(results)) + " metadata records"
        obResults = []
        # Remove archived metadata records.
        for x in results:
            try:
                object = x.getObject()
                if object.aq_inner.aq_parent.meta_type != 'Archive':
                    obResults += [x.getObject()]
            except Exception, e:
                print e
        for ob in obResults:
            print '>', ob.metadatatype
        
        if extent and spatialtype:                        
            obResults = [x for x in obResults if x.mBounds]            
            obResults = [x for x in obResults if self.checkExtent(x.mBounds,extent, spatialtype)]
        if anytext:            
            obResults = [x for x in obResults if x.xml.lower().find(anytext.lower()) != -1]
        if title and not anytext:            
            obResults = [x for x in obResults if x.mTitle.lower().find(title.lower()) != -1]
        if abstract and not anytext:            
            obResults = [x for x in obResults if x.mAbstract.lower().find(abstract.lower()) != -1]
        #if keywords and not anytext:            
        #    obResults = [x for x in obResults if x.mKeywords.lower().find(keywords.lower()) != -1]
        if scale:            
            obResults = [x for x in obResults if x.mScale]
            obResults = [x for x in obResults if x.mScale < scale]            
        if category:
            obResults = [x for x in obResults if x.metadatacategory.lower().find(category.lower()) != -1]
        if fromdate:            
            obResults = [x for x in obResults if x.mDate and x.mDate >= fromdate]
        if todate:            
            obResults = [x for x in obResults if x.mDate and x.mDate <= todate]
        
        count = len(obResults)           

        print "SEARCH TIME:", time.time()-startTime

        if count == 0:
            return "No matches found"
        else:            
            s = REQUEST.SESSION
            if not modal:
                resultIds = [x.getId() for x in obResults]
            else:
                resultIds = [x.UID() for x in obResults]
            
            
            print 'resultIds', resultIds
            s["resultIds"] = resultIds
            
            saveString = '?'
            for key in f.keys():
                value = urllib.quote(str(f[key]))               
                saveString += ('%s=%s&' % (key, value))
            REQUEST["data"] = saveString
            REQUEST.RESPONSE['data'] = saveString
            s["data"] = saveString
            return 1
        
    def getSearchResultTemplateName(self):
        """
        @summary: returns the searchresult template to use
        """                
        res = Global.config.getSearchResultTemplateName()        
        return res                         
        
    def checkExtent(self, metaExtent, checkExtent, operation):
        """
        @summary: checks polygons against operation
        @param metaExtent: list in the format [minx,miny,maxx,maxy]
        @param checkExtent: list in the format [minx,miny,maxx,maxy]
        """        
        metaExtent = [float(x) for x in metaExtent]
        checkExtent = [float(x) for x in checkExtent]
        
        metaPoly = Polygon(((metaExtent[0],metaExtent[1]), (metaExtent[0],metaExtent[3]), (metaExtent[2],metaExtent[3]), (metaExtent[2],metaExtent[1])))
        checkPoly = Polygon(((checkExtent[0],checkExtent[1]), (checkExtent[0],checkExtent[3]), (checkExtent[2],checkExtent[3]), (checkExtent[2],checkExtent[1])))
        
        if operation == "Contains":
            return checkPoly.contains(metaPoly)   
        if operation == "Intersects":
            return checkPoly.intersects(metaPoly)
        if operation == "Equals":
            return checkPoly.equals(metaPoly)
        if operation == "Touches":
            return checkPoly.touches(metaPoly)
        if operation == "Within":            
            return checkPoly.within(metaPoly)
        if operation == "Outside":
            return checkPoly.disjoint(metaPoly)                    
    
    def getMetadataCategories(self):
        """
        @summary: returns a list of metadata categories
        """        
        return Global.config.getMetadataCategories();             
        
    def cleanLogFolders(self):
        """
        """
        results = self.portal_catalog.searchResults(meta_type = "Logs")        
        obResults = [x.getObject() for x in results]
        for collection in obResults:
            collection.checkLogMove()
        
    
    def cleanMetadataCollections(self):
        """
        @summary: checks the count of metadata records in the
        collection and restructures the collection according to recordsPerFolder paramater in Global
        """
        results = self.portal_catalog.searchResults(meta_type = "MetadataCollection")        
        obResults = [x.getObject() for x in results]
        for collection in obResults:
            collection.checkMetadataMove()
            
    def getMetadataCatalogueData(self,REQUEST=None):
        """
        @summary: returns a list of all published metadata summaries in the portal
        """        
        resList = []
        results = self.portal_catalog.searchResults(meta_type = "Metadata", review_state = "published")        
        obResults = [x.getObject() for x in results]
        for metadata in obResults:
            resList.append(metadata.getSummaryHTML())        
        return resList        
    
    def triggerAllHarvesters(self,REQUEST=None):
        """
        @summary: manually trigger all the harvesters in the website for re-harvest
        """
        res = ""
        
        msgTemplate = "<a href='%s'>%s</a>  did not update correctly.\n"
        
        results = self.portal_catalog.searchResults(meta_type = "Harvester")        
        obResults = [x.getObject() for x in results]
        for harvester in obResults:
            msg = harvester.harvest()
            if msg > 0:
                res += msgTemplate %(harvester.absolute_url(), harvester.title)
                #res += "Harvester with the name : " + harvester.title + " did not update correctly.\n"
        
        if not res:
            res = "All harvesters updated"
        return self.metadata_harvester_admin(self,response=res)
                    
    def getHarvesterStats(self,REQUEST=None):
        """
        """
        return MetadataManager._v_multiPing.getStats()
    
    def checkHarvesterPing(self):
        """
        """        
        try:
            # search for all harvesters and check that all the urls are in the multi ping
            urls = []
            results = self.portal_catalog.searchResults(meta_type = "Harvester")        
            
            harvesters = [x.getObject() for x in results]        
            tmpUrls = {}
            for harvester in harvesters:
                url = harvester.getUrl()
                parts = urlparse.urlparse(url)
                if len(parts) > 2:
                    tmpUrls[parts[1]] = ""
            urls = tmpUrls.keys()            
                        
            # use current multi ping
            if len(urls) > len(MetadataManager._v_multiPing.getAddresses()): # need to add addresses
                for url in urls:
                    if url not in MetadataManager._v_multiPing.getAddresses():
                        MetadataManager._v_multiPing.addAddress(url)
                        
            if len(urls) < len(MetadataManager._v_multiPing.getAddresses()):
                MetadataManager._v_multiPing.stop() 
                MetadataManager._v_multiPing = None                                    
                MetadataManager._v_multiPing = MultiPinger(urls,25)
                    
        except:
            io = StringIO()
            traceback.print_exc(file=io)
            io.seek(0)            
            trace = io.read()
            print trace
        print "checkHarvesterPing"    
    
    def checkHarvest(self):
        """
        @summary: method that checks all custodians for harvesters and each harvester for harvest period
        """     
        items = self.objectItems()
        for item in items:            
            if item[1].meta_type == "Custodian": 
                custodian = item[1]
                hList = custodian.getHarvesters()
                for h in hList:
                    if h.mustUpdate():
                        h.harvest()
        print "Done with checkHarvest"
        
    def getAvailableMetadataStandards(self):
        """
        """
        standard = []
        items = self.objectItems()
        for item in items:            
            if item[1].meta_type == "Standard": 
                standard = item[1]
                standard.append(standard.title)
        return standard
        
    def linkDataSave(self, REQUEST = None):
        """
        """
        context = self.portal_catalog(UID=REQUEST.form['UID'])[0].getObject()
        if REQUEST.form.has_key('form.button.cancel'):
            context.plone_utils.addPortalMessage(_(u'Data Links Not Changed.'))
            REQUEST.RESPONSE.redirect(context.absolute_url()+'/view')
            return

        if REQUEST.form.has_key('relatedItem'):
            brains = self.portal_catalog(UID=REQUEST.form['relatedItem'])
        else:
            brains = []
        if brains:
            relatedItem = brains[0].getObject()
            data = [relatedItem] + [item for item in [x for x in context.getRelatedItems() if x] if item.portal_type in ['Document', 'Link', 'Layer', 'File', 'Folder', 'Image']]
            context.setRelatedItems(data)
            context.setOnlineURL(relatedItem.absolute_url())
            for item in data:
                item.reindexObject()
        else:
            context.setRelatedItems([])
            context.setOnlineURL('')
        context.reindexObject()
        context.plone_utils.addPortalMessage(_(u'Data Links Saved.'))

        print [x for x in context.getRelatedItems() if x]

        REQUEST.RESPONSE.redirect(context.absolute_url())

    def linkMetadataSave(self, REQUEST= None):
        """
        """
        context = self.portal_catalog(UID=REQUEST.form['UID'])[0].getObject()
        if REQUEST.form.has_key('form.button.cancel'):
            context.plone_utils.addPortalMessage(_(u'Metadata Links Not Changed.'))
            REQUEST.RESPONSE.redirect(context.absolute_url()+'/view')
            return
        
        items = [item for item in [x for x in context.getRelatedItems() if x] if item.meta_type != 'Metadata']
        standards = [standard for standard in REQUEST.form['standard'] if standard]

        for standard in standards:
            results = self.portal_catalog(portal_type="Metadata", UID=standard)[0].getObject()
            items += [results]
        stds = {'ISO19115':0, 'ISO19115p2':0, 'ISO19139':0, 'SANS1878':0, 'EML':0, 'DublinCore':0}
        print items
        context.setRelatedItems([x for x in items if x])
        
        for item in items:
            item.setOnlineURL(context.absolute_url())        
            item.reindexObject()
        
        context.reindexObject()
        context.plone_utils.addPortalMessage(_(u'Metadata Links Saved.'))
        
        REQUEST.RESPONSE.redirect(context.absolute_url()+'/view')
             
        
    def manage_afterAdd(self,item, container):
        """
        """ 
        metadataTypes = Global.config.getMetadataTypes() 
        if "ISO19115" in metadataTypes:
            self._setObject("ISO19115",Standard("ISO19115","ISO19115"))
            ISO19115 = getattr(self,"ISO19115")
            ISO19115.setXsd(ISO19115.getProductPath() + "/standards/iso19139/gmd/gmd.xsd") #/gmd/gmd.xsd
            ISO19115.setXsl(ISO19115.getProductPath() + "/standards/generic.xsl")
            ISO19115.setName("ISO19115");
            ISO19115.setType("ISO19115");
        
        if "ISO19115p2" in metadataTypes:
            self._setObject("ISO19115p2",Standard("ISO19115p2","ISO19115p2"))
            ISO19115p2 = getattr(self,"ISO19115p2")
            ISO19115p2.setXsd(ISO19115p2.getProductPath() + "/standards/iso19139/gmd/gmd.xsd")
            ISO19115p2.setXsl(ISO19115p2.getProductPath() + "/standards/generic.xsl")
            ISO19115p2.setName("ISO19115p2");
            ISO19115p2.setType("ISO19115p2");
        
        if "ISO19139" in metadataTypes:
            self._setObject("ISO19139",Standard("ISO19139","ISO19139"))
            ISO19139 = getattr(self,"ISO19139")
            ISO19139.setXsd(ISO19139.getProductPath() + "/standards/iso19139/gmd/gmd.xsd")
            ISO19139.setXsl(ISO19139.getProductPath() + "/standards/generic.xsl")
            ISO19139.setName("ISO19139");
            ISO19139.setType("ISO19139");
            
        if "SANS1878" in metadataTypes:
            self._setObject("SANS1878",Standard("SANS1878","SANS1878"))
            SANS1878 = getattr(self,"SANS1878")
            SANS1878.setXsd(SANS1878.getProductPath() + "/standards/iso19139/gmd/gmd.xsd")
            SANS1878.setXsl(SANS1878.getProductPath() + "/standards/generic.xsl")
            SANS1878.setName("SANS1878");
            SANS1878.setType("SANS1878");
            
        if "DublinCore" in metadataTypes:
            self._setObject("DublinCore",Standard("DublinCore","DublinCore"))
            Dublin_Core = getattr(self,"DublinCore")
            Dublin_Core.setXsd(Dublin_Core.getProductPath() + "/standards/dublin-core/no_container_qualifieddc.xsd")
            Dublin_Core.setXsl(Dublin_Core.getProductPath() + "/standards/generic.xsl")
            Dublin_Core.setName("DublinCore");
            Dublin_Core.setType("DublinCore");
        
        if "FGDC" in metadataTypes:
            self._setObject("FGDC",Standard("FGDC","FGDC"))
            FGDC = getattr(self,"FGDC")
            FGDC.setXsd(FGDC.getProductPath() + "/standards/fgdc-std/schema.xsd")
            FGDC.setXsl(FGDC.getProductPath() + "/standards/generic.xsl")
            FGDC.setName("FGDC");
            FGDC.setType("FGDC");        
        
        if "EML" in metadataTypes:
            self._setObject("EML",Standard("EML","EML"))
            EML = getattr(self,"EML")
            EML.setXsd(EML.getProductPath() + "/standards/eml/eml.xsd")
            EML.setXsl(EML.getProductPath() + "/standards/generic.xsl")
            EML.setName("EML");
            EML.setType("EML");     
            
    
    #=======================================================================================
    #=================================Dummy Methods for Community Search Dev================
    #=======================================================================================
    
    def searchForMetadata(self, formValues, typeFilter=None):
        """
        @summary: does a search for all
        @param formValues: the formValues received from the search interface post
        @return: returns a list of dictinaries with results or an empty list 
        """                    
        # get all metadata documents that match search values
        results = self.portal_catalog.searchResults(meta_type = "Metadata")
        obResults = [x.getObject() for x in results]
        
        allStandards = XPathConfig.getMergedStandards()
        
        # filter for a given metadata standard
        if typeFilter:
            obResults = [x for x in obResults if x.getMetadatatype().lower().strip() == typeFilter.strip().lower()]        
                
        for field in formValues.keys():
            if field == "common_Title":
                obResults = [x for x in obResults if x.mTitle.lower().find(formValues['common_Title'].lower()) != -1]
            if field == "common_Date":
                # XXX change this to not include time  but just the date
                parts = formValues['common_Date'].split("-")
                d = date(int(parts[0]), int(parts[1]), int(parts[2]))                
                obResults = [x for x in obResults if x.mDate == d]                
            if field == "common_Keywords":
                obResults = [x for x in obResults if x.mKeywords.lower().find(formValues['common_Keywords'].lower()) != -1]                
            if field == "common_Abstract":
                obResults = [x for x in obResults if x.mAbstract.lower().find(formValues['common_Abstract'].lower()) != -1]
            if field == "common_Organization":
                obResults = [x for x in obResults if x.mOrganization.lower().find(formValues['common_Organization'].lower()) != -1]
            if field == "common_Language":
                obResults = [x for x in obResults if x.mLanguage.lower().find(formValues['common_Language'].lower()) != -1]
            if field == "common_Bounds":
                maxy = formValues["common_Bounds_North"]
                miny = formValues["common_Bounds_South"]
                maxx = formValues["common_Bounds_East"]
                minx = formValues["common_Bounds_West"]
                # check for intersect with metadata bounds
                # checkExtent(self, metaExtent, checkExtent, "Intersects"):
                obResults = [x for x in obResults if x.mBounds] # filter out all metadata without bounds                
                obResults = [x for x in obResults if self.checkExtent(x.mBounds, [minx,miny,maxx,maxy], "Intersects")] 
            
            # handle the standards, except common fields
            if not field in XPathConfig.COMMON.keys():
                # its a standard field
                fieldValue = formValues[field]
                xpathString = allStandards[field]                
                # use xpath from config to search for field                
                obResults = [x for x in obResults if str(x.getFirstExpressionResult(xpathString, minidom.parseString(x.xml))).lower().find(fieldValue.lower()) != -1] 
                        
        return obResults
    
    def getDataForMetadata(self, metadataDocuments):
        """
        @summary: gets all the data that has references to the given metadata documents
        @param metadataDocuments: list of metadata documents
        """             
        tmpDict = {} # e.g {"EML":[doc1,doc2,doc3], "DublinCore":[doc1,doc3]} ...
                
        for meta in metadataDocuments:            
            if tmpDict.has_key(meta.getMetadatatype()):                
                tmpDict[meta.getMetadatatype()].add([x for x in meta.getRelatedItems() if x])
            else:
                tmpDict[meta.getMetadatatype()] = set([x for x in meta.getRelatedItems() if x])
                
        # get a list off all sets
        setList = tmpDict.values();
        if len(setList) == 0:
            return []
        
        resSet = setList.pop(0)
        for sSet in setList:
            resSet = resSet.intersection(sSet)
        return list(resSet)
        
    def getComminutySearchDict(self, formValues):
        """
        """     
        all = XPathConfig.getMergedStandards()   
        searchDict = {}
        for field in formValues.keys():            
            if formValues[field].lower().strip() != "" and field in all.keys():
                if field.find("common_Bounds") != -1:
                    searchDict["common_Bounds_North"] = formValues["common_Bounds_North"]
                    searchDict["common_Bounds_South"] = formValues["common_Bounds_South"]
                    searchDict["common_Bounds_East"] = formValues["common_Bounds_East"]
                    searchDict["common_Bounds_West"] = formValues["common_Bounds_West"]
                searchDict[field] = formValues[field] 
                
        return searchDict
    
    def isValidDate(self,stringDate):
        """
        @summary: must be yyyy-mm-dd
        @return: boolean
        """
        if len(stringDate) != 10:
            return False
        parts = stringDate.split("-")
        if len(parts) != 3:
            return False        
        try:
            d = date(int(parts[0]), int(parts[1]), int(parts[2]))
            return True
        except:
            return False
    
    def validateFormValues(self, formValues):
        """
        @summary: does the validation of the passed form values from the search post
        @param formValues: the formValues received from the search interface post
        @return: an error list with dictionaries with descriptions or an empty list if there are no errors 
        """
        errorList = []
        searchDict = self.getComminutySearchDict(formValues)        
        # check all the common fields in the searchDict
        for field in searchDict.keys():
            if field.find("common_Bounds") != -1:   
                if field == "common_Bounds_North":
                    if not searchDict["common_Bounds_North"].replace("-","").replace(".","").isdigit():
                        errorList.append({"North value incorrect": ""})
                if field == "common_Bounds_South": 
                    if not searchDict["common_Bounds_South"].replace("-","").replace(".","").isdigit():
                        errorList.append({"South value incorrect": ""})
                if field == "common_Bounds_East":
                    if not searchDict["common_Bounds_East"].replace("-","").replace(".","").isdigit():
                        errorList.append({"East value incorrect": ""})
                if field == "common_Bounds_West":
                    if not searchDict["common_Bounds_West"].replace("-","").replace(".","").isdigit():
                        errorList.append({"West value incorrect": ""})
                if not errorList and searchDict.has_key("common_Bounds_North") and searchDict.has_key("common_Bounds_South") and searchDict.has_key("common_Bounds_East") and searchDict.has_key("common_Bounds_North"):
                    north = float(searchDict["common_Bounds_North"])
                    south = float(searchDict["common_Bounds_South"])
                    east = float(searchDict["common_Bounds_East"])
                    west = float(searchDict["common_Bounds_West"])
                    if north < south or west > east:
                        errorList.append({"Bounds values are incorrect": ""})                    
            if field == "common_Date":
                if not self.isValidDate(searchDict["common_Date"]):
                    errorList.append({"Common Date field is not valid": ""})
        return errorList
    
    def getCommunitySearchResults(self, results, REQUEST=None):
        """
        @summary: returns the search results page for community data and metadata
        """
        return self.view_community_search_results(self, data=results);        
     
    def getCommunityMetadataSearchView(self,REQUEST=None):
        """
        @summary: returns the interface for community metadata search
        """
        return self.view_community_metadata_search(self,data=self.getDummyValue(), standards=self.getDummyStandards())
        
     
    def getCommunityDataSearchView(self,REQUEST=None):
        """
        @summary: returns the interface for community data search
        """        
        return self.view_community_data_search(self,data=self.getDummyValue(), standards=self.getDummyStandards())    
    
    def getSummaryPartForId(self, metadataId):
        """
        """
        results = self.portal_catalog.searchResults(id = metadataId)#, meta_type = "Metadata")
        obj = results[0].getObject()
        #return obj.getSummaryHTML()
        return obj.metadata_search_summary()
    
    def getSummaryPartForUid(self, data):
        """
        """
        #results = self.portal_catalog.searchResults(uid = uid)#, meta_type = "Metadata")
        #obj = results[0].getObject()
        #return obj.getSummaryHTML()
        return obj.metadata_search_summary_results(data = data)
    
    
    def getModalSummaryPartForId(self, uid, fieldName, recordType):
        """
        """        
        results = self.portal_catalog.searchResults(UID = uid)
        obj = results[0].getObject()
        return obj.getModalSummaryHTML(fieldName, recordType)    

    def getPageList(self,numberOfRecords):
        """
        @summary: generate page breaks for results navigation
        """
        partSize = Global.config.getResultsPerPage()
        partList = []
        res = numberOfRecords/partSize
        
        last = 0
        if partSize >= numberOfRecords:
            return []
        if numberOfRecords == 0:
            return []    
        for x in range(1,res+2):
            if len(partList) == 0:
                t = [1,partSize]
                last = partSize + 1           
            else:
                if last + partSize > numberOfRecords:
                    t = [last, numberOfRecords]
                else:
                    t = [last, last+partSize]
                last = last+partSize                    
            partList.append(t)    
        print partList
        return partList
    
    def showZipFile(self, object):
        """
        """
        metadata_tool = getToolByName(self, "metadata_tool")
        
        if object.portal_type in ['MetadataCollection', 'MetadataContainer']:
            print 1
            return metadata_tool.absolute_url() + '/zipMetadata?id=' + object.absolute_url(1)
        elif object.portal_type in ['Topic']:
            if 'crit__Type_ATPortalTypeCriterion' in object.objectIds():
                if object.crit__Type_ATPortalTypeCriterion.getRawValue() == ('Metadata', 'MetadataContainer'):
                    print '/'.join(object.absolute_url(1).split('/')[:-1])
                    return metadata_tool.absolute_url() + '/zipMetadata?id=' + '/'.join(object.absolute_url(1).split('/')[:-1])
                else:
                    return False
            else:
                return False
        else:
            return False
            

registerType(MetadataManager, PROJECTNAME)
# end of class MetadataManager

##code-section module-footer #fill in your manual code here
##/code-section module-footer



