""" A Factory that hold all entities definitions that are use to spawn the entity. """

from components.ai_component import HostileEnemy, HostileRangedEnemy, StaticEnemy, TurretEnemy
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
    consumable=consumable.ExplosiveConsumable(damage=20, radius=3),
    weight=3,
)

bandage = Item(
    char="!",
    color=(127, 0, 255),
    name="Nano patch",
    consumable=consumable.HealingConsumable(amount=60),
    weight=2,
)

bandage2 = Item(
    char="!",
    color=(251, 243, 0),
    name="Nano patch++",
    consumable=consumable.HealingConsumable(amount=180),
    weight=3,
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

scythe = Item(char="/", color=(160, 86, 221), name="Galactic Scythe", equippable=equippable.Scythe(), weight=8,)

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
    weight=15,
)

combat_jumpsuit = Item(
    char="{",
    color=(160, 86, 221),
    name="Combat Jumpsuit",
    equippable=equippable.CombatJumpSuit(),
    weight=20,
)

combat_armor = Item(
    char="{",
    color=(255, 218, 0),
    name="Combat Armor",
    equippable=equippable.CombatArmor(),
    weight=24,
)

pistol = Item(
    char=";", color=(139, 69, 19), name="Nk-1 Pistol", equippable=equippable.Pistol(),
    weight=4,
)

smg = Item(
    char=";", color=(0, 191, 255), name="NK-2 Sub Machine Gun", equippable=equippable.SMG(),
    weight=6,
)

carbine_sa = Item(
    char=";", color=(88, 88, 88), name="NK-5 Semi-Auto Carbine", equippable=equippable.CarbineSA(),
    weight=8,
)

carbine_ba = Item(
    char=";", color=(255, 218, 0), name="NK-6 Burst Carbine", equippable=equippable.CarbineBA(),
    weight=8,
)

rifle_ap = Item(
    char=";", color=(160, 86, 221), name="NK-9 Anti Material Rifle", equippable=equippable.RifleAP(),
    weight=12,
)

rifle_laser = Item(
    char=";", color=(255, 0, 0), name="NK-11 Laser Rifle", equippable=equippable.RifleLaser(),
    weight=12,
)

beam_t = Item(
    char=";", color=(139, 69, 19), name="Turret Beam Emitter", equippable=equippable.TurretBeam(),
    weight=40,
)

pulse_t = Item(
    char=";", color=(139, 69, 19), name="Turret Beam Emitter", equippable=equippable.TurretPulse(),
    weight=40,
)

##############
# ACTORS     #
##############

player = Actor(char="☺", color=(255, 255, 255),
               name="Player",
               ai_class=HostileEnemy,equipment=Equipment(), 
               fighter=Fighter(hp=100, agility=14, strength=14, ammo=0),
               inventory=Inventory(capacity=0),
               level=Level(level_up_base=200),
               item_drop_chance = 0
               )

janitor = Actor(
    char="♥", 
    color=(255, 255, 255), 
    name="Janitor", 
    ai_class=HostileEnemy,
    equipment=Equipment(weapon=mop), 
    fighter=Fighter(hp=6, agility=6, strength=7, ammo=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=25),
    item_drop_chance = 0.3
    )

crew = Actor(
    char="♦", 
    color=(255, 255, 255), 
    name="Crew", 
    ai_class=HostileEnemy,equipment=Equipment(weapon=dagger, armor=leather_armor), 
    fighter=Fighter(hp=12, agility=6, strength=8, ammo=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=40),
    item_drop_chance = 0.16
    )

security = Actor(
    char="♣", 
    color=(255, 255, 255), 
    name="Security", 
    ai_class=HostileRangedEnemy,equipment=Equipment(weapon=pistol, armor=chain_mail), 
    fighter=Fighter(hp=16, agility=8, strength=8, ammo=6),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=45),
    item_drop_chance = 0.24
    )

security_smg = Actor(
    char="♠", 
    color=(255, 255, 255), 
    name="Security", 
    ai_class=HostileRangedEnemy,equipment=Equipment(weapon=smg, armor=chain_mail), 
    fighter=Fighter(hp=16, agility=8, strength=8, ammo=6),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=50),
    item_drop_chance = 0.3
    )

security_op = Actor(
    char="‼", 
    color=(255, 255, 255), 
    name="Security", 
    ai_class=HostileEnemy,equipment=Equipment(armor=chain_mail), 
    fighter=Fighter(hp=70, agility=8, strength=29, ammo=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
    item_drop_chance = 0.18
    )

security_laser = Actor(
    char="▬", 
    color=(255, 255, 255), 
    name="Security", 
    ai_class=HostileRangedEnemy,equipment=Equipment(weapon=rifle_laser, armor=chain_mail), 
    fighter=Fighter(hp=60, agility=9, strength=33, ammo=6),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=105),
    item_drop_chance = 0.19
    )

security_scythe = Actor(
    char="↨", 
    color=(255, 255, 255), 
    name="Security", 
    ai_class=HostileEnemy,equipment=Equipment(weapon=scythe, armor=chain_mail), 
    fighter=Fighter(hp=60, agility=7, strength=28, ammo=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=110),
    item_drop_chance = 0.4
    )

