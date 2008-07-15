##############################################################################
#
# Copyright (c) 2003 gocept gmbh & co. kg. All rights reserved.
#
# See also LICENSE.txt
#
##############################################################################
"""CMFLinkChecker - retriever for ZWiki pages

$Id$"""

from Products.ZWiki.ZWikiPage import ZWikiPage
from Products.CMFLinkChecker.retrievers import retrieveHTML, retrievers, resolveRelativeLink

# This is way out of date. Therefor I am disallowing any usage.
raise Exception, "Can't use WikiRetriever -- it's very out of date and does not work"

def retrieverWiki(linkchecker, object):
    """Usable for ZWiki.ZWikiPage objects."""
    if not isinstance(object, ZWikiPage):   # XXX ... report warning here
        return
    html = object.render()
    links = retrieveHTML(html)

    wiki_links = [ "/"+x for x in object.canonicalLinks()]
    # Handle link registration
    for link in links:
        # No Wiki editlinks
        if link.find("editform?page") != -1:
            continue
        if link.find("createform?page") != -1:
            continue
        if link.find("in_reply_to") != -1:
            continue
        if link.find("#") != -1 and link.find("@") != -1:               # Probably a comment
            continue

        # No internal wiki Links
        is_wiki_link = 0
        for x in wiki_links:
            if link.endswith(x):
                is_wiki_link = 1
                break
        if is_wiki_link:
            continue

        link = resolveRelativeLink(link, object)
        info = linkchecker.getInfoForURL(link)
        info.addObject(object)

retrievers.register(retrieverWiki, default=["Wiki Page"])

## Need to monkeypatch them

def new_edit(self, page=None, text=None, type=None, title='',
             timeStamp=None, REQUEST=None,
             subjectSuffix='', log='', check_conflict=1, # temp (?)
             leaveplaceholder=1, updatebacklinks=1,
             subtopics=None):
    """asdf"""
    old_edit(self, page, text, type, title, timeStamp, REQUEST, 
                subjectSuffix, log, check_conflict, 
                leaveplaceholder, updatebacklinks, subtopics)
    self.lc_updatelinks(redirect=0)

from Products.ZWiki.Editing import EditingSupport

old_edit = EditingSupport.edit
EditingSupport.edit = new_edit
