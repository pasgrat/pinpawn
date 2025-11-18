
import unittest
import sys

sys.path.append('..')
from utils import _n2c, _c2n

class TestUtils(unittest.TestCase):

    def test_n2c(self):
        self.assertEqual(_n2c('a1'), (0, 0))
        self.assertEqual(_n2c('h8'), (7, 7))
        self.assertEqual(_n2c('e4'), (3, 4))

    def test_c2n(self):
        self.assertEqual(_c2n(0, 0), 'a1')
        self.assertEqual(_c2n(7, 7), 'h8')
        self.assertEqual(_c2n(3, 4), 'e4')

    def test_conversion_roundtrip(self):
        # tests that converting back and forth yields the original
        notation_original = 'd5'
        coords = _n2c(notation_original)
        notation_new = _c2n(coords[0], coords[1])
        self.assertEqual(notation_original, notation_new)