import unittest
from src.protocols.crsf import CRSF_RC_Generator

class TestCRSF(unittest.TestCase):
    crsf = CRSF_RC_Generator()

    def setUp(self):
        print("start")
    def tearDown(self):
        print("end")

    def test_disarm(self):
        disarm_packet = TestCRSF.crsf.build_rc_packet(992,992,189,992,189,992,992,992,
                                            992,992,992,992,992,992,992,992)
        self.assertEqual(disarm_packet, b'\xc8\x18\x16\xe0\x03_/\xc0\xd7\x0b\xf0\x81\x0f|\xe0\x03\x1f\xf8\xc0\x07>\xf0\x81\x0f|\x9d')

    def test_arm(self):
        arm_packet    = TestCRSF.crsf.build_rc_packet(992,992,189,992,1800,992,992,992,
                                            992,992,992,992,992,992,992,992)
        self.assertEqual(arm_packet, b'\xc8\x18\x16\xe0\x03_/\xc0\x87p\xf0\x81\x0f|\xe0\x03\x1f\xf8\xc0\x07>\xf0\x81\x0f|^')