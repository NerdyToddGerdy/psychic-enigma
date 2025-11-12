# Version Information

## Current Version: v0.2.0

### Version History

#### v0.2.0 (2025-11-12)
- **Bug Fixes:**
  - Fixed combat persistence bug where fleeing from dungeon combat caused monsters to reappear
  - Fixed death save bug where multiple monster attacks occurred after successful death save

- **Features:**
  - Implemented versioning system with API endpoint
  - Version display in UI header
  - Save file version tracking

#### v0.1.0 (Initial Release)
- Core hex grid exploration gameplay
- Character creation and management
- Quest system with dungeon exploration
- Combat system with death saves (PDF rules)
- Save/load functionality
- Currency system
- Inventory management
- Day/night cycle with rations

---

## Versioning System

The game uses **Semantic Versioning** (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible API changes or save file format changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Components

1. **version.py**: Central version configuration file
   - Game version (`VERSION`)
   - Save file version (`SAVE_VERSION`)
   - Build metadata

2. **API Endpoint**: `GET /api/version`
   - Returns version information as JSON
   - Includes game version, save version, build date

3. **UI Display**: Version shown in header below game title
   - Format: "v0.2.0"
   - Automatically loaded on page load

4. **Save File Compatibility**:
   - Each save file contains a version number
   - `is_save_compatible()` function checks compatibility
   - Same major version = compatible

### Updating the Version

To release a new version:

1. Edit `version.py`:
   ```python
   VERSION_MAJOR = 0
   VERSION_MINOR = 2
   VERSION_PATCH = 1  # Increment for bug fixes
   BUILD_DATE = "2025-11-12"  # Update date
   ```

2. If save format changes, update `SAVE_VERSION`:
   ```python
   SAVE_VERSION = "1.4"  # Increment major for breaking changes
   ```

3. Update this file (VERSION_INFO.md) with changelog

4. Commit and tag the release:
   ```bash
   git add version.py VERSION_INFO.md
   git commit -m "Release v0.2.1"
   git tag v0.2.1
   git push && git push --tags
   ```
