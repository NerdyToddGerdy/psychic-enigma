# RPG Hex Grid Game

A web-based hexagonal grid exploration game with procedurally generated quests, terrain, and discoveries.

## Features

- **Character System**: Create characters with random attributes (STR, DEX, CON, INT, WIS, CHA), HP, and attack/shooting bonuses
- **Hex Grid System**: Axial coordinate-based hex grid with 6-directional movement
- **Quest Generation**: Procedurally generated quests with specific destinations
- **Dungeon Exploration**: Navigate procedurally generated dungeons with multiple rooms, treasures, and encounters
- **Combat System**: Turn-based combat with monsters, including attack rolls, damage, and flee options
- **Item & Equipment System**: Find and equip weapons, armor, and items with various modifiers
- **Currency System**: Silver and gold pieces (10 silver = 1 gold) for trading and services
- **Exploration**: Discover terrain, weather, dangers, and treasures as you explore
- **Settlement Services**: Heal at settlements for currency, consume day rations
- **Save/Load**: Persist your game state to JSON files
- **Web-Based UI**: Interactive SVG-rendered hex grid with real-time updates

## Gameplay

1. **Create Character**: Start by creating a random character with attributes, HP, and starting equipment
2. **Generate Quests**: Click "Generate Quest" to create new quests with dungeon destinations
3. **Accept Quests**: View available quests and click "Accept" to make one active
4. **Quest Destinations**: Accepting a quest reveals its destination hex (greyed out)
5. **Movement**: Click on revealed hexes to move to them
6. **Exploration**: Moving to a hex explores it, revealing:
   - Terrain type
   - Weather conditions
   - Water presence
   - Discoveries (natural features, ruins, settlements, etc.)
   - Dangers (hostiles, hazards, unnatural threats)
   - Combat encounters (automatic when encountering monsters)
7. **Enter Dungeons**: At quest destinations, enter dungeons to explore
8. **Dungeon Exploration**: Navigate through rooms, fight monsters, avoid traps, and collect treasure
9. **Combat**: During combat, attack monsters or flee to escape
10. **Equipment**: Collect and equip weapons and armor found in dungeons and loot
11. **Settlements**: Visit settlements to heal (costs currency based on missing HP)
12. **Complete Quests**: Clear dungeons and collect rewards to complete objectives

## Infrastructure

This project includes modern infrastructure components:

- ⚙️ **Environment Configuration** - Configurable via `.env` files
- 📝 **Logging Framework** - Structured logging with rotation
- 🐳 **Docker Support** - Full containerization with Docker Compose
- 🔄 **CI/CD Pipeline** - GitHub Actions for automated testing and builds

For detailed infrastructure documentation, see [INFRASTRUCTURE.md](INFRASTRUCTURE.md)

## Installation

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker
- Docker Compose

**Quick Start:**

```bash
# 1. Clone the repository
git clone <repository-url>
cd rpgGame

# 2. Copy environment file
cp .env.example .env

# 3. Start with Docker Compose
docker-compose up
```

Access the game at `http://localhost:5000`

**Docker Commands:**

```bash
# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Rebuild after changes
docker-compose up --build
```

### Option 2: Local Python Installation

**Prerequisites:**
- Python 3.10+
- pip

**Setup:**

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy environment file
cp .env.example .env

