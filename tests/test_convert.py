import unittest
from Converter.convert import Convert

class TestConvert(unittest.TestCase):

	def test_ASS_color_to_hex_color(self):
		self.assertEqual(Convert.ASS_color_to_hex_color('&HAA'), 'AA')
		self.assertEqual(Convert.ASS_color_to_hex_color('&HBBGGRR&'), '#RRGGBB')
		self.assertEqual(Convert.ASS_color_to_hex_color('&HBBGGRRAA'), '#RRGGBBAA')
	
	def test_hex_color_to_ASS_color(self):
		self.assertEqual(Convert.hex_color_to_ASS_color('AA'), '&HAA')
		self.assertEqual(Convert.hex_color_to_ASS_color('#RRGGBB'), '&HBBGGRR&')
		self.assertEqual(Convert.hex_color_to_ASS_color('#RRGGBBAA'), '&HBBGGRRAA')

	def test_hex_RGBA_to_hex_RGB(self):
		self.assertEqual(Convert.hex_RGBA_to_hex_RGB('#RRGGBBAA'), '#RRGGBB')

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

	def test_to_good_type(self):
		# Digit
		self.assertEqual(Convert.to_good_type('1'), 1)
		self.assertEqual(Convert.to_good_type('-1'), -1)

		# Alpha
		self.assertEqual(Convert.to_good_type('chaîne'), 'chaîne')

		# Float
		self.assertEqual(Convert.to_good_type('1.1'), 1.1)

		# List of alpha
		self.assertEqual(Convert.to_good_type(['list']), ['list'])

		# List of digit
		self.assertEqual(Convert.to_good_type(['1']), [1])
		self.assertEqual(Convert.to_good_type(['-1']), [-1])

		# List of float
		self.assertEqual(Convert.to_good_type(['1.1']), [1.1])

		# Dict of alpha
		self.assertEqual(Convert.to_good_type({'key':'value'}), {'key':'value'})

		# Dict of digit
		self.assertEqual(Convert.to_good_type({'key':'1'}), {'key':1})
		self.assertEqual(Convert.to_good_type({'key':'-1'}), {'key':-1})

		# Dict of float
		self.assertEqual(Convert.to_good_type({'key':'1.1'}), {'key':1.1})

		# Dict of list
		self.assertEqual(Convert.to_good_type({'key':['list']}), {'key':['list']})
		self.assertEqual(Convert.to_good_type({'key':['1']}), {'key':[1]})
		self.assertEqual(Convert.to_good_type({'key':['-1']}), {'key':[-1]})
  
		# Hardcore challenge
		TEST = [
			{
   				'key1' : "1",
				'key2' : {
					'list' : ['5.25', {
						'argent' : '56€'
					}]
				}
			},
			{
				'key1' : "1.g.fgh",
				'key2' : {
					'list' : ['5,25', {
						'argent' : '5812147672121742115748'
					}]
				}
			}]
		TEST_OK = [
			{
   				'key1' : 1,
				'key2' : {
					'list' : [5.25, {
						'argent' : '56€'
					}]
				}
			},
			{
				'key1' : "1.g.fgh",
				'key2' : {
					'list' : ['5,25', {
						'argent' : 5812147672121742115748
					}]
				}
			}]
		self.assertEqual(Convert.to_good_type(TEST), TEST_OK)

unittest.main()