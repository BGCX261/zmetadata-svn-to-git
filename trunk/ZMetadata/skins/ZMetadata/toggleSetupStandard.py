## Script (Python) "holycow"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=standardName
##title=
##
# Example code:

# Import a standard function, and get the HTML request and response objects.
from Products.PythonScripts.standard import html_quote
request = container.REQUEST
RESPONSE =  request.RESPONSE

self = context
setup = self.setup

if standardName not in setup.getMyStandards():
    raise Exception('Unknown standard: ' + standardName)

if standardName in self.setup.getShowStandards():
    self.setup.setShowStandards([std for std in self.setup.getShowStandards() if std != standardName])
else:
    self.setup.setShowStandards([standardName] + list(self.setup.getShowStandards()))
    
RESPONSE.redirect(self.absolute_url())