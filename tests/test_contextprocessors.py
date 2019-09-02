from django.test import TestCase, RequestFactory
from djlotrek.context_processors import settings, alternate_seo_url


class ContextProcessorsTestCase(TestCase):

    def test_settings(self):
        """
        settings context processor returns all the settings into your context automagically
        """
        self.assertEqual(
            settings(None)['settings'].AES_ENCRIPTION_KEY, 'abcdefgh01234567'
        )

    def test_alternate_seo_url(self):
        """
        order_dict_from_list utils pass dictionary and ordered key list
        then return ordered dictionary
        """
        request = RequestFactory().get(
            '/about',
            HTTP_HOST='localhost:8000'
        )
        self.assertEqual(
            alternate_seo_url(request)['alternate_urls']['it'],
            'http://localhost:8000/about'
        )
        self.assertEqual(
            alternate_seo_url(request)['alternate_urls']['en'],
            'http://localhost:8000/en/about'
        )
