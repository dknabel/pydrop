"""Tests for specialized menu UI components."""

import pytest
import pygame
from unittest.mock import MagicMock, Mock
from pathlib import Path
from tempfile import TemporaryDirectory

from src.ui.menu_components import SearchBar
from src.ui.presets_data import PresetManager
from src.ui.models import Preset


# Initialize pygame for testing
pygame.init()


class TestSearchBar:
    """Test SearchBar component."""

    @pytest.fixture
    def preset_manager(self):
        """Create a PresetManager with test presets."""
        manager = PresetManager()
        return manager

    def test_searchbar_init(self, preset_manager):
        """SearchBar initializes with correct properties."""
        search_bar = SearchBar(10, 20, 300, 40, preset_manager)

        assert search_bar.rect.x == 10
        assert search_bar.rect.y == 20
        assert search_bar.rect.width == 300
        assert search_bar.rect.height == 40
        assert search_bar.placeholder == "Search presets..."
        assert search_bar.preset_manager is preset_manager
        assert search_bar.search_results == []

    def test_searchbar_with_callback(self, preset_manager):
        """SearchBar initializes with callback."""
        callback = Mock()
        search_bar = SearchBar(10, 20, 300, 40, preset_manager, on_search_changed=callback)

        assert search_bar.on_search_changed is callback

    def test_searchbar_empty_search_returns_all_presets(self, preset_manager):
        """Empty search returns all built-in presets."""
        callback = Mock()
        search_bar = SearchBar(10, 20, 300, 40, preset_manager, on_search_changed=callback)

        # Trigger search with empty string
        search_bar._text = ""
        search_bar._perform_search()

        # Should return all presets
        assert len(search_bar.search_results) > 0
        assert search_bar.search_results == preset_manager.builtin_presets

    def test_searchbar_search_by_name(self, preset_manager):
        """SearchBar searches by preset name."""
        callback = Mock()
        search_bar = SearchBar(10, 20, 300, 40, preset_manager, on_search_changed=callback)

        # Search for first preset's name
        first_preset = preset_manager.builtin_presets[0]
        search_bar._text = first_preset.name
        search_bar._perform_search()

        # Should find the preset
        assert len(search_bar.search_results) > 0
        assert any(p.id == first_preset.id for p in search_bar.search_results)

    def test_searchbar_case_insensitive_search(self, preset_manager):
        """SearchBar search is case-insensitive."""
        callback = Mock()
        search_bar = SearchBar(10, 20, 300, 40, preset_manager, on_search_changed=callback)

        # Get a preset name and search with different cases
        first_preset = preset_manager.builtin_presets[0]
        original_query = first_preset.name

        # Search with lowercase
        search_bar._text = original_query.lower()
        search_bar._perform_search()
        lowercase_results = len(search_bar.search_results)

        # Search with uppercase
        search_bar._text = original_query.upper()
        search_bar._perform_search()
        uppercase_results = len(search_bar.search_results)

        # Should find same number of results
        assert lowercase_results == uppercase_results
        assert lowercase_results > 0

    def test_searchbar_search_by_description(self, preset_manager):
        """SearchBar searches by preset description."""
        callback = Mock()
        search_bar = SearchBar(10, 20, 300, 40, preset_manager, on_search_changed=callback)

        # Find a word in a preset description
        if preset_manager.builtin_presets:
            first_preset = preset_manager.builtin_presets[0]
            # Search for a word from the description
            if first_preset.description:
                word = first_preset.description.split()[0]
                search_bar._text = word
                search_bar._perform_search()

                # Should find presets with that word in description
                assert len(search_bar.search_results) > 0

    def test_searchbar_search_by_tags(self, preset_manager):
        """SearchBar searches by preset tags."""
        callback = Mock()
        search_bar = SearchBar(10, 20, 300, 40, preset_manager, on_search_changed=callback)

        # Find a preset with tags
        for preset in preset_manager.builtin_presets:
            if preset.tags:
                search_bar._text = preset.tags[0]
                search_bar._perform_search()

                # Should find the preset
                assert len(search_bar.search_results) > 0
                break

    def test_searchbar_callback_on_search(self, preset_manager):
        """SearchBar calls callback with results."""
        callback = Mock()
        search_bar = SearchBar(10, 20, 300, 40, preset_manager, on_search_changed=callback)

        # Trigger search
        search_bar._text = "test"
        search_bar._perform_search()

        # Callback should be called with results
        callback.assert_called_once()
        args = callback.call_args[0]
        assert isinstance(args[0], list)

    def test_searchbar_callback_called_on_event(self, preset_manager):
        """SearchBar calls callback when handling event."""
        callback = Mock()
        search_bar = SearchBar(10, 20, 300, 40, preset_manager, on_search_changed=callback)

        # Focus the search bar
        search_bar.focused = True

        # Simulate typing
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_a, 'unicode': 'a'})
        search_bar.handle_event(event)

        # Callback should be called
        assert callback.called

    def test_searchbar_clear(self, preset_manager):
        """SearchBar.clear() resets search."""
        callback = Mock()
        search_bar = SearchBar(10, 20, 300, 40, preset_manager, on_search_changed=callback)

        # Set some text
        search_bar._text = "query"
        search_bar._perform_search()

        # Clear
        search_bar.clear()

        # Text should be empty
        assert search_bar.text == ""
        # Results should be all presets
        assert search_bar.search_results == preset_manager.builtin_presets

    def test_searchbar_no_matches(self, preset_manager):
        """SearchBar returns empty list for no matches."""
        callback = Mock()
        search_bar = SearchBar(10, 20, 300, 40, preset_manager, on_search_changed=callback)

        # Search for something unlikely to exist
        search_bar._text = "xyzabc123notarealpreset"
        search_bar._perform_search()

        # Should return empty list
        assert search_bar.search_results == []

    def test_searchbar_multiple_matches(self, preset_manager):
        """SearchBar returns multiple matches."""
        callback = Mock()
        search_bar = SearchBar(10, 20, 300, 40, preset_manager, on_search_changed=callback)

        # Search for "a" (likely to match multiple presets)
        search_bar._text = "a"
        search_bar._perform_search()

        # Should return multiple results
        assert len(search_bar.search_results) > 1

    def test_searchbar_renders_without_error(self, preset_manager):
        """SearchBar renders without error."""
        surface = pygame.Surface((400, 100))
        search_bar = SearchBar(10, 20, 300, 40, preset_manager)
        search_bar.visible = True

        # Should not raise
        search_bar.render(surface)

    def test_searchbar_inherits_from_textinput(self, preset_manager):
        """SearchBar extends TextInput."""
        from src.ui.components import TextInput

        search_bar = SearchBar(10, 20, 300, 40, preset_manager)
        assert isinstance(search_bar, TextInput)

    def test_searchbar_max_length(self, preset_manager):
        """SearchBar has reasonable max length."""
        search_bar = SearchBar(10, 20, 300, 40, preset_manager)

        # Should have max_length set (100 from requirements)
        assert search_bar.max_length == 100

    def test_searchbar_substring_matching(self, preset_manager):
        """SearchBar uses substring matching, not exact matching."""
        callback = Mock()
        search_bar = SearchBar(10, 20, 300, 40, preset_manager, on_search_changed=callback)

        # Search with partial name
        if preset_manager.builtin_presets:
            first_preset = preset_manager.builtin_presets[0]
            # Use first 2 characters of name
            if len(first_preset.name) >= 2:
                search_bar._text = first_preset.name[:2]
                search_bar._perform_search()

                # Should find the preset
                assert len(search_bar.search_results) > 0

    def test_searchbar_whitespace_handling(self, preset_manager):
        """SearchBar handles whitespace correctly."""
        callback = Mock()
        search_bar = SearchBar(10, 20, 300, 40, preset_manager, on_search_changed=callback)

        # Search with only whitespace
        search_bar._text = "   "
        search_bar._perform_search()

        # Should treat as empty and return all presets
        assert search_bar.search_results == preset_manager.builtin_presets

    def test_searchbar_focus_handling(self, preset_manager):
        """SearchBar handles focus correctly."""
        search_bar = SearchBar(10, 20, 300, 40, preset_manager)

        # Click to focus
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (50, 30), 'button': 1})
        search_bar.handle_event(event)

        assert search_bar.focused is True

    def test_searchbar_callback_none_optional(self, preset_manager):
        """SearchBar works without callback."""
        search_bar = SearchBar(10, 20, 300, 40, preset_manager)

        # Should not raise even with no callback
        search_bar._text = "test"
        search_bar._perform_search()

        assert search_bar.search_results is not None
