import unittest
from src.Sub.sub import Sub

class TestSub(unittest.TestCase):

	def test_getSubs(self):
		self.assertEqual(Sub.getSubs(), ('C:/Users/Im4g1/Documents/Cours/Mini_Projet/SUBMODULE/tests/test.ass',))

unittest.main()