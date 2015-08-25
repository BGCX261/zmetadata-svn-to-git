# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
##/code-section HEAD

class ICommunities(Interface):
    """Marker interface for .communities.Communities
    """

class ICommunity(Interface):
    """Marker interface for .community.Community
    """

class IContent(Interface):
    """Marker interface for .community.Community
    """

class IOntology(Interface):
    """Marker interface for .ontology.Ontology
    """

class ISTDSetup(Interface):
    """Marker interface for .setup.STDSetup
    """

class ICommonFields(Interface):
    """Marker interface for .commonfields.CommonFields
    """

class ICSIRUser(Interface):
    """Marker interface for .csiruser.CSIRUser
    """

class IStandardSetups(Interface):
    """Marker interface for .standardsetups.StandardSetups
    """

class ICommunityTool(Interface):
    """Marker interface for .CommunityTool.CommunityTool
    """

class IOntologies(Interface):
    """Marker interface for .ontologies.Ontologies
    """

class ISANSSetup(Interface):
    """Marker interface for .sanssetup.SANSSetup
    """

class ISANSFields(Interface):
    """Marker interface for .sansfields.SANSFields
    """

class ICommonSetup(Interface):
    """Marker interface for .commonsetup.CommonSetup
    """

class IFields(Interface):
    """Marker interface for .fields.Fields
    """

class IISO19139Fields(Interface):
    """Marker interface for .iso19139fields.ISO19139Fields
    """

class IISO19139Setup(Interface):
    """Marker interface for .iso19139.ISO19139Setup
    """

class IISO19115Setup(Interface):
    """Marker interface for .iso19115.ISO19115Setup
    """

class IISO19115Fields(Interface):
    """Marker interface for .iso19115Fields.ISO19115Fields
    """

class IEMLSetup(Interface):
    """Marker interface for .eml.EMLSetup
    """

class IEMLFields(Interface):
    """Marker interface for .emlfields.EMLFields
    """

class IDCSetup(Interface):
    """Marker interface for .dc.DCSetup
    """

class IDCFields(Interface):
    """Marker interface for .dcfields.DCFields
    """

class ICommunitySearch(Interface):
    """Marker interface for .communitysearch.CommunitySearch
    """

class IMetadataCollection(Interface):
    """Marker interface for .MetadataCollection.MetadataCollection
    """

class IMetadataContainer(Interface):
    """Marker interface for .MetadataContainer.MetadataContainer
    """

##code-section FOOT
##/code-section FOOT
