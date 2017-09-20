import os
import mock

import datetime

from django.test import TestCase

from djlotrek.templatetags.djlotrek_tags import absolute_url, auto_update_year_range

from django.test import RequestFactory

from mock import Mock, patch

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
        self.assertNotEqual(abs_url, '/')


    @patch('djlotrek.templatetags.djlotrek_tags.datetime')
    def test_auto_update_year_range(self,datetime_now):
        datetime_now.datetime.now.return_value = datetime.date(2017,12,12)
        current_year = 2017

        tested_year = auto_update_year_range()
        self.assertEqual(tested_year, current_year)
        self.assertNotEqual(tested_year, current_year+1)

        tested_year_start = auto_update_year_range('1995')

        composed_year = "1995-"+str(current_year)
        self.assertEqual(tested_year_start, composed_year)
        self.assertNotEqual(tested_year_start, "-")




