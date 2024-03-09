import unittest
from src.Converter.convert import Convert

class TestSub(unittest.TestCase):

	def test_getSubs(self):
		self.assertEqual(Convert.ASScolor2Hex('&HBBGGRR'), '#RRGGBB')

unittest.main()