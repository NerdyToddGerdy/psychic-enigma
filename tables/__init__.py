"""
Tables package for RPG Game
Contains all game tables and table rolling utilities
"""

from .table_roller import (
    roll_on_table,
    roll_on_table_by_name,
    roll_d4,
    roll_d6,
    roll_2d6,
    roll_3d6,
    roll_d66,
    roll_d20,
    roll_d100,
    roll_dice,
    get_all_table_names
)

from . import overland_tables
from . import dungeon_tables

__all__ = [
    'roll_on_table',
    'roll_on_table_by_name',
    'roll_d4',
    'roll_d6',
    'roll_2d6',
    'roll_3d6',
    'roll_d66',
    'roll_d20',
    'roll_d100',
    'roll_dice',
    'get_all_table_names',
    'overland_tables',
    'dungeon_tables'
]
