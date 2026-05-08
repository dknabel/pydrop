"""Preset management system for loading, searching, and managing presets.

Handles loading of built-in presets from JSON and custom presets from user
directory. Provides methods for searching, filtering, and managing presets.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Union

from src.ui.models import Preset, CustomPreset

# Set up logging
logger = logging.getLogger(__name__)


class PresetManager:
    """Manages built-in and custom presets with search and filtering.

    Loads presets from two sources:
    - Built-in presets from src/presets/presets.json
    - Custom presets from ~/.audiovisualizer/custom_presets/

    Provides methods for searching by name/description/tags, filtering by theme,
    and managing custom presets (save/delete).

    Attributes:
        builtin_presets: List of built-in Preset objects
        custom_presets: Dictionary mapping preset_id to CustomPreset objects
    """

    def __init__(self) -> None:
        """Initialize PresetManager and load all presets.

        Loads both built-in presets from JSON and custom presets from user
        directory. Creates custom presets directory if it doesn't exist.
        """
        self.builtin_presets: List[Preset] = []
        self.custom_presets: Dict[str, CustomPreset] = {}

        # Load presets
        self.builtin_presets = self.load_builtin_presets()
        self.custom_presets = self.load_custom_presets()

    def load_builtin_presets(self) -> List[Preset]:
        """Load built-in presets from JSON file.

        Attempts to load from src/presets/presets.json. Only loads presets with
        valid visual_type assignments to use the new visual type system.
        Returns empty list with a warning if file is not found or JSON is invalid.

        Returns:
            List of Preset objects loaded from JSON with visual_type set

        Raises:
            No exceptions - handles all errors gracefully with logging
        """
        presets_file = Path(__file__).parent.parent / "presets" / "presets.json"

        if not presets_file.exists():
            logger.warning(
                f"Presets JSON file not found at {presets_file}. "
                "Returning empty preset list."
            )
            return []

        try:
            with open(presets_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            presets = []
            for item in data:
                try:
                    # Only load presets with visual_type (part of new visual type system)
                    if 'visual_type' not in item or not item.get('visual_type'):
                        continue

                    preset = Preset.from_dict(item)
                    presets.append(preset)
                except ValueError as e:
                    logger.warning(f"Skipping invalid preset: {e}")
                    continue

            logger.info(f"Loaded {len(presets)} built-in presets")
            return presets

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in presets file: {e}")
            return []
        except Exception as e:
            logger.error(f"Error loading presets: {e}")
            return []

    def load_custom_presets(self) -> Dict[str, CustomPreset]:
        """Load custom presets from user directory.

        Loads from ~/.audiovisualizer/custom_presets/ directory. Creates
        directory if it doesn't exist.

        Returns:
            Dictionary mapping preset_id to CustomPreset objects

        Raises:
            No exceptions - handles all errors gracefully with logging
        """
        custom_dir = Path.home() / ".audiovisualizer" / "custom_presets"

        # Create directory if it doesn't exist
        try:
            custom_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            logger.warning(f"Could not create custom presets directory: {e}")
            return {}

        custom_presets = {}

        try:
            # Iterate through JSON files in custom presets directory
            for preset_file in custom_dir.glob("*.json"):
                try:
                    with open(preset_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    custom_preset = CustomPreset.from_dict(data)
                    custom_presets[custom_preset.id] = custom_preset

                except json.JSONDecodeError as e:
                    logger.warning(f"Invalid JSON in {preset_file.name}: {e}")
                    continue
                except ValueError as e:
                    logger.warning(f"Invalid custom preset {preset_file.name}: {e}")
                    continue
                except Exception as e:
                    logger.warning(f"Error loading {preset_file.name}: {e}")
                    continue

            logger.info(f"Loaded {len(custom_presets)} custom presets")
            return custom_presets

        except Exception as e:
            logger.error(f"Error loading custom presets: {e}")
            return {}

    def get_preset(self, preset_id: int) -> Optional[Preset]:
        """Get a built-in preset by ID.

        Args:
            preset_id: The integer ID of the preset

        Returns:
            Preset object if found, None otherwise
        """
        for preset in self.builtin_presets:
            if preset.id == preset_id:
                return preset
        return None

    def get_custom_preset(self, preset_id: str) -> Optional[CustomPreset]:
        """Get a custom preset by ID.

        Args:
            preset_id: The string ID of the custom preset

        Returns:
            CustomPreset object if found, None otherwise
        """
        return self.custom_presets.get(preset_id)

    def search(self, query: str) -> List[Preset]:
        """Search presets by name, description, or tags.

        Case-insensitive search across name, description, and tags.

        Args:
            query: Search query string

        Returns:
            List of Preset objects matching the query
        """
        query_lower = query.lower()
        results = []

        for preset in self.builtin_presets:
            # Check name
            if query_lower in preset.name.lower():
                results.append(preset)
                continue

            # Check description
            if query_lower in preset.description.lower():
                results.append(preset)
                continue

            # Check tags
            if any(query_lower in tag.lower() for tag in preset.tags):
                results.append(preset)

        return results

    def filter_by_theme(self, theme: str) -> List[Preset]:
        """Get all presets with a specific theme.

        Args:
            theme: Theme name to filter by

        Returns:
            List of Preset objects with the specified theme
        """
        return [p for p in self.builtin_presets if p.theme == theme]

    def get_all_themes(self) -> List[str]:
        """Get all available themes.

        Returns themes as a sorted list with 'core' theme first.

        Returns:
            List of theme names, sorted alphabetically with 'core' first
        """
        themes = set(p.theme for p in self.builtin_presets)
        themes_list = sorted(themes)

        # Move 'core' to the front if it exists
        if 'core' in themes_list:
            themes_list.remove('core')
            themes_list.insert(0, 'core')

        return themes_list

    def save_custom_preset(self, custom: CustomPreset) -> None:
        """Save a custom preset to file.

        Saves the custom preset as a JSON file in the custom presets directory.
        The filename is based on the preset ID.

        Args:
            custom: CustomPreset object to save

        Raises:
            OSError: If file cannot be written
            ValueError: If preset ID is invalid
        """
        custom_dir = Path.home() / ".audiovisualizer" / "custom_presets"

        # Ensure directory exists
        try:
            custom_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            logger.error(f"Could not create custom presets directory: {e}")
            raise

        # Validate preset ID format
        if not custom.id.startswith("custom_"):
            raise ValueError(f"Invalid custom preset ID format: {custom.id}")

        # Save to file
        preset_file = custom_dir / f"{custom.id}.json"

        try:
            with open(preset_file, 'w', encoding='utf-8') as f:
                json.dump(custom.to_dict(), f, indent=2, ensure_ascii=False)

            # Update in-memory cache
            self.custom_presets[custom.id] = custom
            logger.info(f"Saved custom preset: {custom.id}")

        except Exception as e:
            logger.error(f"Error saving custom preset: {e}")
            raise

    def delete_custom_preset(self, preset_id: str) -> None:
        """Delete a custom preset file.

        Args:
            preset_id: The string ID of the custom preset to delete

        Raises:
            FileNotFoundError: If preset file is not found
            ValueError: If preset ID is invalid
        """
        custom_dir = Path.home() / ".audiovisualizer" / "custom_presets"
        preset_file = custom_dir / f"{preset_id}.json"

        # Validate preset ID format
        if not preset_id.startswith("custom_"):
            raise ValueError(f"Invalid custom preset ID format: {preset_id}")

        if not preset_file.exists():
            raise FileNotFoundError(f"Custom preset not found: {preset_id}")

        try:
            preset_file.unlink()

            # Remove from in-memory cache
            if preset_id in self.custom_presets:
                del self.custom_presets[preset_id]

            logger.info(f"Deleted custom preset: {preset_id}")

        except Exception as e:
            logger.error(f"Error deleting custom preset: {e}")
            raise


class FavoritesManager:
    """Manage favorite presets with file persistence.

    Stores a set of favorite preset IDs in a JSON file. Allows adding,
    removing, toggling, and checking favorite status. Supports automatic
    persistence to disk.

    Attributes:
        favorites_file: Path to the JSON file storing favorites
        favorites: Set of favorite preset IDs
    """

    def __init__(self, favorites_file: Path = None) -> None:
        """Initialize FavoritesManager.

        Args:
            favorites_file: Path to favorites JSON file. Defaults to
                ~/.audiovisualizer/favorites.json
        """
        if favorites_file is None:
            favorites_file = Path.home() / ".audiovisualizer" / "favorites.json"
        self.favorites_file = favorites_file
        self.favorites = set()
        self.load()

    def load(self) -> None:
        """Load favorites from file.

        If file doesn't exist or is corrupt, initializes with empty favorites.
        Logs warnings for any errors encountered.

        Raises:
            No exceptions - handles all errors gracefully with logging
        """
        if self.favorites_file.exists():
            try:
                with open(self.favorites_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.favorites = set(data.get('favorites', []))
                logger.info(f"Loaded {len(self.favorites)} favorites")
            except (json.JSONDecodeError, IOError, OSError) as e:
                logger.warning(f"Failed to load favorites: {e}")
                self.favorites = set()
        else:
            self.favorites = set()

    def save(self) -> None:
        """Save favorites to file.

        Creates parent directories if they don't exist. Raises exceptions
        if file cannot be written.

        Raises:
            OSError: If file cannot be written
        """
        try:
            self.favorites_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump({'favorites': list(self.favorites)}, f, indent=2)
            logger.info(f"Saved {len(self.favorites)} favorites")
        except Exception as e:
            logger.error(f"Error saving favorites: {e}")
            raise

    def add(self, preset_id: Union[int, str]) -> None:
        """Add a preset to favorites.

        Args:
            preset_id: The ID of the preset to add (int or str)
        """
        self.favorites.add(preset_id)

    def remove(self, preset_id: Union[int, str]) -> None:
        """Remove a preset from favorites.

        Args:
            preset_id: The ID of the preset to remove (int or str)
        """
        self.favorites.discard(preset_id)

    def toggle(self, preset_id: Union[int, str]) -> bool:
        """Toggle favorite status of a preset.

        Args:
            preset_id: The ID of the preset to toggle

        Returns:
            True if preset is now favorited, False if removed
        """
        if self.is_favorite(preset_id):
            self.remove(preset_id)
            return False
        else:
            self.add(preset_id)
            return True

    def is_favorite(self, preset_id: Union[int, str]) -> bool:
        """Check if a preset is favorited.

        Args:
            preset_id: The ID of the preset to check

        Returns:
            True if preset is in favorites, False otherwise
        """
        return preset_id in self.favorites
