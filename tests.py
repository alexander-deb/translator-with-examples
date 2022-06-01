import shelve
import unittest

from translate import translate_message


class TestStringMethods(unittest.TestCase):
    def test_please(self):
        with shelve.open('assets/user_langs') as database:
            with shelve.open('assets/test1') as testing:
                self.assertEqual(translate_message(
                    '977304455', database, 'please'), testing['please'])

    def test_hello(self):
        with shelve.open('assets/user_langs') as database:
            with shelve.open('assets/test1') as testing:
                self.assertEqual(translate_message(
                    '977304455', database, 'hello'), testing['hello'])


if __name__ == '__main__':
    unittest.main()
