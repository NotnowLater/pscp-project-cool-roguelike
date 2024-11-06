""" Define all the game's rendering functions. """

from __future__ import annotations

from typing import Tuple,TYPE_CHECKING

import textwrap

import colors

if TYPE_CHECKING:
    from tcod.console import Console
    from engine import Engine
    from game_map import GameMap

wrapper = textwrap.TextWrapper(width=34, max_lines=3, placeholder="...")

def render_progress_bars(
        console : Console,
        current : int,
        max : int,
        total_width : int,
    ) -> None :
    """ Draw a progress bar with given value and size at the given location. """
    bar_width = int(float(current) / max * total_width)
    # Draw the bar's background.
    console.draw_rect(x=0, y=46, width=total_width, height=1, ch=1, bg=colors.bar_empty)
    # Draw the actual bar.
    if bar_width > 0:
        console.draw_rect(x=0, y=46, width=bar_width, height=1, ch=1, bg=colors.bar_filled)
    console.print(x=1, y=46, string=f"HP: {current}/{max}", fg=colors.bar_text)

def get_names_at_location(x : int, y : int, game_map : GameMap) -> str:
    """ Return entities names at the given location """
    if not game_map.is_in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(entity.name for entity in game_map.entities if entity.x == x and entity.y == y)

    return names.capitalize()

def render_dungeon_level(console: Console, dungeon_level: int, location: Tuple[int, int]) -> None:
    """
    Render the level the player is currently on, at the given location.
    """
    x, y = location

    console.print(x=x, y=y, string=f"Floor: {dungeon_level}")

def render_player_inventory_cap(console: Console, cap: int, max_cap: int, location: Tuple[int, int]) -> None:
    """
    Render the player's inventory capacity, at the given location.
    """
    x, y = location

    console.print(x=x, y=y, string=f"INV : {cap}/{max_cap}")

def render_player_ammo(console: Console, cap: int, location: Tuple[int, int]) -> None:
    """
    Render the player's ammo, at the given location.
    """
    x, y = location

    console.print(x=x, y=y, string=f"AM : {cap}")


def render_names_at_mouse_location(console: Console, x: int, y: int, engine: Engine) -> None:
    """ Render the entities name at the given location on the console."""
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(x=mouse_x, y=mouse_y, game_map=engine.game_map)
    # names_at_mouse_location = textwrap.wrap(names_at_mouse_location, width=34, max_lines=3, placeholder="...")
    offset = 0
    for i in wrapper.wrap(names_at_mouse_location):
        console.print(x=x, y=y + offset, string=i, fg=colors.impossible)
        offset += 1