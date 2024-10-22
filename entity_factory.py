""" A Factory that hold all entities definitions that are use to spawn the entity. """

from components.ai_component import HostileEnemy, HostileRangedEnemy, StaticEnemy
from components.fighter_component import Fighter
from components import consumable, equippable
from components.equipment import Equipment
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

##############
# ITEMS      #
##############
mop = Item(char="l", color=(125, 125, 125), name="Cleaning Mop", equippable=equippable.Mop(), weight=5)

flash_grenade = Item(
    char="~",
    color=(240, 240, 240),
    name="Flash grenade",
    consumable=consumable.FlashConsumable(number_of_turns=10, radius=3),
    weight=3,
)

explosive_grenade = Item(
    char="~",
    color=(255, 0, 0),
    name="Explosive grenade",
    consumable=consumable.ExplosiveConsumable(damage=12, radius=3),
    weight=3,
)

bandage = Item(
    char="!",
    color=(127, 0, 255),
    name="Nano patch",
    consumable=consumable.HealingConsumable(amount=60),
    weight=2,
)

ammo20 = Item(
    char="!",
    color=(0, 127, 255),
    name="Box of 20 Ammo",
    consumable=consumable.AmmoConsumable(amount=20),
    weight=4,
)

dagger = Item(
    char="/", color=(150, 150, 150), name="Knife", equippable=equippable.Dagger(),
    weight=2,
)

sword = Item(char="/", color=(0, 191, 255), name="Razorblade", equippable=equippable.Sword(), weight=4,)

leather_armor = Item(
    char="[",
    color=(69, 69, 69),
    name="Jumpsuit",
    equippable=equippable.LeatherArmor(),
    weight=10,
)

chain_mail = Item(
    char="[",
    color=(0, 191, 255),
    name="Reinforced Jumpsuit",
    equippable=equippable.ChainMail(),
    weight=20,
)

pistol = Item(
    char=";", color=(139, 69, 19), name="Nk-1 Pistol", equippable=equippable.Pistol(),
    weight=4,
)

##############
# ACTORS     #
##############

player = Actor(char="☺", color=(255, 255, 255), name="Player", ai_class=HostileEnemy,equipment=Equipment(), fighter=Fighter(hp=100, agility=14, strength=14, ammo=0),inventory=Inventory(capacity=0),level=Level(level_up_base=200),item_drop_chance = 0)

orc = Actor(
    char="♥", 
    color=(255, 255, 255), 
    name="Janitor", 
    ai_class=HostileEnemy,
    equipment=Equipment(weapon=mop), 
    fighter=Fighter(hp=6, agility=6, strength=6, ammo=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
    item_drop_chance = 0.35
    )
troll = Actor(
    char="♦", 
    color=(255, 255, 255), 
    name="Crew", 
    ai_class=HostileEnemy,equipment=Equipment(), 
    fighter=Fighter(hp=12, agility=6, strength=8, ammo=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
    item_drop_chance = 0
    )

security = Actor(
    char="♣", 
    color=(255, 255, 255), 
    name="Security", 
    ai_class=HostileRangedEnemy,equipment=Equipment(weapon=pistol, armor=leather_armor), 
    fighter=Fighter(hp=14, agility=8, strength=8, ammo=1),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=125),
    item_drop_chance = 0.2
    ) 
item_box = Actor(
    char="Γ", 
    color=(255, 255, 255), 
    name="Item box", 
    ai_class=StaticEnemy,equipment=Equipment(), 
    fighter=Fighter(hp=14, agility=0, strength=0, ammo=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=0),
    item_drop_chance = 0
    ) 
