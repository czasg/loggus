import unittest

from loggus.formatter import *


class TestStringMethods(unittest.TestCase):

    def test_IsIFormatter(self):
        self.assertTrue(IsIFormatter(TextFormatter))
        self.assertTrue(IsIFormatter(JsonFormatter))


if __name__ == '__main__':
    unittest.main()
