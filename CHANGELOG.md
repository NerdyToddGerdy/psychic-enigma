# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-11-12

### Added
- Versioning system with centralized version management
- `/api/version` endpoint to retrieve version information
- Version display in UI header (shows current game version)
- `VERSION_INFO.md` documentation for versioning system
- Comprehensive `CHANGELOG.md` to track all changes

### Fixed
- **Combat Persistence Bug**: Monsters no longer reappear after fleeing from dungeon combat
  - Issue: When fleeing combat in a dungeon, monsters remained in the room
  - Solution: Clear monsters from dungeon room after successful flee (api/game_state.py:1608-1614)

- **Death Save Multiple Attacks Bug**: Player now gets a turn after making death save
  - Issue: After making a successful death save (surviving with 1 HP), remaining monsters would continue attacking in the same turn, causing multiple death saves
  - Solution: Monster turn loop now breaks immediately after a player makes a death save, giving player a chance to flee or heal (combat/combat_system.py:361-377)

### Changed
- Save file version tracking now uses centralized `SAVE_VERSION` from `version.py`
- Updated header styling to accommodate version display

## [0.1.0] - Initial Release

### Added
- Core hex grid exploration gameplay with procedurally generated world
- Character creation system with random and custom options
- Character attributes based on Single Sheet Game System (STR, DEX, CON, INT, WIS, CHA)
- Quest generation system with dungeon exploration
- Turn-based combat system with attack, use item, and flee actions
- Death save system following PDF rules (WIL save at 0 HP)
  - Success: Stay at 1 HP and continue fighting
  - Failure: Dying state, perish in 60 turns if untreated
- Game over system when player dies
- Inventory management with equipment slots (weapon, armor, shield)
- Currency system (gold and silver pieces with auto-conversion)
- Save/load functionality with JSON persistence
- Day/night cycle (every 5 hex movements = 1 day)
- Ration system for healing between combats
- Settlement healing mechanic
- Dungeon exploration with procedural room generation
- Combat log with detailed attack/damage information
- Status effects system (paralyzed, poisoned, etc.)
- Monster variety with special abilities
- Loot system with treasure generation
- Quest completion rewards (XP, gold, items)
- Character progression tracking (encounters defeated, quests completed)
- Hex terrain variety (desert, forest, mountains, grasslands, hills, swamp)
- Visual hex grid with terrain-based tile graphics
- Modal-based UI for character, combat, quests, and dungeons
- Git repository initialization and GitHub integration

### Technical Details
- Flask REST API backend
- Vanilla JavaScript frontend
- SVG-based hex grid rendering
- Modal system for UI interactions
- Client-server state synchronization
- Comprehensive error handling
- Debug mode with detailed logging

---

## Version Format

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version (X.0.0): Incompatible API changes or breaking save file format changes
- **MINOR** version (0.X.0): New features added in a backward-compatible manner
- **PATCH** version (0.0.X): Backward-compatible bug fixes

### Save File Compatibility

Save files include a version number. The game checks compatibility:
- Same **major** version = compatible (e.g., 1.2 can load 1.3 saves)
- Different **major** version = incompatible (e.g., 1.x cannot load 2.x saves)

---

## Links

- [GitHub Repository](https://github.com/NerdyToddGerdy/psychic-enigma)
- [Version Documentation](VERSION_INFO.md)
- [Game Rules Implementation](SINGLE_SHEET_IMPLEMENTATION.md)
- [Main README](README.md)
