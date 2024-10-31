""" Define all the equipment (equippable) in the game. """

from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item


class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        tohit: int = 0,
        attack_die: int = 0,
        attack_roll: int = 0,
        attack_base: int = 0,
        dv_bonus: int = 0,
        ranged: bool = False,
        ranged_tohit: int = 0,
        ranged_attack_die: int = 0,
        ranged_attack_roll: int = 0,
        ranged_attack_base: int = 0,
        ranged_attack_shot: int = 0,
        defense: int = 0,
        atk_snd_id: str = "knife_1",
    ):
        self.equipment_type = equipment_type
        self.tohit = tohit
        self.attack_die = attack_die
        self.attack_roll = attack_roll
        self.attack_base = attack_base
        self.dv_bonus = dv_bonus
        self.ranged = ranged
        self.ranged_tohit = ranged_tohit
        self.ranged_attack_die = ranged_attack_die
        self.ranged_attack_roll = ranged_attack_roll
        self.ranged_attack_base = ranged_attack_base
        self.ranged_attack_shot = ranged_attack_shot
        self.defense = defense
        self.atk_snd_id = atk_snd_id

class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_die=1, attack_roll=4, atk_snd_id="knife_1")


class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_die=2, attack_roll=4, atk_snd_id="knife_1")

class Mop(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON, 
            attack_die=1, 
            attack_roll=2,
            tohit=-2,
            atk_snd_id="punch_1"
            )

class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, dv_bonus=2, defense=1)


class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, dv_bonus=4, defense=2)

class CombatJumpSuit(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, dv_bonus=6, defense=2)

class CombatArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, dv_bonus=7, defense=3)

class Pistol(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON, 
            attack_die=1, 
            attack_roll=2, 
            ranged=True,
            ranged_attack_die=2,
            ranged_attack_roll=4,
            ranged_attack_base=2,
            ranged_tohit=1,
            ranged_attack_shot=1,
            atk_snd_id="gun_1",
            )
        
class SMG(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON, 
            attack_die=1, 
            attack_roll=2, 
            ranged=True,
            ranged_attack_die=2,
            ranged_attack_roll=4,
            ranged_attack_base=2,
            ranged_tohit=0,
            ranged_attack_shot=3,
            atk_snd_id="gun_1",
            )

class CarbineSA(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON, 
            attack_die=2, 
            attack_roll=2, 
            ranged=True,
            ranged_attack_die=2,
            ranged_attack_roll=6,
            ranged_attack_base=2,
            ranged_tohit=2,
            ranged_attack_shot=1,
            atk_snd_id="gun_1",
            )

class CarbineBA(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON, 
            attack_die=2, 
            attack_roll=2, 
            ranged=True,
            ranged_attack_die=2,
            ranged_attack_roll=6,
            ranged_attack_base=2,
            ranged_tohit=1,
            ranged_attack_shot=2,
            atk_snd_id="gun_1",
            )
        
class RifleAP(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON, 
            attack_die=2, 
            attack_roll=2, 
            ranged=True,
            ranged_attack_die=4,
            ranged_attack_roll=4,
            ranged_attack_base=4,
            ranged_tohit=3,
            ranged_attack_shot=1,
            atk_snd_id="gun_1",
            )

class RifleLaser(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON, 
            attack_die=2, 
            attack_roll=2, 
            ranged=True,
            ranged_attack_die=1,
            ranged_attack_roll=12,
            ranged_attack_base=4,
            ranged_tohit=2,
            ranged_attack_shot=1,
            atk_snd_id="gun_1",
            )
   
class TurretBeam(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON, 
            attack_die=1, 
            attack_roll=1, 
            ranged=True,
            ranged_attack_die=1,
            ranged_attack_roll=8,
            ranged_attack_base=0,
            ranged_tohit=4,
            ranged_attack_shot=1,
            atk_snd_id="gun_1",
            )
        
class TurretPulse(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON, 
            attack_die=1, 
            attack_roll=1, 
            ranged=True,
            ranged_attack_die=1,
            ranged_attack_roll=2,
            ranged_attack_base=0,
            ranged_tohit=2,
            ranged_attack_shot=4,
            atk_snd_id="gun_1",
            )