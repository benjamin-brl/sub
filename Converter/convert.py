import json, random, string
from dataclasses import dataclass
from loguru import logger

@dataclass
class Convert():
    """Class for converting various elements to "standard" and/or special elements"""

    @staticmethod
    def ASS_color_to_hex_color(color:str)->str|None:
        """Converts ASS color formatting to hexadecimal color format

        Args:
            ```py
            color (str): Color to convert
            ```

        Returns:
            ```py
            str: Convert color
            ```
        
        &H`BBGGRR`& --> #`RRGGBB`
        """
        try:
            logger.info(f'Convert the following color "{color}"')
            if len(color) == 4:
                return f"{color[2:4]}"
            elif len(color) == 9:
                return f"#{color[6:8]}{color[4:6]}{color[2:4]}"
            elif len(color) == 10:
                return f"#{color[6:8]}{color[4:6]}{color[2:4]}{color[8:10]}"
            else:
                None

        except Exception as e:
            logger.error(f'Unknown error when converting the "{color}" color | {e}')

    @staticmethod
    def hex_color_to_ASS_color(color:str)->str|None:
        """Converts hexadecimal color formatting to ASS format

        Args:
            ```py
            color (str): Color to convert
            ```

        Returns:
            ```py
            str: Convert color
            ```
        
        #`RRGGBB` --> &H`BBGGRR`&
        """
        try:
            logger.info(f'Convert the following color "{color}"')
            if len(color) == 2:
                return f"&H{color}"
            elif len(color) == 7:
                return f"&H{color[5:7]}{color[3:5]}{color[1:3]}&"
            elif len(color) == 9:
                return f"&H{color[5:7]}{color[3:5]}{color[1:3]}{color[7:9]}"
            else:
                return None

        except Exception as e:
            logger.error(f'Unknown error when converting the "{color}" color | {e}')

    @staticmethod
    def hex_RGBA_to_hex_RGB(color:str)->str|None:
        """Converts RGBA hexadecimal color formatting to RGB hexadecimal

        Args:
            ```py
            color (str): Color to convert
            ```

        Returns:
            ```py
            str: Convert color
            ```
        
        #`RRGGBBAA` --> #`RRGGBB`
        """
        try:
            logger.info(f'Convert the following color "{color}"')
            if len(color) == 9:
                return color[:-2]
            else:
                return None

        except Exception as e:
            logger.error(f'Unknown error when converting the "{color}" color | {e}')

    @staticmethod
    def ASS_timecode_to_standard_timecode(timecode:str)->str:
        """Converts ASS format timecode to standard format

        Args:
            ```py
            timecode (str): Timecode to convert
            ```

        Returns:
            ```py
            time: Convert timecode
            ```
        """
        try:
            logger.info(f'Converts the following ASS timecode "{timecode}" to standard timecode format')
            h, m, s = timecode.split(':', 3)
            return f"{h.zfill(2)}:{m}:{s}0"
        except Exception as e:
            logger.error(f'Unknown error when converting the "{timecode}" timecode | {e}')

    @staticmethod
    def SRT_timecode_to_standard_timecode(timecode:str)->str:
        """Converts SRT format timecode to standard format

        Args:
            ```py
            timecode (str): Timecode to convert
            ```

        Returns:
            ```py
            time: Convert timecode
            ```
        """
        try:
            logger.info(f'Converts the following SRT timecode "{timecode}" to standard timecode format')
            hms, ms = timecode.split(',', 1)
            return f"{hms}.{ms}"
        except Exception as e:
            logger.error(f'Unknown error when converting the "{timecode}" timecode | {e}')

    @staticmethod
    def standard_timecode_to_SRT_timecode(timecode:str)->str:
        """Converts standard timecode to SRT format

        Args:
            ```py
            timecode (time): Timecode to convert
            ```

        Returns:
            ```py
            str: Convert timecode
            ```
        """
        try:
            logger.info(f'Converts the following standard timecode "{timecode}" to SRT timecode format')
            hms, ms = timecode.split('.', 1)
            return f"{hms},{ms}"
        except Exception as e:
            logger.error(f'Unknown error when converting the "{timecode}" timecode | {e}')

    @staticmethod
    def standard_timecode_to_ASS_timecode(timecode:str)->str:
        """Converts standard format timecode to ASS format

        Args:
            ```py
            timecode (str): Timecode to convert
            ```

        Returns:
            ```py
            str: Convert timecode
            ```
        """
        try:
            logger.info(f"Convertit le timecode standard \"{timecode}\" au format ASS")
            hms, ms = timecode.split('.', 1)
            h, m, s = hms.split(':', 2)
            if h[0] == '0':
                return f'{h[1]}:{m}:{s}.{ms[:2]}'
            else:
                return f'{h}:{m}:{s}.{ms[:2]}'
        except Exception as e:
            logger.error(f'Unknown error when converting the "{timecode}" timecode | {e}')

    @staticmethod
    def to_good_type(info:str|list[str]|dict[str, str | list[str]])->str|int|dict|list|float:
        """Convert an element into the typing it should be

        Args:
            ```py
            info (str | list | dict): Element to convert
            ```

        Returns:
            ```py
            str|int|dict|list|float: Convert element
            ```
        """
        try:
            logger.info(f'The "{info}" element being processed')

            if isinstance(info, str):
                logger.info(f'The element "{info}" is a String')
                if info.lstrip('-').isdigit():
                    logger.info(f'The "{info}" element is actually an Int')
                    return int(info)
                elif info.count('.') == 1 and all(c.isdigit() for c in info.replace('.', '', 1)):
                    logger.info(f'The "{info}" element is actually a Float')
                    return float(info)
                else:
                    logger.info(f'The element "{info}" is actually a String')
                    return info

            elif isinstance(info, list):
                logger.info(f'The element "{info}" is a List')
                info_tmp = []
                for i in info:
                    info_tmp.append(Convert.to_good_type(i))
                return info_tmp

            elif isinstance(info, dict):
                logger.info(f'The element "{info}" is a Dict')
                for i in info.keys():
                    info[i] = Convert.to_good_type(info[i])
                return info
            else:
                logger.info(f'The "{info}" element is either an Int or a Float or other')
                return info
        except Exception as e:
            logger.error(f"Unknown error | {e}")

    @staticmethod
    def get_tags_use(Events:dict, Styles:dict, i:int)->dict[str, str | int] | None:
            """Builds the Dict of tags used in the dialog being processed

            Args:
                ```py
                Events (dict): Dict of dialogues
                Styles (dict): Dict of styles
                i (int): Dialog line name
                ```

            Returns:
                ```py
                list[str | dict[str, str]]: Dict of tags
                ```
            """
            try:
                DEFAULT_VALUE_STYLE:dict[str, list[str | int]] = {
                    'Fontname': ['fn', 'Arial'], # Arial by default
                    'Fontsize': ['fs', 48], # 48px by default
                    'Bold': ['b', 0], # None by default
                    'Italic': ['i', 0], # None by default
                    'Underline': ['u', 0], # None by default
                    'PrimaryColour': ['c', '#FFFFFF00'], # white by default
                    'SecondaryColour': ['c2', '#FF000000'], # red by default
                    'OutlineColour': ['c3', '#00000000'], # dark by default
                    'BackColour': ['c4', '#00000000'], # dark by default
                    'StrikeOut': ['s', 0], # None by default
                    'ScaleX': ['fscx', 100], # 100% by default
                    'ScaleY': ['fscy', 100], # 100% by default
                    'Spacing': ['fsp', 0], # 0 by default
                    'Angle': ['frz', 0], # 0 by default
                    'Outline': ['bord', 2], # 2px by default
                    'Shadow': ['shad', 2], # 2px by default
                    'Alignment': ['an', 2], # middle down by default
                    'Encoding': ['fe', 1] # 1 / default by default
                    }
                DEFAULT_TAG:list[str] = ['b', 'i', 'u', 'pos', 'fad', 'fade', 'move', 'org',
                                'k', 'K', 'ko', 'kf', 'iclip', 'clip', 't', 'p',
                                's', 'an', 'be', 'bord', 'blur', 'fax', 'fay', 'faz',
                                'fs', 'fsc', 'fsp', 'fsv', 'fscx', 'fscy', 'frx', 'fry',
                                'frz', 'fe', 'shad', 'xbord', 'ybord', 'xshad', 'yshad', 'fn',
                                'c', '1c', '2c', '3c', '4c', 'alpha', '2a', '3a', '4a', 'a']
                Tags = {}
                Style = Styles.get(Events[i]["Style"])

                try:
                    if Style:
                        logger.info(f'The "{i}" line style exists')
                        for tag in DEFAULT_VALUE_STYLE.keys():
                            if Style.get(tag):
                                if isinstance(Style[tag], int):
                                    if Style[tag] >= 0:
                                        logger.info(f'The "{tag}" tag is valid')
                                        Tags[DEFAULT_VALUE_STYLE[tag][0]] = Style[tag]
                                    else:
                                        logger.info(f'The "{tag}" tag is invalid, so we use the default value')
                                        Tags[DEFAULT_VALUE_STYLE[tag][0]] = DEFAULT_VALUE_STYLE[tag][1]
                                elif isinstance(Style[tag], str):
                                    if Style[tag] != '':
                                        logger.info(f'The "{tag}" tag is valid')
                                        Tags[DEFAULT_VALUE_STYLE[tag][0]] = Style[tag]
                                    else:
                                        logger.info(f'The "{tag}" tag is invalid, so we use the default value')
                                        Tags[DEFAULT_VALUE_STYLE[tag][0]] = DEFAULT_VALUE_STYLE[tag][1]
                                else:
                                    logger.info(f'The "{tag}" tag is invalid, so we use the default value')
                                    Tags[DEFAULT_VALUE_STYLE[tag][0]] = DEFAULT_VALUE_STYLE[tag][1]
                            else:
                                logger.info(f'The "{tag}" tag is invalid, so we use the default value')
                                Tags[DEFAULT_VALUE_STYLE[tag][0]] = DEFAULT_VALUE_STYLE[tag][1]

                except Exception as e:
                    logger.error(f'Unknown error | {e}')

                try:
                    for tag in DEFAULT_TAG:
                        dialogue_tags = Events[i]['Tags']

                        if dialogue_tags.get(tag):
                            logger.info(f'The "{tag}" tag is present in the dialog tags')
                            if dialogue_tags[tag] != 0 or dialogue_tags[tag] != '':
                                logger.info(f'The "{tag}" tag is valid')
                                Tags[tag] = dialogue_tags[tag]
                            elif dialogue_tags[tag] == 0 or dialogue_tags[tag] == '':
                                logger.info(f'The "{tag}" tag is invalid')
                                Tags.pop(tag)

                except Exception as e:
                    logger.error(f'Unknown error | {e}')

                return Tags if Tags != {} else None

            except Exception as e:
                logger.error(f'Unknown error | {e}')

    # TODO : Poursuivre cette méthode
    @staticmethod
    def create_styles(Events:dict)->dict[str, str | int]:
        """Create styles for tags common to all dialogs

        Args:
            ```py
            Events (dict): Dictionary of events containing the tags
            ```

        Returns:
            ```py
            dict[str, str | int]: Dialogs styles
            ```
            ```json
            {
                "Exemple": {
                    "Fontname": "Arial",
		            "Fontsize": 48,
		            "PrimaryColour": "#FFFF00FF",
		            "SecondaryColour": "#000000FF",
		            "OutlineColour": "#00000000",
		            "BackColour": "#00000000",
		            "Bold": 0,
		            "Italic": "-1",
		            "Underline": 0,
                    ...
                }
            }
            ```
        """
        
        def create_style_name()->str:
            """Generates a random style name

            Returns:
                ```py
                str: Style name
                ```
            """
            try:
                logger.info(f'Create a new style name')
                return f'Default-{''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))}'
            except Exception as e:
                logger.error(f'Unknown error | {e}')
        
        try:
            
            styles = {}
            all_styles = {}
            mutual_tags = {}
            
            for i in Events.keys():
                logger.info(f'Get the tags')
                Tags = Events[i].get('Tags')
                
                if Tags:
                    for tag in Tags.keys():
                        if mutual_tags.get(tag):
                            logger.info(f'The "{tag}" tag is in common tags')
                            if Tags[tag] != mutual_tags[tag]:
                                style_name = create_style_name()
                                styles[style_name] = mutual_tags
                                Events[i]['Style'] = style_name
                                logger.info(f'Void the common tags')
                                mutual_tags = {}
                            else:
                                logger.info(f'The value of the "{tag}" tag is identical between the shared tag ("{mutual_tags[tag]}") and the retrieved tag ("{Tags[tag]}")')
                                pass

                        else:
                            logger.info(f'The "{tag}" tag is not included in common tags.')
                            logger.info(f'Adding the "{tag}" tag to common tags')
                            mutual_tags[tag] = Tags[tag]
                    
                    if styles == {}:
                        styles[create_style_name()] = mutual_tags
                        return styles

            return styles

        except Exception as e:
            logger.error(f'Unknown error | {e}')

    @staticmethod
    def to_SRT(Parts:dict, title:str, dir:str = "./")->None:
        """Converts loaded subtitle info to SRT format

        Args:
            ```py
            Parts (dict): Dict containing dialogues and styles
            dir (str): Output dir
            title (str): Output filename (without extension)
            ```
        """

        def builder() -> str:
            """Builds the string for the dialog construction

            Returns:
                ```py
                str: Output string
                ```
            """
            try:
                SRT_TAGS = ['b', 'u', 'i', 'c']
                Tags = Convert.get_tags_use(Events, Parts['Styles'], i)
                tag = ''
                haveTag = False

                text = f"{i}\n"
                text += f"{Convert.standard_timecode_to_SRT_timecode(Events[i]['Start'])} --> {Convert.standard_timecode_to_SRT_timecode(Events[i]['End'])} "
                
                if Tags:
                    logger.info(f'Some tags have been found on the line "{i}"')
                    if 'pos' in Tags:
                        logger.info(f'"{tag}" tag have been found')
                        pos = Tags['pos']
                        text += f"X1:{pos['x']} X2:{pos['x']+50} Y1:{pos['y']} Y2:{pos['y']+50}\n"
                    else:
                        logger.info(f'No "{tag}" tag have been')
                        text += "\n"

                    logger.info(f'Building the line "{i}" with "{Tags}" tags')
                    for tag in Tags.keys():
                        if tag in SRT_TAGS:
                            logger.info(f'"{tag}" tag have been found')
                            if not haveTag:
                                try:
                                    logger.info(f'The text under construction have no tag yet')
                                    if tag == 'c' and Tags[tag] != '':
                                        logger.info(f'Construct the "{tag}" tag')
                                        dialogue = f'<font color="{Convert.hex_RGBA_to_hex_RGB(Tags[tag])}">{Events[i]['Text']}</font>'
                                        haveTag = True
                                    elif Tags[tag] != 0: 
                                        logger.info(f'Construct the "{tag}" tag')
                                        dialogue = f"<{tag}>{Events[i]['Text']}</{tag}>"
                                        haveTag = True
                                except Exception as e:
                                    logger.error(f'Unknown error during the building of the line "{i}" and the "{tag}" tag | {e}')

                            else:
                                try:
                                    logger.info(f'The text under construction have one or multiple tag(s)')
                                    if tag == 'c' and Tags[tag] != '':
                                        logger.info(f'Construct the "{tag}" tag')
                                        dialogue = f'<font color="{Convert.hex_RGBA_to_hex_RGB(Tags[tag])}">{dialogue}</font>'
                                    else:
                                        if Tags[tag] != 0: 
                                            logger.info(f'Construct the "{tag}" tag')
                                            dialogue = f"<{tag}>{dialogue}</{tag}>"
                                except Exception as e:
                                    logger.error(f'Unknown error during the building of the line "{i}" and the "{tag}" tag | {e}')

                    if not haveTag:
                        return text + Events[i]["Text"] + '\n\n'
                    else:
                        return text + dialogue + '\n\n'
                return text + '\n' + Events[i]["Text"] + '\n\n'

            except Exception as e:
                logger.error(f'Unknown error during the building of the line "{i}" and the "{tag}" tag | {e}')

        try:
            Events = Parts['Events']

            with open(f"{dir}{title}.srt", "w", encoding="utf-8") as f:
                for i in Events.keys():
                    f.write(builder())

        except Exception as e :
            logger.error(f'Unknown error | {e}')

    @staticmethod
    def to_JSON(Parts:dict, title:str, dir:str = "./")->None:
        """Converts loaded subtitle info to SRT format

        Args:
            ```py
            Parts (dict): Dict containing dialogues and styles
            dir (str): Output dir
            title (str): Output filename (without extension)
            ```
        """
        json.dump(Parts, open(f'{dir}{title}.json', 'w'), indent=4)

    # ! FIXME : Marche pas
    @staticmethod
    def to_ASS(Parts:dict, title:str, dim:str = "1280x720", dir:str = "./")->None:
        """Converts loaded subtitle to ASS format (even if the file in the input is an ASS file)

        Args:
            ```py
            Parts (dict): Dict containing dialogues and styles
            dir (str): Output dir
            title (str): Output filename (without extension)
            dim (str): Video size for script adaptation. Example: 1920x1080
            ```
        """      

        def buildScriptInfo()->str:
            try:
                logger.info(f'Create the "Script Info" section')
                x, y = dim.split('x',1)
                script_info = '[Script Info]\n'
                script_info += f'Title: {title}\n'
                script_info += 'ScriptType: v4.00+\n'
                script_info += 'WrapStyle: 0\n'
                script_info += 'ScaledBorderAndShadow: yes\n'
                script_info += 'YCbCr Matrix: None\n'
                script_info += f'PlayResX: {x}\n'
                script_info += f'PlayResY: {y}\n\n'

                return script_info

            except Exception as e:
                logger.error(f'Unknown error | {e}')
                
        def buildStyles()->str:
            try:
                logger.info(f'Create the "Styles" section')
                text = '[V4+ Styles]\n'
                text += 'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n'

                for name in Styles.keys():
                    style = f'Style: {name},'
                    for tag in ['Fontname', 'Fontsize', 'PrimaryColour', 'SecondaryColour',
                                'OutlineColour', 'BackColour', 'Bold', 'Italic',
                                'Underline', 'StrikeOut', 'ScaleX', 'ScaleY',
                                'Spacing', 'Angle', 'BorderStyle','Outline',
                                'Shadow', 'Alignment', 'MarginL', 'MarginR',
                                'MarginV', 'Encoding']:
                        if tag != 'Encoding':
                            style += f'{Styles[name][tag]},'
                        else:
                            style += f'{Styles[name][tag]}'
                    style += '\n'

                return text + style + '\n'
            except Exception as e:
                logger.error(f'Unknown error | {e}')

        def buildEvents()->str:
            
            def buildTags(i:str|int, t:bool=False)->str:
                """Construit les balises

                Args:
                    ```py
                    i (int|str): ID du dialogue en cours de traitement
                    t (bool): Utilisation suite à une balise t
                    ```

                Returns:
                    ```py
                    str: Chaîne de caractère contenant les balises
                    ```
                """
                try:
                    if not t:
                        try:
                            Tags = Convert.get_tags_use(Events, Styles, i)
                            print(Tags)
                            if Tags:
                                balise = '{'
                                for tag in Tags:
                                    if not isinstance(tag, dict):
                                        val = Events[i]['Tags'][tag]
                                        if isinstance(val, int|str):
                                            balise += f'\\{tag}{val}'

                                        elif isinstance(val, dict):

                                            if tag in ['clip', 'iclip']:
                                                balise += f'\\{tag}({val})'

                                            if tag in ['pos', 'org']:
                                                balise += f'\\{tag}({val['x']}, {val['y']})'

                                            if tag in ['move']:
                                                balise += f'\\{tag}({val['x1']}, {val['y1']}, {val['x2']}, {val['y2']}, {val['t1']}, {val['t2']})'

                                            if tag in ['fad', 'fade']:
                                                balise += f'\\{tag}({val['a1']}, {val['a2']}, {val['a3']}, {val['t1']}, {val['t2']}, {val['t3']}, {val['t4']})'

                                            if tag == 't':
                                                balise += f'\\{tag}({val['t1'], val['t2'], val['accel'], buildTags(i, True)})'

                                    else:
                                        val = Events[i]['Tags']['c']
                                        balise += f'\\{tag}{Convert.Hex_color_to_ASS_color(val)}'
                            
                                return balise + '}'
                            
                            return ''

                        except Exception as e:
                            logger.error(f'Unknown error | {e}')

                    elif t:
                        try:
                            Tags = Events[i]['Tags']['t']['tags']
                            if Tags:
                                balise = '('
                                for tag in Tags:
                                    if not isinstance(Tags[tag], list) or not isinstance(Tags[tag], dict):
                                        if tag in ['c', '1c', '2c', '3c', '4c']:
                                            balise += f'\\{tag}{Convert.Hex_color_to_ASS_color(Convert, Tags[tag])}'
                                        else:
                                            balise += f'\\{tag}{Tags[tag]}'

                                    elif isinstance(Events[i]['Tags']['t']['tags'][tag], dict):
                                        val = Tags[tag]

                                        if tag in ['clip', 'iclip']:
                                            balise += f'\\{tag}({val})'

                                        if tag in ['pos', 'org']:
                                            balise += f'\\{tag}({val['x']}, {val['y']})'

                                        if tag in ['move']:
                                            balise += f'\\{tag}({val['x1']}, {val['y1']}, {val['x2']}, {val['y2']}, {val['t1']}, {val['t2']})'

                                        if tag in ['fad', 'fade']:
                                            balise += f'\\{tag}({val['a1']}, {val['a2']}, {val['a3']}, {val['t1']}, {val['t2']}, {val['t3']}, {val['t4']})'

                                        if tag == 't':
                                            balise += f'\\{tag}({val['t1'], val['t2'], val['accel'], buildTags(Convert, i, True)})'

                                return balise + ')'

                        except Exception as e:
                            logger.error(f'Unknown error | {e}')

                    return ''

                except Exception as e:
                    logger.error(f'Unknown error | {e}')
            
            try:
                logger.info(f'Create the "Events" section')
                dialogues = ''
                text = '[Events]\n'
                text += 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
                for i in Events.keys():
                    dialogues += 'Dialogue: '
                    for info in ['Layer', 'Start', 'End', 'Style',
                                 'Name', 'MarginL', 'MarginR', 'MarginV',
                                 'Effect', 'Text']:

                        if info != 'Text':

                            if info == 'Start' or info == 'End':
                                dialogues += f'{Convert.standard_timecode_to_ASS_timecode(Events[i][info])},'

                            else:
                                dialogues += f'{Events[i][info]},'

                        else:
                            dialogues += f'{buildTags(i)}{Events[i][info]}\n'
                        
                return text + dialogues
            except Exception as e:
                logger.error(f'Unknown error | {e}')

        try:
            Styles = Parts['Styles']
            Events = Parts['Events']

            with open(f"{dir}{title}.ass", "w", encoding="utf-8") as f:
                f.write(buildScriptInfo())
                f.write(buildStyles())
                f.write(buildEvents())
        except Exception as e:
            logger.error(f'Unknown error | {e}')


def main():
    from Sub.sub import Sub
    SousTitre = Sub()
    
    parts = SousTitre.get_parts('C:/Users/Im4g1/Documents/Cours/Mini_Projet/SUBMODULE/doc/test.ass')
    
    Styles = Convert.create_styles(parts["Events"])
    
    json.dump(Styles, open('C:/Users/Im4g1/Documents/Cours/Mini_Projet/SUBMODULE/doc/test.json', 'w'),indent=4)

if __name__ == "__main__":
    main()