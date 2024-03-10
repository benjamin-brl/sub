from dataclasses import dataclass
from loguru import logger

@dataclass
class Convert():
    """Class de conversion des différents éléments vers des éléments "standard" et/ou vers des éléments spéciaux"""

    # * WORK : Fonctionne parfaitement
    @staticmethod
    def ASS_color_to_hex_color(color:str)->str:
        """Convertit le formatage de couleur ASS vers Hexadecimal

        Args:
            ```py
            color (str): Couleur à convertir
            ```

        Returns:
            ```py
            str: Couleur convertit
            ```
        
        &H`BBGGRR`& --> #`RRGGBB`
        """
        try:
            logger.info(f"Convertit le code couleur \"{color}\"")
            if len(color) == 4:
                return f"{color[2:4]}"
            elif len(color) == 9:
                return f"#{color[6:8]}{color[4:6]}{color[2:4]}"
            elif len(color) == 10:
                return f"#{color[6:8]}{color[4:6]}{color[2:4]}{color[8:10]}"
        except Exception as e:
            logger.error(f"Il y a eu une erreur inattendu lors de la conversion de la couleur {color} | {e}")

    # * WORK : Fonctionne parfaitement
    @staticmethod
    def hex_color_to_ASS_color(color:str)->str:
        """Convertit le formatage de couleur Hexadecimal vers ASS

        Args:
            ```py
            color (str): Couleur à convertir
            ```

        Returns:
            ```py
            str: Couleur convertit
            ```
        
        #`RRGGBB` --> &H`BBGGRR`&
        """
        try:
            logger.info(f"Convertit le code couleur \"{color}\"")
            if len(color) == 2:
                return f"&H{color}"
            elif len(color) == 7:
                return f"&H{color[5:7]}{color[3:5]}{color[1:3]}&"
            elif len(color) == 9:
                return f"&H{color[5:7]}{color[3:5]}{color[1:3]}{color[7:9]}"
            else:
                return None

        except Exception as e:
            logger.error(f"Il y a eu une erreur inattendu lors de la conversion de la couleur {color} | {e}")

    # * WORK : Fonctionne parfaitement
    @staticmethod
    def ASS_timecode_to_standard_timecode(timecode:str)->str:
        """Convertit un timecode au format ASS vers un format standard

        Args:
            ```py
            timecode (str): timecode d'entrée
            ```

        Returns:
            ```py
            time: timecode au format time pour une harmonisation du format
            ```
        """
        try:
            logger.info(f"Convertit le timecode ASS \"{timecode}\" au format standard")
            h, m, s = timecode.split(':', 3)
            return f"{h.zfill(2)}:{m}:{s}0"
        except Exception as e:
            logger.error(f"Il y a eu une erreur inattendu lors de la conversion du timecode {timecode} | {e}")

    # * WORK : Fonctionne parfaitement
    @staticmethod
    def SRT_timecode_to_standard_timecode(timecode:str)->str:
        """Convertit un timecode au format SRT vers un format standard

        Args:
            ```py
            timecode (str): timecode d'entrée
            ```

        Returns:
            ```py
            time: timecode au format standard pour une harmonisation du format
            ```
        """
        try:
            logger.info(f"Convertit le timecode SRT \"{timecode}\" au format standard")
            hms, ms = timecode.split(',', 1)
            return f"{hms}.{ms}"
        except Exception as e:
            logger.error(f"Il y a eu une erreur inattendu lors de la conversion du timecode {timecode} | {e}")

    # * WORK : Fonctionne parfaitement
    @staticmethod
    def standard_timecode_to_SRT_timecode(timecode:str)->str:
        """Convertit le formatage de timecode ASS vers timecode SRT

        Args:
            ```py
            timecode (time): Timecode d'entrée au format time
            ```

        Returns:
            ```py
            str: Timecode de sortie
            ```
        """
        try:
            logger.info(f"Convertit le timecode standard \"{timecode}\" au format SRT")
            hms, ms = timecode.split('.', 1)
            return f"{hms},{ms}"
        except Exception as e:
            logger.error(f"Il y a eu une erreur inattendu lors de la conversion du timecode {timecode} | {e}")

    # * WORK : Fonctionne parfaitement
    @staticmethod
    def standard_timecode_to_ASS_timecode(timecode:str)->str:
        """Convertit le timecode "standard" en un timecode ASS

        Args:
            ```py
            timecode (str): Timecode standard
            ```

        Returns:
            ```py
            str: Timecode ASS
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
            logger.error(f'Une erreur inattendu est survenu | {e}')

    @staticmethod
    def get_tags_use(Events:dict, Styles:dict, i:int)->dict[str, str | int]:
            """Construit le tableau des balises en utilisations dans le dialogue en cours de traitement

            Args:
                ```py
                Events (dict): Dictionnaire des dialogues
                Styles (dict): Dictionnaire des styles
                i (int): Numéro de ligne de dialogues
                ```

            Returns:
                ```py
                list[str | dict[str, str]]: Tableau des balises
                ```
            """
            try:
                DEFAULT_VALUE_STYLE = {
                    'Fontname': ['fn', 'Arial'], # Arial by default
                    'Fontsize': ['fs', 48], # 48px by default
                    'Bold': ['b', 0], # None by default
                    'Italic': ['i', 0], # None by default
                    'Underline': ['u', 0], # None by default
                    'PrimaryColour': ['c', '#FFFFFF'], # white by default
                    'SecondaryColour': ['c2', '#FF0000'], # red by default
                    'OutlineColour': ['c3', '#000000'], # dark by default
                    'BackColour': ['c4', '#000000'], # dark by default
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
                DEFAULT_TAG = ['b', 'i', 'u', 'pos', 'fad', 'fade', 'move', 'org',
                                'k', 'K', 'ko', 'kf', 'iclip', 'clip', 't', 'p',
                                's', 'an', 'be', 'bord', 'blur', 'fax', 'fay', 'faz',
                                'fs', 'fsc', 'fsp', 'fsv', 'fscx', 'fscy', 'frx', 'fry',
                                'frz', 'fe', 'shad', 'xbord', 'ybord', 'xshad', 'yshad', 'fn',
                                'c', '1c', '2c', '3c', '4c', 'alpha', '2a', '3a', '4a', 'a']
                Tags = {}
                Style = Styles.get(Events[i]["Style"])

                try:
                    if Style:
                        for tag in DEFAULT_VALUE_STYLE.keys():
                            Tags[DEFAULT_VALUE_STYLE[tag][0]] = Style[tag] if Style.get(tag) and (Style[tag] > 0 or Style[tag] != '') else DEFAULT_VALUE_STYLE[tag][1]

                except Exception as e:
                    logger.error(f'Une erreur inattendue est survenue | {e}')

                try:
                    for tag in DEFAULT_TAG:
                        dialogue_tags = Events[i]['Tags']
                        if (tag == 'pos' or tag == 'org') and tag in dialogue_tags:
                            if isinstance(dialogue_tags[tag], dict):
                                Tags[tag] = dialogue_tags[tag]
                            else:
                                Tags.pop(tag)
                        elif tag in dialogue_tags:
                            Tags[tag] = dialogue_tags[tag]

                except Exception as e:
                    logger.error(f'Une erreur inattendue est survenue | {e}')

                return Tags if Tags != {} else None

            except Exception as e:
                logger.error(f'Une erreur inattendue est survenue | {e}')

    @staticmethod
    def to_SRT(Parts:dict, dir:str, title:str)->None:
        """Convertit les infos du sous-titre chargé vers un format SRT

        Args:
            ```py
            Parts (dict): Dictionnaire contenant les dialogues et les styles
            dir (str): Répertoire de sortie
            title (str): Nom du fichier de sortie
            ```
        """
        
        def builder() -> str:
            """Construits la chaîne de caractères pour la construction du dialogue

            Returns:
                ```py
                str: Chaîne de caractère de sortie
                ```
            """
            try:
                haveTag = False
                Tags = Convert.get_tags_use(Events, Styles, i)

                text = f"{i}\n"
                text += f"{Convert.standard_timecode_to_SRT_timecode(Events[i]['Start'])} --> {Convert.standard_timecode_to_SRT_timecode(Events[i]['End'])} "

                if 'pos' in Tags:
                    pos = Events[i]['Tags']['pos']
                    text += f"X1:{pos['x']} X2:{pos['x']+50} Y1:{pos['y']} Y2:{pos['y']+50}\n"
                else:
                    text += '\n'

                for tag in [tag for tag in Tags if not isinstance(tag, dict)]:
                    if not haveTag and tag not in ['pos', 'fad', 'fade', 'move',
                                                   'org', 'k', 'K', 'ko',
                                                   'kf', 'iclip', 'clip', 't',
                                                   'p', 's', 'an', 'be',
                                                   'bord', 'blur', 'fax', 'fay',
                                                   'faz', 'fs', 'fsc', 'fsp',
                                                   'fsv', 'fscx', 'fscy', 'frx',
                                                   'fry', 'frz', 'fe', 'shad',
                                                   'xbord', 'ybord', 'xshad', 'yshad',
                                                   'fn']:
                        dialogue = f"<{tag}>{Events[i]['Text']}</{tag}>"
                        haveTag = True

                    elif tag not in ['pos', 'fad', 'fade', 'move',
                                    'org', 'k', 'K', 'ko',
                                    'kf', 'iclip', 'clip', 't',
                                    'p', 's', 'an', 'be',
                                    'bord', 'blur', 'fax', 'fay',
                                    'faz', 'fs', 'fsc', 'fsp',
                                    'fsv', 'fscx', 'fscy', 'frx',
                                    'fry', 'frz', 'fe', 'shad',
                                    'xbord', 'ybord', 'xshad', 'yshad',
                                    'fn']:
                        dialogue = f"<{tag}>{dialogue}</{tag}>"

                if any(isinstance(tag, dict) for tag in Tags):
                    for tag in Tags:
                        if isinstance(tag, dict) and 'c' in tag:
                            if not haveTag:
                                dialogue = f'<font color="{tag["c"]}">{Events[i]["Text"]}</font>'
                                haveTag = True
                                break
                            else:
                                dialogue = f'<font color="{tag["c"]}">{dialogue}</font>'

                if not haveTag:
                    dialogue = f'{Events[i]["Text"]}'

                return text + dialogue + '\n\n'

            except Exception as e:
                logger.error(f'Une erreur inattendue est survenue lors de la construction du sous-titre {i} et la balise {tag} | {e}')

        try:
            Styles = Parts['Styles']
            Events = Parts['Events']

            with open(f"{dir}{title}.srt", "w", encoding="utf-8") as f:
                for i in Events.keys():
                    f.write(builder())

        except Exception as e :
            logger.error(f'Une erreur inattendu est survenu | {e}')

    @staticmethod
    def to_ASS(Parts:dict, dir:str, title:str, dim:str)->None:
        """Convertit les infos du sous-titre chargé vers un format ASS

        Args:
            ```py
            Parts (dict): Dictionnaire contenant les dialogues et les styles
            dir (str): Répertoire de sortie
            title (str): Nom du fichier de sortie
            dim (str): Dimension de la vidéo pour adaptation du script. Exemple : 1920x1080
            ```
        """      

        def buildScriptInfo()->str:
            try:
                script_info = '[Script Info]\n'
                script_info += f'Title: {title}\n'
                script_info += 'ScriptType: v4.00+\n'
                script_info += 'WrapStyle: 0\n'
                script_info += 'ScaledBorderAndShadow: yes\n'
                script_info += 'YCbCr Matrix: None\n'
                script_info += f'PlayResX: {dim.split('x',1)[0]}\n'
                script_info += f'PlayResY: {dim.split('x',1)[1]}\n\n'

                return script_info

            except Exception as e:
                logger.error(f'Une erreur inattendu est survenu | {e}')
                
        def buildStyles()->str:
            try:                
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
                logger.error(f'Une erreur inattendu est survenu | {e}')

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
                            logger.error(f'Une erreur inattendu est survenu | {e}')

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
                            logger.error(f'Une erreur inattendu est survenu | {e}')

                    return ''

                except Exception as e:
                    logger.error(f'Une erreur inattendu est survenu | {e}')
            
            try:
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
                logger.error(f'Une erreur inattendu est survenu | {e}')

        try:
            Styles = Parts['Styles']
            Events = Parts['Events']

            with open(f"{dir}{title}.ass", "w", encoding="utf-8") as f:
                f.write(buildScriptInfo())
                f.write(buildStyles())
                f.write(buildEvents())
        except Exception as e:
            logger.error(f'Une erreur inattendu est survenu | {e}')