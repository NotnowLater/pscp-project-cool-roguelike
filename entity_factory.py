""" A Factory that hold all entities definitions that are use to spawn the entity. """

from components.ai_component import HostileEnemy
from components.fighter_component import Fighter
from components import consumable, equippable
from components.equipment import Equipment
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

player = Actor(char="☺", color=(255, 255, 255), name="Player", ai_class=HostileEnemy,equipment=Equipment(), fighter=Fighter(hp=100, agility=10, strength=10),inventory=Inventory(capacity=26),level=Level(level_up_base=200),)

orc = Actor(char="J", color=(63, 127, 63), name="Janitor", ai_class=HostileEnemy,equipment=Equipment(), fighter=Fighter(hp=10, agility=6, strength=8),inventory=Inventory(capacity=0),level=Level(xp_given=35),)
troll = Actor(char="C", color=(0, 127, 0), name="Crew", ai_class=HostileEnemy,equipment=Equipment(), fighter=Fighter(hp=16, agility=8, strength=6),inventory=Inventory(capacity=0),level=Level(xp_given=100),)

flash_grenade = Item(
    char="~",
    color=(207, 63, 255),
    name="Flash grenade",
    consumable=consumable.FlashConsumable(number_of_turns=10, radius=3),
)

explosive_grenade = Item(
    char="~",
    color=(255, 0, 0),
    name="Explosive grenade",
    consumable=consumable.ExplosiveConsumable(damage=12, radius=3),
)

bandage = Item(
    char="!",
    color=(127, 0, 255),
    name="Nano patch",
    consumable=consumable.HealingConsumable(amount=4),
)

dagger = Item(
    char="/", color=(0, 191, 255), name="Knife", equippable=equippable.Dagger()
)

sword = Item(char="/", color=(0, 191, 255), name="Razorblade", equippable=equippable.Sword())

leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Jumpsuit",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char="[", color=(139, 69, 19), name="Reinforced Jumpsuit", equippable=equippable.ChainMail()
)
