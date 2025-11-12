"""
Flask REST API Server for RPG Game
Provides endpoints for game state management
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from api.game_state import GameManager
from version import VERSION_INFO

# Initialize Flask app
app = Flask(__name__,
            static_folder='../static',
            static_url_path='')
CORS(app)  # Enable CORS for development

# Global game manager instance
game_manager = GameManager()


# Serve static files
@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve asset files (Terrenos hex tiles, etc.)"""
    import os
    assets_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
    return send_from_directory(assets_folder, filename)


# API Endpoints

@app.route('/api/version', methods=['GET'])
def get_version():
    """Get game version information"""
    return jsonify(VERSION_INFO)


@app.route('/api/game/new', methods=['POST'])
def new_game():
    """Start a new game"""
    try:
        state = game_manager.new_game()
        return jsonify({
            "success": True,
            "state": state
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/game/state', methods=['GET'])
def get_state():
    """Get current game state"""
    try:
        state = game_manager.get_state()
        return jsonify({
            "success": True,
            "state": state
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/game/save', methods=['POST'])
def save_game():
    """Save current game"""
    try:
        data = request.get_json() or {}
        filename = data.get('filename')
        result = game_manager.save(filename)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/game/load', methods=['POST'])
def load_game():
    """Load a saved game"""
    try:
        data = request.get_json()
        if not data or 'filename' not in data:
            return jsonify({
                "success": False,
                "error": "Filename required"
            }), 400

        result = game_manager.load(data['filename'])
        return jsonify(result)
    except FileNotFoundError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/game/saves', methods=['GET'])
def list_saves():
    """List all available save files"""
    try:
        result = game_manager.list_saves()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/quest/generate', methods=['POST'])
def generate_quest():
    """Generate a new quest"""
    try:
        quest = game_manager.generate_quest()
        return jsonify({
            "success": True,
            "quest": quest
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/quest/accept', methods=['POST'])
def accept_quest():
    """Accept a quest"""
    try:
        data = request.get_json()
        if not data or 'quest_index' not in data:
            return jsonify({
                "success": False,
                "error": "quest_index required"
            }), 400

        result = game_manager.accept_quest(data['quest_index'])
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/quest/complete', methods=['POST'])
def complete_quest():
    """Complete a quest at destination"""
    try:
        data = request.get_json()
        if not data or 'quest_index' not in data:
            return jsonify({
                "success": False,
                "error": "quest_index required"
            }), 400

        result = game_manager.complete_quest(data['quest_index'])
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/player/move', methods=['POST'])
def move_player():
    """Move player to a hex"""
    try:
        data = request.get_json()
        if not data or 'q' not in data or 'r' not in data:
            return jsonify({
                "success": False,
                "error": "Coordinates (q, r) required"
            }), 400

        result = game_manager.move_player(data['q'], data['r'])
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/hex/<int:q>/<int:r>', methods=['GET'])
def get_hex_info(q, r):
    """Get information about a specific hex"""
    try:
        hex_info = game_manager.get_hex_info(q, r)
        if hex_info is None:
            return jsonify({
                "success": False,
                "error": f"Hex ({q}, {r}) not found"
            }), 404

        return jsonify({
            "success": True,
            "hex": hex_info
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/player/consume_day_ration', methods=['POST'])
def consume_day_ration():
    """Consume a ration at day's end to heal half HP"""
    try:
        result = game_manager.consume_day_ration()
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/dungeon/enter', methods=['POST'])
def enter_dungeon():
    """Enter the dungeon at current location"""
    try:
        result = game_manager.enter_dungeon()
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/dungeon/room', methods=['GET'])
def get_current_room():
    """Get current dungeon room information"""
    try:
        result = game_manager.get_current_room()
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/dungeon/advance', methods=['POST'])
def advance_room():
    """Advance to next room in dungeon"""
    try:
        result = game_manager.advance_dungeon_room()
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/dungeon/complete', methods=['POST'])
def complete_dungeon():
    """Complete the current dungeon"""
    try:
        result = game_manager.complete_dungeon()
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/dungeon/treasure/collect', methods=['POST'])
def collect_dungeon_treasure():
    """Collect treasure from dungeon room with optional item replacement"""
    try:
        data = request.get_json() or {}
        item_to_drop = data.get('item_to_drop_name')
        result = game_manager.collect_treasure_with_replacement(item_to_drop)
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Character Management Endpoints

@app.route('/api/character/create', methods=['POST'])
def create_character():
    """Create a custom character"""
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({
                "success": False,
                "error": "Character name required"
            }), 400

        result = game_manager.create_character(
            name=data['name'],
            race=data.get('race', 'Human'),
            character_type=data.get('character_type', 'Adventurer'),
            hp=data.get('hp', 10),
            ac=data.get('ac', 10),
            attack_bonus=data.get('attack_bonus', 0),
            weapon=data.get('weapon'),
            armor=data.get('armor')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/character/random', methods=['POST'])
def generate_random_character():
    """Generate a random character"""
    try:
        data = request.get_json() or {}
        name = data.get('name')
        result = game_manager.generate_random_character(name)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/character/save', methods=['POST'])
def save_character():
    """Save current character to file"""
    try:
        data = request.get_json() or {}
        filename = data.get('filename')
        result = game_manager.save_character(filename)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/character/load', methods=['POST'])
def load_character():
    """Load a character from file"""
    try:
        data = request.get_json()
        if not data or 'filename' not in data:
            return jsonify({
                "success": False,
                "error": "Filename required"
            }), 400

        result = game_manager.load_character(data['filename'])
        return jsonify(result)
    except FileNotFoundError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/character/list', methods=['GET'])
def list_characters():
    """List all saved characters"""
    try:
        result = game_manager.list_characters()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Combat Endpoints

@app.route('/api/combat/status', methods=['GET'])
def get_combat_status():
    """Get current combat status"""
    try:
        result = game_manager.get_combat_status()
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/combat/attack', methods=['POST'])
def combat_attack():
    """Player attacks in combat"""
    try:
        data = request.get_json() or {}
        target_index = data.get('target_index', 0)
        result = game_manager.combat_attack(target_index)
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/combat/item', methods=['POST'])
def combat_use_item():
    """Use an item in combat"""
    try:
        data = request.get_json()
        if not data or 'item_name' not in data:
            return jsonify({
                "success": False,
                "error": "item_name required"
            }), 400

        result = game_manager.combat_use_item(data['item_name'])
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/combat/flee', methods=['POST'])
def combat_flee():
    """Attempt to flee from combat"""
    try:
        result = game_manager.combat_flee()
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/player/heal', methods=['POST'])
def heal_at_settlement():
    """Heal the player at a settlement for gold"""
    try:
        result = game_manager.heal_at_settlement()
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/player/use_item', methods=['POST'])
def use_consumable():
    """Use a consumable item from inventory"""
    try:
        data = request.get_json()
        if not data or 'item_name' not in data:
            return jsonify({
                "success": False,
                "error": "item_name required"
            }), 400

        result = game_manager.use_consumable(data['item_name'])
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Error handlers
@app.errorhandler(404)
def not_found():
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "Not found"
    }), 404


@app.errorhandler(500)
def internal_error():
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


def run_server(host='127.0.0.1', port=5000, debug=True):
    """
    Run the Flask server.

    Args:
        host (str): Host address
        port (int): Port number
        debug (bool): Debug mode
    """
    print(f"Starting RPG Game Server on https://{host}:{port}")
    print(f"Open your browser to https://{host}:{port} to play!")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server()
