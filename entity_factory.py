""" A Factory that hold all entities definitions that are use to spawn the entity. """

from components.ai_component import HostileEnemy
from components.fighter_component import Fighter
from components import consumable
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

player = Actor(char="☺", color=(255, 255, 255), name="Player", ai_class=HostileEnemy, fighter=Fighter(hp=100, dv=50, attack=60),inventory=Inventory(capacity=26),level=Level(level_up_base=200),)

orc = Actor(char="o", color=(63, 127, 63), name="Orc", ai_class=HostileEnemy, fighter=Fighter(hp=10, dv=0, attack=20),inventory=Inventory(capacity=0),level=Level(xp_given=35),)
troll = Actor(char="T", color=(0, 127, 0), name="Troll", ai_class=HostileEnemy, fighter=Fighter(hp=16, dv=1, attack=20),inventory=Inventory(capacity=0),level=Level(xp_given=100),)

flash_grenade = Item(
    char="~",
    color=(207, 63, 255),
    name="flash grenade",
    consumable=consumable.FlashConsumable(number_of_turns=10, radius=3),
)

explosive_grenade = Item(
    char="~",
    color=(255, 0, 0),
    name="explosive grenade",
    consumable=consumable.ExplosiveConsumable(damage=12, radius=3),
)

bandage = Item(
    char="!",
    color=(127, 0, 255),
    name="Bandage",
    consumable=consumable.HealingConsumable(amount=4),
)
