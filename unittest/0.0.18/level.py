import unittest

from loggus.level import *


class TestStringMethods(unittest.TestCase):

    def test_IsLevel(self):
        self.assertTrue(IsLevel(DEBUG))
        self.assertTrue(IsLevel(INFO))
        self.assertTrue(IsLevel(WARNING))
        self.assertTrue(IsLevel(ERROR))
        self.assertTrue(IsLevel(PANIC))

    def test_GetAllLevels(self):
        self.assertEqual(GetAllLevels(), [DEBUG, INFO, WARNING, ERROR, PANIC])


if __name__ == '__main__':
    unittest.main()
