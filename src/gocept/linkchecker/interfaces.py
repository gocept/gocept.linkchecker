# Copyright (c) 2003-2005 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$"""
"""CMF link checker tool interface definitions"""


from Interface import Interface, Attribute

from Products.Archetypes import public as atapi


class ILinkManager(Interface):

    database = Attribute("A link database implementing the "
                         "ILinkDatabase interface.")
    reports = Attribute("A report utility implementing the "
                        "IBaseReports interface.")
    retrieving = Attribute("A retrieve manager implementing the "
                           "IRetrieveManager interface.")

    def shortURL(url, target=50):
        """Context aware wrapper for creating a shortened URL"""

    def isManaged(object):
        """Tells if the object is managed by the link manager."""

    def resolveRelativeLink(url, context):
        """Resolve relative URL from context to an absolute URL.

        This is similar to the absolute_url(), but does not require an object
        and honours the prefix settings from the link management settings.
        """

    def isUserAllowed():
        """Returns whether the user is allowed to use link management
        services.

        Returns True, iff the currently logged in user is allowed to use link
            management services at all.

        This function checks whether the user has the 'Use link management functions'
        permission in the Plone root.
        """

    def getLinkManager():
        """return self"""


class IBaseReports(Interface):
    """Supplement functions for various basic reports."""

    def GroupedLinksForAuthenticatedMember():
        """Returns a list of links aggregated by state for the current user.

           The list only features catalog brains from the database.
        """

    def DocumentsInState(state):
        """Returns a list of all objects that contain links in the given state.
        """

    def LinksInState(state):
        """Returns a list of links in the given state."""

    def ManagementOverview():
        """Returns a comprehensive management overview over the complete site.
        """


class ILinkDatabase(Interface):
    """A database of links. 

       Manages the physical storage of link information.
    """

    defaultURLPrefix = Attribute("A valid URL that is used (component wise) to "
                                 "prepend incomplete links")

    def configure(defaultURLPrefix=None):
        """Set configuration values."""

    def unregisterLink(link, object):
        """Unregisters a given link/object pair at the database.

           If the given link isn't referenced by any object anymore, it will 
           be removed from the database completely.

           Raises KeyError if the given pair isn't registered.

           Returns None.
        """

    def unregisterObject(object):
        """Unregisters all links for this object.

           Returns None.
        """

    def getLinksForObject(object):
        """Retrieve information about an object.

           Returns a list of ILink objects. 
           Returns an empty list if the object hasn't been registered yet.
        """

    def getLinksForURL(url):
        """Retrieve links for an url.

        Returns all links that point to the given url.
        """

    def getAllLinks():
        """Returns a list of all ILink objects.

           Warning: This is likely to be a slow method in large data sets.
        """

    def getAllLinkIds():
        """Returns a list of the ids of all ILink objects.

           Warning: This is likely to be a slow method in large data sets.
        """

    def getLinkCount():
        """Returns the amount of links currently in the database."""

    def queryLinks(self, **args):
        """Returns the result of querying the ZCatalog that indexes links."""

    def queryURLs(self, **args):
        """Returns the result of querying the ZCatalog that indexes urls."""


class IRetrieveManager(Interface):
    """Local registry that manages the mapping between portal_type and 
       specific retrievers for a single plone instance and allows to trigger
       retrieving for an object or the whole site.
    """

    def registerRetriever(portal_type, retriever_name):
        """Registers the retriever to be called on objects of portal_type.

            portal_type: portal type to assign retriever to
            retriever_name: Name of a retriever as registered at the global 
                            retriever registry, or None to remove assignment
            Returns None

            Raises KeyError if the portal_type or retriever name is invalid.

            If the portal_type already has a registered retriever, the
            registration will be overwritten.

        """

    def isRetrieverForType(retriever_name, portal_type):
        """Tells if the given retriever name is the retriever for this type.

           Returns True or False.
        """

    def listSupportedTypes():
        """Returns a list of portal_types that are currently supported by
           this retrieve manager.
        """

    def retrieveObject(object):
        """Retrieves the links from the given object."""

    def retrieveSite():
        """Retrieves the links from all objects in the site.

           Raises RuntimeError if no connection to the lms can be established.
        """

    def supportsRetrieving(object):
        """Tells if the object is supported for retrieving links."""

    def getAllRetrieverNames():
        """Returns the name of all available retrievers."""


class IGlobalRetrieverRegistry(Interface):
    """Process global registry that holds information
       about all system wide available retrievers.
    """

    def register(method, name, defaults=[]):
        """Register a retriever method globally under the given title and as a
           default for the given portal_types.

           Defaults are overwritten subsequently by later calls.

           Raises ValueError if the method has been registered already.

           Returns None
        """

    def getByName(name):
        """Returns a retriever by it's name.

           Raises KeyError if a retriever with this name doesn't exists.
        """

    def getDefault(type):
        """Returns the default retriever for a type.

           Raises KeyError if there is no retriever for the given type.
        """

    def listNames():
        """Returns a list of all retriever names."""


class IURL(Interface):
    """URL status information

    The URL as transmitted to the LMS. It must be absolute and include protocol
    and netlocation.

    A URL can be referred to by many links as, depending on the context, a URL
    can be expressed by several relative spellings.

    """

    url = Attribute("Contains the URL the link refers to.")
    registered = Attribute("Has this link been registered with the web service?")
    lastcheck = Attribute("DateTime when the last check was performed.") 
    lastupdate = Attribute("DateTime when the last status change ocurred.")
    laststate = Attribute("The state before the current state was assumed.")
    state = Attribute("The current state of the link. Can be one of ['red', " \
                      "'green', 'orange', 'grey'].")
    reason = Attribute("A verbose reason describing the error")
    links = Attribute(
        "A property that returns all currently associated links"
        "(as catalog brains).")

    def updateStatus(state, reason):
        """Updates the status information for this URL."""


class ILink(Interface):
    """A link as used from an object."""

    link = Attribute("Link as stored on the object")
    object = Attribute("The UID of the object containing the link.")
    url = Attribute(
        "URL as computed from the link and the object as context.")

    # Fields to support caching of data
    state = Attribute("The current state of the URL.")
    reason = Attribute("The current state of the URL.")

    def getObject():
        """Returns a list of objects referencing this link."""

    def getURL():
        """Return the URL object this link refers to."""


class IRetriever(Interface):
    """A class that implements a routine to retrieve and update URLs stored on
    an object.
    """

    name = Attribute("Name of the retriever, suitable to identify it.")
    defaults = Attribute(
        "A list of portal_types this retriever is a default for.")

    def retrieveLinks(self, object):
        """Finds all links from the object and return them.

           Returns a list of URLs.

        """

    def updateLink(self, oldurl, newurl, object):
        """Replace all occurances of <oldurl> on object with <newurl>."""


# Additional fields a CMFMember object requires in order to be usable with
# CMFLinkChecker
memberSchema = atapi.Schema((
    atapi.LinesField('lc_notify_details', regfield=False),
    atapi.LinesField('lc_notify_frequency', regfield=False),
    atapi.BooleanField('lc_notify_changes_only', regfield=False),
    atapi.DateTimeField('lc_notify_last_notification', regfield=False),
))