# 4. Run the server
python run_server.py
```

### Access the Game

Open your web browser to:
```
http://127.0.0.1:5000
```

## Project Structure

```
rpgGame/
├── api/                        # Flask REST API
│   ├── game_server.py         # Flask endpoints
│   └── game_state.py          # Game state manager
├── generators/                 # Procedural generation
│   ├── character.py           # Character creation and stats
│   ├── hex_grid.py            # Hex grid system
│   ├── quest_generator.py     # Quest generation
│   ├── dungeon_generator.py   # Dungeon generation
│   ├── item.py                # Item and equipment generation
│   └── monster.py             # Monster generation
├── combat/                     # Combat system
│   ├── combat_system.py       # Combat mechanics and encounters
│   └── encounter_parser.py    # Encounter parsing utilities
├── tables/                     # Random tables
│   ├── overland_tables.py     # Overland exploration tables
│   ├── dungeon_tables.py      # Dungeon generation tables
│   ├── table_roller.py        # Dice rolling utilities
│   └── table_utilities.py     # Table helper functions
├── static/                     # Web frontend
│   ├── index.html             # Main HTML
│   ├── css/
│   │   └── style.css          # Styling
│   └── js/
│       ├── hex_renderer.js    # SVG hex rendering
│       ├── game_client.js     # API client
│       ├── quest_manager.js   # Quest UI
│       ├── character_manager.js # Character UI
│       ├── combat_ui.js       # Combat UI
│       └── app.js             # Main application
├── tests/                      # Unit tests
├── saves/                      # Saved games (created automatically)
├── save_load.py               # Save/load utilities
├── run_server.py              # Launch script
└── README.md

## API Endpoints

### Game Management
- `POST /api/game/new` - Start new game
- `GET /api/game/state` - Get current game state
- `POST /api/game/save` - Save game
- `POST /api/game/load` - Load game
- `GET /api/game/saves` - List save files

### Character Management
- `POST /api/character/create` - Create custom character
- `POST /api/character/random` - Generate random character
- `GET /api/character/list` - List all characters
- `POST /api/character/select` - Select character for game
- `POST /api/player/consume_day_ration` - Consume a day ration
- `POST /api/player/heal_at_settlement` - Heal at settlement (costs currency)

### Quest Management
- `POST /api/quest/generate` - Generate new quest
- `POST /api/quest/accept` - Accept a quest

### Player Actions
- `POST /api/player/move` - Move player to hex
- `GET /api/hex/:q/:r` - Get hex information

### Dungeon Management
- `POST /api/dungeon/enter` - Enter dungeon at current location
- `GET /api/dungeon/room` - Get current dungeon room details
- `POST /api/dungeon/advance` - Advance to next dungeon room
- `POST /api/dungeon/complete` - Complete dungeon and quest
- `POST /api/dungeon/treasure/collect` - Collect treasure from room

### Combat System
- `POST /api/combat/attack` - Attack a monster in combat
- `POST /api/combat/flee` - Attempt to flee from combat
- `GET /api/combat/status` - Get current combat status

## Controls

### Header Buttons
- **New Game**: Start a fresh game (warning: unsaved progress will be lost)
- **Save Game**: Save current progress to a JSON file
- **Load Game**: Load a previously saved game
- **Generate Quest**: Create a new quest with random destination

### Hex Grid
- **Click on Hex**: Move to that hex (if revealed)
- **Mouse Drag**: Pan the view
- **Mouse Wheel**: Zoom in/out

### Quest Panel
- **Accept Button**: Make a quest active (reveals destination)
- **Quest Cards**: View quest details (action, target, location, opposition, etc.)

## Game Mechanics

### Character System
Based on the Single Sheet Game System:

