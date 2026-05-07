"""Data models for preset system with JSON serialization support."""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Union, Set, Any
from datetime import datetime
import json


@dataclass
class Preset:
    """Built-in preset metadata.

    Represents a preset that comes with the application. Contains metadata
    about the preset such as theme, shader path, and difficulty level.

    Attributes:
        id: Unique integer identifier for the preset
        name: Display name of the preset
        theme: Theme category (e.g., 'core', 'cyberpunk')
        description: Human-readable description of the preset
        shader: Path to the shader file used by this preset
        tags: List of tags for categorization (default: [])
        difficulty: Difficulty level: 'easy', 'medium', 'hard' (default: 'medium')
    """

    id: int
    name: str
    theme: str
    description: str
    shader: str
    tags: List[str] = field(default_factory=list)
    difficulty: str = "medium"

    def to_dict(self) -> Dict[str, Any]:
        """Convert preset to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the preset
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Preset":
        """Create preset from dictionary.

        Args:
            data: Dictionary containing preset data

        Returns:
            Preset instance

        Raises:
            ValueError: If required fields are missing
        """
        try:
            return cls(
                id=data['id'],
                name=data['name'],
                theme=data['theme'],
                description=data['description'],
                shader=data['shader'],
                tags=data.get('tags', []),
                difficulty=data.get('difficulty', 'medium')
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")


@dataclass
class CustomPreset:
    """User-created preset with customizable parameters.

    Represents a preset that users have created by customizing a base preset
    with additional parameters. Tracks creation and modification timestamps
    in ISO format.

    Attributes:
        id: Unique string identifier (format: "custom_###")
        name: Display name of the custom preset
        base_preset: ID of the base preset this is derived from
        parameters: Dictionary of parameter name to float value
        mix_preset: Optional ID of a second preset to mix with (default: None)
        created: ISO format datetime string of creation time (auto-generated)
        modified: ISO format datetime string of last modification (auto-generated)
    """

    id: str
    name: str
    base_preset: int
    parameters: Dict[str, float] = field(default_factory=dict)
    mix_preset: Optional[int] = None
    created: str = field(default_factory=lambda: datetime.now().isoformat())
    modified: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert custom preset to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the custom preset
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "CustomPreset":
        """Create custom preset from dictionary.

        Args:
            data: Dictionary containing custom preset data

        Returns:
            CustomPreset instance

        Raises:
            ValueError: If required fields are missing
        """
        try:
            return cls(
                id=data['id'],
                name=data['name'],
                base_preset=data['base_preset'],
                parameters=data.get('parameters', {}),
                mix_preset=data.get('mix_preset'),
                created=data.get('created', datetime.now().isoformat()),
                modified=data.get('modified', datetime.now().isoformat())
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")


class FavoritesManager:
    """Manages a set of favorited preset IDs.

    Tracks which presets (both built-in and custom) are marked as favorites.
    Uses set-based storage for O(1) lookup and supports JSON serialization
    via list conversion.

    Attributes:
        favorites: Internal set of preset IDs marked as favorites
    """

    def __init__(self) -> None:
        """Initialize an empty favorites manager."""
        self.favorites: Set[Union[int, str]] = set()

    def add(self, preset_id: Union[int, str]) -> None:
        """Add a preset to favorites.

        Args:
            preset_id: ID of the preset to add (int for built-in, str for custom)
        """
        self.favorites.add(preset_id)

    def remove(self, preset_id: Union[int, str]) -> None:
        """Remove a preset from favorites.

        Args:
            preset_id: ID of the preset to remove
        """
        self.favorites.discard(preset_id)

    def toggle(self, preset_id: Union[int, str]) -> bool:
        """Toggle a preset's favorite status.

        Args:
            preset_id: ID of the preset to toggle

        Returns:
            True if the preset is now favorited, False if removed
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
            preset_id: ID of the preset to check

        Returns:
            True if the preset is favorited, False otherwise
        """
        return preset_id in self.favorites

    def to_list(self) -> List[Union[int, str]]:
        """Convert favorites to list for JSON serialization.

        Returns:
            List of favorited preset IDs
        """
        return list(self.favorites)

    def from_list(self, favorites_list: List[Union[int, str]]) -> None:
        """Load favorites from list.

        Args:
            favorites_list: List of preset IDs to mark as favorites
        """
        self.favorites = set(favorites_list)
