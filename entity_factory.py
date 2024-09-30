""" A Factory that hold all entities definitions that are use to spawn the entity. """

from components.ai_component import HostileEnemy
from components.fighter_component import Fighter
from entity import Actor

player = Actor(char="@", color=(255, 255, 255), name="Player", ai_class=HostileEnemy, fighter=Fighter(hp=100, dv=200, attack=60),)

orc = Actor(char="o", color=(63, 127, 63), name="Orc", ai_class=HostileEnemy, fighter=Fighter(hp=10, dv=0, attack=20),)
troll = Actor(char="T", color=(0, 127, 0), name="Troll", ai_class=HostileEnemy, fighter=Fighter(hp=16, dv=1, attack=20),)

