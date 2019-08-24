import datetime
from mock import patch

from django.test import TestCase, RequestFactory

from djlotrek.templatetags.djlotrek_tags import (
    absolute_url,
    auto_update_year_range,
    active
)


class TemplateTagsTestCase(TestCase):

    def test_absolute_url(self):
        """
        templatetags absolute_url use for get full url of the current
        request context it pass context and url and return full url
        """
        request_factory = RequestFactory()
        request = request_factory.get('/path')
        request.META['HTTP_HOST'] = 'localhost'

        context = {
            'request': request
        }

        abs_url = absolute_url(context, '')
        self.assertEqual(abs_url, '')

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
        """
        templatetags absolute_url use for get full url of the current
        request context it pass context and url it will return blank
        string when context is none
        """
        context = {}

        abs_url = absolute_url(context, '/ciao/')
        self.assertEqual(abs_url, '/ciao/')
        self.assertNotEqual(abs_url, '/')

    @patch('djlotrek.templatetags.djlotrek_tags.datetime')
    def test_auto_update_year_range(self, datetime_now):
        """
        templatetags auto_update_year_range pass string of start year
        and return itself when current year is equal to start year.
        If start year is provided and not current year it will return
        year range in format '{start_year} - {current_year}'. Otherwise,
        it will return current year when start not provided
        """
        datetime_now.datetime.now.return_value = datetime.date(2017, 12, 12)
        current_year = 2017

        tested_year = auto_update_year_range()
        self.assertEqual(tested_year, current_year)
        self.assertNotEqual(tested_year, current_year + 1)

        tested_year_start = auto_update_year_range('1995')

        composed_year = "1995-" + str(current_year)
        self.assertEqual(tested_year_start, composed_year)
        self.assertNotEqual(tested_year_start, "-")

        datetime_now.datetime.now.return_value = datetime.date(2019, 12, 12)
        self.assertEqual(auto_update_year_range(2019), 2019)

    def test_active(self):
        request = RequestFactory().get('/sitemap.xml')
        self.assertEqual(active(
            {'request': request}, 'sitemap'
        ), 'active')

        request = RequestFactory().get('/other')
        self.assertEqual(active(
            {'request': request}, ''
        ), '')
