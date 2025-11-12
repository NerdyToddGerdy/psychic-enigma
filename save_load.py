"""
Save/Load utilities for game state persistence
"""

import json
import os
from datetime import datetime
from generators.hex_grid import HexGrid
from generators.quest_generator import Quest
from generators.character import Player
from version import SAVE_VERSION


class GameState:
    """Represents the complete game state"""

    def __init__(self, hex_grid=None, quests=None, active_quest_index=None, completed_quests=None, player=None,
                 active_combat=None, current_day=1, movement_count=0, game_over=False, game_over_reason=None):
        """
        Initialize game state.

        Args:
            hex_grid (HexGrid): The hex grid
            quests (list[Quest]): List of available/active quests
            active_quest_index (int, optional): Index of currently active quest
            completed_quests (list[Quest]): List of completed quests
            player (Player, optional): Player character
            active_combat (CombatEncounter, optional): Active combat encounter
            current_day (int): Current day number (starts at 1)
            movement_count (int): Number of movements since last day increment (0-4)
            game_over (bool): Whether the game has ended
            game_over_reason (str, optional): Reason for game over
        """
        self.hex_grid = hex_grid if hex_grid else HexGrid()
        self.quests = quests if quests else []
        self.active_quest_index = active_quest_index
        self.completed_quests = completed_quests if completed_quests else []
        self.player = player  # Can be None until character is created
        self.active_combat = active_combat  # None when not in combat
        self.current_day = current_day  # Day counter (every 5 hex movements = 1 day)
        self.movement_count = movement_count  # Movements since last day (0-4)
        self.game_over = game_over  # Game over flag
        self.game_over_reason = game_over_reason  # Reason for game over

    @property
    def active_quest(self):
        """Get the currently active quest"""
        if self.active_quest_index is not None and 0 <= self.active_quest_index < len(self.quests):
            return self.quests[self.active_quest_index]
        return None

    def to_dict(self):
        """
        Convert game state to dictionary.

        Returns:
            dict: Serializable game state
        """
        data = {
            "version": SAVE_VERSION,
            "timestamp": datetime.now().isoformat(),
            "hex_grid": self.hex_grid.to_dict(),
            "quests": [quest.to_dict() for quest in self.quests],
            "active_quest_index": self.active_quest_index,
            "completed_quests": [quest.to_dict() for quest in self.completed_quests],
            "player": self.player.to_dict() if self.player else None,
            "active_combat": self.active_combat.to_dict() if self.active_combat else None,
            "current_day": self.current_day,
            "movement_count": self.movement_count,
            "game_over": self.game_over,
            "game_over_reason": self.game_over_reason,
        }
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Create game state from dictionary.

        Args:
            data (dict): Saved game state data

        Returns:
            GameState: Reconstructed game state
        """
        hex_grid = HexGrid.from_dict(data["hex_grid"])
        quests = [Quest.from_dict(q) for q in data["quests"]]
        active_quest_index = data.get("active_quest_index")
        completed_quests = [Quest.from_dict(q) for q in data.get("completed_quests", [])]

        # Load player if present
        player = None
        if data.get("player"):
            player = Player.from_dict(data["player"])

        # Load active combat if present
        active_combat = None
        if data.get("active_combat"):
            from combat import CombatEncounter
            active_combat = CombatEncounter.from_dict(data["active_combat"])

        # Load day counter fields (with defaults for backward compatibility)
        current_day = data.get("current_day", 1)
        movement_count = data.get("movement_count", 0)

        # Load game over fields (with defaults for backward compatibility)
        game_over = data.get("game_over", False)
        game_over_reason = data.get("game_over_reason", None)

        return cls(hex_grid, quests, active_quest_index, completed_quests, player, active_combat, current_day,
                   movement_count, game_over, game_over_reason)


def save_game(game_state, filename=None, save_dir="saves"):
    """
    Save game state to JSON file.

    Args:
        game_state (GameState): The game state to save
        filename (str, optional): Filename. If None, uses timestamp
        save_dir (str): Directory for save files

    Returns:
        str: Path to saved file
    """
    # Create saves directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"save_{timestamp}.json"

    # Ensure .json extension
    if not filename.endswith('.json'):
        filename += '.json'

    filepath = os.path.join(save_dir, filename)

    # Save to JSON
    with open(filepath, 'w') as f:
        json.dump(game_state.to_dict(), f, indent=2)

    return filepath


def load_game(filename, save_dir="saves"):
    """
    Load game state from JSON file.

    Args:
        filename (str): Name of save file
        save_dir (str): Directory containing save files

    Returns:
        GameState: Loaded game state

    Raises:
        FileNotFoundError: If save file doesn't exist
        ValueError: If save file is invalid
    """
    # Ensure .json extension
    if not filename.endswith('.json'):
        filename += '.json'

    filepath = os.path.join(save_dir, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Save file not found: {filepath}")

    # Load from JSON
    with open(filepath, 'r') as f:
        data = json.load(f)

    # Validate version (in case we need to handle migrations later)
    if "version" not in data:
        raise ValueError("Invalid save file: missing version")

    return GameState.from_dict(data)


def list_saves(save_dir="saves"):
    """
    List all available save files.

    Args:
        save_dir (str): Directory containing save files

    Returns:
        list[dict]: List of save file information
    """
    if not os.path.exists(save_dir):
        return []

    saves = []
    for filename in os.listdir(save_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(save_dir, filename)
            stat = os.stat(filepath)

            # Try to read timestamp from file
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    timestamp = data.get("timestamp", "Unknown")
                    player_pos = data.get("hex_grid", {}).get("player_position", (0, 0))
                    num_hexes = len(data.get("hex_grid", {}).get("hexes", {}))
                    num_quests = len(data.get("quests", []))
            except Exception:
                timestamp = "Unknown"
                player_pos = None
                num_hexes = 0
                num_quests = 0

            saves.append({
                "filename": filename,
                "filepath": filepath,
                "timestamp": timestamp,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "size": stat.st_size,
                "player_position": player_pos,
                "num_hexes": num_hexes,
                "num_quests": num_quests
            })

    # Sort by modification time (newest first)
    saves.sort(key=lambda x: x["modified"], reverse=True)
    return saves


def delete_save(filename, save_dir="saves"):
    """
    Delete a save file.

    Args:
        filename (str): Name of save file to delete
        save_dir (str): Directory containing save files

    Returns:
        bool: True if deleted successfully

    Raises:
        FileNotFoundError: If save file doesn't exist
    """
    # Ensure .json extension
    if not filename.endswith('.json'):
        filename += '.json'

    filepath = os.path.join(save_dir, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Save file not found: {filepath}")

    os.remove(filepath)
    return True
