from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Actor, Item


class Equipment(BaseComponent):
    parent: Actor

    def __init__(self, weapon: Optional[Item] = None, armor: Optional[Item] = None):
        self.weapon = weapon
        self.armor = armor

    @property
    def dv_bonus(self) -> int:
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.dv_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.dv_bonus

        return bonus

    @property
    def attack_base(self) -> int:
        base = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            base += self.weapon.equippable.attack_base

        if self.armor is not None and self.armor.equippable is not None:
            base += self.armor.equippable.attack_base

        return base

    @property
    def ranged_attack_base(self) -> int:
        base = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            base += self.weapon.equippable.ranged_attack_base

        if self.armor is not None and self.armor.equippable is not None:
            base += self.armor.equippable.ranged_attack_base

        return base

    @property 
    def tohit(self) -> int:
        th = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            th += self.weapon.equippable.tohit
        if self.armor is not None and self.armor.equippable is not None:
            th += self.armor.equippable.tohit
        return th
    
    @property
    def attack_roll(self) -> int:
        ar = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            ar += self.weapon.equippable.attack_roll
        if self.armor is not None and self.armor.equippable is not None:
            ar += self.armor.equippable.attack_roll
        return ar

    @property
    def attack_die(self) -> int:
        ad = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            ad += self.weapon.equippable.attack_die
        if self.armor is not None and self.armor.equippable is not None:
            ad += self.armor.equippable.attack_die
        return ad
    
    @property
    def ranged(self) -> int:
        if self.weapon is not None and self.weapon.equippable is not None:
            return self.weapon.equippable.ranged
        # if self.armor is not None and self.armor.equippable is not None:
        #     return True
        return False
    
    @property
    def ranged_attack_die(self) -> int:
        ra = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            ra += self.weapon.equippable.ranged_attack_die
        if self.armor is not None and self.armor.equippable is not None:
            ra += self.armor.equippable.ranged_attack_die
        return ra

    @property
    def ranged_tohit(self) -> int:
        ad = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            ad += self.weapon.equippable.ranged_tohit
        if self.armor is not None and self.armor.equippable is not None:
            ad += self.armor.equippable.ranged_tohit
        return ad

    @property
    def ranged_attack_roll(self) -> int:
        ad = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            ad += self.weapon.equippable.ranged_attack_roll
        if self.armor is not None and self.armor.equippable is not None:
            ad += self.armor.equippable.ranged_attack_roll
        return ad

    @property
    def ranged_attack_shot(self) -> int:
        ad = 0
        if self.weapon is not None and self.weapon.equippable is not None:
            ad += self.weapon.equippable.ranged_attack_shot
        if self.armor is not None and self.armor.equippable is not None:
            ad += self.armor.equippable.ranged_attack_shot
        return ad

    def item_is_equipped(self, item: Item) -> bool:
        return self.weapon == item or self.armor == item

    def unequip_message(self, item_name: str) -> None:
        self.parent.game_map.engine.message_log.add_message(
            f"You remove the {item_name}."
        )

    def equip_message(self, item_name: str) -> None:
        self.parent.game_map.engine.message_log.add_message(
            f"You equip the {item_name}."
        )

    def equip_to_slot(self, slot: str, item: Item, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if current_item is not None:
            self.unequip_from_slot(slot, add_message)

        setattr(self, slot, item)

        if add_message:
            self.equip_message(item.name)

    def unequip_from_slot(self, slot: str, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if add_message:
            self.unequip_message(current_item.name)

        setattr(self, slot, None)

    def toggle_equip(self, equippable_item: Item, add_message: bool = True) -> None:
        """ Determine if the equip action will equip or unequip the item. """
        if (
            equippable_item.equippable
            and equippable_item.equippable.equipment_type == EquipmentType.WEAPON
        ):
            slot = "weapon"
        else:
            slot = "armor"

        if getattr(self, slot) == equippable_item:
            self.unequip_from_slot(slot, add_message)
        else:
            self.equip_to_slot(slot, equippable_item, add_message)