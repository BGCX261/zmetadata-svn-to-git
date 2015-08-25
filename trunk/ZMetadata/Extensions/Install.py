__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from StringIO import StringIO
from sets import Set
from App.Common import package_home
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import manage_addTool
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from zExceptions import NotFound, BadRequest
from Products.ZMetadata.config import JAVASCRIPTS
from Products.ZMetadata.config import STYLESHEETS

from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes.Extensions.utils import install_subskin
from Products.Archetypes.config import TOOL_NAME as ARCHETYPETOOLNAME
from Products.Archetypes.atapi import listTypes
from Products.ZMetadata.config import PROJECTNAME
from Products.ZMetadata.config import product_globals as GLOBALS
from Products.ZMetadata.MetadataManager import MetadataManager
from Products.ZMetadata.Standard import Standard
from Products.ZMetadata.LogContainer import LogContainer
from Products.Communities.content.MetadataContainer import MetadataContainer
from Products.ZMetadata import Global
import sys
import traceback
from Globals import package_home
   
        
def install(self, reinstall=False):
    """ External Method to install ZMetadata """
    out = StringIO()
    print >> out, "Installation log of %s:" % PROJECTNAME

    # If the config contains a list of dependencies, try to install
    # them.  Add a list called DEPENDENCIES to your custom
    # AppConfig.py (imported by config.py) to use it.
    try:
        from Products.ZMetadata.config import DEPENDENCIES
    except:
        DEPENDENCIES = []
    portal = getToolByName(self,'portal_url').getPortalObject()
    
    quickinstaller = portal.portal_quickinstaller
    for dependency in DEPENDENCIES:
        print >> out, "Installing dependency %s:" % dependency
        quickinstaller.installProduct(dependency)
        get_transaction().commit(1)

    classes = listTypes(PROJECTNAME)
    installTypes(self, out,
                 classes,
                 PROJECTNAME)
    install_subskin(self, out, GLOBALS)


    # try to call a workflow install method
    # in 'InstallWorkflows.py' method 'installWorkflows'
    try:
        installWorkflows = ExternalMethod('temp', 'temp',
                                          PROJECTNAME+'.InstallWorkflows',
                                          'installWorkflows').__of__(self)
    except NotFound:
        installWorkflows = None

    if installWorkflows:
        print >>out,'Workflow Install:'
        res = installWorkflows(self,out)
        print >>out,res or 'no output'
    else:
        print >>out,'no workflow install'

    # enable portal_factory for given types
    factory_tool = getToolByName(self,'portal_factory')
    factory_types=[
        "Custodian",
        "Harvester",
        "Log",
        "Metadata",
        "MetadataManager",
        "Standard",       
        "Logs",
#        "MetadataCollection",
#        "MetadataContainer",
        "LogContainer",
        "Archive",
        ] + factory_tool.getFactoryTypes().keys()
    factory_tool.manage_setPortalFactoryTypes(listOfTypeIds=factory_types)

    
    try:
        portal_css = getToolByName(portal, 'portal_css')
        for stylesheet in STYLESHEETS:
            try:
                portal_css.unregisterResource(stylesheet['id'])
            except:
                pass
            defaults = {'id': '',
            'media': 'all',
            'enabled': True}
            defaults.update(stylesheet)
            portal_css.registerStylesheet(**defaults)
    except:
        # No portal_css registry
        pass
    
    try:
        portal_javascripts = getToolByName(portal, 'portal_javascripts')
        for javascript in JAVASCRIPTS:
            try:
                portal_javascripts.unregisterResource(javascript['id'])
            except:
                pass
            defaults = {'id': ''}
            defaults.update(javascript)
            portal_javascripts.registerScript(**defaults)
    except:
        # No portal_javascripts registry
        pass

    # try to call a custom install method
    # in 'AppInstall.py' method 'install'
    try:
        install = ExternalMethod('temp', 'temp',
                                 PROJECTNAME+'.AppInstall', 'install')
    except NotFound:
        install = None

    if install:
        print >>out,'Custom Install:'
        try:
            res = install(self, reinstall)
        except TypeError:
            res = install(self)
        if res:
            print >>out,res
        else:
            print >>out,'no output'
    else:
        print >>out,'no custom install'
        
    # document_actions : uploadMetadata
    # create single MetadataManager
    # URL :  string:${portal_url}/Metadata/uploadMetadataFromPortalAction?id=${object_url}
    # condition:  python:(member is not None) 
    # permissions : "View management screens", "View"
    
    instanceName = "metadata_tool"
    currentIds = self.objectIds()
    if instanceName not in currentIds:
        self._setObject(instanceName,MetadataManager(instanceName))
    # add custom portal_action
    pt = self.portal_actions    

    actions = self.portal_actions.listActions()
    actionNames = [x.id for x in actions]
    
    #string:${portal_url}/metadata_tool/metadata_from_template?id=${object_url}
    
    
