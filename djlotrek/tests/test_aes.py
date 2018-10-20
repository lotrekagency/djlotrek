from django.test import TestCase

import djlotrek.aes


class AESTestCase(TestCase):

    def test_aes(self):
        """
        aes.encode() module pass a raw string and return
        AES encoded string and aes.decode() module pass
        an encoded AES string and return decoded string
        """
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

        enc = djlotrek.aes.encode('m.marot@eglab.it')
        dec = djlotrek.aes.decode(enc)
        self.assertEqual(dec, 'm.marot@eglab.it')
