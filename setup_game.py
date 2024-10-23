"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod
import libtcodpy

import colors
from engine import Engine
import entity_factory
from game_map import GameWorld
import input_handlers

import audio

# Load the background image and remove the alpha channel.
background_image = tcod.image.load("menu_background.png")[:, :, :3]


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""
    map_width, map_height = 94, 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factory.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
    )
    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", colors.welcome_text
    )

    # dagger = copy.deepcopy(entity_factory.dagger)
    # leather_armor = copy.deepcopy(entity_factory.leather_armor)
    # pistol = copy.deepcopy(entity_factory.pistol)
    grenade = copy.deepcopy(entity_factory.explosive_grenade)

    # dagger.parent = player.inventory
    # leather_armor.parent = player.inventory

    # player.inventory.items.append(dagger)
    # player.equipment.toggle_equip(dagger, add_message=False)
    # player.inventory.items.append(leather_armor)
    # player.equipment.toggle_equip(leather_armor, add_message=False)

    # print(pistol.equippable.equipment_type)
    # player.inventory.items.append(pistol)

    return engine

def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine

class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""
    main_menu_snd : audio.AudioPlayBack = None

    def on_render(self, console: tcod.console.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)
        console.print(
            console.width // 2,
            console.height // 2 - 6,
            "RogueLike@Home",
            fg=colors.menu_title,
            alignment=libtcodpy.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By Who?",
            fg=colors.menu_title,
            alignment=libtcodpy.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        ):  
            dis = 2
            if i == 1:
                dis = 0
            elif i == 2:
                dis = -2
            console.print(
                console.width // 2,
                console.height // 2 - dis + i,
                text,
                # text.ljust(menu_width),
                fg=colors.menu_text,
                alignment=libtcodpy.CENTER,
                bg_blend=libtcodpy.BKGND_ALPHA(64),
            )
        star_pos = [(5, 5), (19, 9), (40, 45), (8, 24), (25, 35), (60, 25),
                    (20, 50), (37, 4), (55, 40),]
        for x,y in star_pos:
            console.print(x,y,"☻",fg=colors.white)
        # play the main menu sound
        if not self.main_menu_snd:
            self.main_menu_snd = audio.AudioPlayBack("sounds/scifimain.mp3", True)
        if not self.main_menu_snd.playback.playing:
            self.main_menu_snd.play()

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.KeySym.q, tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.c:
            try:
                ld = input_handlers.MainGameEventHandler(load_game("savegame.sav"))
                if ld:
                    self.main_menu_snd.stop()
                return ld
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.KeySym.n:
            self.main_menu_snd.stop()
            return input_handlers.MainGameEventHandler(new_game())
        return None