"""Transformer un fichier de sous-titre 'ASS' (textuelle) au format 'PGS' (graphique)

Analyse d'un script ASS :
"
[Script Info]
...
PlayResX: 2560
PlayResY: 1440
...

[Aegisub Project Garbage]
...

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial Black,80,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,4,0,2,67,67,50,0
Style: Credit,MOON GET!,100,&H00FFFEFF,&H000000FF,&H004B3A8F,&H006155AB,-1,0,0,0,100,100,0,0,1,2,6,7,0,0,0,1
...

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:01.01,0:00:04.01,Default,,0,0,0,,[musique élégante jouée]
Dialogue: 0,0:25:22.98,0:25:25.00,Credit,,0,0,0,,{\\blur2\\pos(230,1120)\\fs84}Traduit et réadapté en français
...
Comment: 0,0:00:32.96,0:00:51.28,Default,,0,0,0,,{}=== Karaoké EN ==={}
...
"

fonctions :
- Qui récupère et vérifie le fichier sous-titre d'entrée au format 'ASS' (.ass / .ssa)
- Qui extrait les différentes partie du fichier ASS ([Script Info], [V4+ Styles], [Events])
- Qui récupère la résolution de l'écran (PlayResX, PlayResY)
- Qui extrait les différents style (Style:)
- Qui extrait le contenu de chaque ligne du fichier 'ASS' (Dialogue:)
- Qui extrait les Tags du texte (les Tags sont entre '{}' et sont différencier par un '\', certain on les paramètres entre '()')
"""

