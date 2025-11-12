"""
Game State Manager for API
Handles game state operations and quest management
"""

from datetime import datetime

from generators import generate_quest_with_location
from generators.dungeon_generator import parse_treasure_to_item
from save_load import GameState, save_game, load_game, list_saves
from tables import overland_tables, dungeon_tables
from tables.table_roller import roll_on_table, roll_d6


class GameManager:
    """Manages game state for the API"""

    def __init__(self):
        """Initialize game manager with new game"""
        self.game_state = GameState()

    def new_game(self):
        """
        Start a new game.

        Returns:
            dict: New game state
        """
        self.game_state = GameState()
        return self.get_state()

    def get_state(self):
        """
        Get complete game state for client.

        Returns:
            dict: Complete game state including player and combat
        """
        return {
            "hex_grid": {
                "player_position": self.game_state.hex_grid.player_position,
                "hexes": [
                    self._hex_to_client_format(hex_obj)
                    for hex_obj in self.game_state.hex_grid.hexes.values()
                ],
                "visible_hexes": [
                    self._hex_to_client_format(hex_obj)
                    for hex_obj in self.game_state.hex_grid.get_visible_hexes()
                ]
            },
            "quests": [
                {
                    **quest.to_dict(),
                    "index": i,
                    "is_active": i == self.game_state.active_quest_index
                }
                for i, quest in enumerate(self.game_state.quests)
            ],
            "active_quest": {
                **self.game_state.active_quest.to_dict(),
                "index": self.game_state.active_quest_index
            } if self.game_state.active_quest else None,
            "completed_quests": [
                {
                    **quest.to_dict(),
                    "completion_order": i + 1
                }
                for i, quest in enumerate(self.game_state.completed_quests)
            ],
            "player": self.game_state.player.to_dict() if self.game_state.player else None,
            "active_combat": self.game_state.active_combat.get_combat_status()
            if self.game_state.active_combat else None,
            "current_day": self.game_state.current_day,
            "movement_count": self.game_state.movement_count
        }

    def _hex_to_client_format(self, hex_obj):
        """
        Convert hex to client-friendly format.

        Args:
            hex_obj (Hex): Hex object

        Returns:
            dict: Client-formatted hex data
        """
        # Check if this hex has a dungeon (from active quest)
        has_dungeon = False
        if self.game_state.active_quest and self.game_state.active_quest.dungeon:
            quest_coords = self.game_state.active_quest.coordinates
            if quest_coords and hex_obj.q == quest_coords[0] and hex_obj.r == quest_coords[1]:
                has_dungeon = True

        data = {
            "q": hex_obj.q,
            "r": hex_obj.r,
            "terrain": hex_obj.terrain,
            "water": hex_obj.water,
            "revealed": hex_obj.revealed,
            "explored": hex_obj.explored,
            "is_settlement": hex_obj.is_settlement,
            "settlement_type": hex_obj.settlement_type,
            "has_dungeon": has_dungeon
        }

        # Only include detailed info if explored
        if hex_obj.explored:
            data["weather"] = hex_obj.weather
            data["discoveries"] = hex_obj.discoveries

            # Serialize dangers (convert Monster objects to dicts)
            serialized_dangers = []
            for danger in hex_obj.dangers:
                danger_copy = danger.copy()
                # If danger detail contains monsters, serialize them
                if isinstance(danger_copy.get("detail"), dict) and "monsters" in danger_copy["detail"]:
                    detail_copy = danger_copy["detail"].copy()
                    from generators.monster import Monster
                    monsters = detail_copy.get("monsters", [])
                    if monsters:
                        detail_copy["monsters"] = [m.to_dict() for m in monsters]
                    danger_copy["detail"] = detail_copy
                serialized_dangers.append(danger_copy)
            data["dangers"] = serialized_dangers

        return data

    def _process_hazard_save(self, hazard_name, player):
        """
        Process a hazard save according to Single Sheet rules (page 3).
        Roll 1d20 equal to or under the relevant attribute to avoid the hazard.

        Args:
            hazard_name (str): Name of the hazard
            player: Player character

        Returns:
            dict: Save result with roll, target, success, and consequences
        """
        import random

        # Determine appropriate save attribute and damage for each hazard type
        hazard_config = {
            # Overland hazards
            "Bog": {"attribute": "strength", "damage": 0, "description": "escape the bog"},
            "Landslide": {"attribute": "dexterity", "damage": "1d6", "description": "avoid falling rocks"},
            "Sinkhole": {"attribute": "dexterity", "damage": "1d6", "description": "dodge the collapsing ground"},
            "Poison": {"attribute": "toughness", "damage": "1d6", "description": "resist the poison"},
            "Weather": {"attribute": "toughness", "damage": 0, "description": "endure harsh weather"},

            # Dungeon hazards
            "Debris": {"attribute": "strength", "damage": 0, "description": "clear the debris"},
            "Collapse": {"attribute": "toughness", "damage": "1d6", "description": "survive the collapse"},
            "Vapor": {"attribute": "toughness", "damage": "1d6", "description": "resist toxic vapors"},
            "Toxin": {"attribute": "toughness", "damage": "1d6", "description": "resist the toxin"},
            "Ruin": {"attribute": "dexterity", "damage": "1d6", "description": "avoid crumbling ruins"}
        }

        config = hazard_config.get(hazard_name, {"attribute": "toughness", "damage": "1d6", "description": "survive"})

        # Get the appropriate attribute value
        attribute_name = config["attribute"]
        attribute_value = getattr(player, attribute_name, 10)

        # Roll 1d20 vs attribute (≤ attribute = success)
        roll = random.randint(1, 20)
        success = roll <= attribute_value

        result = {
            "hazard": hazard_name,
            "attribute": attribute_name.upper()[:3],  # STR, DEX, WIL, TOU
            "roll": roll,
            "target": attribute_value,
            "success": success,
            "description": config["description"]
        }

        # Apply consequences
        if not success and config["damage"]:
            # Failed save - take damage
            if config["damage"] == "1d6":
                damage = random.randint(1, 6)
            else:
                damage = 0

            player.hp_current = max(0, player.hp_current - damage)
            result["damage"] = damage
            result["consequence"] = f"Failed to {config['description']}! Took {damage} damage."
        elif not success:
            result["consequence"] = f"Failed to {config['description']}, but no damage taken."
        else:
            result["consequence"] = f"Successfully {config['description']}!"

        return result

    @staticmethod
    def _process_trap_save(trap_name, player):
        """
        Process a trap save according to Single Sheet rules (page 3).
        Roll 1d20 equal to or under the relevant attribute to avoid the trap.

        Args:
            trap_name (str): Name of the trap
            player: Player character

        Returns:
            dict: Save result with roll, target, success, and consequences
        """
        import random

        # Determine appropriate save attribute and damage for each trap type
        trap_config = {
            "Pit": {"attribute": "dexterity", "damage": "1d6", "description": "dodge the pit trap"},
            "Dart": {"attribute": "dexterity", "damage": "1d6", "description": "dodge the poison dart"},
            "Spike": {"attribute": "dexterity", "damage": "1d6", "description": "avoid the spike trap"},
            "Pendulum": {"attribute": "dexterity", "damage": "1d6", "description": "duck under the swinging blade"},
            "Boulder": {"attribute": "toughness", "damage": "1d6", "description": "withstand the rolling boulder"},
            "Acid": {"attribute": "toughness", "damage": "1d6", "description": "resist the acid spray"}
        }

        config = trap_config.get(trap_name,
                                 {"attribute": "dexterity", "damage": "1d6", "description": "avoid the trap"})

        # Get the appropriate attribute value
        attribute_name = config["attribute"]
        attribute_value = getattr(player, attribute_name, 10)

        # Roll 1d20 vs attribute (≤ attribute = success)
        roll = random.randint(1, 20)
        success = roll <= attribute_value

        result = {
            "trap": trap_name,
            "attribute": attribute_name.upper()[:3],  # DEX or TOU
            "roll": roll,
            "target": attribute_value,
            "success": success,
            "description": config["description"]
        }

        # Apply consequences
        if not success and config["damage"]:
            # Failed save - take damage
            if config["damage"] == "1d6":
                damage = random.randint(1, 6)
            else:
                damage = 0

            player.hp_current = max(0, player.hp_current - damage)
            result["damage"] = damage
            result["consequence"] = f"Failed to {config['description']}! Took {damage} damage."
        elif not success:
            result["consequence"] = f"Failed to {config['description']}, but no damage taken."
        else:
            result["consequence"] = f"Successfully {config['description']}!"

        return result

    def generate_quest(self):
        """
        Generate a new quest and add to quest list.
        Can only be done in settlements.

        Returns:
            dict: Generated quest with index

        Raises:
            ValueError: If not in a settlement
        """
        # Check if player is in a settlement
        current_hex = self.game_state.hex_grid.get_current_hex()

        # Check for active quest destination (quest destinations count as settlements)
        at_quest_destination = False
        if self.game_state.active_quest:
            quest_coords = self.game_state.active_quest.coordinates
            if quest_coords and quest_coords == self.game_state.hex_grid.player_position:
                at_quest_destination = True

        if not (current_hex.is_settlement or at_quest_destination):
            raise ValueError("Must be in a settlement to generate quests")

        # Collect all existing quest coordinates to avoid duplicates
        excluded_coords = []

        # Add active quest coordinates
        if self.game_state.active_quest and self.game_state.active_quest.coordinates:
            excluded_coords.append(self.game_state.active_quest.coordinates)

        # Add available quest coordinates
        for quest in self.game_state.quests:
            if quest.coordinates:
                excluded_coords.append(quest.coordinates)

        # Add completed quest coordinates
        for quest in self.game_state.completed_quests:
            if quest.coordinates:
                excluded_coords.append(quest.coordinates)

        quest = generate_quest_with_location(self.game_state.hex_grid, excluded_coords)
        self.game_state.quests.append(quest)
        quest_index = len(self.game_state.quests) - 1

        return {
            **quest.to_dict(),
            "index": quest_index,
            "is_active": False
        }

    def accept_quest(self, quest_index):
        """
        Accept a quest by index.

        Args:
            quest_index (int): Index of quest to accept

        Returns:
            dict: Result of quest acceptance

        Raises:
            ValueError: If quest index is invalid
        """
        if quest_index < 0 or quest_index >= len(self.game_state.quests):
            raise ValueError(f"Invalid quest index: {quest_index}")

        self.game_state.active_quest_index = quest_index
        quest = self.game_state.quests[quest_index]

        return {
            "success": True,
            "quest": quest.to_dict(),
            "message": f"Quest accepted: {quest.action} {quest.target}"
        }

    def complete_quest(self, quest_index):
        """
        Complete a quest and roll on CLUE_FOUND table.
        On 5-6, generate a new quest.

        Args:
            quest_index (int): Index of quest to complete

        Returns:
            dict: Completion results with CLUE_FOUND roll and any new quest

        Raises:
            ValueError: If quest index invalid or player not at destination
        """
        if quest_index < 0 or quest_index >= len(self.game_state.quests):
            raise ValueError(f"Invalid quest index: {quest_index}")

        quest = self.game_state.quests[quest_index]

        # Verify player is at quest destination
        if not quest.coordinates:
            raise ValueError("Quest has no destination coordinates")

        if quest.coordinates != self.game_state.hex_grid.player_position:
            raise ValueError("Must be at quest destination to complete it")

        # Mark quest as completed
        quest.completed = True
        quest.completion_timestamp = datetime.now().isoformat()
        quest.completion_coordinates = self.game_state.hex_grid.player_position

        # Award XP for quest completion
        # PDF Rule: 1 XP per completed dungeon/quest
        quest_xp = 1

        levels_gained = self.game_state.player.gain_xp(quest_xp)

        # Roll on CLUE_FOUND table
        clue_result = roll_on_table(overland_tables.CLUE_FOUND)

        result = {
            "success": True,
            "quest": quest.to_dict(),
            "clue_found": clue_result,
            "new_quest": None,
            "xp_gained": quest_xp,
            "levels_gained": levels_gained
        }

        # On 5 or 6 (Narrative Shift or Clues), generate a new quest
        if clue_result in ["Narrative Shift", "Clues"]:
            # Collect all existing quest coordinates to avoid duplicates
            excluded_coords = []

            # Add active quest coordinates (but not the one we just completed)
            if self.game_state.active_quest and self.game_state.active_quest.coordinates:
                if self.game_state.active_quest != quest:  # Don't exclude the just-completed quest
                    excluded_coords.append(self.game_state.active_quest.coordinates)

            # Add available quest coordinates
            for q in self.game_state.quests:
                if q.coordinates:
                    excluded_coords.append(q.coordinates)

            # Add completed quest coordinates (including the one being completed)
            for q in self.game_state.completed_quests:
                if q.coordinates:
                    excluded_coords.append(q.coordinates)
            # Also add the quest being completed
            if quest.coordinates:
                excluded_coords.append(quest.coordinates)

            new_quest = generate_quest_with_location(self.game_state.hex_grid, excluded_coords)
            self.game_state.quests.append(new_quest)
            new_quest_index = len(self.game_state.quests) - 1

            result["new_quest"] = {
                **new_quest.to_dict(),
                "index": new_quest_index,
                "is_active": False
            }

        # Move quest to completed_quests list
        self.game_state.completed_quests.append(quest)

        # Remove quest from active quests list
        self.game_state.quests.pop(quest_index)

        # Clear active quest index
        if self.game_state.active_quest_index == quest_index:
            self.game_state.active_quest_index = None
        elif self.game_state.active_quest_index is not None and self.game_state.active_quest_index > quest_index:
            # Adjust active quest index if it's after the removed quest
            self.game_state.active_quest_index -= 1

        return result

    def move_player(self, q, r):
        """
        Move player to specific hex coordinates.

        Args:
            q (int): Target column coordinate
            r (int): Target row coordinate

        Returns:
            dict: Movement results including exploration

        Raises:
            ValueError: If hex is not revealed or reachable
        """
        target_hex = self.game_state.hex_grid.get_hex_at(q, r)

        # Check if hex exists and is revealed
        if target_hex is None:
            raise ValueError(f"Hex ({q}, {r}) does not exist")

        if not target_hex.revealed and not target_hex.explored:
            raise ValueError(f"Hex ({q}, {r}) is not yet revealed")

        # Calculate direction and distance from current position
        current_pos = self.game_state.hex_grid.player_position
        distance = self.game_state.hex_grid.distance_between(current_pos, (q, r))

        if distance == 0:
            return {
                "success": False,
                "message": "Already at that location",
                "current_position": current_pos
            }

        # For simplicity, we'll teleport to adjacent hexes
        # In a real implementation, you might want pathfinding
        if distance > 1:
            # Check if this is the active quest destination
            active_quest = self.game_state.active_quest
            if active_quest and active_quest.coordinates == (q, r):
                # Allow direct travel to quest destination
                pass
            else:
                raise ValueError(f"Can only move to adjacent hexes (distance: {distance})")

        # Perform movement by calculating direction
        dq = q - current_pos[0]
        dr = r - current_pos[1]

        # Find matching direction or use direct coordinate setting for quest destinations
        direction = None
        from generators.hex_grid import AXIAL_DIRECTIONS
        for dir_num, (dir_dq, dir_dr) in AXIAL_DIRECTIONS.items():
            if dir_dq * distance == dq and dir_dr * distance == dr:
                direction = dir_num
                break

        if direction:
            # Use normal movement
            result = self.game_state.hex_grid.move_player(direction, distance)
        else:
            # Direct teleport to quest destination
            self.game_state.hex_grid.player_position = (q, r)
            if not target_hex.explored:
                exploration_result = target_hex.explore()
                result = {
                    "direction": "Direct",
                    "distance": distance,
                    "path": [target_hex],
                    "explorations": [{
                        "hex": (q, r),
                        "result": exploration_result
                    }],
                    "final_position": (q, r)
                }
            else:
                result = {
                    "direction": "Direct",
                    "distance": distance,
                    "path": [target_hex],
                    "explorations": [],
                    "final_position": (q, r)
                }

            # Reveal adjacent hexes around new position
            self.game_state.hex_grid.reveal_adjacent_hexes()

        # Check if arriving at active quest destination and generate dungeon
        dungeon_generated = None
        if self.game_state.active_quest:
            quest = self.game_state.active_quest
            # Only generate dungeon if:
            # 1. Player is at quest coordinates
            # 2. Quest doesn't already have a dungeon
            # 3. Quest is not completed
            if quest.coordinates == (q, r) and quest.dungeon is None and not quest.completed:
                # Generate dungeon when arriving at quest destination
                from generators import generate_dungeon
                dungeon = generate_dungeon()
                quest.dungeon = dungeon
                # Only show discovery modal if dungeon hasn't been entered yet
                if not dungeon.entered:
                    dungeon_generated = dungeon.to_dict()

        # Check for hostile encounters and hazards in explorations
        combat_started = False
        hazard_saves = []
        for exp in result.get("explorations", []):
            if exp["result"].get("dangers"):
                for danger in exp["result"]["dangers"]:
                    # Handle hostile encounters
                    if not combat_started and danger["type"] == "Hostile" and isinstance(danger["detail"], dict):
                        # Hostile danger with monsters encountered
                        if "monsters" in danger["detail"] and danger["detail"]["monsters"]:
                            # Start combat with the monsters
                            from combat import CombatEncounter
                            monsters = danger["detail"]["monsters"]

                            # Create combat encounter
                            self.game_state.active_combat = CombatEncounter(
                                self.game_state.player,
                                monsters
                            )
                            combat_started = True
                    # Handle unnatural encounters (undead/demons)
                    elif not combat_started and danger["type"] == "Unnatural" and isinstance(danger["detail"], dict):
                        # Unnatural danger with monsters encountered
                        if "monsters" in danger["detail"] and danger["detail"]["monsters"]:
                            # Start combat with the unnatural monsters
                            from combat import CombatEncounter
                            monsters = danger["detail"]["monsters"]

                            # Create combat encounter
                            self.game_state.active_combat = CombatEncounter(
                                self.game_state.player,
                                monsters
                            )
                            combat_started = True
                    # Handle hazards with saves
                    elif danger["type"] == "Hazard" and self.game_state.player:
                        # Process hazard save
                        hazard_name = danger.get("detail")
                        if hazard_name:
                            save_result = self._process_hazard_save(hazard_name, self.game_state.player)
                            hazard_saves.append(save_result)

        # Helper function to sanitize exploration results (serialize Monster objects)
        def sanitize_exploration_result(exp_result):
            """Serialize non-serializable objects (like Monsters) from exploration results"""
            sanitized = exp_result.copy()
            if "dangers" in sanitized:
                sanitized_dangers = []
                for danger in sanitized["dangers"]:
                    danger_copy = danger.copy()
                    # Serialize Monster objects from detail if present
                    if isinstance(danger_copy.get("detail"), dict) and "monsters" in danger_copy["detail"]:
                        detail_copy = danger_copy["detail"].copy()
                        # Convert Monster objects to dictionaries
                        from generators.monster import Monster
                        monsters = detail_copy.get("monsters", [])
                        if monsters:
                            detail_copy["monsters"] = [m.to_dict() for m in monsters]
                        danger_copy["detail"] = detail_copy
                    sanitized_dangers.append(danger_copy)
                sanitized["dangers"] = sanitized_dangers
            return sanitized

        # Award XP for exploration (1 XP per newly explored hex - PDF rule)
        num_explored = len(result.get("explorations", []))
        exploration_xp = num_explored * 1
        levels_gained = []
        if exploration_xp > 0 and self.game_state.player:
            levels_gained = self.game_state.player.gain_xp(exploration_xp)

        # Track day counter (every 5 hex movements = 1 day)
        self.game_state.movement_count += 1
        day_advanced = False
        ration_prompt_available = False
        ration_heal_amount = 0

        if self.game_state.movement_count >= 5:
            self.game_state.current_day += 1
            self.game_state.movement_count = 0
            day_advanced = True

            # Check if ration prompt should be offered
            if self.game_state.player:
                has_ration = self.game_state.player.find_item_by_name("Ration") is not None
                not_at_full_hp = self.game_state.player.hp_current < self.game_state.player.hp_max

                if has_ration and not_at_full_hp:
                    ration_prompt_available = True
                    # Calculate potential heal amount (half HP, rounded up)
                    import math
                    max_hp = self.game_state.player.hp_max
                    heal_amount = math.ceil(max_hp / 2)
                    ration_heal_amount = min(heal_amount, max_hp - self.game_state.player.hp_current)

        # Format response
        response = {
            "success": True,
            "movement": {
                "from": current_pos,
                "to": result["final_position"],
                "distance": result["distance"]
            },
            "explorations": [
                {
                    "coordinates": exp["hex"],
                    "hex": self._hex_to_client_format(
                        self.game_state.hex_grid.get_hex_at(exp["hex"][0], exp["hex"][1])
                    ),
                    "results": sanitize_exploration_result(exp["result"])
                }
                for exp in result.get("explorations", [])
            ],
            "current_position": result["final_position"],
            "xp_gained": exploration_xp,
            "levels_gained": levels_gained,
            "hazard_saves": hazard_saves,  # Include hazard save results
            "day_advanced": day_advanced,
            "current_day": self.game_state.current_day,
            "movement_count": self.game_state.movement_count,
            "ration_prompt_available": ration_prompt_available,
            "ration_heal_amount": ration_heal_amount
        }

        # Add combat info if started
        if combat_started and self.game_state.active_combat:
            response["combat_started"] = True
            response["combat"] = self.game_state.active_combat.get_combat_status()

        # Add dungeon info if generated
        if dungeon_generated:
            response["dungeon_generated"] = dungeon_generated

        return response

    def get_hex_info(self, q, r):
        """
        Get information about a specific hex.

        Args:
            q (int): Column coordinate
            r (int): Row coordinate

        Returns:
            dict: Hex information or None
        """
        hex_obj = self.game_state.hex_grid.get_hex_at(q, r)
        if hex_obj is None:
            return None

        return self._hex_to_client_format(hex_obj)

    def save(self, filename=None):
        """
        Save current game state.

        Args:
            filename (str, optional): Save filename

        Returns:
            dict: Save result
        """
        filepath = save_game(self.game_state, filename)
        return {
            "success": True,
            "filepath": filepath,
            "message": f"Game saved to {filepath}"
        }

    def load(self, filename):
        """
        Load game state from file.

        Args:
            filename (str): Save filename

        Returns:
            dict: Load result with game state

        Raises:
            FileNotFoundError: If save file doesn't exist
        """
        self.game_state = load_game(filename)
        return {
            "success": True,
            "message": f"Game loaded from {filename}",
            "state": self.get_state()
        }

    @staticmethod
    def list_saves():
        """
        List all available save files.

        Returns:
            dict: List of saves
        """
        saves = list_saves()
        return {
            "success": True,
            "saves": saves
        }

    def enter_dungeon(self):
        """
        Enter the dungeon at current location.

        Returns:
            dict: Dungeon entry result

        Raises:
            ValueError: If no dungeon available
        """
        if not self.game_state.active_quest:
            raise ValueError("No active quest")

        quest = self.game_state.active_quest
        if not quest.dungeon:
            raise ValueError("No dungeon at this location")

        if quest.dungeon.completed:
            raise ValueError("Dungeon already completed")

        # Allow re-entry if not completed - just mark as entered if first time
        if not quest.dungeon.entered:
            quest.dungeon.enter()

        return {
            "success": True,
            "dungeon": quest.dungeon.to_dict(),
            "message": f"Entered {quest.dungeon.name}"
        }

    def get_current_room(self):
        """
        Get current dungeon room information and trigger combat if monsters present.

        Returns:
            dict: Room information with contents and combat status

        Raises:
            ValueError: If not in a dungeon or no character
        """
        if not self.game_state.active_quest:
            raise ValueError("No active quest")

        quest = self.game_state.active_quest
        if not quest.dungeon or not quest.dungeon.entered:
            raise ValueError("Not in a dungeon")

        if not self.game_state.player:
            raise ValueError("No character - create a character first")

        dungeon = quest.dungeon

        # Get the actual room from the dungeon grid (if using grid system)
        # Otherwise fall back to simple room generation
        if dungeon.grid:
            current_room = dungeon.grid.get_current_room()
            if current_room:
                # AUTO-COMBAT TRIGGER: Check if there are alive monsters and no active combat
                combat_started = False
                if current_room.monsters:
                    alive_monsters = [m for m in current_room.monsters if hasattr(m, 'is_alive') and m.is_alive]

                    if alive_monsters and not self.game_state.active_combat:
                        # Start combat automatically
                        from combat import CombatEncounter
                        self.game_state.active_combat = CombatEncounter(
                            self.game_state.player,
                            alive_monsters
                        )
                        combat_started = True

                # Return room with combat info (even if no monsters)
                return {
                    "success": True,
                    "dungeon": dungeon.to_dict(),
                    "room_number": dungeon.current_room + 1,
                    "total_rooms": dungeon.total_rooms,
                    "room": current_room.to_dict(),
                    "combat_active": self.game_state.active_combat is not None,
                    "combat_started": combat_started,
                    "combat": self.game_state.active_combat.get_combat_status()
                    if self.game_state.active_combat else None
                }

        # Fallback: Generate simple room contents (for backward compatibility)
        room_type = roll_on_table(dungeon_tables.ROOM)
        room_contents = {"type": room_type}

        if room_type == "Spoor":
            spoor = roll_on_table(dungeon_tables.SPOOR)
            room_contents["spoor"] = spoor

        elif room_type == "Discovery":
            discovery_type = roll_on_table(dungeon_tables.DISCOVERY)
            room_contents["discovery_type"] = discovery_type

            if discovery_type == "Special Room":
                special_roll = roll_d6()
                if special_roll <= 3:
                    special_room = roll_on_table(dungeon_tables.SPECIAL_ROOM_1)
                else:
                    special_room = roll_on_table(dungeon_tables.SPECIAL_ROOM_2)
                room_contents["discovery_detail"] = special_room
            elif discovery_type == "Feature":
                room_contents["discovery_detail"] = roll_on_table(dungeon_tables.FEATURE)
            elif discovery_type == "Item":
                room_contents["discovery_detail"] = roll_on_table(dungeon_tables.ITEM)
            elif discovery_type == "Treasure A":
                treasure_string = roll_on_table(dungeon_tables.TREASURE_A)
                room_contents["discovery_detail"] = treasure_string
            elif discovery_type == "Treasure B":
                # Generate actual Item object from Treasure B
                treasure_string = roll_on_table(dungeon_tables.TREASURE_B)
                treasure_item = parse_treasure_to_item(treasure_string, tier=1)

                # Add to player inventory (add the Item object, not just the name)
                if self.game_state.player:
                    self.game_state.player.add_item(treasure_item)
                    # Also add gold value if it's coins/gems
                    if "Coins" in treasure_item.name or "Gem" in treasure_item.name:
                        self.game_state.player.gold += treasure_item.value

                room_contents["discovery_detail"] = f"Found: {treasure_item.name}"
                room_contents["treasure_item"] = treasure_item.to_dict()

            # Check for danger also (2-in-6 chance)
            danger_roll = roll_d6()
            if danger_roll <= 2:
                room_contents["also_danger"] = True
                danger_type = roll_on_table(dungeon_tables.DANGER)
                room_contents["danger_type"] = danger_type
                room_contents["danger_detail"] = self._get_danger_detail(danger_type)

        elif room_type == "Danger":
            danger_type = roll_on_table(dungeon_tables.DANGER)
            room_contents["danger_type"] = danger_type
            room_contents["danger_detail"] = self._get_danger_detail(danger_type)

        # Store room in explored rooms
        room_data = {
            "room_number": dungeon.current_room + 1,
            "contents": room_contents
        }
        dungeon.explored_rooms.append(room_data)

        # Check if we need to trigger combat for Monster dangers
        combat_started = False
        if room_type == "Danger" or room_contents.get("also_danger"):
            danger_type = room_contents.get("danger_type")
            if danger_type and "Monster" in danger_type and ("(T1)" in danger_type or "(T2)" in danger_type):
                # Create monsters and trigger combat
                from generators.monster import Monster, roll_number_appearing
                from generators.dungeon_generator import select_denizen_table

                tier = 1 if "(T1)" in danger_type else 2
                denizen_table = select_denizen_table(tier)
                roll_2d6 = roll_d6() + roll_d6()
                monster_data = denizen_table.get(roll_2d6, denizen_table[7])

                num_appearing = roll_number_appearing(tier, solo_pc=True)
                monsters = []
                for i in range(num_appearing):
                    monster = Monster.from_table_entry(monster_data)
                    if num_appearing > 1:
                        monster.name = f"{monster.name} #{i + 1}"
                    monsters.append(monster)

                # Start combat if not already in combat
                if monsters and not self.game_state.active_combat:
                    from combat import CombatEncounter
                    self.game_state.active_combat = CombatEncounter(
                        self.game_state.player,
                        monsters
                    )
                    combat_started = True

        return {
            "success": True,
            "dungeon": dungeon.to_dict(),
            "room_number": dungeon.current_room + 1,
            "total_rooms": dungeon.total_rooms,
            "contents": room_contents,
            "combat_active": self.game_state.active_combat is not None,
            "combat_started": combat_started,
            "combat": self.game_state.active_combat.get_combat_status() if self.game_state.active_combat else None
        }

    @staticmethod
    def _get_danger_detail(danger_type):
        """Get danger details based on type"""
        from tables import dungeon_tables
        from generators.dungeon_generator import select_denizen_table

        if danger_type == "Hazard":
            return roll_on_table(dungeon_tables.HAZARD)
        elif danger_type == "Trap":
            return roll_on_table(dungeon_tables.TRAP)
        elif danger_type == "Encounter":
            # Roll 2d6 for encounter
            return "Encounter (roll 2d6 on encounter table)"
        elif "Monster" in danger_type and ("(T1)" in danger_type or "(T2)" in danger_type):
            # Handle Monster (T1) and Monster (T2) with DENIZEN tables
            tier = 1 if "(T1)" in danger_type else 2

            # Select DENIZEN table based on tier and d6 roll
            denizen_table = select_denizen_table(tier)

            # Roll 2d6 on the selected table to get monster
            roll_2d6 = roll_d6() + roll_d6()
            monster_data = denizen_table.get(roll_2d6)

            # Fallback if roll not in table
            if not monster_data:
                monster_data = denizen_table[7]

            # Return monster name and stats
            return (f"{monster_data['name']} (HD: {monster_data['hd']}, AC: {monster_data['ac']},"
                    f" Attack: {monster_data['attack']})")

        return danger_type

    def advance_dungeon_room(self):
        """
        Advance to next room in dungeon by automatically choosing an available exit.

        Returns:
            dict: Result of advancing

        Raises:
            ValueError: If not in dungeon or dungeon complete
        """
        if not self.game_state.active_quest:
            raise ValueError("No active quest")

        quest = self.game_state.active_quest
        if not quest.dungeon or not quest.dungeon.entered:
            raise ValueError("Not in a dungeon")

        dungeon = quest.dungeon

        if dungeon.current_room >= dungeon.total_rooms:
            return {
                "success": False,
                "message": "Already at the last room",
                "can_complete": True
            }

        # Use grid system: automatically pick an available exit and move
        if dungeon.grid:
            available_exits = dungeon.get_available_exits()
            if available_exits:
                # Prefer directions that lead to unexplored rooms
                current_room = dungeon.grid.get_current_room()

                # Build list of exits that lead to new (un-generated) rooms
                unexplored_exits = []
                for exit_dir in available_exits:
                    new_x, new_y = dungeon.grid.get_adjacent_pos(current_room.x, current_room.y, exit_dir)
                    if (new_x, new_y) not in dungeon.grid.rooms:
                        unexplored_exits.append(exit_dir)

                # Prefer unexplored exits, otherwise pick randomly from all exits
                import random
                if unexplored_exits:
                    direction = random.choice(unexplored_exits)
                else:
                    direction = random.choice(available_exits)

                new_room = dungeon.move_in_direction(direction)

                if new_room:
                    # AUTO-COMBAT TRIGGER: Check if there are alive monsters and no active combat
                    combat_started = False
                    if new_room.monsters:
                        alive_monsters = [m for m in new_room.monsters if hasattr(m, 'is_alive') and m.is_alive]

                        if alive_monsters and not self.game_state.active_combat:
                            # Start combat automatically
                            from combat import CombatEncounter
                            self.game_state.active_combat = CombatEncounter(
                                self.game_state.player,
                                alive_monsters
                            )
                            combat_started = True

                    # Process traps and hazards in the room
                    trap_saves = []
                    hazard_saves = []

                    # Check for traps
                    if new_room.contents.get("danger") == "Trap" and new_room.contents.get("trap"):
                        trap_name = new_room.contents.get("trap")
                        if self.game_state.player:
                            trap_result = self._process_trap_save(trap_name, self.game_state.player)
                            trap_saves.append(trap_result)

                    # Check for hazards
                    if new_room.contents.get("danger") == "Hazard" and new_room.contents.get("hazard"):
                        hazard_name = new_room.contents.get("hazard")
                        if self.game_state.player:
                            hazard_result = self._process_hazard_save(hazard_name, self.game_state.player)
                            hazard_saves.append(hazard_result)

                    # Auto-collect treasure if inventory has space
                    treasure_collected = []
                    treasure_overflow = None

                    if new_room.treasure and self.game_state.player:
                        # Process each treasure item
                        remaining_treasure = []
                        for treasure_dict in new_room.treasure:
                            # Convert dict back to Item object
                            from generators.item import Item
                            treasure_item = Item.from_dict(treasure_dict)

                            # Check if player has inventory space
                            available_slots = self.game_state.player.get_available_inventory_slots()
                            item_slot_size = treasure_item.get_slot_size()

                            if available_slots >= item_slot_size:
                                # Auto-collect treasure
                                self.game_state.player.add_to_inventory(treasure_item)
                                treasure_collected.append(treasure_item.to_dict())
                            else:
                                # Inventory full - set overflow flag for first overflow item only
                                if not treasure_overflow:
                                    treasure_overflow = {
                                        "item": treasure_item.to_dict(),
                                        "requires_slots": item_slot_size,
                                        "available_slots": available_slots
                                    }
                                # Keep this treasure in room for later
                                remaining_treasure.append(treasure_dict)

                        # Update room treasure to only uncollected items
                        new_room.treasure = remaining_treasure

                    # Success - return the new room data with combat info and save results
                    response = {
                        "success": True,
                        "dungeon": dungeon.to_dict(),
                        "direction_moved": direction,
                        "room": new_room.to_dict(),
                        "combat_started": combat_started,
                        "combat": self.game_state.active_combat.get_combat_status() if self.game_state.active_combat
                        else None,
                        "trap_saves": trap_saves,
                        "hazard_saves": hazard_saves,
                        "treasure_collected": treasure_collected
                    }

                    # Add overflow info if present
                    if treasure_overflow:
                        response["treasure_overflow"] = treasure_overflow

                    return response

        # Fallback: just advance the counter (old system)
        advanced = dungeon.advance_room()

        return {
            "success": advanced,
            "dungeon": dungeon.to_dict(),
            "message": f"Moved to room {dungeon.current_room + 1}"
        }

    def complete_dungeon(self):
        """
        Complete the current dungeon and quest.

        Returns:
            dict: Completion result

        Raises:
            ValueError: If not in dungeon or not at end
        """
        if not self.game_state.active_quest:
            raise ValueError("No active quest")

        quest = self.game_state.active_quest
        if not quest.dungeon or not quest.dungeon.entered:
            raise ValueError("Not in a dungeon")

        dungeon = quest.dungeon

        if dungeon.current_room + 1 < dungeon.total_rooms:
            raise ValueError(
                f"Must explore all rooms first ({dungeon.current_room + 1}/{dungeon.total_rooms} explored)")

        # Mark dungeon as completed
        dungeon.complete()

        # Complete the quest
        quest_index = self.game_state.active_quest_index
        if quest_index is not None:
            # Use existing quest completion logic
            return self.complete_quest(quest_index)

        return {
            "success": False,
            "message": "Could not complete quest"
        }

    def collect_treasure_with_replacement(self, item_to_drop_name=None):
        """
        Collect treasure from current dungeon room by replacing an inventory item.

        Args:
            item_to_drop_name: Name of item to drop (None to decline treasure)

        Returns:
            dict: Collection result

        Raises:
            ValueError: If not in dungeon or no treasure to collect
        """
        if not self.game_state.active_quest:
            raise ValueError("No active quest")

        quest = self.game_state.active_quest
        if not quest.dungeon or not quest.dungeon.entered:
            raise ValueError("Not in a dungeon")

        if not self.game_state.player:
            raise ValueError("No player character")

        # Get current room
        current_room = quest.dungeon.grid.get_current_room()
        if not current_room or not current_room.treasure:
            raise ValueError("No treasure in current room")

        # Get the first treasure item
        from generators.item import Item
        treasure_dict = current_room.treasure[0]
        treasure_item = Item.from_dict(treasure_dict)

        # If declining treasure
        if item_to_drop_name is None:
            # Remove treasure from room (declined)
            current_room.treasure.pop(0)
            return {
                "success": True,
                "declined": True,
                "message": f"Declined {treasure_item.name}"
            }

        # Find and remove the item to drop
        item_dropped = self.game_state.player.remove_from_inventory(item_to_drop_name)
        if not item_dropped:
            raise ValueError(f"Item '{item_to_drop_name}' not found in inventory")

        # Add new treasure to inventory
        self.game_state.player.add_to_inventory(treasure_item)

        # Remove treasure from room
        current_room.treasure.pop(0)

        return {
            "success": True,
            "collected": treasure_item.to_dict(),
            "dropped": item_dropped.to_dict() if hasattr(item_dropped, 'to_dict') else item_dropped,
            "message": f"Collected {treasure_item.name}, dropped {item_to_drop_name}"
        }

    # Character Management Methods

    def create_character(self, name, race='Human', character_type='Adventurer',
                         hp=10, ac=10, attack_bonus=0, weapon=None, armor=None):
        """
        Create a custom player character.

        Args:
            name: Character name
            race: Character race
            character_type: Character type/class
            hp: Hit points
            ac: Armor class
            attack_bonus: Attack bonus
            weapon: Starting weapon
            armor: Starting armor

        Returns:
            dict: Character creation result
        """
        from generators import create_character

        player = create_character(name, race, character_type, hp, ac, attack_bonus, weapon, armor)
        self.game_state.player = player

        return {
            "success": True,
            "message": f"Character {name} created!",
            "character": player.to_dict()
        }

    def generate_random_character(self, name=None):
        """
        Generate a random character.

        Args:
            name: Optional character name

        Returns:
            dict: Generated character
        """
        from generators import generate_random_character

        player = generate_random_character(name)
        self.game_state.player = player

        return {
            "success": True,
            "message": f"Random character {player.name} generated!",
            "character": player.to_dict()
        }

    def save_character(self, filename=None):
        """
        Save current character to file.

        Args:
            filename: Optional filename

        Returns:
            dict: Save result

        Raises:
            ValueError: If no character to save
        """
        if not self.game_state.player:
            raise ValueError("No character to save")

        from generators import save_character

        filepath = save_character(self.game_state.player, filename)

        return {
            "success": True,
            "filepath": filepath,
            "message": f"Character saved to {filepath}"
        }

    def load_character(self, filename):
        """
        Load a character from file.

        Args:
            filename: Filename to load

        Returns:
            dict: Load result

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        from generators import load_character

        player = load_character(filename)
        self.game_state.player = player

        return {
            "success": True,
            "message": f"Character {player.name} loaded",
            "character": player.to_dict()
        }

    @staticmethod
    def list_characters():
        """
        List all saved characters.

        Returns:
            dict: List of characters
        """
        from generators import list_saved_characters

        characters = list_saved_characters()

        return {
            "success": True,
            "characters": characters
        }

    # Healing Methods

    def heal_at_settlement(self):
        """
        Heal the player at a settlement for currency.
        Cost: 5 gold per 10 HP healed (rounded up)
        PDF Rule: 10 silver pieces = 1 gold piece

        Returns:
            dict: Healing result with success status

        Raises:
            ValueError: If not at settlement, already at full HP, or not enough currency
        """
        if not self.game_state.player:
            raise ValueError("No character - create a character first")

        player = self.game_state.player

        # Check if at settlement
        current_hex = self.game_state.hex_grid.get_current_hex()

        if not current_hex or not current_hex.is_settlement:
            raise ValueError("Must be at a settlement to heal")

        # Check if already at full HP
        if player.hp_current >= player.hp_max:
            raise ValueError("Already at full health")

        # Calculate missing HP and currency cost
        missing_hp = player.hp_max - player.hp_current
        gold_cost = ((missing_hp - 1) // 10 + 1) * 5  # 5 gold per 10 HP, rounded up
        silver_cost = 0  # Cost in gold only for simplicity

        # Check if player has enough currency (using new currency system)
        total_available_in_silver = player.get_total_currency_in_silver()
        total_needed_in_silver = silver_cost + (gold_cost * 10)

        if total_available_in_silver < total_needed_in_silver:
            current_display = f"{player.gold}gp {player.silver}sp"
            cost_display = f"{gold_cost}gp" if silver_cost == 0 else f"{gold_cost}gp {silver_cost}sp"
            raise ValueError(f"Not enough currency. Healing costs {cost_display}, but you only have {current_display}")

        # Deduct currency and heal using new currency system
        if not player.remove_currency(silver=silver_cost, gold=gold_cost):
            raise ValueError("Failed to deduct healing cost")

        hp_healed = missing_hp
        player.hp_current = player.hp_max

        return {
            "success": True,
            "hp_healed": hp_healed,
            "gold_cost": gold_cost,
            "silver_cost": silver_cost,
            "current_hp": player.hp_current,
            "current_gold": player.gold,
            "current_silver": player.silver
        }

    # Combat Methods

    def get_combat_status(self):
        """
        Get current combat status.

        Returns:
            dict: Combat status

        Raises:
            ValueError: If not in combat
        """
        if not self.game_state.active_combat:
            raise ValueError("Not in combat")

        return {
            "success": True,
            "combat": self.game_state.active_combat.get_combat_status()
        }

    def combat_attack(self, target_index=0):
        """
        Player attacks in combat.

        Args:
            target_index: Index of monster to attack

        Returns:
            dict: Attack result

        Raises:
            ValueError: If not in combat or not player's turn
        """
        if not self.game_state.active_combat:
            # Return graceful response if combat already ended (race condition)
            return {
                "success": False,
                "error": "Combat has already ended",
                "combat_ended": True
            }

        combat = self.game_state.active_combat
        result = combat.player_attack(target_index)

        # If combat ended, transfer loot and clear combat
        if combat.is_combat_over():
            from combat.combat_system import CombatResult

            # Transfer loot to player inventory on victory
            if combat.combat_result == CombatResult.VICTORY:
                if combat.loot:
                    from generators.item import Item
                    import re

                    for item in combat.loot:
                        # Check if it's a currency string (gold and/or silver)
                        if isinstance(item, str) and ("gold" in item.lower() or "silver" in item.lower()):
                            # Parse gold and silver amounts
                            # Format can be: "5 gold", "3 silver", or "2 gold, 5 silver"
                            gold_match = re.search(r'(\d+)\s*gold', item, re.IGNORECASE)
                            silver_match = re.search(r'(\d+)\s*silver', item, re.IGNORECASE)

                            gold_amount = int(gold_match.group(1)) if gold_match else 0
                            silver_amount = int(silver_match.group(1)) if silver_match else 0

                            # Add currency using new currency system (auto-converts silver to gold)
                            self.game_state.player.add_currency(silver=silver_amount, gold=gold_amount)
                        elif isinstance(item, Item):
                            # Add Item object to inventory
                            self.game_state.player.add_item_to_inventory(item)
                        else:
                            # Legacy string item
                            self.game_state.player.add_to_inventory(item)

                # Increment encounters defeated counter
                self.game_state.player.encounters_defeated += 1
            elif combat.combat_result == CombatResult.DEFEAT:
                # PDF: Death save already handled in combat system
                # Player is either at 1 HP (save success) or dying (save failed)
                pass

            self.game_state.active_combat = None

        # Execute monster turn if combat continues
        if not combat.is_combat_over() and not combat.is_player_turn:
            combat.monster_turn()

        return {
            "success": True,
            "attack_result": result,
            "combat_status": combat.get_combat_status()
        }

    def combat_use_item(self, item_name):
        """
        Use an item in combat.

        Args:
            item_name: Name of item to use

        Returns:
            dict: Use item result

        Raises:
            ValueError: If not in combat
        """
        if not self.game_state.active_combat:
            # Return graceful response if combat already ended (race condition)
            return {
                "success": False,
                "error": "Combat has already ended",
                "combat_ended": True
            }

        combat = self.game_state.active_combat
        result = combat.player_use_item(item_name)

        # If combat ended, transfer loot and clear it
        if combat.is_combat_over():
            from combat.combat_system import CombatResult

            # Transfer loot to player inventory on victory
            if combat.combat_result == CombatResult.VICTORY and combat.loot:
                from generators.item import Item
                import re

                for item in combat.loot:
                    # Check if it's a currency string (gold and/or silver)
                    if isinstance(item, str) and ("gold" in item.lower() or "silver" in item.lower()):
                        # Parse gold and silver amounts
                        # Format can be: "5 gold", "3 silver", or "2 gold, 5 silver"
                        gold_match = re.search(r'(\d+)\s*gold', item, re.IGNORECASE)
                        silver_match = re.search(r'(\d+)\s*silver', item, re.IGNORECASE)

                        gold_amount = int(gold_match.group(1)) if gold_match else 0
                        silver_amount = int(silver_match.group(1)) if silver_match else 0

                        # Add currency using new currency system (auto-converts silver to gold)
                        self.game_state.player.add_currency(silver=silver_amount, gold=gold_amount)
                    elif isinstance(item, Item):
                        # Add Item object to inventory
                        self.game_state.player.add_item_to_inventory(item)
                    else:
                        # Legacy string item
                        self.game_state.player.add_to_inventory(item)
            elif combat.combat_result == CombatResult.DEFEAT:
                # PDF: Death save already handled in combat system
                # Player is either at 1 HP (save success) or dying (save failed)
                pass

            self.game_state.active_combat = None

        # Execute monster turn if combat continues
        if not combat.is_combat_over() and not combat.is_player_turn:
            combat.monster_turn()

        return {
            "success": True,
            "use_result": result,
            "combat_status": combat.get_combat_status()
        }

    def combat_flee(self):
        """
        Attempt to flee from combat.

        Returns:
            dict: Flee attempt result

        Raises:
            ValueError: If not in combat
        """
        if not self.game_state.active_combat:
            # Return graceful response if combat already ended (race condition)
            return {
                "success": False,
                "error": "Combat has already ended",
                "combat_ended": True
            }

        combat = self.game_state.active_combat
        result = combat.player_flee()

        # Check if combat was already over (race condition)
        if result.get("combat_ended"):
            self.game_state.active_combat = None
            return {
                "success": False,
                "error": result.get("message", "Combat has already ended"),
                "combat_ended": True
            }

        # If fled successfully or combat ended, clear it
        if result.get("fled") or combat.is_combat_over():
            from combat.combat_system import CombatResult

            # PDF: Death save already handled in combat system
            # Player is either at 1 HP (save success) or dying (save failed)
            if combat.combat_result == CombatResult.DEFEAT:
                pass

            self.game_state.active_combat = None

        # Execute monster turn if failed to flee
        if not result.get("fled", False) and not combat.is_combat_over():
            combat.monster_turn()

        return {
            "success": True,
            "flee_result": result,
            "combat_status": combat.get_combat_status() if not combat.is_combat_over() else None
        }

    def use_consumable(self, item_name: str):
        """
        Use a consumable item from inventory (outside of combat).

        Args:
            item_name: Name of the consumable to use

        Returns:
            dict: Result of using the consumable

        Raises:
            ValueError: If item not found, not consumable, or cannot be used
        """
        from generators.item import Item, ItemType

        # Find the item in inventory
        item = self.game_state.player.find_item_by_name(item_name)
        if not item:
            raise ValueError(f"Item '{item_name}' not found in inventory")

        # Apply effects based on item type
        effects_applied = []

        # Handle Item objects with ItemType.CONSUMABLE
        if isinstance(item, Item) and item.item_type == ItemType.CONSUMABLE:
            if item.effect_type == "heal":
                if self.game_state.player.hp_current >= self.game_state.player.hp_max:
                    raise ValueError("Already at full health")

                heal_amount = min(item.healing_amount,
                                  self.game_state.player.hp_max - self.game_state.player.hp_current)
                self.game_state.player.hp_current += heal_amount
                effects_applied.append(f"Healed {heal_amount} HP")

            elif item.effect_type == "cure_poison":
                # For now, just provide feedback - poison system not yet implemented
                effects_applied.append("Cured poison (if any)")

            elif item.effect_type in ["buff_attack", "buff_defense"]:
                # Temporary buffs - would need a buff system to track duration
                # For now, just provide feedback
                effects_applied.append(
                    f"Applied {item.effect_type.replace('_', ' ')} buff for {item.effect_duration} turns")

            else:
                raise ValueError(f"Unknown consumable effect: {item.effect_type}")

            # Remove Item object from inventory
            self.game_state.player.remove_item_from_inventory(item)

        # Handle legacy string-based healing items
        elif isinstance(item, str):
            item_lower = item.lower()

            # Check if it's a healing item (healing herbs, healing potion, etc.)
            if "healing" in item_lower or "herb" in item_lower or "potion" in item_lower:
                if self.game_state.player.hp_current >= self.game_state.player.hp_max:
                    raise ValueError("Already at full health")

                # Determine healing amount based on item name
                if "minor" in item_lower or "herb" in item_lower:
                    heal_amount = 3
                elif "greater" in item_lower or "major" in item_lower:
                    heal_amount = 6
                else:
                    heal_amount = 4  # Default healing

                # Cap healing at max HP
                actual_heal = min(heal_amount, self.game_state.player.hp_max - self.game_state.player.hp_current)
                self.game_state.player.hp_current += actual_heal
                effects_applied.append(f"Healed {actual_heal} HP")

                # Remove string item from inventory
                self.game_state.player.remove_from_inventory(item)

            elif "antidote" in item_lower:
                # Cure poison
                if self.game_state.player.remove_status_effect("poisoned"):
                    effects_applied.append("Cured poison")
                else:
                    effects_applied.append("No poison to cure")

                self.game_state.player.remove_from_inventory(item)

            else:
                raise ValueError(f"Item '{item_name}' is not a usable consumable")

        else:
            raise ValueError(f"Item '{item_name}' is not a consumable")

        return {
            "success": True,
            "item_used": item_name,
            "effects": effects_applied,
            "player_hp": self.game_state.player.hp_current,
            "player_hp_max": self.game_state.player.hp_max
        }

    def consume_day_ration(self):
        """
        Consume a ration at day's end to heal half HP (rounded up).

        Returns:
            dict: Result of consuming ration

        Raises:
            ValueError: If no rations available or already at full health
        """
        import math

        if not self.game_state.player:
            raise ValueError("No player character")

        # Find ration in inventory
        ration = self.game_state.player.find_item_by_name("Ration")
        if not ration:
            raise ValueError("No rations available")

        # Check if already at full health
        if self.game_state.player.hp_current >= self.game_state.player.hp_max:
            raise ValueError("Already at full health")

        # Calculate heal amount (half HP, rounded up)
        max_hp = self.game_state.player.hp_max
        heal_amount = math.ceil(max_hp / 2)

        # Apply healing (can't exceed max HP)
        actual_heal = min(heal_amount, max_hp - self.game_state.player.hp_current)
        self.game_state.player.hp_current += actual_heal

        # Remove ration from inventory
        self.game_state.player.remove_from_inventory("Ration")

        return {
            "success": True,
            "item_used": "Ration",
            "heal_amount": actual_heal,
            "player_hp": self.game_state.player.hp_current,
            "player_hp_max": self.game_state.player.hp_max
        }
