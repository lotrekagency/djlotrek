import os
import mock

from django.test import TestCase
from requests import RequestException

from django.test import RequestFactory

from djlotrek.utils import group_objects_by_attribute, order_dict_from_list
from djlotrek.aes import decode


class UtilsTestCase(TestCase):

    def setUp(self):
        pass

    def test_group_objects_by_attribute(self):
        """Our beloved get_host_url utility"""
        class Human():
            name = ''
            age = 0

            def __init__(self, name, age):
                self.name = name
                self.age = age

        humans = []
        humans.append(Human('Andrea', 30))
        humans.append(Human('Marco', 30))
        humans.append(Human('Salvatore', 22))
        humans.append(Human('Giulio', 22))
        humans.append(Human('Ale', 26))

        grouped_objects = group_objects_by_attribute(humans, 'age')

        self.assertEqual (len(grouped_objects[30]), 2)
        self.assertEqual (len(grouped_objects[26]), 1)
        self.assertEqual (len(grouped_objects[22]), 2)

    def test_order_dict_from_list(self):
        """Our beloved get_host_url utility"""
        my_dict = {
            'italian' : 'ciao',
            'english' : 'hello',
            'spanish' : 'hola',
        }

        ordered_dict = order_dict_from_list(my_dict, ['english', 'spanish', 'italian', 'german'])
        self.assertEqual(list(ordered_dict.keys()), ['english', 'spanish', 'italian'])