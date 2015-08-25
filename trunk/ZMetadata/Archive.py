

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

#Archive_schema = BaseFolderSchema.copy() +  schema.copy()
Archive_schema = ATContentTypeSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Archive(BaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Archive'

    meta_type = 'Archive'
    portal_type = 'Archive'
    allowed_content_types = ['Metadata']
    filter_content_types = 1
    global_allow = 0
    content_icon = 'archive.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Archive"
    typeDescMsgId = 'description_edit_archive'

    _at_rename_after_creation = True

    schema = Archive_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    def __init__(self,id,title="Archive"):
        ""
        self.id = id;
        self.title = title;

registerType(Archive, PROJECTNAME)
# end of class Archive

##code-section module-footer #fill in your manual code here
##/code-section module-footer



