import os
import mock

from django.test import TestCase
from requests import RequestException

from django.test import RequestFactory

import djlotrek.aes


class AESTestCase(TestCase):

    def setUp(self):
        pass

    def test_aes(self):
        """Our beloved get_host_url utility"""
        enc = djlotrek.aes.encode('m.allegra92@gmail.com')
        dec = djlotrek.aes.decode(enc)
        self.assertEqual(dec, 'm.allegra92@gmail.com')
        
        enc = djlotrek.aes.encode('stagi.andrea@gmail.com')
        dec = djlotrek.aes.decode(enc)
        self.assertEqual(dec, 'stagi.andrea@gmail.com')

        enc = djlotrek.aes.encode('m.allegrà@gmail.com')
        dec = djlotrek.aes.decode(enc)
        self.assertEqual(dec, 'm.allegrà@gmail.com')

        enc = djlotrek.aes.encode('marco@lotrek.it')
        dec = djlotrek.aes.decode(enc)
        self.assertEqual(dec, 'marco@lotrek.it')

        enc = djlotrek.aes.encode('marco123@gmail.com')
        dec = djlotrek.aes.decode(enc)
        self.assertEqual(dec, 'marco123@gmail.com')

        enc = djlotrek.aes.encode('m.marotta@eglab.it')
        dec = djlotrek.aes.decode(enc)
        self.assertEqual(dec, 'm.marotta@eglab.it')
