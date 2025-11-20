# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-11-19

### Added - Infrastructure Improvements
- **Environment Configuration**
  - `.env` file support for configuration management
  - `config.py` module for centralized configuration
  - `.env.example` template file
  - Configurable server host, port, debug mode, CORS origins
  - Separate configuration for development/staging/production

- **Logging Framework**
  - Structured logging with Python's `logging` module
  - `logging_config.py` for centralized logging setup
  - Rotating file handler (10MB default, 5 backups)
  - Console and file output with configurable log levels
  - Replaced debug `print()` statements with proper logging
  - Log file: `logs/rpg_game.log` (configurable)

- **Docker Containerization**
  - `Dockerfile` for containerized deployment
  - `docker-compose.yml` for easy orchestration
  - `.dockerignore` for optimized builds
  - Health check for container monitoring
  - Volume mounts for persistent saves, characters, and logs
  - Environment variable configuration in containers

- **CI/CD Pipeline**
  - GitHub Actions workflow (`.github/workflows/ci.yml`)
  - Automated testing on Python 3.10 and 3.11
  - Code quality checks (Black, Flake8)
  - Docker image build validation
  - Security scanning (Safety, Bandit)
  - Runs on push and pull requests to main/develop

- **Documentation**
  - `INFRASTRUCTURE.md` - Comprehensive infrastructure guide
  - Updated `README.md` with Docker installation instructions
  - Development workflow documentation
  - Production deployment guide
  - Troubleshooting section

### Changed
- **Dependencies**
  - Added `python-dotenv~=1.0.0` to requirements.txt
  - Updated `run_server.py` to use config module
  - Updated `api/game_server.py` to use config and logging

### Technical
- Configuration now loaded from environment variables with sensible defaults
- All logging centralized through `logging_config.py`
- Application fully containerized and ready for cloud deployment
- CI pipeline ensures code quality on every commit
- Infrastructure ready for production deployment

## [0.3.0] - 2025-11-16

### Added - Party System
- **Party-based Gameplay**: Support for up to 3 characters adventuring together
  - Create multiple characters (up to 3) who adventure as a party
  - All party members displayed in character panel with HP bars
  - Active character indicator (green dot) shows which character is currently acting
  - Party size displayed throughout UI (e.g., "Party: 3/3")

- **Shared Resources**
  - Party Inventory: 10-slot shared inventory for all party members
  - Party Currency: Shared gold and silver pool
  - Vendor transactions use party resources
  - Items purchased go to party inventory

- **Individual Progression**
  - Each character has separate HP, stats (STR/DEX/WIL/TOU), level, and XP
  - Each character has individual equipment slots (weapon, armor, shield, helmet)
  - All party members receive XP from combat victories
  - Each character levels up independently

- **Combat Updates**
  - Combat UI displays all party members with individual HP bars
  - All party members shown during combat encounters
  - Party members listed with color-coded HP bars (green/orange/red)
  - XP awarded to all party members simultaneously

- **UI Enhancements**
  - Character creation modal shows party roster (X/3)
  - Creation options hidden when party is full (3 characters)
  - Main character panel shows all party members in compact cards
  - "Shared Resources" section for party inventory and currency
  - Party member cards show name, level, race, class, HP with mini health bars

### Changed
- Character creation now adds to party instead of replacing player
- Character panel reorganized to show party members and shared resources
- Currency display changes to "Party Gold" when party size > 1
- Inventory display changes to "Party Inventory" when party size > 1
- Combat system uses party array while maintaining active character for actions
- Save file format updated to include party data (backwards compatible)

### Technical
- `GameState` updated with party array, active_character_index, shared inventory/currency
- Backwards compatibility: single-player saves auto-migrate to 1-character party
- API endpoint `/api/game/state` now returns party data
- Combat encounters support party parameter
- All party members receive XP in `_award_xp()` method
- Save file version bumped to 1.4

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
