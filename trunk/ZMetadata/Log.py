
__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ZMetadata.config import *
from datetime import datetime
from Products.ATContentTypes.content.schemata import ATContentTypeSchema

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='message',
        required=1,
        widget=StringWidget(
            label='Message',
            label_msgid='ZMetadata_label_messages',
            i18n_domain='ZMetadata',
        )
    ),
    
    StringField(
        name='logtype',
        required=1,
        default = '',
        widget=SelectionWidget
        (
            label='Log Type',
            label_msgid='ZMetadata_label_logtype',
            i18n_domain='ZMetadata',
        ),
        vocabulary=['Warning','Info','Error']        
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

#Log_schema = BaseSchema.copy() + schema.copy()
Log_schema = ATContentTypeSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Log(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Log'

    meta_type = 'Log'
    portal_type = 'Log'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    content_icon = 'log.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Log"
    typeDescMsgId = 'description_edit_log'

    _at_rename_after_creation = True

    schema = Log_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    def __init__(self,id, title="Log"):
        """
        """        
        self.id = id;
        self.title = title;
        
    def getDate(self):
        """
        """
        #print dir(self.getRawCreation_date())
        #print type(self.getRawCreation_date())
        #print self.getRawCreation_date()
        rawDate = self.getRawCreation_date()        
        tmpDate = datetime(rawDate.year(), rawDate.month(), rawDate.day(), rawDate.hour(),rawDate.minute())
        return tmpDate        

registerType(Log, PROJECTNAME)
# end of class Log

##code-section module-footer #fill in your manual code here
##/code-section module-footer



