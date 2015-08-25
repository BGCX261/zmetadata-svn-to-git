# -*- coding: utf-8 -*-
#
# File: ViewCommunityDataSearch.py
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
from Products.Communities.content.communitysearch import CommunitySearch
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin


class ViewCommunityDataSearch(BrowserView):
    """
    """

    ##code-section class-header_ViewCommunityDataSearch #fill in your manual code here
    ##/code-section class-header_ViewCommunityDataSearch



    def __init__(self, context, request):
        """
        """
        try:
            self.context = context
            self.request = request
            self.data = context.assembleDisplayFields()
            self.standards = context.getMyStandards()
            self.errors = []
        except Exception, e:
            print str(e)
            import traceback
            traceback.print_exc()


##code-section module-footer #fill in your manual code here
##/code-section module-footer


