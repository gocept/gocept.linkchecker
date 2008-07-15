==============
CMFLinkChecker
==============

Meta
====

Copyright (c) 2003-2005 gocept gmbh & co. kg
See also LICENSE.txt

:Valid for:  CMFLinkChecker 1.9
:Author:     Christian Theune <ct@gocept.com>,
             Christian Zagrodnick <cz@gocept.com>
:CVS:        $Id$


What is CMFLinkChecker
======================

CMFLinkchecker is a Plone product which both monitors the availability
of links (URLs) within the *content* o the site and shows which objects are
referencing each other.

- High level overview

  A coloured and grouped list of all links of the site gives a detailed and
  high level overview on the status of the links (Balanced Score Card).

- Author and object level overview

  Additional reporting is available to the content authors who can see their
  personal link status page (My Links) as well as an overview over all links in
  one object (Links tab of object)

- Referenced by

  A new portlet shows if an object is referenced by another object (due to
  HTML anchor or img tag).

- Email notifications

  The email notification completes the set of reporting tools by providing in
  time information to the content authors when links break or recover.


How to install or upgrade
=========================

See INSTALL.txt


Acknowledgements
================

The initial development was sponsored by the Bertelsmann Foundation 
(http://www.bertelsmann-stiftung.de/) in late 2003.

The bi-direcitonal reference management was sponsored by the Land Office of
Criminal Investigation of a German state in 2004-2005.


What? Problems?
===============

If you encounter any problems or have an inquiry about the product, feel free
to contact Christian Theune:"ct@gocept.com" or put a bug report in
http://bugs.gocept.com. Any feedback is appreciated.

Commercial support is available from gocept. Contact via mail@gocept.com or
+49 (0)345 122 9889 0


Known Issues
============

Problems with QueueCatalog
++++++++++++++++++++++++++

When your portal_catalog is a QueueCatalog it is not possible to install the
CMFLinkchecker.
