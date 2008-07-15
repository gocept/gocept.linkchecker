# Copyright (c) 2003-2005 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$
"""CMF link checker tool - retrieve manager

"""

# Zope imports
import transaction
import zLOG
import zope.lifecycleevent.interfaces
import zope.component
from AccessControl import ClassSecurityInfo, getSecurityManager, Unauthorized
from Globals import InitializeClass, PersistentMapping
from OFS.SimpleItem import SimpleItem

import Products.Archetypes.interfaces

# CMF/Plone imports
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.utils import getToolByName

# CMFLinkChecker imports
from Products.CMFLinkChecker.interfaces import IGlobalRetrieverRegistry
from Products.CMFLinkChecker.interfaces import IRetrieveManager


def manage_addRetrieveManager(container, id):
    """Add a new retriever manager to a link manager."""
    container._setObject(id, RetrieveManager(id))


class RetrieveManager(SimpleItem):
    """Local registry that manages the mapping between portal_type and 
       specific retrievers for a single plone instance and allows to trigger
       retrieving for an object or the whole site.
    """

    __implements__ = (IRetrieveManager,) + SimpleItem.__implements__ 
    security = ClassSecurityInfo()

    def __init__(self, id):
        self.id = id
        self._retrievers = PersistentMapping()

    def manage_afterAdd(self, item, container):
        # Register default retrievers for the types that are
        # in our portal, if a default retriever is available.
        pt = getToolByName(self, "portal_types")
        for type in pt.objectIds():
            try:
                retriever = GlobalRegistry.getDefault(type)
            except KeyError:
               continue

            self.registerRetriever(type, retriever.name)

    ##################
    # IRetrieveManager

    def registerRetriever(self, portal_type, retriever_name):
        """Registers the retriever to be called on objects of portal_type.
        """

        types = getToolByName(self, "portal_types").objectIds()

        # Check that the type exists
        if not portal_type in types:
            raise KeyError, "Invalid portal_type %s" % portal_type

        if retriever_name is None:
            # remove
            try:
                del self._retrievers[portal_type]
            except KeyError:
                pass
        else:
            # Check that the retriever exists
            retriever = GlobalRegistry.getByName(retriever_name)

            self._retrievers[portal_type] = retriever_name

    def listSupportedTypes(self):
        """Returns a list of portal_types that are currently supported by
           this retrieve manager.
        """
        return self._retrievers.keys()

    security.declarePublic('retrieveObject')
    def retrieveObject(self, object):
        # Check for ModifyPortalContent-Permission on context object.
        # This is dangerous, but I think I know what I'm doing.
        sm = getSecurityManager()
        if not sm.checkPermission(ModifyPortalContent, object):
            raise Unauthorized, "You can't retrieve links for this object."
        if (not
            Products.Archetypes.interfaces.IReferenceable.providedBy(object)):
            return
        database = self.getParentNode().database
        database.unregisterObject(object)
        retriever = self._getRetrieverForObject(object)
        if retriever is not None:
            links = retriever.retrieveLinks(object)
            database.registerLinks(links, object)

    security.declarePublic('updateObject')
    def updateLink(self, old_link, new_link, object):
        # Check for ModifyPortalContent-Permission on context object.
        # This is dangerous, but I think I know what I'm doing.
        sm = getSecurityManager()
        if not sm.checkPermission(ModifyPortalContent, object):
            raise Unauthorized, "You can't update links for this object."
        retriever = self._getRetrieverForObject(object)
        if retriever is not None:
            retriever.updateLink(old_link, new_link, object)
        self.retrieveObject(object)

    security.declareProtected(ManagePortal, 'isRetrieverForType')
    def isRetrieverForType(self, retriever_name, portal_type):
        """Tells if the given retriever name is the retriever
           for this type.

           Returns True or False.
        """
        if not self._retrievers.has_key(portal_type):
            return False

        return self._retrievers[portal_type] == retriever_name

    security.declareProtected(ManagePortal, 'retrieveSite')
    def retrieveSite(self):
        """Retrieves the links from all objects in the site."""
        server = self.getParentNode().database._getWebServiceConnection()
        if server is None:
            raise RuntimeError, "The site could not be crawled because no " \
                                "connection to the lms could be established."
        server.setClientNotifications(False)

        try:
            database = self.getParentNode().database
            # gather all objects that are of a type we can check for links
            for type in self.listSupportedTypes():
                objects = self.portal_catalog(portal_type=type, Language='all')
                os_ = len(objects)
                i = 0
                for ob in objects:
                    i += 1
                    zLOG.LOG("CMFLinkChecker", zLOG.BLATHER,
                             "Site Crawl Status",
                             "%s of %s (%s)" % (i, os_, ob.getPath()))
                    ob = ob.getObject()
                    if ob is None:
                        # Maybe the catalog isn't up to date
                        continue
                    self.retrieveObject(ob)
                transaction.savepoint()
            # Remove unused urls
            database.cleanup()
        finally:
            server.setClientNotifications(True)

    def supportsRetrieving(self, object):
        """Tells if the object is supported for retrieving links."""
        return self._retrievers.has_key(object.portal_type)

    def getAllRetrieverNames(self):
        """Returns the name of all available retrievers."""
        return GlobalRegistry.listNames()

    #################
    # Private methods

    def _getRetrieverForObject(self, object):
        type = object.portal_type
        retriever_name = self._retrievers.get(type)
        if retriever_name is None:
            retriever = None
        else:
            retriever = GlobalRegistry.getByName(retriever_name)
        return retriever 

InitializeClass(RetrieveManager)

class GlobalRegistry(object):
    """Process global registry that holds information
       about all system wide available retrievers.
    """

    __implements__ = (IGlobalRetrieverRegistry,)

    def __init__(self):
        self._defaults = {}     # Access by defaults
        self._retrievers = {}   # Access by name
        
    def register(self, retriever):
        """Register a retriever globally under the given title and as a 
           default for the given portal_types.

           Defaults are overwritten subsequently by later calls.

           Raises ValueError if the method has been registered already.

           Returns None
        """
        if self._retrievers.has_key(retriever.name):
            zLOG.LOG('CMFLinkChecker', zLOG.INFO,
                     "Retriever '%s' is already registered." % retriever.name)
        self._retrievers[retriever.name] = retriever
       
        for default in retriever.defaults:
            self._defaults[default] = retriever

    def getByName(self, name):
        """Returns a retriever by it's name.

           Raises KeyError if a retriever with this name doesn't exists.
        """
        return self._retrievers[name]

    def getDefault(self, type):
        """Returns the default retriever for a type.

           Raises KeyError if there is no retriever for the given type.
        """
        return self._defaults[type]

    def listNames(self):
        """Returns a list of all retriever names."""
        return self._retrievers.keys()


@zope.component.adapter(
    zope.lifecycleevent.interfaces.IObjectModifiedEvent)
def update_links(event):
    object = event.object
    try:
        link_checker = getToolByName(object, 'portal_linkchecker')
    except AttributeError:
        return
    if not link_checker.active:
        return
    link_checker.retrieving.retrieveObject(object)


GlobalRegistry = GlobalRegistry()