#    if actionNames.count("metadataFromTemplate") == 0:
#        pt.addAction('metadataFromTemplate', name='Metadata from Template',             
#             action='string:${portal_url}/metadata_tool/metadata_from_template?id=${object_url}',
#             #condition='python:(member is not None)',
#             condition='python: object.meta_type in ["MetadataCollection", "MetadataContainer"]',
#             permission='Modify portal content',
#             category='object_buttons')
        
    if actionNames.count("zipMetadata.zip") == 0:
        pt.addAction('zipMetadata.zip', name='Zip Metadata',             
             action='python: object.metadata_tool.showZipFile(object)',
             condition='python: object.metadata_tool.showZipFile(object)',
             permission='Modify portal content',
             category='document_actions')      
    
    if Global.config.getShowUploadTab():
        if actionNames.count("uploadMetadata") == 0:
            pt.addAction('uploadMetadata', name='Link New Metadata',
                 action='string:${portal_url}/metadata_tool/uploadMetadataFromPortalAction?id=${object_url}',
                 condition='python:(member is not None)',
                 permission='View management screens',
                 category='metadata')
    
    if actionNames.count("linkMetadata") == 0:
        pt.addAction('linkMetadata', name='Linked Metadata',
             action='string:${object_url}/linkMetadata',
             condition='python:(member is not None)',
             permission='View management screens',
             category='metadata')

    if actionNames.count("linkData") == 0:
        pt.addAction('linkData', name='Link Data',
            action='string:${object_url}/linkData',
            condition='python:(member is not None) and (object.portal_type in ["Metadata"])',
            permission='View management screens',
            category='metadata')

    if Global.config.getShowSpatialSearchLink():
        if actionNames.count("spatialSearch") == 0:
            pt.addAction('spatialSearch', name='Spatial Search',
                 action='string:${portal_url}/metadata_tool/search_metadata',
                 condition='python:1',
                 permission='View',
                 category='site_actions')
    
    if Global.config.getShowSpatialSearchLink():
        if actionNames.count("communitySearch") == 0:
            pt.addAction('communitySearch', name='Community Search',
                 action='string:${portal_url}/portal_communitytool/getDefaultSearch',
                 condition='python:1',
                 permission='View',
                 category='site_actions')
    
        #self.manage_delObjects([instanceName])        
    return out.getvalue()

def uninstall(self, reinstall=False):
    out = StringIO()
    # try to call a workflow uninstall method
    # in 'InstallWorkflows.py' method 'uninstallWorkflows'
    # remove custom portal_action
    
    actions = self.portal_actions.listActions()
    index = 0
    # remove actions created by installer
    deleteIndexes = []
    for action in actions:        
        if action.id == "zipMetadata":
            deleteIndexes.append(index)
        if action.id == "zipMetadata.zip":
            deleteIndexes.append(index)
        if action.id == "metadataFromTemplate":
            deleteIndexes.append(index)        
        if action.id == "uploadMetadata":
            deleteIndexes.append(index)
        if action.id == "linkMetadata":
            deleteIndexes.append(index)
        if action.id == "linkData":
            deleteIndexes.append(index)
            #self.portal_actions.deleteActions((index,))
        if action.id == "spatialSearch":
            deleteIndexes.append(index)
            #self.portal_actions.deleteActions((index,))
        if action.id == "communitySearch":
            deleteIndexes.append(index)
        index += 1
    for deleteIndex in deleteIndexes:
        self.portal_actions.deleteActions((deleteIndex,))
    
    try:
        uninstallWorkflows = ExternalMethod('temp', 'temp',
                                            PROJECTNAME+'.InstallWorkflows',
                                            'uninstallWorkflows').__of__(self)
    except NotFound:
        uninstallWorkflows = None

    if uninstallWorkflows:
        print >>out, 'Workflow Uninstall:'
        res = uninstallWorkflows(self, out)
        print >>out, res or 'no output'
    else:
        print >>out,'no workflow uninstall'

    # try to call a custom uninstall method
    # in 'AppInstall.py' method 'uninstall'
    try:
        uninstall = ExternalMethod('temp', 'temp',
                                   PROJECTNAME+'.AppInstall', 'uninstall')
    except:
        uninstall = None

    if uninstall:
        print >>out,'Custom Uninstall:'
        try:
            res = uninstall(self, reinstall)
        except TypeError:
            res = uninstall(self)
        if res:
            print >>out,res
        else:
            print >>out,'no output'
    else:
        print >>out,'no custom uninstall'

    return out.getvalue()

def beforeUninstall(self, reinstall, product, cascade):
    """ try to call a custom beforeUninstall method in 'AppInstall.py'
        method 'beforeUninstall'
    """
    out = StringIO()
    try:
        beforeuninstall = ExternalMethod('temp', 'temp',
                                   PROJECTNAME+'.AppInstall', 'beforeUninstall')
    except:
        beforeuninstall = []

    if beforeuninstall:
        print >>out, 'Custom beforeUninstall:'
        res = beforeuninstall(self, reinstall=reinstall
                                  , product=product
                                  , cascade=cascade)
        if res:
            print >>out, res
        else:
            print >>out, 'no output'
    else:
        print >>out, 'no custom beforeUninstall'
    return (out,cascade)

def afterInstall(self, reinstall, product):
    """ try to call a custom afterInstall method in 'AppInstall.py' method
        'afterInstall'
    """
    out = StringIO()
    try:
        afterinstall = ExternalMethod('temp', 'temp',
                                   PROJECTNAME+'.AppInstall', 'afterInstall')
    except:
        afterinstall = None

    if afterinstall:
        print >>out, 'Custom afterInstall:'
        res = afterinstall(self, product=None
                               , reinstall=None)
        if res:
            print >>out, res
        else:
            print >>out, 'no output'
    else:
        print >>out, 'no custom afterInstall'
    return out
