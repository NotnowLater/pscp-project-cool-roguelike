""" A Factory that hold all entities definitions that are use to spawn the entity. """

from components.ai_component import HostileEnemy
from components.fighter_component import Fighter
from components import consumable, equippable
from components.equipment import Equipment
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

player = Actor(char="☺", color=(255, 255, 255), name="Player", ai_class=HostileEnemy,equipment=Equipment(), fighter=Fighter(hp=100, base_dv=50, base_attack=60),inventory=Inventory(capacity=26),level=Level(level_up_base=200),)

orc = Actor(char="o", color=(63, 127, 63), name="Orc", ai_class=HostileEnemy,equipment=Equipment(), fighter=Fighter(hp=10, base_dv=0, base_attack=20),inventory=Inventory(capacity=0),level=Level(xp_given=35),)
troll = Actor(char="T", color=(0, 127, 0), name="Troll", ai_class=HostileEnemy,equipment=Equipment(), fighter=Fighter(hp=16, base_dv=1, base_attack=20),inventory=Inventory(capacity=0),level=Level(xp_given=100),)

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

dagger = Item(
    char="/", color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger()
)

sword = Item(char="/", color=(0, 191, 255), name="Sword", equippable=equippable.Sword())

leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char="[", color=(139, 69, 19), name="Chain Mail", equippable=equippable.ChainMail()
)