import sys, re, os, json
from pprint import pprint
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
    """Classe représentant la gestion des sous-titres."""

    subs:tuple[str] = None
    """Variable des sous-titres chargés"""
    
    title:str = ''
    """Variable du sous-titre chargé en cours"""
    
    root:str = ''
    """Variable de la racine du sous-titre chargé en cours"""

    # * WORK : Fonctionne parfaitement
    def get_subs(self)->tuple[str]:
        """Récupère le fichier de sous-titre à traité
        
        Args:
            ```py
            escape (bool): Valeur qui définit si oui ou non il y a tentative d'annulation du script
            ```

        Returns:
            ```py
            list[str]: Liste de fichier à traité (peu être unique)
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
            subs = filedialog.askopenfilenames(title="Sélectionner un ou plusieurs sous-titre(s)", filetypes=ALL_FORMAT)
            if subs:
                logger.info(f"L'utilisateur a chargé des sous-titres")
                self.subs = subs
                return subs
            else:
                logger.info(f"L'utilisateur n'a pas chargé des sous-titres")
                return None

        except FileNotFoundError as e:
            logger.error(f"Impossible de trouver le fichier | {e}")
        except Exception as e:
            logger.error(f"Erreur inattendu | {e}")

    # * WORK : Fonctionne parfaitement
    # TODO : Ajouté des informations complémentaires et traité les autres cas de figure
    def get_sub_infos(self, sub:str)->dict[str, str | int | list[str | int] | dict[str, float]]:
        """Créer un tableau associatif entre le sous-titre chargé et ces différentes valeurs

        Args:
            ```py
            sub (str): _description_
            ```

        Returns:
            ```py
            dict[str, str | int | list[str | int]]: _description_
            ```
        
        ```json
        {
            "name" : "test",
            "type" : "ass",
            "countOfLine" : 150,
            ...
        }
        ```
        """

        # * WORK : Fonctionne parfaitement
        # TODO : Ajouté des informations complémentaires
        def get_basic_infos(sub:str, Parts:dict)->dict[str, str | int | list[str | int] | dict[str, float]]:
            """Récupère les informations basique du sous-titre

            Args:
                ```py
                sub (str): Chemin du sous-titre
                at (dict[str, str | int | list[str | int]]): Si un dictionnaire contenant des informations du script à déjà été créé
                ```

            Returns:
                ```py
                dict[str, str | int | list[str | int] | dict[str, float]]: Dictionnaire contenant les informations basiques du script
                ```
                
            ```json
            {
                "name" : "test",
                "type" : "ass",
                "countOfLine" : 150,
                "weight" : 2184576,
                ...
            }
            ```
            """
            try:
                at = {}
                name, ext = os.path.splitext(os.path.basename(sub))
                at["name"] = name
                at["extension"] = ext
                at["weight"] = os.path.getsize(sub)
                at["countOfLineScriptInfo"] = len(Parts["Script Info"])
                at["countOfDifferentStyles"] = len(Parts["Styles"])
                at["countOfLineDialogue"] = len(Parts["Events"])
                at["lang"] = self.get_global_langs_dialogue(Parts["Events"])
                return at
            except Exception as e :
                logger.error(f'Une erreur inattendu est survenu | {e}')

        try:
            Parts = self.get_parts(sub)
            at = get_basic_infos(sub, Parts)
            match at["extension"]:
                case '.ass':
                    at["type"] = "Advanced SubStation Alpha"
                    at["parts"] = Parts
                case '.ssa':
                    at["type"] = "SubStation Alpha"
                case '_':
                    logger.info(f'Le fichier est dans un format inconnu ou non pris en charge | {at["type"]}')
            return at
        except Exception as e:
            logger.error(f'Une erreur inattendu est survenu | {e}')

    # * WORK : Fonctionne parfaitement
    def get_global_langs_dialogue(self, Events:dict)->dict[str, float]:
        """Récupère les langues les plus probables sur l'ensemble des dialogues

        Args:
            ```py
            Events (dict): Ensemble des dialogues
            ```

        Returns:
            ```py
            dict[str, float]: Dictionnaire des langues trouvé et leur taux d'implication
            ```
        
        ```json
        {
            "fr": 0.822,
            "en": 0.033,
        }
        ``` 
        """

        # * WORK : Fonctionne parfaitement
        def getLangsOfLine(line:str)->dict[str, float]:
            """Récupère les langues présente dans une ligne et leur taux d'implication

            Args:
                ```py
                line (str): Ligne de dialogue
                ```

            Returns:
                ```py
                dict[str, float]: langues présente dans la ligne et leur taux d'implication
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
                DetectorFactory.seed = 0
                langues:dict[str, float] = {}
                for langue in detect_langs(line):
                    langues[langue.lang] = round(langue.prob,3)
                return {langue: prob for langue, prob in langues.items() if prob >= 0.01}
            except Exception as e :
                logger.error(f'Une erreur inattendu est survenu pour la ligne "{line}" | {e}')
        
        try:
            langues = {}
            total_lignes = len(Events.keys())
            for i in range(1, total_lignes + 1):
                line = Events[i]["Text"].replace("\\N", " ")
                logger.info(f'La ligne "{line}" est en cours de traitement')
                try:
                    langues_ligne = getLangsOfLine(line)
                    for langue, prob in langues_ligne.items():
                        langues[langue] = round(langues.get(langue, 0) + (prob / total_lignes), 3)
                except Exception as e:
                    logger.error(f'Une erreur inattendu est survenu à la ligne {line} | {e}')

            return {langue: prob for langue, prob in langues.items() if prob >= 0.03}
        except Exception as e:
            logger.error(f'Une erreur inattendu est survenu | {e}')

    # * WORK : Fonctionne parfaitement
    def get_parts(self, sub:str)->dict[str, dict[str, str | dict[str, str]]]:
        """Extrait les différentes parties d'un fichier ASS

        Args:
            ```py
            file (str): Chemin vers le fichier sous-titre
            ```

        Returns:
            ```py
            list[dict[str, str]]: Liste des différentes pa
            ```

        ```json
        {
            "Script Info" : {
                ...
                "PlayResX" : 2560,
                "PlayResY" : 1440,
                ...
            },
            "V4+ Styles" :
            [
                "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
                "Style: Default,Arial Black,80,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,4,0,2,67,67,50,0",
                "Style: Credit,MOON GET!,100,&H00FFFEFF,&H000000FF,&H004B3A8F,&H006155AB,-1,0,0,0,100,100,0,0,1,2,6,7,0,0,0,1",
                ...,
            ],
            "Events" :
            [
                "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
                "Dialogue: 0,0:00:01.01,0:00:04.01,Default,,0,0,0,,[musique élégante jouée]",
                "Dialogue: 0,0:25:22.98,0:25:25.00,Credit,,0,0,0,,{\\blur2\\pos(230,1120)\\fs84}Traduit et réadapté en français",
                ...
                "Comment: 0,0:00:32.96,0:00:51.28,Default,,0,0,0,,{}=== Karaoké EN ==={}",
                ...
            ]
        }
        ```
        """
        Parts = {}
        try:
            logger.info(f"Lecture du fichier \"{sub}\"")
            with open(sub, "r", encoding="utf-8") as f:
                lines = f.readlines()
                Parts["Script Info"] = self.get_script_infos(lines)
                Parts["Styles"] = self.get_styles(lines)
                Parts["Events"] = self.get_events(lines)
                
                self.title = Parts["Script Info"]["Title"].replace(":", "-")
                self.root = f'{os.path.dirname(sub)}/'
            
            return Parts

        except Exception as e:
            logger.error(f"Il y a eu une erreur inattendu | {e}")

    # * WORK : Fonctionne parfaitement
    def get_script_infos(self, lines:list[str])->dict[str, str]:
        """Extrait les informations de la partie [Script Info]

        Args:
            ```py
            lines (list[str]): Lignes du fichier sous-titres
            ```

        Returns:
            ```py
            dict[str, str | int]: Dictionnaire nominatif aux valeurs
            ```
        
        ```json
        {
            ...
            "PlayResX" : 2560,
            "PlayResY" : 1440,
            ...
        }
        ```
        """

        ScriptInfo = {}
        inScriptInfo = True

        try:
            logger.info(f"Entrée dans la balise \"[Script Infos]\"")
            for line in lines:
                line = line.strip()
                if line == "[Aegisub Project Garbage]":
                    logger.info(f"Sortie de la balise \"[Script Info]\"")
                    inScriptInfo = False
                    break

                if inScriptInfo and not (((";" in  line) or ("[" in line)) or line == ''):
                    logger.info(f"Ajout de la ligne \"{line}\"")
                    infos = line.split(":", 1)
                    if infos[0] == "Title":
                        self.title = infos[1].strip().replace(":","-")
                    ScriptInfo[infos[0].strip()] = Convert.to_good_type(infos[1].strip())

            return ScriptInfo
        except Exception as e:
            logger.error(f"Une erreur inattendu est survenu | {e}")

    # * WORK : Fonctionne parfaitement
    def get_styles(self, lines:list[str])->dict[str, dict[str, str]]:
        """Extrait les différents style de la partie [V4+ Styles]

        Args:
            ```py
            lines (list[str]): Lignes du fichier sous-titres
            ```

        Returns:
            ```py
            dict[str, str | int]: Dictionnaire nominatif aux valeurs
            ```
        
        ```json
        {
            "default" : {
                "FontName" : "Arial",
                "FontSize" : "24",
                "PrimaryColour" : "&H000000FF",
                ...
            },
            "Credit" : {
                "FontName" : "MOON GET!",
                "FontSize" : "100",
                "PrimaryColour" : "&H00FFFEFF",
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
                    logger.info(f"Entrée dans la balise \"[V4+ Styles]\"")
                    inStyles = True
                elif line == "[Events]":
                    logger.info(f"Sortie de la balise \"[V4+ Styles]\"")
                    inStyles = False
                    break

                if inStyles and not (((";" in  line) or ("[" in line) or ("Format:" in line)) or line == ''):
                    logger.info(f"Ajout de la ligne \"{line}\"")
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
            logger.error(f"Une erreur inattendu est survenu | {e}")

    # * WORK : Fonctionne parfaitement
    def get_events(self, lines:list[str])->dict[str, dict[str, str]]:
        """Extraits les dialogues des lignes

        Args:
            ```py
            lines (list[str]): Lignes du fichier sous-titre
            ```

        Returns:
            ```py
            dict[str, dict[str, str]]: Dictionnaire contenant les informations des lignes de dialogues (numéroté de 1 à n)
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
            "2" : {
                "Layer" : "0",
                "Start" : "0:25:22.98",
                "End" : "0:25:25.00",
                "Style" : "Credit",
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
                    logger.info(f"Entrée dans la balise \"[Events]\"")
                    inEvents = True

                if inEvents and not (((";" in  line) or ("[" in line) or ("Format:" in line) or ("Comment:" in line)) or line == ''):
                    logger.info(f"Ajout de la ligne \"{line}\"")
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
            logger.error(f"Une erreur inattendu est survenu | {e}")

    # * WORK : Fonctionne parfaitement
    def get_tags(self, dialogue:str, recursive:bool = False)->dict[str, str | int | list | dict] | None:
        """Extrait les Tags du dialogue d'entrée

        Args:
            ```py
            dialogue (str): Dialogue en entré
            ```

        Returns:
            ```py
            dict[str, str | int | list[int]] | None: Retourne soit un dictionnaire ou rien si il y a oui un non des Tags dans le dialogue
            ```
        
        ```json
        {
            "blur" : "2",
            "pos" : ["230", "1120"],
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
                logger.info(f"Essaie de retrouver les Tags du dialogue \"{dialogue}\"")
                for group in re.findall(REGEX_ENTER, dialogue):
                    balise_num = re.findall(REGEX_NUM, group)
                    balise_color = re.findall(REGEX_COLOR, group)
                    balise_special = re.findall(REGEX_SPECIAL, group)
                    balise_t = re.findall(REGEX_T, group)
                    balise_string = re.findall(REGEX_STRING, group)

                    for balise in balise_num:
                        if re.match(r'(k|K|ko|kf)', balise[0]):
                            if balise[0] not in Tags:
                                Tags[balise[0]] = []
                            Tags[balise[0]].append(int(balise[1]))
                        else:
                            Tags[balise[0]] = int(balise[1])

                    for balise in balise_color:
                        Tags[balise[0]] = Convert.ASS_color_to_hex_color(balise[1])

                    for balise in balise_special:

                        if re.match(r'(iclip|clip)', balise[0]):
                            for var in re.findall(r'\((.*)?\)', balise[1]):
                                Tags[balise[0]] = var

                        if re.match(r'(pos|org)', balise[0]):
                            var = [int(var) for var in re.findall(r'\((.*)?\)', balise[1])[0].split(',',2)]
                            Tags[balise[0]] = {"x" : int(var[0]), "y" : int(var[1])}

                        if re.match(r'(move)', balise[0]):
                            var = [int(var) for var in re.findall(r'\((.*)?\)', balise[1])[0].split(',',6)]
                            Tags[balise[0]] = {"x1" : int(var[0]), "y1" : int(var[1]), "x2" : int(var[2]), "y2" : int(var[3]), "t1" : int(var[4]), "t2" : int(var[5])}

                        if re.match(r'(fad|fade)', balise[0]):
                            var = [int(var) for var in re.findall(r'\((.*)?\)', balise[1])[0].split(',',7)]
                            Tags[balise[0]] = {"a1" : int(var[0]), "a2" : int(var[1]), "a3" : int(var[2]), "t1" : int(var[3]), "t2" : int(var[4]), "t3" : int(var[5]), "t4" : int(var[6])}

                    for balise in balise_t:
                        var = balise[1].split(',', 4)
                        Tags[balise[0]] = {"t1" : int(var[0]), "t2" : int(var[1]), "accel" : int(var[2]), "tags" : self.get_tags(var[3], True)}

                    for balise in balise_string:
                        Tags[balise[0]] = balise[1]

            else:
                logger.info(f"Essaie de retrouver les Tags suite à une balise t \"{dialogue}\"")
                for group in re.findall(REGEX_ENTER_2, dialogue):
                    balise_num = re.findall(REGEX_NUM, group)
                    balise_color = re.findall(REGEX_COLOR, group)
                    balise_special = re.findall(REGEX_SPECIAL, group)
                    balise_t = re.findall(REGEX_T, group)
                    balise_string = re.findall(REGEX_STRING, group)

                    for balise in balise_num:
                        if re.match(r'(k|K|ko|kf)', balise[0]):
                            if balise[0] not in Tags:
                                Tags[balise[0]] = []
                            Tags[balise[0]].append(int(balise[1]))
                        else:
                            Tags[balise[0]] = int(balise[1])

                    for balise in balise_color:
                        Tags[balise[0]] = Convert.ASS_color_to_hex_color(balise[1])

                    for balise in balise_special:

                        if re.match(r'(iclip|clip)', balise[0]):
                            for var in re.findall(r'\((.*)?\)', balise[1]):
                                Tags[balise[0]] = var

                        if re.match(r'(pos|org)', balise[0]):
                            var = [int(var) for var in re.findall(r'\((.*)?\)', balise[1])[0].split(',',2)]
                            Tags[balise[0]] = {"x" : int(var[0]), "y" : int(var[1])}

                        if re.match(r'(move)', balise[0]):
                            var = [int(var) for var in re.findall(r'\((.*)?\)', balise[1])[0].split(',',6)]
                            Tags[balise[0]] = {"x1" : int(var[0]), "y1" : int(var[1]), "x2" : int(var[2]), "y2" : int(var[3]), "t1" : int(var[4]), "t2" : int(var[5])}

                        if re.match(r'(fad|fade)', balise[0]):
                            var = [int(var) for var in re.findall(r'\((.*)?\)', balise[1])[0].split(',',7)]
                            Tags[balise[0]] = {"a1" : int(var[0]), "a2" : int(var[1]), "a3" : int(var[2]), "t1" : int(var[3]), "t2" : int(var[4]), "t3" : int(var[5]), "t4" : int(var[6])}

                    for balise in balise_t:
                        var = balise[1].split(',', 4)
                        Tags[balise[0]] = {"t1" : int(var[0]), "t2" : int(var[1]), "accel" : int(var[2]), "tags" : self.get_tags(var[3], True)}

                    for balise in balise_string:
                        Tags[balise[0]] = balise[1]

            return Tags
        except Exception as e:
            logger.error(f"Il y a eu une erreur inattendu pour la balise \"{balise[0]}\" | {e}")

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