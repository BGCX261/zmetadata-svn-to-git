## Script (Python) "holycow"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=portalTypes, resultsPerQuery, SearchableText
##title=
##
# Example code:

# Import a standard function, and get the HTML request and response objects.
from Products.PythonScripts.standard import html_quote
request = container.REQUEST
RESPONSE =  request.RESPONSE


resultsPerQuery = int(resultsPerQuery)
if '' in portalTypes:
    portalTypes.remove('')
    

brains = context.portal_catalog(SearchableText='*'+SearchableText+'*', portal_type=portalTypes)[:resultsPerQuery-1]


if not brains:
    return "Sorry, no results found!"

result = "<ul>"

typeInfos = {}

typeTool = context.portal_types

checked = ''

for brain in brains:
    obj = brain.getObject()
    if not typeInfos.has_key(obj.portal_type):
        try:
            typeInfos[obj.portal_type] = typeTool.getTypeInfo(obj.portal_type) 
        except Exception, e:
            result += str(e)
    result += '<li><input type="radio" %s class="relatedItem" value="%s" name="relatedItem"/><a target="preview" href="%s"<img src="/%s">%s</a></li>' % (checked, obj.UID(), obj.absolute_url(), typeInfos[obj.portal_type].getIcon(), obj.title_or_id())
    result += '<br/>'
    checked = ''

return result