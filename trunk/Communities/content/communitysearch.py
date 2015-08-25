# -*- coding: utf-8 -*-
#
# File: communitysearch.py
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
from Products.Communities.content.standardsetups import StandardSetups
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.Communities.config import *

# additional imports from tagged value 'import'
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.ZMetadata import XPathConfig

##code-section module-header #fill in your manual code here
from xml.dom import minidom
import urllib
import traceback
import sys
import time
from Products.ZMetadata import Global
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CommunitySearch_schema = ATFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class CommunitySearch(ATFolder):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ICommunitySearch)

    meta_type = 'CommunitySearch'
    _at_rename_after_creation = True

    schema = CommunitySearch_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('_renameAfterCreation')
    def _renameAfterCreation(self, check_auto_id=True):
        """
        """
        self._setObject("setup", StandardSetups("setup"))
        self["setup"].setTitle("Search Setup")
        self['setup']._renameAfterCreation(check_auto_id)
        self["setup"].reindexObject()

    security.declarePublic('handleSearchForDataPost')
    def handleSearchForDataPost(self, REQUEST=None):
        """
        """
        errorList = [] # this is a list that will show the user any errors in the input
        hasFields = False

        searchDict = self.getComminutySearchDict(REQUEST.form)
        searchedStandards = []

        if searchDict.keys():
            hasFields = True

        for key in REQUEST.form.keys():
            if key.find("chb_Standard_") != -1:
                standard = key.replace("chb_Standard_","").lower()
                searchedStandards.append(XPathConfig.STANDARDS_LOOKUP[standard])

        if not searchedStandards:
            desc = {}
            desc["No standards selected for searching"] = ""
            errorList.append(desc)

        if hasFields:
            errors = self.validateFormValues(REQUEST.form);
            if errors:
                return self.view_community_data_search(self,data=self.assembleDisplayFields(), standards=self.getMyStandards(), errors=errors)
        if not hasFields:
            desc = {}
            desc["No fields selected for search"] = ""
            errorList.append(desc)
        if errorList:
            return self.view_community_data_search(self,data=self.assembleDisplayFields(), standards=self.getMyStandards(), errors=errorList)
        else:
            if REQUEST.form.has_key("cbxSpatialType"):
                spatialType = REQUEST.form["cbxSpatialType"]
            else:
                spatialType = "Intersects"

            searchDict = self.getComminutySearchDict(REQUEST.form)
            results = self.searchForMetadata(searchDict, spatialOperation=spatialType)

            res = self.getDataForMetadata(results, searchedStandards)
            saveString = '?'
            for key in REQUEST.form.keys():
                value = urllib.quote(str(REQUEST.form[key]))                
                saveString += ('%s=%s&' % (key, value))
            return self.getCommunitySearchResults(res, saveString)
        return self.view_community_data_search(self,data=self.assembleDisplayFields(), standards=self.getMyStandards())

    security.declarePublic('getComminutySearchDict')
    def getComminutySearchDict(self, formValues):
        """
        """
        all = XPathConfig.getMergedStandards()
        searchDict = {}
        for field in formValues.keys():
            try:
                if (str(formValues[field]).lower().strip() != "" and field in all.keys()):
                    if field.find("common_Bounds") != -1:
                        searchDict["common_Bounds_North"] = formValues["common_Bounds_North"]
                        searchDict["common_Bounds_South"] = formValues["common_Bounds_South"]
                        searchDict["common_Bounds_East"] = formValues["common_Bounds_East"]
                        searchDict["common_Bounds_West"] = formValues["common_Bounds_West"]
                    searchDict[field] = formValues[field]
            except:
                traceback.print_exc(file=sys.stdout)
                print "ERROR"

        return searchDict

    security.declarePublic('validateFormValues')
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
    
    

    security.declarePublic('searchForMetadata')
    def searchForMetadata(self, formValues, typeFilter=[], spatialOperation="Intersects"):
        """
        @summary: does a search for all
        @param formValues: the formValues received from the search interface post
        @return: returns a list of dictinaries with results or an empty list
        """
        # get all metadata documents that match search values
        results = self.portal_catalog.searchResults(meta_type = "Metadata")
        max = Global.config.getMaxSearchResults()        
        results = results[0:max]        
        obResults = []
        for x in results:
            try:
                obResults += [x.getObject()]
            except Exception, e:
                print e
        allStandards = XPathConfig.getMergedStandards()
        
        print 'obResults', len(obResults)
            
        # filter for a given metadata standard
        if typeFilter:
            obResults = [x for x in obResults if x.getMetadatatype().strip() in typeFilter]
        
        print 'obResults2', len(obResults)
        for field in formValues.keys():
            if field == "common_Title":
                obResults = [x for x in obResults if x.mTitle.lower().find(formValues['common_Title'].lower()) != -1]
            elif field == "common_Date":
                # XXX change this to not include time  but just the date
                parts = formValues['common_Date'].split("-")
                d = date(int(parts[0]), int(parts[1]), int(parts[2]))
                obResults = [x for x in obResults if x.mDate == d]
            elif field == "common_Keywords":                
                if type(formValues['common_Keywords']) == list:                    
                    for keyword in formValues['common_Keywords']:
                        obResults = [x for x in obResults if x.mKeywords.lower().find(keyword.lower()) != -1]                    
                if type(formValues['common_Keywords']) == str:
                    obResults = [x for x in obResults if x.mKeywords.lower().find(formValues['common_Keywords'].lower()) != -1]                
                
            elif field == "common_Abstract":
                obResults = [x for x in obResults if x.mAbstract.lower().find(formValues['common_Abstract'].lower()) != -1]
            elif field == "common_Organization":
                obResults = [x for x in obResults if x.mOrganization.lower().find(formValues['common_Organization'].lower()) != -1]
            elif field == "common_Language":
                obResults = [x for x in obResults if x.mLanguage.lower().find(formValues['common_Language'].lower()) != -1]
            elif field == "common_Bounds":
                maxy = formValues["common_Bounds_North"]
                miny = formValues["common_Bounds_South"]
                maxx = formValues["common_Bounds_East"]
                minx = formValues["common_Bounds_West"]
                # check for intersect with metadata bounds
                # checkExtent(self, metaExtent, checkExtent, "Intersects"):
                obResults = [x for x in obResults if x.mBounds] # filter out all metadata without bounds
                obResults = [x for x in obResults if self.checkExtent(x.mBounds, [minx,miny,maxx,maxy], spatialOperation)]

            # handle the standards, except common fields
            if not field in XPathConfig.COMMON.keys():
                # its a standard field
                fieldValue = formValues[field]
                xpathString = allStandards[field]
                # use xpath from config to search for field
                results = obResults
                obResults = []
                
                for x in results:
                    try:
                        if str(x.getFirstExpressionResult(xpathString, minidom.parseString(x.xml))).lower().find(fieldValue.lower()) != -1:
                            obResults += [x]
                    except Exception, e:
                        print e
        
        return obResults

    security.declarePublic('getDataForMetadata')
    def getDataForMetadata(self, metadataDocuments, searchedStandards = []):
        """
        @summary: gets all the data that has references to the given metadata documents
        @param metadataDocuments: list of metadata documents
        """
        tmpDict = {} # e.g {"EML":[doc1,doc2,doc3], "DublinCore":[doc1,doc3]} ...

        for meta in metadataDocuments:
            if (meta.getMetadatatype() in searchedStandards) and meta.getRelatedItems():
                for relatedItem in meta.getRelatedItems():
                    pass
                if tmpDict.has_key(meta.getMetadatatype()):
                    for relatedItem in meta.getRelatedItems():
                        tmpDict[meta.getMetadatatype()].add(relatedItem)
                else:
                    if meta.getRelatedItems():
                        tmpDict[meta.getMetadatatype()] = set(meta.getRelatedItems())

        # get a list off all sets
        setList = tmpDict.values();
        if len(setList) == 0:
            return []

        resSet = setList.pop(0) #??
        for sSet in setList:            
            resSet = resSet.intersection(sSet)        
        return list(resSet)

    security.declarePublic('getCommunitySearchResults')
    def getCommunitySearchResults(self, results, saveString, REQUEST=None):
        """
        @summary: returns the search results page for community data and metadata
        """
        return self.view_community_search_results(self, data=results, saveString=saveString);

    security.declarePublic('isValidDate')
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

    security.declarePublic('getMyStandards')
    def getMyStandards(self):
        """
        """
        interfaceTool = getToolByName(self, 'portal_interface')

        standards = []
        for standard in self['setup'].getShowStandards():
            if standard != 'COMMON':
                standards += [standard]
        return standards

    security.declarePublic('assembleDisplayFields')
    def assembleDisplayFields(self):
        """
        """
        result = {}
        standards = self['setup'].getShowStandards()
        for standard in standards:
            result[standard] = []
            fields = self['setup'][standard].getShowFields()
            for field in fields:
                result[standard] += [self['setup'][standard]['fields'].getFieldInfo(field)]
        return result

    # Manually created methods

    def getCommunityDataSearchView(self, REQUEST=None):
        """
        @summary: returns the interface for community data search
        """
        return self.view_community_data_search(self,data=self.assembleDisplayFields(), standards=self.getMyStandards())

    def getCommunityMetadataSearchView(self, REQUEST=None):
        """
        @summary: returns the interface for community metadata search
        """
        return self.view_community_metadata_search(self,data=self.assembleDisplayFields(), standards=self.getMyStandards())

    def handleSearchForMetadataPost(self, REQUEST=None):
        """
        """
        errorList = [] # this is a list that will show the user any errors in the input

        searchDict = self.getComminutySearchDict(REQUEST.form)

        if searchDict.keys():
            hasFields = True
        else:
            hasFields = False

        if hasFields:
            errors = self.validateFormValues(REQUEST.form);
            if errors:
                return self.view_community_metadata_search(self,data=self.assembleDisplayFields(), standards=self.getMyStandards(), errors=errors)
        else:
            desc = {}
            desc["No fields selected for search"] = ""
            errorList.append(desc)
        if errorList:
            return self.view_community_metadata_search(self,data=self.assembleDisplayFields(), standards=self.getMyStandards(), errors=errorList)
        else:
            if REQUEST.form.has_key("cbxSpatialType"):
                spatialType = REQUEST.form["cbxSpatialType"]
            else:
                spatialType = "Intersects"

            typeFilter = REQUEST.form["metadataRadios"]
            if typeFilter == "All":
                results = self.searchForMetadata(searchDict, spatialOperation=spatialType)
            else:
                results = self.searchForMetadata(searchDict, typeFilter=[typeFilter], spatialOperation=spatialType)
            
            print 'results:', len(results)
            
            s = REQUEST.SESSION                        
            #stringResults = [x.getSummaryHTML() for x in results]            
            resultIds = [x.getId() for x in results]            
            s["resultIds"] = resultIds
            
            print 's["resultIds"]', s["resultIds"]            
            #s["searchResults"] = stringResults
            saveString = '?'
            for key in REQUEST.form.keys():
                value = urllib.quote(str(REQUEST.form[key]))
                saveString += ('%s=%s&' % (key, value))
            s["data"] = saveString
            REQUEST.RESPONSE.redirect(self.absolute_url() + "/search_result_display?data=" + urllib.quote(saveString))
        return self.view_community_metadata_search(self,data=self.assembleDisplayFields(), standards=self.getMyStandards(), searchDict=searchDict)



registerType(CommunitySearch, PROJECTNAME)
# end of class CommunitySearch

##code-section module-footer #fill in your manual code here
##/code-section module-footer



