"""Tests for FavoritesManager persistence functionality."""

import pytest
import tempfile
from pathlib import Path
from src.ui.presets_data import FavoritesManager


def test_favorites_save_and_load():
    """Favorites can be saved to file and loaded"""
    with tempfile.TemporaryDirectory() as tmpdir:
        fav_file = Path(tmpdir) / "favorites.json"

        mgr = FavoritesManager(fav_file)
        mgr.add(5)
        mgr.add(12)
        mgr.save()

        # Load in new manager
        mgr2 = FavoritesManager(fav_file)
        assert mgr2.is_favorite(5)
        assert mgr2.is_favorite(12)
        assert not mgr2.is_favorite(99)


def test_favorites_toggle():
    """Toggle favorite status"""
    with tempfile.TemporaryDirectory() as tmpdir:
        mgr = FavoritesManager(Path(tmpdir) / "fav.json")

        assert mgr.toggle(5) == True  # Add
        assert mgr.toggle(5) == False  # Remove
        assert mgr.toggle(5) == True  # Add again
