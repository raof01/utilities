# -*- coding: utf-8 

import sys
import unittest

sys.path.append('..')
import utilities


class UtilitiesTest(unittest.TestCase):
    def test_validIpAddress_returnFalse_whenStringContainsIllegalChar(self):
        self.assertFalse(utilities.valid_ip_address('password'))

    def test_validIpAddress_returnFalse_whenIpAddressOutOfRange(self):
        self.assertFalse(utilities.valid_ip_address('255.256.345.0'))

    def test_validIpAddress_returnTrue_whenIpAddressIsLocalHost(self):
        self.assertTrue(utilities.valid_ip_address('localhost'))

    def test_validIpAddress_returnTrue_whenIpAddressIsValid(self):
        self.assertTrue(utilities.valid_ip_address('192.168.0.118'))

    def test_validIpAddress_returnTrue_whenIpAddressIsInValid(self):
        self.assertFalse(utilities.valid_ip_address('192.168.0.'))

    def test_validPort_returnTrue_whenPortIsValid(self):
        self.assertTrue(utilities.valid_port('8889'))

    def test_validPort_returnFalse_whenPortStringContainsNoneDigit(self):
        self.assertFalse(utilities.valid_port('88a9'))

    def test_validPort_returnFalse_whenPortIsOutOfRange(self):
        self.assertFalse(utilities.valid_port('-9'))

    def test_validPort_returnFalse_whenPortIsOutOfRange(self):
        self.assertFalse(utilities.valid_port('0'))

    def test_validPort_returnFalse_whenPortIsOutOfRange(self):
        self.assertFalse(utilities.valid_port('65536'))


if __name__ == '__main__':
    unittest.main()
