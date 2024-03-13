import sys, re, os
from dataclasses import dataclass

from src.Converter.convert import Convert

from loguru import logger
from tkinter import filedialog
from langdetect import detect_langs, DetectorFactory

logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add('logs.log', level="INFO")

@dataclass
class Sub:
    """Subtitle management class"""

    subs:tuple[str] = None
    """Variable for loaded subtitles"""

    title:str = ''
    """Variable of the current loaded subtitle title"""

    root:str = ''
    """Root variable of the currently loaded subtitle"""

    def get_subs(self)->tuple[str]:
        """Get subtitles to be processed

        Returns:
            ```py
            list[str]: List of files to be processed (may be unique)
            ```
        """
        try:
            ALL_FORMAT:list[tuple[str, str | list[str] | tuple[str, ...]]] = [
                ("Advanced SubStation Alpha", ("*.ass")),
                ("SubStation Alpha", ("*.ssa")),
                ("SubRip", ("*.srt")),
                ("MicroDVD", ("*.sub")),
                ("Universal Subtitle Format", ("*.usf")),
                ("Timed Text Markup Language", ("*.ttxt")),
                ("WebVTT", ("*.vtt")),
                ("Scenarist Closed Caption", ("*.scc")),
                ("DVD Subtitle System", ("*.idx", "*.sub")),
                ("JACOSub", ("*.jss", "*.js")),
                ("QuickTime Text", ("*.qt.txt")),
                ("RealText", ("*.rt")),
                ("MPL2", ("*.mpl")),
                ("DKS Subtitle Format", ("*.dks")),
                ("Karaoke Lyrics LRC", ("*.lrc"))
            ]
            subs = filedialog.askopenfilenames(title="Select one or multiple subtitle(s)", filetypes=ALL_FORMAT)
            if subs:
                logger.info(f"The user have loaded subtitle(s)")
                self.subs = subs
                return subs
            else:
                logger.info(f"The user haven't loaded subtitle(s)")
                return None

        except FileNotFoundError as e:
            logger.error(f"Error : Unable to find file | {e}")
        except Exception as e:
            logger.error(f"Unknown error | {e}")

    # TODO : Ajouté des informations complémentaires et traité les autres cas de figure, Ajouté des conditions pour évité les erreurs bêtes
    def get_sub_infos(self, sub:str)->dict:
        """Create a `dict` of all informations and extras

        Args:
            ```py
            sub (str): Path to the subtitle file
            ```

        Returns:
            ```py
            dict[str, str | int | list[str | int]]: All the information about the subtitle loaded
            ```
            ```json
            {
                "name": "test",
                "type": "ass",
                "countOfLine" : 150,
                "lang": {
                    "fr": 0.323,
                    "en": 0.556
                },
                ...
                "parts": {
                    ...
                },
                ...
            }
            ```
        """

        # TODO : Ajouté des informations complémentaires
        def get_extras_infos()->dict:
            """Get extra information about the loaded subtitle

            Args:
                ```py
                sub (str): Path of the subtitle file
                ```

            Returns:
                ```py
                dict: Dictionnaire contenant les informations basiques du script
                ```
                ```json
                {
                    "name": "test",
                    "type": "ass",
                    "countOfLine": 150,
                    "weight": 2184576,
                    ...
                }
                ```
            """
            try:
                
                match ext:
                    case '.ass':
                        Parts = self.get_parts(sub)
                        type = "Advanced SubStation Alpha"
                    case '.ssa':
                        type = "SubStation Alpha"
                    case '_':
                        logger.info(f'The file is in an unknown or unsupported format | {ext}')
                
                return {
                    "name": name,
                    "extension": ext,
                    "weight": os.path.getsize(sub),
                    "count_different_styles": len(Parts["Styles"]),
                    "count_line_dialog": len(Parts["Events"]),
                    "lang": self.get_global_langs_dialog(Parts["Events"]),
                    "type": type,
                }
            except Exception as e :
                logger.error(f'Unknown error | {e}')

        try:
            name, ext = os.path.splitext(os.path.basename(sub))
            match ext:
                case '.ass':
                    Parts = self.get_parts(sub)
                case '.ssa':
                    ...
                case '_':
                    logger.info(f'The file is in an unknown or unsupported format | {ext}')
            return {
                "extras": get_extras_infos(),
                "parts": Parts
            }
        except Exception as e:
            logger.error(f'Unknown error | {e}')

    def get_global_langs_dialog(self, Events:dict)->dict[str, float]:
        """Get the most plausible languages for all dialogs

        Args:
            ```py
            Events (dict): Events section of "parts" from get_parts() or get_sub_infos()
            ```

        Returns:
            ```py
            dict[str, float]: Dict of found languages and their rate of involvement
            ```
            ```json
            {
                "fr": 0.822,
                "en": 0.033,
            }
            ```
        """

        def getLangsOfLine()->dict[str, float]:
            """Get the most plausible languages on a line of dialogs

            Returns:
                ```py
                dict[str, float]: Languages in the line and their rate of involvement
                ```
                ```json
                {
                    "fr": 0.456,
                    "en": 0.125,
                    "jp": 0.257,
                    "es": 0.162
                }
                ```
            """
            try:
                # Set the seed to 0 for better quality
                # See here why : https://github.com/Mimino666/langdetect?tab=readme-ov-file#basic-usage
                DetectorFactory.seed = 0
                langs:dict[str, float] = {}
                for lang in detect_langs(line):
                    logger.info(f'The language "{lang}" has been detected at {round(lang.prob,3)*100}%')
                    langs[lang.lang] = round(lang.prob,3)
                return {lang: prob for lang, prob in langs.items() if prob >= 0.01}
            except Exception as e :
                logger.error(f'Unknown error for the line "{line}" | {e}')

        try:
            langs = {}
            total_lines = len(Events.keys())
            for i in Events.keys():
                # Clean the line of "soft" tags
                line = re.sub(r'\\[Nhn]', ' ', Events[i]["Text"])
                logger.info(f'Getting the lang of line "{line}" in process...')
                try:
                    line_langs = getLangsOfLine()
                    for lang, prob in line_langs.items():
                        # Let's do some maths
                        langs[lang] = round(langs.get(lang, 0) + (prob / total_lines), 3)
                except Exception as e:
                    logger.error(f'Unknown error for the line "{line}" | {e}')

            return {langue: prob for langue, prob in langs.items() if prob >= 0.03}
        except Exception as e:
            logger.error(f'Unknown error | {e}')

    def get_parts(self, sub:str)->dict:
        """Extracts the different parts of an ASS file

        Args:
            ```py
            file (str): Path to the ASS file
            ```

        Returns:
            ```py
            dict[str, dict[str, str | dict[str, str]]]: Dict of get_script_info(), get_styles(), get_events()
            ```
            ```json
            {
                "Script Info" : {
                    ...
                },
                "Styles" : {
                    ...
                },
                "Events" : {
                    ...
                }
            }
            ```
        """
        Parts = {}
        try:
            logger.info(f"Read file \"{sub}\"")
            with open(sub, "r", encoding="utf-8") as f:
                lines = f.readlines()
                Parts["Script Info"] = self.get_script_infos(lines)
                Parts["Styles"] = self.get_styles(lines)
                Parts["Events"] = self.get_events(lines)
                
                self.title = Parts["Script Info"]["Title"].replace(":", "-")
                self.root = f'{os.path.dirname(sub)}/'
            
            return Parts

        except Exception as e:
            logger.error(f"Unknown error | {e}")

    def get_script_infos(self, lines:list[str])->dict[str, str]:
        """Extracts information from the [Script Info] section

        Args:
            ```py
            lines (list[str]): Lines of the subtitle script
            ```

        Returns:
            ```py
            dict[str, str | int]: Dict with value of different elements
            ```
            ```json
            {
                ...
                "Title": "Exemple of title"
                "PlayResX": 2560,
                "PlayResY": 1440,
                ...
            }
            ```
        """

        ScriptInfo = {}
        inScriptInfo = True

        try:
            logger.info(f'Entry in the "[Script Infos]" tag')
            for line in lines:
                line = line.strip()
                if line == "[Aegisub Project Garbage]":
                    logger.info(f'Output of the "[Script Info]" tag')
                    inScriptInfo = False
                    break

                if inScriptInfo and not (((";" in  line) or ("[" in line)) or line == ''):
                    logger.info(f'Add line "{line}"')
                    infos = line.split(":", 1)
                    if infos[0] == "Title":
                        self.title = infos[1].strip().replace(":","-")
                    ScriptInfo[infos[0].strip()] = Convert.to_good_type(infos[1].strip())

            return ScriptInfo
        except Exception as e:
            logger.error(f"Unknown error | {e}")

    def get_styles(self, lines:list[str])->dict[str, dict[str, str]]:
        """Extract the different styles from the [V4+ Styles] section

        Args:
            ```py
            lines (list[str]): Lines of the subtitle script
            ```

        Returns:
            ```py
            dict[str, str | int]: Dict with value of different elements
            ```
            ```json
            {
                "Default" : {
                    "FontName" : "Arial",
                    "FontSize" : "24",
                    "PrimaryColour" : "&H000000FF",
                    ...
                },
                ...
            }
            ```
        """
        
        Styles = {}
        inStyles = False

        try:
            for line in lines:
                line = line.strip()
                if line == "[V4+ Styles]":
                    logger.info(f'Entry in the "[V4+ Styles]" tag')
                    inStyles = True
                elif line == "[Events]":
                    logger.info(f'Output of the "[V4+ Styles]" tag')
                    inStyles = False
                    break

                if inStyles and not (((";" in  line) or ("[" in line) or ("Format:" in line)) or line == ''):
                    logger.info(f'Add line "{line}"')
                    infos = line.split(":", 1)[1].strip().split(',', 22)
                    Styles[infos[0].strip()] = {
                        "Fontname" :        Convert.to_good_type(infos[1].strip()),
                        "Fontsize" :        Convert.to_good_type(infos[2].strip()),
                        "PrimaryColour" :   Convert.ASS_color_to_hex_color(infos[3].strip()),
                        "SecondaryColour" : Convert.ASS_color_to_hex_color(infos[4].strip()),
                        "OutlineColour" :   Convert.ASS_color_to_hex_color(infos[5].strip()),
                        "BackColour" :      Convert.ASS_color_to_hex_color(infos[6].strip()),
                        "Bold" :            Convert.to_good_type(infos[7].strip()),
                        "Italic" :          Convert.to_good_type(infos[8].strip()),
                        "Underline" :       Convert.to_good_type(infos[9].strip()),
                        "StrikeOut" :       Convert.to_good_type(infos[10].strip()),
                        "ScaleX" :          Convert.to_good_type(infos[11].strip()),
                        "ScaleY" :          Convert.to_good_type(infos[12].strip()),
                        "Spacing" :         Convert.to_good_type(infos[13].strip()),
                        "Angle" :           Convert.to_good_type(infos[14].strip()),
                        "BorderStyle" :     Convert.to_good_type(infos[15].strip()),
                        "Outline" :         Convert.to_good_type(infos[16].strip()),
                        "Shadow" :          Convert.to_good_type(infos[17].strip()),
                        "Alignment" :       Convert.to_good_type(infos[18].strip()),
                        "MarginL" :         Convert.to_good_type(infos[19].strip()),
                        "MarginR" :         Convert.to_good_type(infos[20].strip()),
                        "MarginV" :         Convert.to_good_type(infos[21].strip()),
                        "Encoding" :        Convert.to_good_type(infos[22].strip())
                    }

            return Styles
        except Exception as e:
            logger.error(f"Unknown error | {e}")

    def get_events(self, lines:list[str])->dict[str, dict[str, str]]:
        """Extract the different dialogs from the [Events] section

        Args:
            ```py
            lines (list[str]):  Lines of the subtitle script
            ```

        Returns:
            ```py
            dict[str, dict[str, str]]:  Dict with value of different elements (numbered from 1 to n)
            ```
            ```json
            {
                "1" : {
                    "Layer" : "0",
                    "Start" : "0:00:01.01",
                    "End" : "0:00:04.01",
                    "Style" : "Default",
                    "Name" : "",
                    ...
                },
                ...
            }
            ```
        """
        Events = {}
        inEvents = False
        count = 1

        try:
            for line in lines:
                line = line.strip()
                if line == "[Events]":
                    logger.info(f'Entry to the "[Events]" tag')
                    inEvents = True

                if inEvents and not (((";" in  line) or ("[" in line) or ("Format:" in line) or ("Comment:" in line)) or line == ''):
                    logger.info(f"Add line \"{line}\"")
                    infos = line.split(":", 1)[1].strip().split(',', 9)

                    Text = infos[9].strip()
                    Tags = self.get_tags(Text)

                    Events[count] = {
                        "Layer" :   Convert.to_good_type(infos[0].strip()),
                        "Start" :   Convert.ASS_timecode_to_standard_timecode(infos[1].strip()),
                        "End" :     Convert.ASS_timecode_to_standard_timecode(infos[2].strip()),
                        "Style" :   Convert.to_good_type(infos[3].strip()),
                        "Name" :    Convert.to_good_type(infos[4].strip()),
                        "MarginL" : Convert.to_good_type(infos[5].strip()),
                        "MarginR" : Convert.to_good_type(infos[6].strip()),
                        "MarginV" : Convert.to_good_type(infos[7].strip()),
                        "Effect" :  Convert.to_good_type(infos[8].strip()),
                        "Text" :    re.sub(r'{.*?}', '', Text),
                        "Tags" :    Tags
                    }

                    count += 1

            return Events
        except Exception as e:
            logger.error(f"Unknown error | {e}")

    def get_tags(self, dialog:str, recursive:bool = False)->dict[str, str | int | list | dict] | None:
        """Extracts tags from a dialog line

        Args:
            ```py
            dialog (str): Dialog line
            ```

        Returns:
            ```py
            dict[str, str | int | list | dict] | None: Returns either a dict or None if there are tags in the dialog.
            ```
            ```json
            {
                "blur" : "2",
                "pos" : {
                    "x": 230,
                    "y": 1120
                },
                "fn" : "Arial",
                ...
            }
            ```
        """
        REGEX_ENTER = r'\{([^}]+)\}'
        REGEX_ENTER_2 = r'(\\[^\\]*)'
        REGEX_NUM = r'\\(a|p|s|u|i|b|k|K|an|be|bord|blur|fa[xyz]|fs|fsc|fsp|fsv|fscx|fscy|fr[xyz]|fe|shad|ko|kf|[xy]bord|[xy]shad)([0-9+\-.]+)'
        REGEX_COLOR = r'\\(1c|2c|3c|4c|c|1a|2a|3a|4a|alpha)(\&.*?\&)'
        REGEX_SPECIAL = r'\\(clip|iclip|fad|fade|move|org|pos)(\(.*?\))'
        REGEX_T = r'\\(t)\((.*?)\)'
        REGEX_STRING = r'\\(fn)(.*)?\\'
        Tags = {}
        try:
            if not recursive:
                logger.info(f'Try to find the tags of the dialog "{dialog}"')
                for group in re.findall(REGEX_ENTER, dialog):
                    tag_num = re.findall(REGEX_NUM, group)
                    tag_color = re.findall(REGEX_COLOR, group)
                    tag_special = re.findall(REGEX_SPECIAL, group)
                    tag_t = re.findall(REGEX_T, group)
                    tag_string = re.findall(REGEX_STRING, group)

                    for tag in tag_num:
                        if re.match(r'(k|K|ko|kf)', tag[0]):
                            if tag[0] not in Tags:
                                Tags[tag[0]] = []
                            Tags[tag[0]].append(int(tag[1]))
                        else:
                            Tags[tag[0]] = int(tag[1])

                    for tag in tag_color:
                        Tags[tag[0]] = Convert.ASS_color_to_hex_color(tag[1])

                    for tag in tag_special:

                        if re.match(r'(iclip|clip)', tag[0]):
                            for value in re.findall(r'\((.*)?\)', tag[1]):
                                Tags[tag[0]] = value

                        if re.match(r'(pos|org)', tag[0]):
                            value = [int(value) for value in re.findall(r'\((.*)?\)', tag[1])[0].split(',',2)]
                            Tags[tag[0]] = {"x" : int(value[0]), "y" : int(value[1])}

                        if re.match(r'(move)', tag[0]):
                            value = [int(value) for value in re.findall(r'\((.*)?\)', tag[1])[0].split(',',6)]
                            Tags[tag[0]] = {"x1" : int(value[0]), "y1" : int(value[1]), "x2" : int(value[2]), "y2" : int(value[3]), "t1" : int(value[4]), "t2" : int(value[5])}

                        if re.match(r'(fad|fade)', tag[0]):
                            value = [int(value) for value in re.findall(r'\((.*)?\)', tag[1])[0].split(',',7)]
                            Tags[tag[0]] = {"a1" : int(value[0]), "a2" : int(value[1]), "a3" : int(value[2]), "t1" : int(value[3]), "t2" : int(value[4]), "t3" : int(value[5]), "t4" : int(value[6])}

                    for tag in tag_t:
                        value = tag[1].split(',', 4)
                        Tags[tag[0]] = {"t1" : int(value[0]), "t2" : int(value[1]), "accel" : int(value[2]), "tags" : self.get_tags(value[3], True)}

                    for tag in tag_string:
                        Tags[tag[0]] = tag[1]

            else:
                logger.info(f'Try to find Tags following a t tag "{dialog}"')
                for group in re.findall(REGEX_ENTER_2, dialog):
                    tag_num = re.findall(REGEX_NUM, group)
                    tag_color = re.findall(REGEX_COLOR, group)
                    tag_special = re.findall(REGEX_SPECIAL, group)
                    tag_t = re.findall(REGEX_T, group)
                    tag_string = re.findall(REGEX_STRING, group)

                    for tag in tag_num:
                        if re.match(r'(k|K|ko|kf)', tag[0]):
                            if tag[0] not in Tags:
                                Tags[tag[0]] = []
                            Tags[tag[0]].append(int(tag[1]))
                        else:
                            Tags[tag[0]] = int(tag[1])

                    for tag in tag_color:
                        Tags[tag[0]] = Convert.ASS_color_to_hex_color(tag[1])

                    for tag in tag_special:

                        if re.match(r'(iclip|clip)', tag[0]):
                            for value in re.findall(r'\((.*)?\)', tag[1]):
                                Tags[tag[0]] = value

                        if re.match(r'(pos|org)', tag[0]):
                            value = [int(value) for value in re.findall(r'\((.*)?\)', tag[1])[0].split(',',2)]
                            Tags[tag[0]] = {"x" : int(value[0]), "y" : int(value[1])}

                        if re.match(r'(move)', tag[0]):
                            value = [int(value) for value in re.findall(r'\((.*)?\)', tag[1])[0].split(',',6)]
                            Tags[tag[0]] = {"x1" : int(value[0]), "y1" : int(value[1]), "x2" : int(value[2]), "y2" : int(value[3]), "t1" : int(value[4]), "t2" : int(value[5])}

                        if re.match(r'(fad|fade)', tag[0]):
                            value = [int(value) for value in re.findall(r'\((.*)?\)', tag[1])[0].split(',',7)]
                            Tags[tag[0]] = {"a1" : int(value[0]), "a2" : int(value[1]), "a3" : int(value[2]), "t1" : int(value[3]), "t2" : int(value[4]), "t3" : int(value[5]), "t4" : int(value[6])}

                    for tag in tag_t:
                        value = tag[1].split(',', 4)
                        Tags[tag[0]] = {"t1" : int(value[0]), "t2" : int(value[1]), "accel" : int(value[2]), "tags" : self.get_tags(value[3], True)}

                    for tag in tag_string:
                        Tags[tag[0]] = tag[1]

            return Tags
        except Exception as e:
            logger.error(f'Unknown error for tag "{tag[0]}" | {e}')

def main():
    """Fonction principal qui va faire le processus de conversion"""
    try:
        SousTitre = Sub()
        for sub in SousTitre.get_subs():
            infos = SousTitre.get_sub_infos(sub)
            Convert.to_SRT(infos["parts"], SousTitre.title, SousTitre.root)
            Convert.to_ASS(infos["parts"], SousTitre.title, '1920x1080', SousTitre.root)

    except TypeError as e:
        logger.error(f"Un sous-titre n'est pas dans le format attendu | {e}")
    except Exception as e:
        logger.error(f'Une erreur inattendu est survenu | {e}')

if __name__ == "__main__":
    main()