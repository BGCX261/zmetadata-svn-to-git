# -*- coding: utf-8 -*-
#
# File: ViewDefaults.py
#
# Copyright (c) 2009 by []
# Generator: ArchGenXML Version 2.3
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

##code-section module-header #fill in your manual code here
##/code-section module-header

from zope import interface
from zope import component
from Products.CMFPlone import utils
from Products.Five import BrowserView
from zope.interface import implements
from Products.Communities.content.fields import Fields
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin


class ViewDefaults(BrowserView):
    """
    """

    ##code-section class-header_ViewDefaults #fill in your manual code here
    ##/code-section class-header_ViewDefaults



    def myFields(self):
        return self.context.getMyFields()


    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.context = self.context.context
        self.request = request


    def defaultValuesForFields(self):
        result = []
        for field in self.context.schema.fields():
            if (field.schemata != 'categorization') and \
               (field.schemata != 'metadata') and \
               (field.getName() not in ('id', 'title', 'description')):
                name = field.getName()
                label = self.context.schema.widgets()[field.getName()].label
                value = field.get(self.context)
                result += [(name, label, value)]
        return result


##code-section module-footer #fill in your manual code here
##/code-section module-footer


