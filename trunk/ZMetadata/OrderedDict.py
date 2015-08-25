from UserDict import UserDict

class OrderedDict(UserDict):
    def __init__(self, dict = None):
        self._keys = []
        UserDict.__init__(self, dict)

    def __delitem__(self, key):
        UserDict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        UserDict.__setitem__(self, key, item)
        if key not in self._keys: self._keys.append(key)

    def clear(self):
        UserDict.clear(self)
        self._keys = []

    def copy(self):
        dict = UserDict.copy(self)
        dict._keys = self._keys[:]
        return dict

    def items(self):
        return zip(self._keys, self.values())

    def keys(self):
        return self._keys

    def popitem(self):
        try:
            key = self._keys[-1]
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)

    def setdefault(self, key, failobj = None):
        UserDict.setdefault(self, key, failobj)
        if key not in self._keys: self._keys.append(key)

    def update(self, dict):
        UserDict.update(self, dict)
        for key in dict.keys():
            if key not in self._keys: self._keys.append(key)

    def values(self):
        return map(self.get, self._keys)
    
if __name__ == "__main__":
    print "start"
    
    EML = OrderedDict(
    {"eml_Title" : "//dataset[1]/title[1]/text()",
           "eml_DataOwnerSalutation" : "//dataset[1]/creator[1]/individualName[1]/salutation[1]/text()",
           "eml_DataOwnerGivenName" : "//dataset[1]/creator[1]/individualName[1]/givenName[1]/text()",
           "eml_DataOwnerSurname" : "//dataset[1]/creator[1]/individualName[1]/surName[1]/text()",
           "eml_DataOwnerOrganization" : "//dataset[1]/creator[1]/organizationName[1]/text()",
           "eml_Abstract" : "//dataset[1]/abstract[1]/para[1]/text()",
           "eml_Keywords" : "//dataset[1]/keywordSet[1]/keyword[1]/text()",
           "eml_WestBoundingCoordinate" : "//dataset[1]/coverage[1]/geographicCoverage[1]/boundingCoordinates[1]/westBoundingCoordinate[1]/text()",
           "eml_EastBoundingCoordinate" : "//dataset[1]/coverage[1]/geographicCoverage[1]/boundingCoordinates[1]/eastBoundingCoordinate[1]/text()",
           "eml_NorthBoundingCoordinate" : "//dataset[1]/coverage[1]/geographicCoverage[1]/boundingCoordinates[1]/northBoundingCoordinate[1]/text()",
           "eml_SouthBoundingCoordinate" : "//dataset[1]/coverage[1]/geographicCoverage[1]/boundingCoordinates[1]/southBoundingCoordinate[1]/text()",
           "eml_TemporalCoverageBeginDate" : "//dataset[1]/coverage[1]/temporalCoverage[1]/rangeOfDates[1]/beginDate[1]/calendarDate[1]/text()",
           "eml_TemporalCoverageEndDate" : "//dataset[1]/coverage[1]/temporalCoverage[1]/rangeOfDates[1]/endDate[1]/calendarDate[1]/text()",
           "eml_TaxonomicCoverageRankName" : "//dataset[1]/coverage[1]/taxonomicCoverage[1]/taxonomicClassification[1]/taxonRankName[1]/text()",
           "eml_TaxonomicCoverageRankValue" : "//dataset[1]/coverage[1]/taxonomicCoverage[1]/taxonomicClassification[1]/taxonRankValue[1]/text()",
           "eml_ContactSalutation" : "//dataset[1]/contact[1]/individualName[1]/salutation[1]/text()",
           "eml_ContactGivenName" : "//dataset[1]/contact[1]/individualName[1]/givenName[1]/text()",
           "eml_ContactSurname" : "//dataset[1]/contact[1]/individualName[1]/surName[1]/text()",
           "eml_ContactOrganizationName" : "//dataset[1]/contact[1]/organizationName[1]/text() "              
           }
    )
    
    print EML.keys()
    
    
