import os
import mock

from django.test import TestCase

from djlotrek.templatetags.djlotrek_filters import key, is_in, is_not_in, get_class, get_sorted


class TemplateFiltersTestCase(TestCase):

    def setUp(self):
        pass

    def test_key(self):
        """Our beloved get_host_url utility"""
        my_dict = {'mykey' : 'value'}
        self.assertEqual(key(my_dict, 'mykey'), 'value')
        self.assertEqual(key(my_dict, 'nokey'), None)

    def test_is_in(self):
        """Our beloved get_host_url utility"""
        self.assertEqual(is_in('ciao', 'hello,ciao'), True)
        self.assertEqual(is_in('hola', 'hello,ciao'), False)

    def test_is_not_in(self):
        """Our beloved get_host_url utility"""
        self.assertEqual(is_not_in('ciao', 'hello,ciao'), False)
        self.assertEqual(is_not_in('hola', 'hello,ciao'), True)

    def test_get_class(self):
        """Our beloved get_host_url utility"""
        a = 1
        my_dict = {'mykey' : 'value'}
        self.assertEqual(get_class(a), 'int')
        self.assertEqual(get_class(my_dict), 'dict')

    def test_get_sorted(self):
        """Our beloved get_host_url utility"""
        a = [10,2,3,5,1]
        self.assertEqual(get_sorted(a), [1,2,3,5,10])
