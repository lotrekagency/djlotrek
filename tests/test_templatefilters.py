from django.test import TestCase

from djlotrek.templatetags.djlotrek_filters import (
    key,
    is_in,
    is_not_in,
    get_class,
    get_sorted,
    media_url,
    regex_match
)


class TemplateFiltersTestCase(TestCase):

    def test_key(self):
        """
        templatefilter key is use for get value from dictionary object it's
        pass dictionary object and key name then return value if
        key exists otherwise return none
        """
        my_dict = {'mykey': 'value'}
        self.assertEqual(key(my_dict, 'mykey'), 'value')
        self.assertEqual(key(my_dict, 'nokey'), None)

    def test_is_in(self):
        """
        templatefilter is_in use check arguments from string list separate
        by comma (,) it pass value and arguments string then return a
        boolean object of existen of value
        """
        self.assertEqual(is_in('ciao', 'hello,ciao'), True)
        self.assertEqual(is_in('hola', 'hello,ciao'), False)

    def test_is_not_in(self):
        """
        templatefilter is_not_in use to check not existen arguments
        from string list separate by comma (,) it pass value and
        arguments string then return a boolean object of not existen of value
        """
        self.assertEqual(is_not_in('ciao', 'hello,ciao'), False)
        self.assertEqual(is_not_in('hola', 'hello,ciao'), True)

    def test_get_class(self):
        """
        templatefilter get_class use to get a class name of retrieved class
        """
        a = 1
        my_dict = {'mykey': 'value'}
        self.assertEqual(get_class(a), 'int')
        self.assertEqual(get_class(my_dict), 'dict')

    def test_get_sorted(self):
        """
        templatefilter get_sorted retrive list objects and return sorted
        version of it
        """
        a = [10, 2, 3, 5, 1]
        self.assertEqual(get_sorted(a), [1, 2, 3, 5, 10])

    def test_media_url(self):
        """
        templatefilter media_url retrive a media object and get the url
        """
        self.assertEqual(media_url(None), '')
        self.assertEqual(media_url({'a' : 2}), '')

    def test_regex_match(self):
        """
        templatefilter regex_match return True if regex matches
        """
        self.assertEqual(
            regex_match(
                'Cats are smarter than dogs', '(.*) are (.*?) .*'
            ), True
        )

        self.assertEqual(
            regex_match(
                'Cats are smarter than dogs', '(.*) àre (.*?) .*'
            ), False
        )
