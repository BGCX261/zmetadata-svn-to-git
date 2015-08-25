# -*- coding: utf-8 -*-
#
# File: CommunityTool.py
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Communities.config import *

# additional imports from tagged value 'import'
from Products.CMFPlone.interfaces import IInterfaceTool
from Products.CMFPlone.interfaces.InterfaceTool import IInterfaceTool as z2IInterfaceTool
from types import ModuleType, ListType, TupleType
from Acquisition import aq_base
from Products.CMFCore.utils import registerToolInterface
from Products.CMFCore.utils import UniqueObject
from OFS.SimpleItem import SimpleItem
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CMFPlone.PloneBaseTool import PloneBaseTool
from Interface.Implements import getImplements, flattenInterfaces
from zope.interface import Interface
from Interface.IMethod import IMethod
from zope.interface import implements
from Products.CMFPlone import PloneMessageFactory as _
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget


from Products.CMFCore.utils import UniqueObject

    
##code-section module-header #fill in your manual code here
_marker = ('module_finder',)
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='defaultCommunity',
        widget=ReferenceBrowserWidget(
            label='Defaultcommunity',
            label_msgid='Communities_label_defaultCommunity',
            i18n_domain='Communities',
        ),
        allowed_types="('Community',)",
        relationship="default_community",
        multiValued=False,
        searchable=1,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CommunityTool_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class CommunityTool(UniqueObject, BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ICommunityTool)

    meta_type = 'CommunityTool'
    _at_rename_after_creation = True

    schema = CommunityTool_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        BaseContent.__init__(self,'portal_communitytool')
        self.setTitle('')
        
        ##code-section constructor-footer #fill in your manual code here
        ##/code-section constructor-footer


    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()
        
        ##code-section post-edit-method-footer #fill in your manual code here
        ##/code-section post-edit-method-footer


    # Methods

    security.declarePublic('objectImplements')
    def objectImplements(self, obj, dotted_name):
        """ Asserts if an object implements a given interface """
        obj = aq_base(obj)
        iface = resolveInterface(dotted_name)
        return iface.isImplementedBy(obj)

    security.declarePublic('classImplements')
    def classImplements(self, obj, dotted_name):
        """ Asserts if an object's class implements a given interface """
        klass = aq_base(obj).__class__
        iface = resolveInterface(dotted_name)
        return iface.isImplementedBy(klass)

    security.declarePublic('namesAndDescriptions')
    def namesAndDescriptions(self, dotted_name, all=0):
        """ Returns a list of pairs (name, description) for a given
        interface"""
        iface = resolveInterface(dotted_name)
        nd = iface.namesAndDescriptions(all=all)
        return [(n, d.getDoc()) for n, d in nd]

    security.declarePublic('getInterfacesOf')
    def getInterfacesOf(self, object):
        """Returns the list of interfaces which are implemented by the object
        """
        impl = getImplements(object)
        if impl:
            if type(impl) in (ListType, TupleType):
                result = flattenInterfaces(impl)
            else:
                result = (impl, )
            return [ iface for iface in result if iface is not Interface ]

    security.declarePublic('getBaseInterfacesOf')
    def getBaseInterfacesOf(self, object):
        """Returns all base interfaces of an object but no direct interfaces

        Base interfaces are the interfaces which are the super interfaces of the
        direct interfaces
        """
        ifaces = self.getInterfacesOf(object)
        bases = []
        for iface in ifaces:
            visitBaseInterfaces(iface, bases)
        return [biface for biface in bases if biface not in ifaces ]

    security.declarePublic('getInterfaceInformations')
    def getInterfaceInformations(self, iface):
        """Gets all useful informations from an iface

        * name
        * dotted name
        * trimmed doc string
        * base interfaces
        * methods with signature and trimmed doc string
        * attributes with trimemd doc string
        """
        bases = [ base for base in iface.getBases() if base is not Interface ]

        attributes = []
        methods = []
        for name, desc in iface.namesAndDescriptions():
            if IMethod.isImplementedBy(desc):
                methods.append({'signature' : desc.getSignatureString(),
                                'name' : desc.getName(),
                                'doc' : _trim_doc_string(desc.getDoc()),
                               })
            else:
                attributes.append({'name' : desc.getName(),
                                   'doc' : _trim_doc_string(desc.getDoc()),
                                  })

        result = {
            'name' : iface.getName(),
            'dotted_name' : getDottedName(iface),
            'doc' : _trim_doc_string(desc.getDoc()),
            'bases' : bases,
            'base_names' : [getDottedName(iface) for base in bases ],
            'attributes' : attributes,
            'methods' : methods,
            }

        return result

    security.declarePublic('getMyCommunities')
    def getMyCommunities(self):
        """
        """
        results = self.portal_catalog.searchResults(meta_type = "Community")
        communities = [x.getObject() for x in results]
        member = self.portal_membership.getAuthenticatedMember()

        communities = [community for community in communities if (member in community.getMembers()) or (community.getIsGlobalCommunity())]
        return communities

    security.declarePublic('getMyCustodians')
    def getMyCustodians(self):
        """
        """
        results = self.portal_catalog.searchResults(meta_type = "Custodian")
        custodians = [x.getObject() for x in results]
        member = self.portal_membership.getAuthenticatedMember()

        custodians = [custodian for custodian in custodians if 'Contributor' in custodian.get_local_roles_for_userid(member.id)]
        return custodians

    security.declarePublic('getCustodianById')
    def getCustodianById(self, id):
        """
        """
        results = self.portal_catalog.searchResults(meta_type = "Custodian")
        custodians = [x.getObject() for x in results]
        member = self.portal_membership.getAuthenticatedMember()

        for custodian in custodians:
            if 'Contributor' in custodian.get_local_roles_for_userid(member.id) and custodian.id == id:
                return custodian
        return None

    security.declarePublic('getCommunityById')
    def getCommunityById(self, id):
        """
        """
        for community in self.getMyCommunities():
            if community.id == id:
                return community
        return None

    security.declarePublic('getDefaultSearch')
    def getDefaultSearch(self, REQUEST=None):
        """
        """
        try:
            member = self.portal_membership.getAuthenticatedMember()
            id = member.getDefaultCommunity()
            community = self.getCommunityById(id)
            print 'community', community 
            if community:
                REQUEST.RESPONSE.redirect(community.absolute_url() + '/search')
                return True
            else:
                #tool = getToolByName(portal, 'relations_library')
                #ruleset = tool.getRuleset("default_community")
                #manfred.getRefs("IsParentOf")[0].getId()
                community = self.getDefaultCommunity()
                print community
                if community:
                    REQUEST.RESPONSE.redirect(community[0].absolute_url() + '/search')
                    return True
            REQUEST.RESPONSE.redirect('/no_community')
            return False
        except Exception, e:
            print e
            REQUEST.RESPONSE.redirect('/not_community_user')
    #

