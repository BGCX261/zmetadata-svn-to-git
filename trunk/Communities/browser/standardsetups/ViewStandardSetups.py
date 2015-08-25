# -*- coding: utf-8 -*-
#
# File: ViewStandardSetups.py
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
from Products.Communities.content.standardsetups import StandardSetups
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin


class ViewStandardSetups(BrowserView):
    """
    """

    ##code-section class-header_ViewStandardSetups #fill in your manual code here
    ##/code-section class-header_ViewStandardSetups



    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.context = self.context.context
        self.request = request


    def selectedStandards(self):
        result = {}
        show = self.context.getShowStandards()
        for standard in self.context.getMyStandards():
            result[standard]            = {}
            result[standard]['display'] = (standard in show)
            result[standard]['title']   = self.context[standard].title_or_id()
            result[standard]['url']     = self.context[standard].absolute_url()
            result[standard]['fields']  = self.context[standard].getMyFields()
            result[standard]['showfields']  = self.context[standard].getShowFields()
        return result


##code-section module-footer #fill in your manual code here
##/code-section module-footer


