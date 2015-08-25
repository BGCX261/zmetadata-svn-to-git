from Products.CMFCore.WorkflowCore import WorkflowException 

# This must be placed under "scripts" of the relevant workflow and then added
# as as "before" transition script.
def before_publish_check(state_change):
    obj = state_change.object
    
    if (obj.meta_type == 'Metadata'):
      xml = obj.getXml()
      standard = obj.getStandard()
      valid = standard.validateXML(xml)[0]
      if (not valid):  
        raise WorkflowException("XML is not valid.  Use 'Edit Metadata' to fix it first.")
