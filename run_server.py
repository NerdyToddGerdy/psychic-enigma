#!/usr/bin/env python3
"""
Launch script for RPG Hex Grid Game Server
"""

import sys
import os
from api.game_server import run_server
from config import config
from logging_config import get_logger

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Get logger for this module
logger = get_logger(__name__)


if __name__ == '__main__':
    print("=" * 70)
    print(config.APP_NAME.upper())
    print("=" * 70)
    print()
    print(f"Environment: {config.FLASK_ENV}")
    print(f"Debug Mode: {config.FLASK_DEBUG}")
    print()
    print("Starting server...")
    print("Once the server is running, open your web browser to:")
    print(f"  http://{config.HOST}:{config.PORT}")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 70)
    print()

    logger.info(f"Starting {config.APP_NAME}")
    logger.info(f"Environment: {config.FLASK_ENV}, Debug: {config.FLASK_DEBUG}")

    try:
        run_server()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        logger.info("Server stopped by user")
        sys.exit(0)
