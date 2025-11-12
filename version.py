"""
Game Version Information
"""

# Semantic Versioning: MAJOR.MINOR.PATCH
# MAJOR: Incompatible API/save file changes
# MINOR: New features, backward compatible
# PATCH: Bug fixes, backward compatible

VERSION_MAJOR = 0
VERSION_MINOR = 2
VERSION_PATCH = 0

# Full version string
VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"

# Save file version (increment when save format changes)
SAVE_VERSION = "1.3"

# Build metadata (optional)
BUILD_DATE = "2025-11-12"

# Version info dictionary
VERSION_INFO = {
    "version": VERSION,
    "save_version": SAVE_VERSION,
    "build_date": BUILD_DATE,
    "game_name": "RPG Hex Grid Explorer"
}


def get_version_string():
    """Get full version string"""
    return f"v{VERSION}"


def get_full_version_string():
    """Get version with build date"""
    return f"v{VERSION} (Built: {BUILD_DATE})"


def is_save_compatible(save_version: str) -> bool:
    """
    Check if a save file version is compatible with current version.

    Args:
        save_version: Version string from save file

    Returns:
        True if save is compatible
    """
    # For now, accept all versions with same major number
    try:
        major, minor = save_version.split(".")[:2]
        current_major, current_minor = SAVE_VERSION.split(".")[:2]

        # Same major version = compatible
        return major == current_major
    except (ValueError, AttributeError):
        # Invalid version format, assume incompatible
        return False
