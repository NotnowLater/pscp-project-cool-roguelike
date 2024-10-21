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

class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_die=1, attack_roll=4)


class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_die=2, attack_roll=4)

class Mop(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON, 
            attack_die=1, 
            attack_roll=2,
            tohit=-2
            )

class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, dv_bonus=2, defense=1)


class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, dv_bonus=5, defense=2)

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
            )