registerType(CommunityTool, PROJECTNAME)
# end of class CommunityTool

##code-section module-footer #fill in your manual code here
def resolveInterface(dotted_name):
    parts = dotted_name.split('.')
    m_name = '.'.join(parts[:-1])
    k_name = parts[-1]
    module = __import__(m_name, globals(), locals(), [k_name])
    klass = getattr(module, k_name)
    print 'parts::', parts
    print 'm_name::', m_name
    print 'k_name::', k_name
    print 'module::', module
    print 'klass::', klass
    if not issubclass(klass, Interface):
	raise """%s
%s
%s
%s
%s
""" % (parts, m_name, k_name, module, klass)
        raise ValueError, '%r is not a valid Interface.' % dotted_name
    return klass

def getDottedName(iface):
    return "%s.%s" % (iface.__module__, iface.__name__)

def _trim_doc_string(text):
    """
    Trims a doc string to make it format
    correctly with structured text.
    """
    text = text.strip().replace('\r\n', '\n')
    lines = text.split('\n')
    nlines = [lines[0]]
    if len(lines) > 1:
        min_indent=None
        for line in lines[1:]:
            indent=len(line) - len(line.lstrip())
            if indent < min_indent or min_indent is None:
                min_indent=indent
        for line in lines[1:]:
            nlines.append(line[min_indent:])
    return '\n'.join(nlines)

def visitBaseInterfaces(iface, lst):
    bases = iface.getBases()
    for base in bases:
        if base is Interface or base in lst:
            return
        lst.append(base)
        visitBaseInterfaces(iface, lst)

class InterfaceFinder:

    _visited = {}
    _found = {}

    def findInterfaces(self, n=None, module=_marker):
        # return class reference info
        dict={}
        pairs = []
        if module is _marker:
            import Products
            module = Products
        self._visited[module] = None
        for sym in dir(module):
            ob=getattr(module, sym)
            if type(ob) is type(Interface) and \
               issubclass(ob, Interface) and \
               ob is not Interface:
                self.found(ob)
            elif type(ob) is ModuleType and ob not in self._visited.keys():
                self.findInterfaces(module=ob)

        ifaces = self._found.keys()
        ifaces.sort()
        ifaces.reverse()
        if n is not None:
            ifaces = ifaces[:n]
        return ifaces

    def found(self, iface):
        self._found[getDottedName(iface)] = iface
##/code-section module-footer



