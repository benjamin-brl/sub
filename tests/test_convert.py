import unittest
from src.Converter.convert import Convert

class TestConvert(unittest.TestCase):

	def test_ASS_color_to_hex_color(self):
		self.assertEqual(Convert.ASS_color_to_hex_color('&HAA'), 'AA')
		self.assertEqual(Convert.ASS_color_to_hex_color('&HBBGGRR&'), '#RRGGBB')
		self.assertEqual(Convert.ASS_color_to_hex_color('&HBBGGRRAA'), '#RRGGBBAA')
	
	def test_hex_color_to_ASS_color(self):
		self.assertEqual(Convert.hex_color_to_ASS_color('AA'), '&HAA')
		self.assertEqual(Convert.hex_color_to_ASS_color('#RRGGBB'), '&HBBGGRR&')
		self.assertEqual(Convert.hex_color_to_ASS_color('#RRGGBBAA'), '&HBBGGRRAA')

	def test_ASS_timecode_to_standard_timecode(self):
		self.assertEqual(Convert.ASS_timecode_to_standard_timecode('1:56:47.28'), '01:56:47.280')
		self.assertEqual(Convert.ASS_timecode_to_standard_timecode('12:30:21.45'), '12:30:21.450')

	def test_SRT_timecode_to_standard_timecode(self):
		self.assertEqual(Convert.SRT_timecode_to_standard_timecode('01:56:47,280'), '01:56:47.280')
		self.assertEqual(Convert.SRT_timecode_to_standard_timecode('12:30:21,450'), '12:30:21.450')

	def test_standard_timecode_to_ASS_timecode(self):
		self.assertEqual(Convert.standard_timecode_to_ASS_timecode('01:56:47.280'), '1:56:47.28')
		self.assertEqual(Convert.standard_timecode_to_ASS_timecode('12:30:21.450'), '12:30:21.45')

	def test_standard_timecode_to_SRT_timecode(self):
		self.assertEqual(Convert.standard_timecode_to_SRT_timecode('01:56:47.280'), '01:56:47,280')
		self.assertEqual(Convert.standard_timecode_to_SRT_timecode('12:30:21.450'), '12:30:21,450')

unittest.main()