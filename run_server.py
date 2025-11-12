#!/usr/bin/env python3
"""
Launch script for RPG Hex Grid Game Server
"""

import sys
import os
from api.game_server import run_server

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


if __name__ == '__main__':
    print("=" * 70)
    print("RPG HEX GRID GAME SERVER")
    print("=" * 70)
    print()
    print("Starting server...")
    print("Once the server is running, open your web browser to:")
    print("  http://127.0.0.1:5000")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 70)
    print()

    try:
        run_server(host='127.0.0.1', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        sys.exit(0)
