"""Tests for PresetManager class.

Tests loading of built-in and custom presets, searching, filtering,
and managing custom presets.
"""

import json
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock

from src.ui.presets_data import PresetManager
from src.ui.models import Preset, CustomPreset


class TestPresetManagerLoadBuiltin:
    """Test loading built-in presets."""

    def test_preset_manager_load_builtin(self):
        """PresetManager loads built-in presets from JSON."""
        manager = PresetManager()

        # Should have loaded presets
        assert len(manager.builtin_presets) > 0
        assert isinstance(manager.builtin_presets[0], Preset)

        # Check first preset has required fields
        first = manager.builtin_presets[0]
        assert first.id == 0
        assert first.name == "Waveform"
        assert first.theme == "core"
        assert first.shader is not None

    def test_preset_manager_loads_all_required_fields(self):
        """Loaded presets have all required fields."""
        manager = PresetManager()

        for preset in manager.builtin_presets:
            assert preset.id is not None
            assert preset.name is not None
            assert preset.theme is not None
            assert preset.description is not None
            assert preset.shader is not None
            assert hasattr(preset, 'tags')
            assert hasattr(preset, 'difficulty')

    def test_preset_manager_presets_have_valid_types(self):
        """Loaded presets have correct types."""
        manager = PresetManager()

        for preset in manager.builtin_presets:
            assert isinstance(preset.id, int)
            assert isinstance(preset.name, str)
            assert isinstance(preset.theme, str)
            assert isinstance(preset.description, str)
            assert isinstance(preset.shader, str)
            assert isinstance(preset.tags, list)
            assert isinstance(preset.difficulty, str)


class TestPresetManagerGetById:
    """Test getting presets by ID."""

    def test_preset_manager_get_by_id(self):
        """PresetManager.get_preset() retrieves preset by ID."""
        manager = PresetManager()

        preset = manager.get_preset(0)
        assert preset is not None
        assert preset.id == 0
        assert preset.name == "Waveform"

    def test_get_preset_returns_none_for_invalid_id(self):
        """PresetManager.get_preset() returns None for invalid ID."""
        manager = PresetManager()

        preset = manager.get_preset(99999)
        assert preset is None

    def test_get_preset_works_for_different_ids(self):
        """PresetManager.get_preset() works for various valid IDs."""
        manager = PresetManager()

        # Should be able to get multiple presets
        preset_0 = manager.get_preset(0)
        preset_1 = manager.get_preset(1)

        assert preset_0 is not None
        assert preset_1 is not None
        assert preset_0.id != preset_1.id


class TestPresetManagerSearch:
    """Test preset searching."""

    def test_preset_manager_search(self):
        """PresetManager.search() finds presets by name."""
        manager = PresetManager()

        results = manager.search("waveform")
        assert len(results) > 0
        assert any(p.name.lower() == "waveform" for p in results)

    def test_search_is_case_insensitive(self):
        """PresetManager.search() is case-insensitive."""
        manager = PresetManager()

        results_lower = manager.search("waveform")
        results_upper = manager.search("WAVEFORM")
        results_mixed = manager.search("WaVeFoRm")

        assert len(results_lower) == len(results_upper) == len(results_mixed)

    def test_search_by_description(self):
        """PresetManager.search() finds presets by description."""
        manager = PresetManager()

        results = manager.search("visualization")
        assert len(results) > 0

    def test_search_by_tags(self):
        """PresetManager.search() finds presets by tags."""
        manager = PresetManager()

        results = manager.search("classic")
        assert len(results) > 0

    def test_search_returns_empty_for_no_matches(self):
        """PresetManager.search() returns empty list for no matches."""
        manager = PresetManager()

        results = manager.search("xyzabc123notarealpreset")
        assert len(results) == 0
        assert isinstance(results, list)

    def test_search_returns_all_matches(self):
        """PresetManager.search() returns all matching presets."""
        manager = PresetManager()

        # Search for something that appears in multiple presets
        results = manager.search("cosmic")

        # Should find at least the cosmic theme presets
        assert len(results) > 0
        assert all(isinstance(p, Preset) for p in results)


