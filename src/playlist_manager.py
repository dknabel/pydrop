"""Playlist Manager - Save/load custom preset sequences"""

from pathlib import Path
import json
from typing import List, Dict, Optional


class PlaylistManager:
    """Manages playlists of preset sequences with save/load functionality."""

    def __init__(self):
        """Initialize the playlist manager with default directory."""
        self.playlist_dir = Path.home() / '.audiovisualizer' / 'playlists'
        self.playlist_dir.mkdir(parents=True, exist_ok=True)
        self.current_playlist = None
        self.playlists = {}
        self.load_all_playlists()

    def load_all_playlists(self) -> None:
        """Load all .json playlist files from the playlists directory."""
        self.playlists = {}

        if not self.playlist_dir.exists():
            return

        for playlist_file in self.playlist_dir.glob('*.json'):
            try:
                with open(playlist_file, 'r') as f:
                    data = json.load(f)
                    playlist_name = data.get('name')
                    presets = data.get('presets', [])

                    if playlist_name:
                        self.playlists[playlist_name] = presets
                        print(f"Loaded playlist: {playlist_name} ({len(presets)} presets)")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading playlist {playlist_file.name}: {e}")

    def save_playlist(self, name: str, preset_names: List[str]) -> bool:
        """
        Save a playlist with the given name and preset sequence.

        Args:
            name: Playlist name
            preset_names: List of preset names in order

        Returns:
            True if successful, False otherwise
        """
        if not name or not preset_names:
            print("Error: Playlist name and presets are required")
            return False

        try:
            playlist_data = {
                'name': name,
                'presets': preset_names
            }

            # Create filename from playlist name (lowercase, replace spaces with underscores)
            filename = name.lower().replace(' ', '_') + '.json'
            filepath = self.playlist_dir / filename

            with open(filepath, 'w') as f:
                json.dump(playlist_data, f, indent=2)

            # Update in-memory dictionary
            self.playlists[name] = preset_names
            print(f"Saved playlist: {name} ({len(preset_names)} presets)")
            return True
        except IOError as e:
            print(f"Error saving playlist: {e}")
            return False

    def activate_playlist(self, name: str) -> bool:
        """
        Activate a playlist by name.

        Args:
            name: Playlist name to activate

        Returns:
            True if successful, False if playlist not found
        """
        if name not in self.playlists:
            print(f"Playlist not found: {name}")
            return False

        self.current_playlist = name
        print(f"Activated playlist: {name}")
        return True

    def deactivate_playlist(self) -> None:
        """Deactivate the current active playlist."""
        if self.current_playlist:
            print(f"Deactivated playlist: {self.current_playlist}")
        self.current_playlist = None

    def get_current_presets(self) -> Optional[List[str]]:
        """
        Get the preset list for the current active playlist.

        Returns:
            List of preset names if a playlist is active, None otherwise
        """
        if self.current_playlist and self.current_playlist in self.playlists:
            return self.playlists[self.current_playlist]
        return None

    def delete_playlist(self, name: str) -> bool:
        """
        Delete a saved playlist.

        Args:
            name: Playlist name to delete

        Returns:
            True if successful, False otherwise
        """
        if name not in self.playlists:
            print(f"Playlist not found: {name}")
            return False

        try:
            # Remove from in-memory dictionary
            del self.playlists[name]

            # Delete the file
            filename = name.lower().replace(' ', '_') + '.json'
            filepath = self.playlist_dir / filename
            filepath.unlink(missing_ok=True)

            # Deactivate if it was the current playlist
            if self.current_playlist == name:
                self.current_playlist = None

            print(f"Deleted playlist: {name}")
            return True
        except Exception as e:
            print(f"Error deleting playlist: {e}")
            return False

    def list_playlists(self) -> List[str]:
        """
        Get a list of available playlist names.

        Returns:
            List of playlist names
        """
        return list(self.playlists.keys())
