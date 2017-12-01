import copy

from nimo import test
from nimo import utils as nimo_utils


class NimoUtilTestCase(test.TestCase):
    _CONF = copy.deepcopy(nimo_utils.CONF)

    def setUp(self):
        super(NimoUtilTestCase, self).setUp()

    def tearDown(self):
        nimo_utils.CONF = copy.deepcopy(self._CONF)
        super(NimoUtilTestCase, self).tearDown()

    def test_libvirt_opts_registration(self):
        CONF = nimo_utils.CONF
        nimo_utils.register_libvirt_opts()
        virt_cfg_grp_name = 'libvirt'
        virt_cfg_opts = ['uri']
        self.assertIn(virt_cfg_grp_name, CONF)
        for opt in virt_cfg_opts:
            self.assertIn(opt, CONF.get(virt_cfg_grp_name))

    def test_nimo_default_opts_registration(self):
        CONF = nimo_utils.CONF
        nimo_utils.register_default_nimo_opts()
        nimo_cfg_opts = ['console_path']
        for opt in nimo_cfg_opts:
            self.assertIn(opt, CONF)
