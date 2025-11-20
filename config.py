"""
Configuration module for RPG Hex Grid Game
Loads configuration from environment variables with sensible defaults
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).parent.absolute()


class Config:
    """Application configuration"""

    # Server Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', '5000'))

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

    @property
    def cors_origins_list(self):
        """Parse CORS_ORIGINS into a list"""
        if self.CORS_ORIGINS == '*':
            return '*'
        return [origin.strip() for origin in self.CORS_ORIGINS.split(',')]

    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/rpg_game.log')
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', '10485760'))  # 10MB default
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', '5'))

    # Game Data Paths
    SAVES_DIR = os.getenv('SAVES_DIR', 'saves')
    CHARACTERS_DIR = os.getenv('CHARACTERS_DIR', 'saved_characters')

    # Application Info
    APP_NAME = os.getenv('APP_NAME', 'RPG Hex Grid Game')

    @classmethod
    def get_abs_path(cls, relative_path):
        """Convert relative path to absolute path from project root"""
        return BASE_DIR / relative_path

    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist"""
        # Create logs directory
        log_dir = cls.get_abs_path(Path(cls.LOG_FILE).parent)
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create saves directory
        saves_dir = cls.get_abs_path(cls.SAVES_DIR)
        saves_dir.mkdir(parents=True, exist_ok=True)

        # Create characters directory
        chars_dir = cls.get_abs_path(cls.CHARACTERS_DIR)
        chars_dir.mkdir(parents=True, exist_ok=True)

    def __repr__(self):
        """String representation of config (masks sensitive data)"""
        return (
            f"Config(ENV={self.FLASK_ENV}, "
            f"DEBUG={self.FLASK_DEBUG}, "
            f"HOST={self.HOST}, "
            f"PORT={self.PORT}, "
            f"LOG_LEVEL={self.LOG_LEVEL})"
        )


# Global config instance
config = Config()

# Ensure directories exist on import
config.ensure_directories()
