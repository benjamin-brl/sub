<div align="center">
    <a href="https://github.com/benjamin-brl/sub" target="_blank">
        <img src="/doc/assets/logo.svg" alt="Sub Logo" width="210" height="140"></img>
    </a>
</div>
<table>
    <tbody>
        <tr>
            <td align="center">Documentation</td>
            <td align="center">
                <a href="https://github.com/benjamin-brl/sub/wiki"><img src="https://img.shields.io/badge/v1-transparent?logo=read-the-docs&logoColor=white&label=docs&color=blue"></a>
            </td>
        </tr>
        <tr>
            <td align="center">In development</td>
            <td align="center">
                <img src="https://img.shields.io/badge/off-grey?logoColor=black&label=on&labelColor=green">
            </td>
        </tr>
    </tbody>
</table>

## What I need for use Sub ?
You need tkinter and langdetect. For this, either use this :
```sh
pip install -r requirements.txt
```
or install package manually :
```sh
pip install tkinter langdetect
```

## How to use it ?
### Instanciation
Get start to import and declare an instance of the module :
```py
import Sub
Subtitle = Sub()
```

### Load Subtitles in the module
```py
Subtitle.GetSubs()
```

### Work with loaded subtitles
```py
for sub in Subtitle.subs:
    ...
```

### Get all informations about subtitle
```py
for sub in Subtitle.subs:
    infos = sub.getSubInfo(sub)
```
If you want create a json file :
```py
import json
for sub in Subtitle.subs:
    infos = sub.getSubInfos(sub)
    # If you want to use filename of subtitle loaded
    with open(f'{infos["name"]}.json', "w", encoding="utf-8") as j:
    # If you want to use title script info of subtitle loaded
    with open(f'{infos["parts"]["Script Info"]["Title"]}.json', "w", encoding="utf-8") as j:
        # For full infos
        json.dump(infos, j)
        # For just dialogue
        json.dump(infos["parts"]["Events"], j)
```

### Get different parts of subtitle loaded
```py
Subtitle.getParts(sub)
```

### Get specific information about subtitle
For use the following methods properly, you need to read lines with the method `with open() as` like that :
```py
Subtitle = Sub()
Subtitle.getSubs()
for sub in Subtitle.subs:
    with open(sub, 'r') as f:
        lines = f.readlines()
        dialogues = Subtitle.getEvents(lines) # for exemple
```
The param `lines` is all the lines of subtitle loaded

#### Script Info
```py
Subtitle.getScriptInfo(lines)
```

#### Styles
```py
Subtitle.getStyles(lines)
```

#### Dialogues
```py
Subtitle.getEvents(lines)
```
##### Get tags of a dialogue
Note that this method processes a single line, not a set of lines. There are two ways to use this method properly:
- For work with dialogue's tags in the instance like this:
```py
Subtitle = Sub()
Subtitle.getSubs()
for sub in Subtitle.subs:
    with open(sub, 'r') as f:
        lines = f.readlines()
        dialogues = Subtitle.getEvents(lines)
        tags = dialogues["Tags"]

        # Work with Tags here
```
- For retrieving all tags individually on a list:
```py
Subtitle = Sub()
Subtitle.getSubs()

Tags = []
inEvents = False

for sub in Subtitle.subs:
    with open(sub, 'r') as f:
        lines = f.readlines()
        for i in range(1, len(lines)):
            line = lines[i].strip()
            if line == "[Events]":
                inEvents = True

            if inEvents and not (((";" in  line) or ("[" in line) or ("Format:" in line) or ("Comment:" in line)) or line == ''):
                Text = line.split(":", 1)[1].strip().split(',', 9)
                Tags.append(Subtitle.getTags(Text[9].strip()))

# Work with Tags here
```