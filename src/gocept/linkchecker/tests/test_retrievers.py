# Copyright (c) 2004 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import unittest

from Products.Archetypes.tests.common import *
from Products.Archetypes.tests.utils import *

from Products.Archetypes.tests.test_sitepolicy import makeContent
from Products.CMFCore.utils import getToolByName

from gocept.linkchecker.retrievers import RetrieverEvent, \
        RetrieverLink, RichTextRetriever

from gocept.linkchecker.tests.base import LinkCheckerTestCase


class LinkCheckerTest(LinkCheckerTestCase):

    def test_event_retriever(self):
        self.loginAsPortalOwner()
        links = ["http://www.asdf.org", "http://www.bauhaus.de",
                 "ftp://www.goodbye.de", "http://www.google.de/img.png"]

        text = " ".join( [ """"asdf":%s\n""" % x for x in links ])
        lc = getToolByName(self.portal, 'portal_linkchecker')

        url = "http://asdf.org"
        event = makeContent(self.portal, portal_type="Event", id="asdf")
        event.edit(event_url=url)
        event.setText(text)

        links = RetrieverEvent().retrieveLinks(event)

        self.assertEqual(len(links), 5)
        self.assertEqual(links[0], url)

        # RichTextRetriever doesn't find the plain url
        links = RichTextRetriever().retrieveLinks(event)
        self.assertEqual(links[0], "http://www.google.de/img.png")
        self.assertEqual(len(links), 4)

    def test_link_retriever(self):
        self.loginAsPortalOwner()
        lc = getToolByName(self.portal, 'portal_linkchecker')

        url = "http://www.asdf.org/asdf?asdf"
        ob = makeContent(self.portal, portal_type="Link", id="asdf")
        ob.edit(url)

        links = RetrieverLink().retrieveLinks(ob)

        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], url)

    def test_document_html_retriever(self):
        self.loginAsPortalOwner()
        links = ["http://www.asdf.org", "http://www.bauhaus.de",
                 "ftp://www.goodbye.de", "http://www.google.de/img.png"]
        text = " ".join( [ """<a href="%s">asdf</a>""" % x for x in links[:-1] ])
        text += """<img src="%s"/>""" % links[-1]

        lc = getToolByName(self.portal, 'portal_linkchecker')

        url = "http://www.asdf.org/asdf?asdf"
        ob = makeContent(self.portal, portal_type="Document", id="asdf")
        ob.setText(text)

        links_ob = RichTextRetriever().retrieveLinks(ob)
        self.assertEqualLinks(links, links_ob)

    def test_document_stx_retriever(self):
        self.loginAsPortalOwner()
        links = ["http://www.asdf.org", "http://www.bauhaus.de",
                 "ftp://www.goodbye.de", "http://www.google.de/img.png"]

        text = " ".join( [ """"asdf":%s\n""" % x for x in links ])

        lc = getToolByName(self.portal, 'portal_linkchecker')

        url = "http://www.asdf.org/asdf?asdf"
        ob = makeContent(self.portal, portal_type="Document", id="asdf")
        ob.setText(text, mimetype='text/structured')

        # RichTextRetriever should work just as well.
        links_ob = RichTextRetriever().retrieveLinks(ob)
        self.assertEqualLinks(links, links_ob)

    def assertEqualLinks(self, links, links_ob):
        self.assertEqual(len(links), len(links_ob))
        for x in links_ob:
            self.assert_(x in links)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LinkCheckerTest))
    return suite
