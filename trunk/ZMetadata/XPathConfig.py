from OrderedDict import OrderedDict
# config file for all standards xpaths

def getMergedStandards():
    """
    @summary: returns a dictionary containing all listed standards
    """
    all = OrderedDict()
    all.update(SANS1878)
    all.update(EML)
    all.update(DublinCore)
    all.update(ISO19115)
    all.update(ISO19115p2)
    all.update(ISO19139)
    all.update(SANS1878)
    all.update(COMMON)
    return all

STANDARDS_LOOKUP = {'iso19115': 'ISO19115', 'iso19115p2': 'ISO19115p2' ,
                    'dc': 'DublinCore', 'dublincore' : 'DublinCore',
                   'iso19139': 'ISO19139', 'eml': 'EML',
                   'sans1878': 'SANS1878', 'common': 'COMMON'}

STANDARD_TO_XPATH = {"ISO19115":"iso19115", "DublinCore":"dc",
                               "ISO19139":"iso19139", "SANS1878":"sans1878",
                                "EML":"eml", "COMMON":"common", "ISO19115p2":"iso19115p2"}

SANS1878 = OrderedDict()
SANS1878["sans1878_DatasetTitle"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString/text()"
SANS1878["sans1878_DatasetReferenceDate"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:DateTime/text()"
SANS1878["sans1878_DatasetResponsibleParty"] = "//gmd:contact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString/text()"
SANS1878["sans1878_DatasetResponsiblePartyOrganization"] = "//gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString/text()"
SANS1878["sans1878_DatasetResponsiblePartyPosition"] = "//gmd:contact/gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString/text()"         
SANS1878["sans1878_DatasetLanguage"] = "//gmd:language/gco:CharacterString/text()" 
SANS1878["sans1878_DatasetCharacterSet"] = "//gmd:characterSet/gmd:MD_CharacterSetCode/@codeListValue" 
SANS1878["sans1878_DatasetTopicCategory"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory/gmd:MD_TopicCategoryCode/text()"
SANS1878["sans1878_DatasetScale"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer/text()" 
SANS1878["sans1878_DatasetAbstract"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString/text()" 
SANS1878["sans1878_DatasetFormatName"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceFormat/gmd:MD_Format/gmd:name/gco:CharacterString/text()" 
SANS1878["sans1878_DatasetFormatVersion"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceFormat/gmd:MD_Format/gmd:version/gco:CharacterString/text()"
        
SANS1878["sans1878_SpatialWest"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal/text()" 
SANS1878["sans1878_SpatialSouth"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal/text()" 
SANS1878["sans1878_SpatialEast"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal/text()" 
SANS1878["sans1878_SpatialNorth"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal/text()" 
SANS1878["sans1878_SpatialBeginDate"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:beginPosition/text()" 
SANS1878["sans1878_SpatialEndDate"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:endPosition/text()" 
SANS1878["sans1878_SpatialVerticalExtentMinimum"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:minimumValue/gco:Real/text()" 
SANS1878["sans1878_SpatialMaximum"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:maximumValue/gco:Real/text()" 
SANS1878["sans1878_SpatialVerticalExtentUnits"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:verticalCRS/gml:VerticalCRS/gml:verticalCS/gml:VerticalCS/gml:axis/gml:CoordinateSystemAxis/@gml:uom" 
SANS1878["sans1878_SpatialVerticalExtentDatum"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:verticalCRS/gml:VerticalCRS/gml:verticalDatum/gml:VerticalDatum/gml:identifier/text()" 
SANS1878["sans1878_SpatialRepresentation"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode/@codeListValue" 
SANS1878["sans1878_SpatialReferenceSystem"] = "//gmd:referenceSystemInfo/gmd:MD_ReferenceSystem /gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString/text()" 
SANS1878["sans1878_SpatialLinageStatement"] = "//gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement/gco:CharacterString/text()" 
SANS1878["sans1878_SpatialOnlineResourceURL"] = "//gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:linkage/gmd:URL/text()" 
SANS1878["sans1878_SpatialOnlineResourceProtocol"] = "//gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString/text()" 
SANS1878["sans1878_SpatialOnlineResourceName"] = "//gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:name/gco:CharacterString/text()" 
SANS1878["sans1878_SpatialOnlineResourceDescription"] = "//gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:description/gco:CharacterString/text()"
        
SANS1878["sans1878_MetadataFileIdentifier"] = "//gmd:fileIdentifier/gco:CharacterString/text()"
SANS1878["sans1878_MetadataStandardName"] = "//gmd:metadataStandardName/gco:CharacterString/text()" 
SANS1878["sans1878_MetadataStandardVersion"] = "//gmd:metadataStandardVersion/gco:CharacterString/text()" 
SANS1878["sans1878_MetadataLanguage"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language/gco:CharacterString/text()" 
SANS1878["sans1878_MetadataCharacterSet"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:characterSet/gmd:MD_CharacterSetCode/@codeListValue" 
SANS1878["sans1878_MetadataTimeStamp"] = "//gmd:dateStamp/gco:DateTime/text()" 
SANS1878["sans1878_MetadataPointOfContactIndividualName"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString/text()" 
SANS1878["sans1878_MetadataPointOfContactOrganizationName"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString/text()" 
SANS1878["sans1878_MetadataPointOfContactPositionName"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString/text()" 
SANS1878["sans1878_MetadataPointOfContactRole"] = "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode/@codeListValue"


ISO19115 = OrderedDict()
ISO19115p2 = OrderedDict() 
ISO19139 = OrderedDict()

# generate iso xpath dicts from sans dict
for k in SANS1878.keys():
    ISO19115[k.replace("sans1878_","iso19115_")] = SANS1878[k]
    ISO19115p2[k.replace("sans1878_","iso19115p2_")] = SANS1878[k]
    ISO19139[k.replace("sans1878_","iso19139_")] = SANS1878[k]

EML = OrderedDict()
EML["eml_Title"] = "//dataset[1]/title[1]/text()"
EML["eml_DataOwnerSalutation"] = "//dataset[1]/creator[1]/individualName[1]/salutation[1]/text()"
EML["eml_DataOwnerGivenName"] = "//dataset[1]/creator[1]/individualName[1]/givenName[1]/text()"
EML["eml_DataOwnerSurname"] = "//dataset[1]/creator[1]/individualName[1]/surName[1]/text()"
EML["eml_DataOwnerOrganization"] = "//dataset[1]/creator[1]/organizationName[1]/text()"
EML["eml_Abstract"] = "//dataset[1]/abstract[1]/para[1]/text()"
EML["eml_Keywords"] = "//dataset[1]/keywordSet[1]/keyword[1]/text()"
EML["eml_WestBoundingCoordinate"] = "//dataset[1]/coverage[1]/geographicCoverage[1]/boundingCoordinates[1]/westBoundingCoordinate[1]/text()"
EML["eml_EastBoundingCoordinate"] = "//dataset[1]/coverage[1]/geographicCoverage[1]/boundingCoordinates[1]/eastBoundingCoordinate[1]/text()"
EML["eml_NorthBoundingCoordinate"] = "//dataset[1]/coverage[1]/geographicCoverage[1]/boundingCoordinates[1]/northBoundingCoordinate[1]/text()"
EML["eml_SouthBoundingCoordinate"] = "//dataset[1]/coverage[1]/geographicCoverage[1]/boundingCoordinates[1]/southBoundingCoordinate[1]/text()"
EML["eml_TemporalCoverageBeginDate"] = "//dataset[1]/coverage[1]/temporalCoverage[1]/rangeOfDates[1]/beginDate[1]/calendarDate[1]/text()"
EML["eml_TemporalCoverageEndDate"] = "//dataset[1]/coverage[1]/temporalCoverage[1]/rangeOfDates[1]/endDate[1]/calendarDate[1]/text()"
EML["eml_TaxonomicCoverageRankName"] = "//dataset[1]/coverage[1]/taxonomicCoverage[1]/taxonomicClassification[1]/taxonRankName[1]/text()"
EML["eml_TaxonomicCoverageRankValue"] = "//dataset[1]/coverage[1]/taxonomicCoverage[1]/taxonomicClassification[1]/taxonRankValue[1]/text()"
EML["eml_ContactSalutation"] = "//dataset[1]/contact[1]/individualName[1]/salutation[1]/text()"
EML["eml_ContactGivenName"] = "//dataset[1]/contact[1]/individualName[1]/givenName[1]/text()"
EML["eml_ContactSurname"] = "//dataset[1]/contact[1]/individualName[1]/surName[1]/text()"
EML["eml_ContactOrganizationName"] = "//dataset[1]/contact[1]/organizationName[1]/text()"              

DublinCore = OrderedDict()
DublinCore["dc_Title"] = "//dc:title[1]/text()"
DublinCore["dc_Creator"] = "//dc:creator/text()"
DublinCore["dc_Subject"] = "//dc:subject/text()"
DublinCore["dc_Description"] = "//dc:description/text()"
DublinCore["dc_Publisher"] = "//dc:publisher/text()"
DublinCore["dc_Contributor"] = "//dc:contributor/text()"
DublinCore["dc_Date"] = "//dc:date/text()"
DublinCore["dc_Type"] = "//dc:type/text()"
DublinCore["dc_Format"] = "//dc:format/text()"
DublinCore["dc_Identifier"] = "//dc:identifier/text()"
DublinCore["dc_Source"] = "//dc:source/text()"
DublinCore["dc_Language"] = "//dc:language/text()"
DublinCore["dc_Relation"] = "//dc:relation/text()"
DublinCore["dc_Coverage"] = "//dc:coverage/text()"
DublinCore["dc_Rights"] = "//dc:rights/text()"


COMMON = OrderedDict()
COMMON["common_Title"] = ""
COMMON["common_Date"] = ""
COMMON["common_Keywords"] = ""
COMMON["common_Abstract"] = ""
COMMON["common_Organization"] = ""
COMMON["common_Language"] = ""
COMMON["common_Bounds"] = ""
COMMON["common_Bounds_North"] = ""
COMMON["common_Bounds_South"] = ""
COMMON["common_Bounds_East"] = ""
COMMON["common_Bounds_West"] = ""    