class TestPresetManagerFilterByTheme:
    """Test filtering presets by theme."""

    def test_preset_manager_filter_by_category(self):
        """PresetManager.filter_by_theme() gets presets by theme."""
        manager = PresetManager()

        core_presets = manager.filter_by_theme("core")
        assert len(core_presets) > 0
        assert all(p.theme == "core" for p in core_presets)

    def test_filter_by_theme_returns_empty_for_invalid_theme(self):
        """PresetManager.filter_by_theme() returns empty list for invalid theme."""
        manager = PresetManager()

        results = manager.filter_by_theme("notarealtheme")
        assert len(results) == 0
        assert isinstance(results, list)

    def test_filter_by_theme_returns_correct_presets(self):
        """PresetManager.filter_by_theme() returns only matching presets."""
        manager = PresetManager()

        cosmic_presets = manager.filter_by_theme("cosmic")
        assert all(p.theme == "cosmic" for p in cosmic_presets)

        # No core presets should be in cosmic filter
        core_presets = manager.filter_by_theme("core")
        assert not any(p.theme == "cosmic" for p in core_presets)


class TestPresetManagerThemes:
    """Test theme management."""

    def test_get_all_themes(self):
        """PresetManager.get_all_themes() returns all themes."""
        manager = PresetManager()

        themes = manager.get_all_themes()
        assert len(themes) > 0
        assert isinstance(themes, list)

    def test_get_all_themes_core_first(self):
        """PresetManager.get_all_themes() puts 'core' first."""
        manager = PresetManager()

        themes = manager.get_all_themes()
        assert themes[0] == "core"

    def test_get_all_themes_sorted(self):
        """PresetManager.get_all_themes() returns sorted list."""
        manager = PresetManager()

        themes = manager.get_all_themes()

        # Check that it's sorted (excluding core which is always first)
        for i in range(1, len(themes) - 1):
            assert themes[i] < themes[i + 1]

    def test_get_all_themes_no_duplicates(self):
        """PresetManager.get_all_themes() has no duplicates."""
        manager = PresetManager()

        themes = manager.get_all_themes()
        assert len(themes) == len(set(themes))


class TestCustomPresets:
    """Test custom preset management."""

    def test_load_custom_presets_creates_directory(self):
        """PresetManager creates custom_presets directory if missing."""
        with patch('pathlib.Path.home') as mock_home:
            with TemporaryDirectory() as temp_dir:
                mock_home.return_value = Path(temp_dir)

                manager = PresetManager()

                custom_dir = Path(temp_dir) / ".audiovisualizer" / "custom_presets"
                assert custom_dir.exists()

    def test_save_custom_preset(self):
        """PresetManager.save_custom_preset() saves to file."""
        with patch('pathlib.Path.home') as mock_home:
            with TemporaryDirectory() as temp_dir:
                mock_home.return_value = Path(temp_dir)

                manager = PresetManager()

                custom = CustomPreset(
                    id="custom_001",
                    name="My Custom Preset",
                    base_preset=0,
                    parameters={"brightness": 1.5}
                )

                manager.save_custom_preset(custom)

                # Check that file was created
                custom_dir = Path(temp_dir) / ".audiovisualizer" / "custom_presets"
                assert (custom_dir / "custom_001.json").exists()

                # Verify it was added to in-memory cache
                assert "custom_001" in manager.custom_presets

    def test_save_custom_preset_writes_valid_json(self):
        """PresetManager.save_custom_preset() writes valid JSON."""
        with patch('pathlib.Path.home') as mock_home:
            with TemporaryDirectory() as temp_dir:
                mock_home.return_value = Path(temp_dir)

                manager = PresetManager()

                custom = CustomPreset(
                    id="custom_002",
                    name="Test Preset",
                    base_preset=1,
                    parameters={"speed": 0.8}
                )

                manager.save_custom_preset(custom)

                # Read the file and verify JSON is valid
                preset_file = Path(temp_dir) / ".audiovisualizer" / "custom_presets" / "custom_002.json"
                with open(preset_file, 'r') as f:
                    data = json.load(f)

                assert data['id'] == "custom_002"
                assert data['name'] == "Test Preset"
                assert data['base_preset'] == 1

    def test_save_custom_preset_invalid_id_raises_error(self):
        """PresetManager.save_custom_preset() raises error for invalid ID."""
        with patch('pathlib.Path.home') as mock_home:
            with TemporaryDirectory() as temp_dir:
                mock_home.return_value = Path(temp_dir)

                manager = PresetManager()

                custom = CustomPreset(
                    id="invalid_001",  # Should start with "custom_"
                    name="Bad ID Preset",
                    base_preset=0
                )

                with pytest.raises(ValueError):
                    manager.save_custom_preset(custom)

    def test_get_custom_preset(self):
        """PresetManager.get_custom_preset() retrieves custom preset."""
        with patch('pathlib.Path.home') as mock_home:
            with TemporaryDirectory() as temp_dir:
                mock_home.return_value = Path(temp_dir)

                manager = PresetManager()

                custom = CustomPreset(
                    id="custom_003",
                    name="Get Test",
                    base_preset=2
                )

                manager.save_custom_preset(custom)

                retrieved = manager.get_custom_preset("custom_003")
                assert retrieved is not None
                assert retrieved.id == "custom_003"
                assert retrieved.name == "Get Test"

    def test_get_custom_preset_returns_none_for_invalid_id(self):
        """PresetManager.get_custom_preset() returns None for invalid ID."""
        manager = PresetManager()

        retrieved = manager.get_custom_preset("custom_999999")
        assert retrieved is None

    def test_delete_custom_preset(self):
        """PresetManager.delete_custom_preset() removes preset file."""
        with patch('pathlib.Path.home') as mock_home:
            with TemporaryDirectory() as temp_dir:
                mock_home.return_value = Path(temp_dir)

                manager = PresetManager()

                custom = CustomPreset(
                    id="custom_004",
                    name="Delete Test",
                    base_preset=3
                )

                manager.save_custom_preset(custom)

                # Verify it exists
                assert "custom_004" in manager.custom_presets

                # Delete it
                manager.delete_custom_preset("custom_004")

                # Verify it's gone
                assert "custom_004" not in manager.custom_presets
                custom_dir = Path(temp_dir) / ".audiovisualizer" / "custom_presets"
                assert not (custom_dir / "custom_004.json").exists()

    def test_delete_custom_preset_invalid_id_raises_error(self):
        """PresetManager.delete_custom_preset() raises error for invalid ID."""
        manager = PresetManager()

        with pytest.raises(ValueError):
            manager.delete_custom_preset("invalid_id")

    def test_delete_custom_preset_not_found_raises_error(self):
        """PresetManager.delete_custom_preset() raises error for missing file."""
        manager = PresetManager()

        with pytest.raises(FileNotFoundError):
            manager.delete_custom_preset("custom_nonexistent")


