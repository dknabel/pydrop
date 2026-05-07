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


def test_favorites_add():
    """Add method adds preset to favorites"""
    with tempfile.TemporaryDirectory() as tmpdir:
        mgr = FavoritesManager(Path(tmpdir) / "fav.json")
        mgr.add(5)
        assert mgr.is_favorite(5)
        assert not mgr.is_favorite(6)


def test_favorites_remove():
    """Remove method removes preset from favorites"""
    with tempfile.TemporaryDirectory() as tmpdir:
        mgr = FavoritesManager(Path(tmpdir) / "fav.json")
        mgr.add(5)
        mgr.remove(5)
        assert not mgr.is_favorite(5)


def test_favorites_remove_nonexistent():
    """Remove on non-existent preset is safe"""
    with tempfile.TemporaryDirectory() as tmpdir:
        mgr = FavoritesManager(Path(tmpdir) / "fav.json")
        mgr.remove(999)  # Should not raise


def test_favorites_multiple():
    """Multiple presets can be favorited"""
    with tempfile.TemporaryDirectory() as tmpdir:
        mgr = FavoritesManager(Path(tmpdir) / "fav.json")
        mgr.add(1)
        mgr.add(5)
        mgr.add(10)
        assert mgr.is_favorite(1)
        assert mgr.is_favorite(5)
        assert mgr.is_favorite(10)


def test_favorites_empty():
    """Empty favorites file loads correctly"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create empty json file
        fav_file = Path(tmpdir) / "fav.json"
        fav_file.write_text('{"favorites": []}', encoding='utf-8')

        mgr = FavoritesManager(fav_file)
        assert len(mgr.favorites) == 0


def test_favorites_corrupt_json():
    """Corrupt JSON is handled gracefully"""
    with tempfile.TemporaryDirectory() as tmpdir:
        fav_file = Path(tmpdir) / "fav.json"
        fav_file.write_text('invalid json{', encoding='utf-8')

        # Should not raise, just log warning
        mgr = FavoritesManager(fav_file)
        assert len(mgr.favorites) == 0


def test_favorites_mixed_types():
    """Can favorite both preset IDs (int) and custom preset IDs (str)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        mgr = FavoritesManager(Path(tmpdir) / "fav.json")
        mgr.add(5)
        mgr.add("custom_001")
        mgr.save()

        mgr2 = FavoritesManager(Path(tmpdir) / "fav.json")
        assert mgr2.is_favorite(5)
        assert mgr2.is_favorite("custom_001")
