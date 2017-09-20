import os
import mock

from django.test import TestCase

from djlotrek.templatetags.djlotrek_tags import absolute_url

from django.test import RequestFactory


class TemplateTagsTestCase(TestCase):

    def setUp(self):
        pass

    def test_absolute_url(self):
        """Our beloved get_host_url utility"""
        request_factory = RequestFactory()
        request = request_factory.get('/path')
        request.META['HTTP_HOST'] = 'localhost'

        context = {
            'request' : request
        }

        abs_url = absolute_url(context, '/ciao/')
        self.assertEqual(abs_url, 'http://localhost/ciao/')

        abs_url = absolute_url(context, 'ciao/')
        self.assertEqual(abs_url, 'http://localhost/ciao/')

        abs_url = absolute_url(context, 'ciao')
        self.assertEqual(abs_url, 'http://localhost/ciao')

        abs_url = absolute_url(context, 'ciao/a/tutti')
        self.assertEqual(abs_url, 'http://localhost/ciao/a/tutti')

        abs_url = absolute_url(context, 'ciao/a/tutti?language=it')
        self.assertEqual(abs_url, 'http://localhost/ciao/a/tutti?language=it')

    def test_absolute_url_without_request(self):
        """Our beloved get_host_url utility"""
        context = {}

        abs_url = absolute_url(context, '/ciao/')
        self.assertEqual(abs_url, '/ciao/')