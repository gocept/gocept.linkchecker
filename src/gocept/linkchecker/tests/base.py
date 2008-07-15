from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc

from Products.Archetypes import public as atapi
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase.setup import default_password, portal_owner


@onsetup
def setup_linkchecker_policy():
    fiveconfigure.debug_mode = True
    import Products.CMFLinkChecker
    zcml.load_config('configure.zcml', Products.CMFLinkChecker)
    fiveconfigure.debug_mode = False

    ztc.installProduct("ZCatalog")
    ztc.installProduct("CMFLinkChecker")

setup_linkchecker_policy()
ptc.setupPloneSite(products=['Products.CMFLinkChecker'])


class CMFLinkCheckerTestCase(ptc.FunctionalTestCase):

    def __init__(self, *args, **kw):
        super(CMFLinkCheckerTestCase, self).__init__(*args, **kw)
        self.portal_owner = portal_owner
        self.default_password = default_password
