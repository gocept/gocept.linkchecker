# Copyright (c) 2005 gocept. All rights reserved.
# See also LICENSE.txt
# $Id$
"""CMF link checker tool initalisation code"""

from Products.Archetypes import public as atapi
from Products.CMFLinkChecker import permissions
from Products.CMFCore import utils as CMFutils

from Products.CMFLinkChecker import config

def initialize_tool(context):
    from Products.CMFLinkChecker import LinkCheckerTool
    tools = (LinkCheckerTool.LinkCheckerTool, )
    tool_init = CMFutils.ToolInit('CMFLinkChecker Tool',
                                  tools=tools,
                                  icon="tool.png")
    tool_init.initialize(context)
   
def initialize_content(context):
    from Products.CMFLinkChecker import database, retrievemanager, reports
    context.registerClass(database.LinkDatabase,
                          constructors=(database.manage_addLinkDatabase,),
                          container_filter = filterLinkManagerAddable)
    context.registerClass(reports.BaseReports,
                          constructors=(reports.manage_addBaseReports,),
                          container_filter=filterLinkManagerAddable)

    context.registerClass(retrievemanager.RetrieveManager,
                          constructors=(retrievemanager.\
                                        manage_addRetrieveManager,),
                          container_filter=filterLinkManagerAddable
        )

def initialize_atcontent(context):
    # this is *only* for test support, therefore we do not import anything
    types = atapi.listTypes(config.PROJECTNAME)
    if not types:
        return
    content_types, constructors, ftis = atapi.process_types(types,
                                                            config.PROJECTNAME)
    content_init = CMFutils.ContentInit(config.PROJECTNAME + ' Content',
                                        content_types=content_types,
                                        permission=\
                                           permissions.AddPortalContent,
                                        extra_constructors=constructors,
                                        fti=ftis)
    content_init.initialize(context)

def initialize_skins(context):
    from Products.CMFCore import DirectoryView
    DirectoryView.registerDirectory(config.SKINS_DIR, config.GLOBALS)


def initialize_retrievers(context):
    from Products.CMFLinkChecker import retrievers
    retrievers.register()


def initialize(context):
    initialize_tool(context)
    initialize_content(context)
    initialize_atcontent(context)
    initialize_skins(context)
    initialize_retrievers(context)
    

def filterLinkManagerAddable(objectmanager):
    """Tools for the Link Manager should not be addable everywhere"""
    if objectmanager.meta_type != "CMF Linkchecker Tool":
        return False
    return True
