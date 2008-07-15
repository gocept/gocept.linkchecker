# Copyright (c) 2005 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$
"""CMF link checker tool - link retriever functions"""

# CMFLinkChecker imports
from Products.CMFLinkChecker.interfaces import IRetriever
from Products.CMFLinkChecker.utils import retrieveHTML, retrieveSTX, \
     retrieveAllRichTextFields, updateAllRichTextFields
from Products.CMFLinkChecker.retrievemanager import GlobalRegistry

class RetrieverLink(object):
    """CMFDefault.Link retriever
    
    Also works for HelpCenterLink, though this has attribute url instead of
    remoteUrl.

    """
    __implements__ = (IRetriever,)

    name = "CMFDefault.Link"
    defaults = ["Link",]

    def retrieveLinks(self, object):
        """Finds all links from the object and return them."""
        try:
            return [object.getRemoteUrl()]
        except AttributeError:
            # Incompatible content selected ... XXX report warning here
            try:
                return [object.getUrl()]
            except AttributeError:
                # Incompatible content selected ... XXX report warning here
                return []

    def updateLink(self, oldurl, newurl, object):
        """Replace all occurances of <oldurl> on object with <newurl>."""
        if object.getRemoteUrl() == oldurl:
            object.setRemoteUrl(newurl)


class RetrieverEvent(object):
    """CMFDefault.Event retriever"""

    __implements__ = (IRetriever,)

    name = "CMFDefault.Event"
    defaults = ["Event",]
    
    def retrieveLinks(self, object):
        """Finds all links from the object and return them."""
        try:
            links = [object.event_url()]
        except AttributeError:
            # Incompatible content selected ... XXX report warning here
            links = []

        for link in retrieveAllRichTextFields(object):
            links.append(link)

        return links

    def updateLink(self, oldurl, newurl, object):
        """Replace all occurances of <oldurl> on object with <newurl>."""
        if self.event_url() == oldurl:
            self.setEventUrl(newurl)
        updateAllRichTextFields(oldurl, newurl, object)


class RichTextRetriever(object):
    """Retriever for documents with one or more RichText widgets."""

    __implements__ = (IRetriever,)

    name = 'RichText'
    defaults = ['Document', 'News Item']

    def retrieveLinks(self, object):
        """Finds all links from the object and return them."""
        return retrieveAllRichTextFields(object)

    def updateLink(self, oldurl, newurl, object):
        """Replace all occurances of <oldurl> on object with <newurl>."""
        updateAllRichTextFields(oldurl, newurl, object)


def register():
    """register retrievers"""
    GlobalRegistry.register(RetrieverLink())
    GlobalRegistry.register(RetrieverEvent())
    GlobalRegistry.register(RichTextRetriever())
