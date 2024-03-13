import unittest
from Sub.sub import Sub

Subtitle = Sub()

ASS_TEST = 'C:/Users/Im4g1/Documents/Cours/Mini_Projet/SUBMODULE/doc/test.ass'

SCRIPT_INFO_TEST = {
    "Title": "Default Aegisub file",
    "ScriptType": "v4.00+",
    "WrapStyle": 0,
    "ScaledBorderAndShadow": "yes",
    "YCbCr Matrix": "None",
    "PlayResX": 1280,
	"PlayResY": 720
}

STYLES_TEST = {
	"Default": {
		"Fontname": "Arial",
		"Fontsize": 48,
		"PrimaryColour": "#FFFF00FF",
		"SecondaryColour": "#000000FF",
		"OutlineColour": "#00000000",
		"BackColour": "#00000000",
		"Bold": 0,
		"Italic": "-1",
		"Underline": 0,
		"StrikeOut": 0,
		"ScaleX": 100,
		"ScaleY": 100,
		"Spacing": 0,
		"Angle": 0,
		"BorderStyle": 1,
		"Outline": 2,
		"Shadow": 2,
		"Alignment": 2,
		"MarginL": 10,
		"MarginR": 10,
		"MarginV": 10,
		"Encoding": 1
	}
}

EVENTS_TEST = {
	"1": {
		"Layer": 0,
		"Start": "00:00:00.000",
		"End": "00:00:02.000",
		"Style": "Default",
		"Name": "",
		"MarginL": 0,
		"MarginR": 0,
		"MarginV": 0,
		"Effect": "",
		"Text": "Bonjour tout le monde.",
		"Tags": {
			"u": 1,
			"c": "#000000",
			"3c": "#000000",
			"fn": "Bahnschrift Condensed"
		}
	},
	"2": {
		"Layer": 0,
		"Start": "00:00:03.980",
		"End": "00:00:05.000",
		"Style": "Credit",
		"Name": "",
		"MarginL": 0,
		"MarginR": 0,
		"MarginV": 0,
		"Effect": "",
		"Text": "Hello everyone.",
		"Tags": {
			"blur": 2,
			"fs": 84,
			"pos": {
				"x": 230,
				"y": 1120
			}
		}
	},
	"3": {
		"Layer": 0,
		"Start": "00:00:07.980",
		"End": "00:00:09.280",
		"Style": "Karaoke EN",
		"Name": "",
		"MarginL": 0,
		"MarginR": 0,
		"MarginV": 0,
		"Effect": "",
		"Text": "Hola a todos.",
		"Tags": {
			"b": 1,
			"K": [
				29,
				21,
				40
			]
		}
	},
	"4": {
		"Layer": 0,
		"Start": "00:00:11.980",
		"End": "00:00:13.280",
		"Style": "Karaoke EN",
		"Name": "",
		"MarginL": 0,
		"MarginR": 0,
		"MarginV": 0,
		"Effect": "",
		"Text": "Boo!",
		"Tags": {
			"an": 5,
			"fscx": 100,
			"fscy": 100,
			"t": {
				"t1": 0,
				"t2": 0,
				"accel": 500,
				"tags": {
					"fscx": 100,
					"fscy": 100
				}
			}
		}
	},
	"5": {
		"Layer": 0,
		"Start": "00:00:14.000",
		"End": "00:00:15.000",
		"Style": "Karaoke EN",
		"Name": "",
		"MarginL": 0,
		"MarginR": 0,
		"MarginV": 0,
		"Effect": "",
		"Text": "No Tag ?!",
		"Tags": {}
	}
}

PARTS_TEST = {
	"Script Infos" : SCRIPT_INFO_TEST,
	"Styles": STYLES_TEST,
	"Events": EVENTS_TEST
}

LINES = open(ASS_TEST).readlines()

TAGS_TEST = {
    "u": 1,
    "c": "#000000",
    "fn": "Bahnschrift Condensed",
    "3c": "#000000"
}

class TestSub(unittest.TestCase):

	# def test_get_subs(self):
	# 	self.assertEqual(Subtitle.get_subs(), (ASS_TEST,))

	def test_get_parts(self):
		self.assertEqual(Subtitle.get_parts(ASS_TEST), PARTS_TEST)

	def test_get_script_infos(self):
		self.assertEqual(Subtitle.get_script_infos(LINES), SCRIPT_INFO_TEST)

	def test_get_styles(self):
		self.assertEqual(Subtitle.get_styles(LINES), STYLES_TEST)

	def test_get_events(self):
		self.assertEqual(Subtitle.get_events(LINES), EVENTS_TEST)
  
	def test_get_tags(self):
		self.assertEqual(Subtitle.get_tags(LINES[21]), TAGS_TEST)

unittest.main()