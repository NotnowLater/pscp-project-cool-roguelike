# RogueLike@Home
A Sci-fi roguelike game made in python with [libtcod](https://github.com/libtcod/python-tcod).

# Requirements
**Python 3.11+.**<br/>
[tcod](https://github.com/libtcod/python-tcod).<br/>
[just-playback](https://github.com/cheofusi/just_playback).<br/>
**Windows 10+.**<br/>
Required **libsdl2** on **Linux**.

# Installation
Clone this repositiory.
```
https://github.com/NotnowLater/pscp-project-cool-roguelike.git
```
Installs all the required modules.
```
pip install tcod just-playback
```
Run the main.py
```
python ./main.py
```

# Controls
|**Key**|**Description**|
|---|---|
|---|**Movement**|
|Kp - 7|Move Northwest|
|Kp - 8, Up|Move North|
|Kp - 9|Move Northeast|
|Kp - 6, Right|Move East|
|Kp - 3|Move Southeast|
|Kp - 2, Down|Move South|
|Kp - 1|Move Southwest|
|Kp - 4, Left|Move West|
|---|**Inventory**|
|i|Open Inventory to use Items|
|d|Open Inventory to drop Items.|
|---|**Gameplay**|
|Enter|Use/Drop/Select/Confirm.|
|g|Get/Pickup Item from the ground.|
|f|Ranged Attack.|
|c|Show character informations.|
|m|show messages log.|
|l|Look Mode.|
|h| Auto Heal If Have Healing Item|
|W|Auto Select Target in Range Attack Select.|
|Shift + .|Ascend Stair/Activate Self Destruct Button.|
|Esc|Save and Exit.|
