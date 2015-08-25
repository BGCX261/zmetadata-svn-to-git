

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ZMetadata.config import *
from Products.ATContentTypes.content.schemata import ATContentTypeSchema

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

#LogContainer_schema = BaseFolderSchema.copy() + schema.copy()
LogContainer_schema = ATContentTypeSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class LogContainer(BaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'LogContainer'

    meta_type = 'LogContainer'
    portal_type = 'LogContainer'
    allowed_content_types = ['Log']
    filter_content_types = 1
    global_allow = 0    
    #immediate_view = 'base_view'
    #default_view = 'base_view'
    #suppl_views = ()
    #typeDescription = "LogContainer"
    #typeDescMsgId = 'description_edit_LogContainer'

    _at_rename_after_creation = True

    schema = LogContainer_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    def __init__(self,id,title="LogContainer"):
        ""
        self.id = id;
        self.title = title;

registerType(LogContainer, PROJECTNAME)


##code-section module-footer #fill in your manual code here
##/code-section module-footer



