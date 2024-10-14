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
        dv_bonus: int = 0,
        ranged: bool = False,
    ):
        self.equipment_type = equipment_type
        self.tohit = tohit
        self.attack_die = attack_die
        self.attack_roll = attack_roll
        self.dv_bonus = dv_bonus
        self.ranged = ranged

class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_die=1, attack_roll=4)


class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_die=2, attack_roll=4)


class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, dv_bonus=1)


class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, dv_bonus=3)