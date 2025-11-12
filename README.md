# RPG Hex Grid Game

A web-based hexagonal grid exploration game with procedurally generated quests, terrain, and discoveries.

## Features

- **Hex Grid System**: Axial coordinate-based hex grid with 6-directional movement
- **Quest Generation**: Procedurally generated quests with specific destinations
- **Exploration**: Discover terrain, weather, dangers, and treasures as you explore
- **Save/Load**: Persist your game state to JSON files
- **Web-Based UI**: Interactive SVG-rendered hex grid with real-time updates

## Gameplay

1. **Starting the Game**: Begin at hex (0,0) - your starting location
2. **Generate Quests**: Click "Generate Quest" to create a new quest
3. **Accept Quests**: View available quests and click "Accept" to make one active
4. **Quest Destinations**: Accepting a quest reveals its destination hex (greyed out)
5. **Movement**: Click on revealed hexes to move to them
6. **Exploration**: Moving to a hex explores it, revealing:
   - Terrain type
   - Weather conditions
   - Water presence
   - Discoveries (natural features, ruins, settlements, etc.)
   - Dangers (hostiles, hazards, unnatural threats)
7. **Complete Quests**: Reach the quest destination to complete objectives

## Installation

### Requirements

- Python 3.8+
- Flask
- Flask-CORS

### Install Dependencies

```bash
pip install flask flask-cors
```

## Running the Game

### Start the Server

```bash
python3 run_server.py
```

Or directly:

```bash
python3 -m api.game_server
```

### Access the Game

Open your web browser to:
```
http://127.0.0.1:5000
```

## Project Structure

```
rpgGame/
├── api/                    # Flask REST API
│   ├── game_server.py     # Flask endpoints
│   └── game_state.py      # Game state manager
├── generators/             # Procedural generation
│   ├── hex_grid.py        # Hex grid system
│   └── quest_generator.py # Quest generation
├── tables/                 # Random tables
│   ├── overland_tables.py # Overland exploration tables
│   ├── dungeon_tables.py  # Dungeon generation tables
│   └── table_roller.py    # Dice rolling utilities
├── static/                 # Web frontend
│   ├── index.html         # Main HTML
│   ├── css/
│   │   └── style.css      # Styling
│   └── js/
│       ├── hex_renderer.js    # SVG hex rendering
│       ├── game_client.js     # API client
│       ├── quest_manager.js   # Quest UI
│       └── app.js             # Main application
├── tests/                  # Unit tests
├── saves/                  # Saved games (created automatically)
├── save_load.py           # Save/load utilities
├── run_server.py          # Launch script
└── README.md

## API Endpoints

### Game Management
- `POST /api/game/new` - Start new game
- `GET /api/game/state` - Get current game state
- `POST /api/game/save` - Save game
- `POST /api/game/load` - Load game
- `GET /api/game/saves` - List save files

### Quest Management
- `POST /api/quest/generate` - Generate new quest
- `POST /api/quest/accept` - Accept a quest

### Player Actions
- `POST /api/player/move` - Move player to hex
- `GET /api/hex/:q/:r` - Get hex information

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

### Running Tests

```bash
# Run all tests
python3 -m unittest discover tests

# Run specific test file
python3 -m unittest tests.test_hex_grid
```

### Adding New Features

1. **Backend (Python)**:
   - Add game logic to `generators/` or `tables/`
   - Add API endpoints to `api/game_server.py`
   - Add state management to `api/game_state.py`

2. **Frontend (JavaScript)**:
   - Update UI in `static/index.html`
   - Add styles to `static/css/style.css`
   - Add logic to `static/js/` modules

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
