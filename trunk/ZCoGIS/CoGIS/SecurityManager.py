import MapServerTemplates
import logging
import cStringIO
import time

logger = logging.getLogger("SecurityManager")
hdlr = logging.FileHandler('SecurityManager.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

class SecurityManager:
    def __init__(self, facade):
        """
        @summary: initializer, sets up the object
        @param userRoleManager: reference to the userRoleManager object
        """       
        self.facade = facade                  
    
    #=======================================================
    # Public interface
    #=======================================================
    
    def getSecurityDefinitionCount(self):
        """
        @summary: gets the number of layers in the security definition
        @return: return (int) number of security def count 
        """        
        return len(self.facade.securityDefinitions.keys())        
    
    def getUserPermissions(self,roles,layerNames=None):
        """
        @summary: returns a structure containing permissions for this role
        @param role: the role name to get layers for
        @return: an xmlrpc encoded string of the permissions structure 
        """        
        try:            
            # e.g {'river':['canRender','canExtract','name','site','system']}
            startTime = time.time()
            retDict = {}      
            
            # loop through the roles
            for role in roles:                   
                for layer in self.facade.securityDefinitions.keys(): 
                    if layerNames:
                        if not layer in layerNames:
                            continue 
                                               
                    if self.facade.securityDefinitions[layer].has_key(role):
                        # get the role
                        lRoleDict = self.facade.securityDefinitions[layer][role]                   
                        canRender = lRoleDict['Render']
                        canExtract = lRoleDict['Extract']
                        if canRender:
                            retDict[layer] = ['canRender']
                        if canExtract:
                            if retDict.has_key(layer):
                                retDict[layer].append('canExtract')
                            else:
                                retDict[layer] = ['canExtract']
                        for field in self.facade.securityDefinitions[layer]['fields']:
                            fRoleDict = self.facade.securityDefinitions[layer]['fields'][field]
                            if fRoleDict.has_key(role):
                                if fRoleDict[role].has_key('Render'):
                                    canRenderField = fRoleDict[role]['Render']
                                    if canRenderField:
                                        retDict[layer].append(field) 
            
            endTime = time.time()             
            return retDict               
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()               
            logger.exception('Could not getUserPermissions')
            return MapServerTemplates.ogcServiceException %("Exception occured with getUserPermissions request, check log for details %s" %trace)    

    def setSecurityDefinition(self,struct,singleSource=0,name=''):
        """
        @summary: set up the role permission settings
        @param xml: xml-rpc encoded string of the definition structure
        @param singleSource: boolean telling if a single layer is being updated or a batch
        """
        try:
            logger.info("setSecurityDefinition")                        
            if singleSource == 1:
                if struct.keys():                             
                    self.facade.securityDefinitions[name] = struct                
            else:                                        
                self.facade.securityDefinitions = struct            
        except:
            import traceback
            sio = cStringIO.StringIO()
            traceback.print_exc(file=sio)
            sio.seek(0)
            trace = sio.read()
            logger.exception('Could not setSecurityDefinition')
            return MapServerTemplates.ogcServiceException %("Exception occured with setSecurityDefinition request, check log for details %s" %trace)    
            
    def getSecurityDefinition(self):
        """         
        """
        return self.facade.securityDefinitions
    
    #=======================================================
    # Protected interface
    #=======================================================
    def _addDefinition(self, definition):
        """        
        """
        self.facade.securityDefinitions[definition.getObjectId()] = definition
        
    def _buildPermissionsStructure(self, roles):
        """        
        """
        try:
            permissions = []
            
            for objectId, role in roles:
                definition = self._getDefinition(objectId)
                objectPermissions = definition.getPermissions(role)
                
                permissions.append((objectId, objectPermissions))
            return permissions
        except:
            logger.exception('error')

    def _getDefinition(self, objectId):
        return self.facade.securityDefinitions[objectId]

            
if __name__ == "__main__":
    pass