**Attributes** (3d6 each):
- **STR** (Strength): Melee damage and carrying capacity
- **DEX** (Dexterity): Ranged attacks and AC
- **CON** (Constitution): HP and fortitude saves
- **INT** (Intelligence): Spellcasting and knowledge
- **WIS** (Wisdom): Perception and willpower saves
- **CHA** (Charisma**: Social interaction and leadership

**Combat Stats**:
- **HP**: Hit points = CON score
- **AC**: Armor Class = 10 + armor bonus
- **Attack Bonus (AB)**: +1 if STR ≥ 14 (used for melee weapons)
- **Shooting Bonus (SB)**: +1 if DEX ≥ 14 (used for ranged weapons like bows)

**Currency**:
- Silver pieces (sp) and gold pieces (gp)
- 10 silver = 1 gold
- Starting currency: 3d6 silver pieces

**Inventory**:
- 10 equipment slots total
- Weapons, armor, items, and day rations

### Combat System
Turn-based combat with the following actions:
- **Attack**: Roll 1d20 + attack bonus vs monster AC
  - Melee weapons use AB (Attack Bonus from STR)
  - Ranged weapons use SB (Shooting Bonus from DEX)
  - On hit: Roll weapon damage
- **Flee**: Attempt to escape combat (success rate varies)

Monster attacks follow the same system, rolling to hit player AC.

### Dungeon System
Procedurally generated dungeons with:
- **Rooms**: Multiple interconnected rooms with exits (north, south, east, west)
- **Contents**: Treasures, monsters, traps, hazards, or empty rooms
- **Progression**: Navigate room-by-room until reaching the final room
- **Treasures**: Automatically collected if inventory has space
- **Completion**: Complete all rooms to finish the dungeon and quest

### Hex States
- **Hidden**: Not yet discovered (not visible)
- **Revealed**: Quest destination (greyed out, limited info)
- **Explored**: Visited (full details visible)

### Exploration Die
When entering a new hex, the game rolls on the EXPLORE_DIE table:
- **Discovery**: Find something interesting (natural, unnatural, ruin, settlement, evidence)
- **Danger**: Encounter a threat (hostile, hazard, unnatural)
- **Spoor**: Signs of activity (tracks, campfires, etc.)
- **Nothing**: Safe passage

### Quest System
Each quest has:
- **Action**: What you must do (explore, rescue, destroy, locate, etc.)
- **Target**: What/who is involved (NPC, item, treasure, location, enemy)
- **Location**: Where it is (castle, cave, mountain, city, etc.)
- **Opposition**: Who holds it (bandits, cult, soldiers, spy, etc.)
- **Source**: Who gave the quest (wizard, noble, cleric, rumor, etc.)
- **Reward**: What you'll receive (gold, silver, item, NPC, etc.)
- **Direction & Distance**: Quest destination in hex grid (1-6 hexes in one of 6 directions)
- **Dungeon**: Each quest generates a procedural dungeon at the destination

## Terrain Types
- Grasslands
- Woods
- Hills
- Mountains
- Swamp
- Wasteland

## Weather Conditions
- Sunny
- Overcast
- Rain
- Fog
- Thunderstorm

## Development

### Development Setup

```bash
# Clone and setup
git clone <repository-url>
cd rpgGame

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests.test_hex_grid

# With Docker
docker-compose run rpg-game python -m unittest discover tests -v
```

### Code Quality

```bash
# Format code with black
black .

# Lint with flake8
flake8 .

# Type checking with mypy
mypy .
```

### CI/CD

The project uses GitHub Actions for continuous integration:

- **Tests**: Runs on Python 3.10 and 3.11
- **Linting**: Black formatting and Flake8 checks
- **Docker Build**: Validates Docker image builds
- **Security**: Dependency and code security scans

Pipeline runs automatically on push and pull requests to `main` and `develop` branches.

### Adding New Features

1. **Backend (Python)**:
   - Add game logic to `generators/` or `tables/`
   - Add API endpoints to `api/game_server.py`
   - Add state management to `api/game_state.py`
   - Use logging: `from logging_config import get_logger`

2. **Frontend (JavaScript)**:
   - Update UI in `static/index.html`
   - Add styles to `static/css/style.css`
   - Add logic to `static/js/` modules

3. **Testing**:
   - Add tests in `tests/` directory
   - Follow existing test patterns
   - Ensure CI pipeline passes

## Save Files

Save files are stored in the `saves/` directory as JSON files. They contain:
- Complete hex grid state (all discovered hexes)
- Player position
- Quest list and active quest
- Exploration results

## Credits

Based on the "Single Sheet Overland Game System" and "Single Sheet Dungeon" reference materials.

## License

This is a personal project for educational and entertainment purposes.
