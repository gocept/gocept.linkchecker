# Copyright (c) 2005-2006 gocept. All rights reserved.
# See also LICENSE.txt
# $Id$

# WARNING: do not make changes here! Change customconfig.py (see
# customconfig_example.py)

# Try to retrieve any archetype on (almost) every reindex?
# NOTE: this patches ArcheTypes.CatalogMultiplex and *could* have some
# impact on performance.
SUPPORT_ATBASE = True
PROTOCOL_VERSION = 2

PROJECTNAME = 'CMFLinkChecker'
SKINS_DIR = 'skins'
GLOBALS = globals()

LMS_REGISTRATION = "http://www.gocept.com/portal_lms_registration"
WEBSERVICE = "http://lms.gocept.com/v2"

# for unit testing
TESTING_WEBSERVICE = "http://lms.gocept.com/v2"
TESTING_CLIENTID = "testing"
TESTING_PASSWORD = "password"

# import customconfig:
try:
    from Products.CMFLinkChecker.customconfig import *
except ImportError:
    pass
