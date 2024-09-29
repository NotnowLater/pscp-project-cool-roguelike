""" Store RenderOrder Enum use for ordering entity when rendering the game. """

from enum import auto, Enum

class RenderOrder(Enum):
    # Render Last
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()
    # Render First