class TestPresetManagerIntegration:
    """Integration tests for PresetManager."""

    def test_preset_manager_full_workflow(self):
        """Full workflow: load, search, filter, and manage presets."""
        with patch('pathlib.Path.home') as mock_home:
            with TemporaryDirectory() as temp_dir:
                mock_home.return_value = Path(temp_dir)

                manager = PresetManager()

                # Load built-in presets
                assert len(manager.builtin_presets) > 0

                # Search
                results = manager.search("waveform")
                assert len(results) > 0

                # Filter by theme
                core = manager.filter_by_theme("core")
                assert len(core) > 0

                # Get themes
                themes = manager.get_all_themes()
                assert "core" == themes[0]

                # Create and save custom preset
                custom = CustomPreset(
                    id="custom_workflow",
                    name="Workflow Test",
                    base_preset=0,
                    parameters={"param1": 1.0}
                )
                manager.save_custom_preset(custom)

                # Retrieve custom preset
                retrieved = manager.get_custom_preset("custom_workflow")
                assert retrieved is not None
                assert retrieved.parameters["param1"] == 1.0

                # Delete custom preset
                manager.delete_custom_preset("custom_workflow")
                assert manager.get_custom_preset("custom_workflow") is None

    def test_custom_presets_persist_across_instances(self):
        """Custom presets persist when loading in new manager instance."""
        with patch('pathlib.Path.home') as mock_home:
            with TemporaryDirectory() as temp_dir:
                mock_home.return_value = Path(temp_dir)

                # Create first manager and save preset
                manager1 = PresetManager()
                custom = CustomPreset(
                    id="custom_persist",
                    name="Persistence Test",
                    base_preset=1
                )
                manager1.save_custom_preset(custom)

                # Create new manager instance
                manager2 = PresetManager()

                # Should load the previously saved preset
                retrieved = manager2.get_custom_preset("custom_persist")
                assert retrieved is not None
                assert retrieved.name == "Persistence Test"
