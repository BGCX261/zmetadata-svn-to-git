from Products.ZCoGIS.config import PROJECTNAME, GLOBALS
from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes,install_subskin
from StringIO import StringIO
from Products.ZCoGIS.MapServerFacade import MapServerFacade

def install(self):
    out = StringIO()

    installTypes(self, out,
                 listTypes(PROJECTNAME),
                 PROJECTNAME)
                 
    install_subskin(self, out, GLOBALS)

#    currentIds = self.objectIds()        
#    for i in currentIds:            
#        if i == "MapServer":
#            self.manage_delObjects(["MapServer"])         
#    
#    #self.invokeFactory(id="MapServer", type_name="MapServer")
#    self._setObject("MapServer",MapServerFacade("MapServer"))
    return out.getvalue()

def uninstall(self):    
    pass
#    currentIds = self.objectIds()        
#    for i in currentIds:        
#        if i == "MapServer":
#            self.manage_delObjects(["MapServer"]) 