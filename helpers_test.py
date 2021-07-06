import unittest
from helpers import *

class CorrectMarkupTestCase(unittest.TestCase):
    def test_group_chat(self):
        self.assertEqual(get_correct_markup('group', "something"), None)

    def test_individual_chat(self):
        self.assertEqual(get_correct_markup('not_group', "something"), "something")


if __name__ == '__main__':
    unittest.main()
