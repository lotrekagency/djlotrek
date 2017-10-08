from django.test import TestCase

from djlotrek.utils import group_objects_by_attribute, order_dict_from_list


class UtilsTestCase(TestCase):

    def test_group_objects_by_attribute(self):
        """
        group_objects_by_attribute utils use for group objects and attribute
        together in a dictionary object
        """
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

        self.assertEqual(len(grouped_objects[30]), 2)
        self.assertEqual(len(grouped_objects[26]), 1)
        self.assertEqual(len(grouped_objects[22]), 2)

    def test_order_dict_from_list(self):
        """
        order_dict_from_list utils pass dictionary and ordered key list
        then return ordered dictionary
        """
        my_dict = {
            'italian': 'ciao',
            'english': 'hello',
            'spanish': 'hola',
        }

        ordered_dict = order_dict_from_list(
            my_dict,
            ['english', 'spanish', 'italian', 'german']
        )
        self.assertEqual(
            list(ordered_dict.keys()),
            ['english', 'spanish', 'italian']
        )
