# Copyright (c) 2003-2005 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$
"""CMF link checker tool - link information object
"""

# Zope imports
from DateTime import DateTime
from OFS.SimpleItem import SimpleItem
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

# CMF/Plone imports
from Products.CMFCore.utils import getToolByName

# Sibling imports
import gocept.linkchecker.interfaces
import gocept.linkchecker.utils


class Link(SimpleItem):
    """A link as used from an object."""

    meta_type = "Link"

    __implements__ = (gocept.linkchecker.interfaces.ILink,)
    # XXX make accessor functions
    __allow_access_to_unprotected_subobjects__ = 1

    object = None
    link = None
    url = None

    manage_options = ({'label': 'Info', 'action':'manage_info'},) + \
                     SimpleItem.manage_options
    manage_info = PageTemplateFile('www/link', globals(), __name__='manage_info')

    def __init__(self, link, id, object):
        self.object = object
        self.link = link
        self.id = id

    # gocept.linkchecker.interfaces.ILink
    def getURL(self):
        """Return the URL object this link refers to."""
        lc = getToolByName(self, "portal_linkchecker")
        return lc.database.queryURLs(url=self.url)[0]

    def getObject(self):
        """Return a reference to the object."""
        references = getToolByName(self, "reference_catalog")
        return references.lookupObject(self.object)

    # Python/Zope helpers 
    def __repr__(self):
        return "<Link %s at %s>" % (self.link, self.object)

    # Catalog support
    def manage_afterAdd(self, container, object):
        self.index()

    def manage_beforeDelete(self, item, container):
        self.unindex()

    def index(self):
        self.url = gocept.linkchecker.utils.resolveRelativeLink(self.link, self.getObject())
        url = self.getURL()
        self.state = url.state
        self.reason = url.reason
        self.lastcheck = url.lastcheck
        path = '/'.join(self.getPhysicalPath())
        self.link_catalog.catalog_object(self, path)

    def unindex(self):
        path = '/'.join(self.getPhysicalPath())
        self.link_catalog.uncatalog_object(path)
