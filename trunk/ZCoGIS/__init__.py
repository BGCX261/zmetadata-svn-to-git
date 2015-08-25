import config

# configure logging
import logging
rootLogger = logging.root
rootLogger.setLevel(config.DEBUG_LEVEL)

if config.PRINT_TO_TERMINAL:
    import sys
    printHandler = logging.StreamHandler(sys.__stdout__)
    formatter = logging.Formatter('-----\n%(asctime)s : %(levelname)s : %(name)s : [%(lineno)d]%(filename)s\n%(message)s')
    printHandler.setFormatter(formatter)
    rootLogger.addHandler(printHandler)

import contentTypesConfig


from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
from Products.ZCoGIS.config import PROJECTNAME, ADD_CONTENT_PERMISSION, SKINS_DIR, GLOBALS

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):   
          
    content_types, constructors, ftis = process_types(
    listTypes(PROJECTNAME), PROJECTNAME)
  
    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types = content_types,
        permission = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti = ftis,).initialize(context)