combat_droid = Actor(
    char="♂", 
    color=(255, 255, 255), 
    name="Combat Droid", 
    ai_class=HostileRangedEnemy,equipment=Equipment(weapon=smg), 
    fighter=Fighter(hp=20, agility=6, strength=4, ammo=100),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=55),
    item_drop_chance = 0.3
    )

marine_sa = Actor(
    char="♀", 
    color=(255, 255, 255), 
    name="Assault Marine", 
    ai_class=HostileRangedEnemy,equipment=Equipment(weapon=carbine_ba, armor=combat_armor),
    fighter=Fighter(hp=30, agility=8, strength=18, ammo=100),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=60),
    item_drop_chance = 0.32
    )

marine_ba = Actor(
    char="♪", 
    color=(255, 255, 255), 
    name="Support Marine", 
    ai_class=HostileRangedEnemy,equipment=Equipment(weapon=carbine_sa, armor=combat_armor), 
    fighter=Fighter(hp=30, agility=8, strength=18, ammo=100),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=60),
    item_drop_chance = 0.3
    )

marine_ap = Actor(
    char="♫", 
    color=(255, 255, 255), 
    name="Marine Sharpshooter", 
    ai_class=HostileRangedEnemy,equipment=Equipment(weapon=rifle_ap, armor=combat_armor), 
    fighter=Fighter(hp=30, agility=10, strength=16, ammo=100),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=70),
    item_drop_chance = 0.2
    )

marine_la = Actor(
    char="☼", 
    color=(255, 255, 255), 
    name="Marine Laser Sharpshooter", 
    ai_class=HostileRangedEnemy,equipment=Equipment(weapon=rifle_laser, armor=combat_armor), 
    fighter=Fighter(hp=30, agility=10, strength=20, ammo=100),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=75),
    item_drop_chance = 0.1
    )

beam_turret = Actor(
    char="►", 
    color=(255, 255, 255), 
    name="Beam Turret", 
    ai_class=TurretEnemy,equipment=Equipment(weapon=beam_t), 
    fighter=Fighter(hp=45, agility=0, strength=19, ammo=500),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=90),
    item_drop_chance = 0.0
    )

pulse_turret = Actor(
    char="◄", 
    color=(255, 255, 255), 
    name="Pulse Turret", 
    ai_class=TurretEnemy,equipment=Equipment(weapon=pulse_t), 
    fighter=Fighter(hp=45, agility=0, strength=19, ammo=1000),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=90),
    item_drop_chance = 0.0
    )

sniper_drone = Actor(
    char="¶", 
    color=(255, 255, 255), 
    name="Sniper Drone", 
    ai_class=HostileEnemy,equipment=Equipment(weapon=rifle_ap), 
    fighter=Fighter(hp=5, agility=30, strength=21, ammo=300),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=95),
    item_drop_chance = 0.0
    )

error_clone01 = Actor(
    char="○", 
    color=(255, 255, 255), 
    name="Failed Clone", 
    ai_class=HostileEnemy,equipment=Equipment(weapon=dagger, armor=chain_mail),
    fighter=Fighter(hp=25, agility=10, strength=10, ammo=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=70),
    item_drop_chance = 0.32
    )
error_clone02 = Actor(
    char="◙", 
    color=(255, 255, 255), 
    name="Failed Clone", 
    ai_class=HostileEnemy,equipment=Equipment(weapon=sword, armor=leather_armor), 
    fighter=Fighter(hp=50, agility=12, strength=11, ammo=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=75),
    item_drop_chance = 0.32
    )
human_kimera = Actor(
    char="•",
    color=(255, 255, 255),
    name="human kimera",
    ai_class=HostileEnemy,equipment=Equipment(weapon=sword, armor=leather_armor),
    fighter=Fighter(hp=60, agility=15, strength=10, ammo=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=80),
    item_drop_chance= 0.3
    )
material_kimera = Actor(
    char="◘",
    color=(255, 255, 255),
    name="material kimera",
    ai_class=HostileEnemy,equipment=Equipment(weapon=dagger),
    fighter=Fighter(hp=30, agility=25, strength=14, ammo=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=80),
    item_drop_chance=0.1
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
combat_droid_v2 = Actor(
    char="§", 
    color=(255, 255, 255), 
    name="Combat Droid V2", 
    ai_class=HostileRangedEnemy,equipment=Equipment(weapon=rifle_laser), 
    fighter=Fighter(hp=45, agility=6, strength=32, ammo=100),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=95),
    item_drop_chance = 0.3
    )
item_box2 = Actor(
    char="ß", 
    color=(255, 255, 255), 
    name="Item box", 
    ai_class=StaticEnemy,equipment=Equipment(), 
    fighter=Fighter(hp=24, agility=0, strength=0, ammo=1),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=0),
    item_drop_chance = 0
    )
table = Actor(
    char="Σ", 
    color=(255, 255, 255), 
    name="Table", 
    ai_class=StaticEnemy,equipment=Equipment(), 
    fighter=Fighter(hp=10, agility=0, strength=0, ammo=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=0),
    item_drop_chance = 0
    )
