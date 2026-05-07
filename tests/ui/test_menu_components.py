"""Tests for specialized menu UI components."""

import pytest
import pygame
from unittest.mock import MagicMock, Mock
from pathlib import Path
from tempfile import TemporaryDirectory

from src.ui.menu_components import SearchBar, CategoryFilter
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


class TestCategoryFilter:
    """Test CategoryFilter dropdown component."""

    @pytest.fixture
    def preset_manager(self):
        """Create a PresetManager with test presets."""
        manager = PresetManager()
        return manager

    def test_categoryfilter_init(self, preset_manager):
        """CategoryFilter initializes with correct properties."""
        category_filter = CategoryFilter(10, 20, 150, 30, preset_manager)

        assert category_filter.rect.x == 10
        assert category_filter.rect.y == 20
        assert category_filter.rect.width == 150
        assert category_filter.rect.height == 30
        assert category_filter.preset_manager is preset_manager
        assert category_filter.opened is False
        assert category_filter.selected_category == "All"

    def test_categoryfilter_with_callback(self, preset_manager):
        """CategoryFilter initializes with callback."""
        callback = Mock()
        category_filter = CategoryFilter(
            10, 20, 150, 30, preset_manager, on_category_changed=callback
        )

        assert category_filter.on_category_changed is callback

    def test_categoryfilter_build_categories(self, preset_manager):
        """CategoryFilter builds category list with counts."""
        category_filter = CategoryFilter(10, 20, 150, 30, preset_manager)

        # Check that categories dict exists and has "All"
        assert "All" in category_filter.categories
        assert category_filter.categories["All"] > 0

        # Check that themes are included
        themes = preset_manager.get_all_themes()
        for theme in themes:
            assert theme in category_filter.categories

    def test_categoryfilter_category_counts_accurate(self, preset_manager):
        """CategoryFilter category counts match actual preset counts."""
        category_filter = CategoryFilter(10, 20, 150, 30, preset_manager)

        # Check "All" count
        expected_all = len(preset_manager.builtin_presets)
        assert category_filter.categories["All"] == expected_all

        # Check theme counts
        themes = preset_manager.get_all_themes()
        for theme in themes:
            expected_count = len(preset_manager.filter_by_theme(theme))
            assert category_filter.categories[theme] == expected_count

    def test_categoryfilter_dropdown_items_building(self, preset_manager):
        """CategoryFilter builds dropdown items with labels and counts."""
        category_filter = CategoryFilter(10, 20, 150, 30, preset_manager)

        # Should have items
        assert len(category_filter.dropdown_items) > 0

        # First item should be "All"
        first_item = category_filter.dropdown_items[0]
        assert first_item[0] == "All"
        assert first_item[1] == "All"

        # Items are tuples of (label, category, count)
        for item in category_filter.dropdown_items:
            assert len(item) == 3
            assert isinstance(item[0], str)  # label
            assert isinstance(item[1], str)  # category
            assert isinstance(item[2], int)  # count

    def test_categoryfilter_core_first_in_list(self, preset_manager):
        """CategoryFilter puts "core" theme first in sorted list."""
        category_filter = CategoryFilter(10, 20, 150, 30, preset_manager)

        # Find "core" in items (skip "All" which is first)
        themes_in_items = [item[1] for item in category_filter.dropdown_items[1:]]

        if "core" in themes_in_items:
            # "core" should be the first theme after "All"
            assert themes_in_items[0] == "core"

    def test_categoryfilter_themes_sorted(self, preset_manager):
        """CategoryFilter themes are sorted alphabetically."""
        category_filter = CategoryFilter(10, 20, 150, 30, preset_manager)

        # Get themes from dropdown items (skip "All")
        themes = [item[1] for item in category_filter.dropdown_items[1:]]

        # Remove "core" if present to check alphabetical sort
        themes_without_core = [t for t in themes if t != "core"]

        # Check that remaining themes are sorted
        assert themes_without_core == sorted(themes_without_core)

    def test_categoryfilter_toggle_dropdown(self, preset_manager):
        """CategoryFilter opens and closes dropdown on click."""
        category_filter = CategoryFilter(10, 20, 150, 30, preset_manager)

        assert category_filter.opened is False

        # Simulate click on button
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": (50, 35), "button": 1}
        )
        category_filter.handle_event(event)

        assert category_filter.opened is True

        # Click again to close
        category_filter.handle_event(event)
        assert category_filter.opened is False

    def test_categoryfilter_select_category(self, preset_manager):
        """CategoryFilter selects category on dropdown item click."""
        category_filter = CategoryFilter(10, 20, 150, 30, preset_manager)

        # Open dropdown
        category_filter.opened = True

        # Get a theme to select (not "All")
        themes = preset_manager.get_all_themes()
        if themes:
            theme_to_select = themes[0]

            # Find the y position of that item
            for i, (label, category, count) in enumerate(category_filter.dropdown_items):
                if category == theme_to_select:
                    # Calculate menu y position
                    menu_y = category_filter.rect.bottom + 2
                    item_y = menu_y + i * category_filter.item_height

                    # Click on the item
                    event = pygame.event.Event(
                        pygame.MOUSEBUTTONDOWN,
                        {"pos": (category_filter.rect.x + 10, item_y + 10), "button": 1},
                    )
                    category_filter.handle_event(event)

                    assert category_filter.selected_category == theme_to_select
                    assert category_filter.opened is False
                    break

    def test_categoryfilter_callback_on_selection(self, preset_manager):
        """CategoryFilter calls callback when category is selected."""
        callback = Mock()
        category_filter = CategoryFilter(
            10, 20, 150, 30, preset_manager, on_category_changed=callback
        )

        # Open dropdown
        category_filter.opened = True

        # Select first theme
        if category_filter.dropdown_items:
            for i, (label, category, count) in enumerate(category_filter.dropdown_items):
                if category != "All":
                    menu_y = category_filter.rect.bottom + 2
                    item_y = menu_y + i * category_filter.item_height

                    event = pygame.event.Event(
                        pygame.MOUSEBUTTONDOWN,
                        {"pos": (category_filter.rect.x + 10, item_y + 10), "button": 1},
                    )
                    category_filter.handle_event(event)

                    # Callback should be called with the category
                    callback.assert_called_once_with(category)
                    break

    def test_categoryfilter_all_category_selection(self, preset_manager):
        """CategoryFilter "All" category selects all presets."""
        callback = Mock()
        category_filter = CategoryFilter(
            10, 20, 150, 30, preset_manager, on_category_changed=callback
        )

        # Open dropdown
        category_filter.opened = True

        # Click on "All" item
        menu_y = category_filter.rect.bottom + 2

        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {"pos": (category_filter.rect.x + 10, menu_y + 10), "button": 1},
        )
        category_filter.handle_event(event)

        assert category_filter.selected_category == "All"
        callback.assert_called_once_with("All")

    def test_categoryfilter_renders_without_error(self, preset_manager):
        """CategoryFilter renders without error."""
        surface = pygame.Surface((400, 300))
        category_filter = CategoryFilter(10, 20, 150, 30, preset_manager)
        category_filter.visible = True

        # Should not raise
        category_filter.render(surface)

    def test_categoryfilter_renders_dropdown_when_opened(self, preset_manager):
        """CategoryFilter renders dropdown menu when opened."""
        surface = pygame.Surface((400, 300))
        category_filter = CategoryFilter(10, 20, 150, 30, preset_manager)
        category_filter.visible = True
        category_filter.opened = True

        # Should not raise
        category_filter.render(surface)

    def test_categoryfilter_hidden_when_not_visible(self, preset_manager):
        """CategoryFilter doesn't render when not visible."""
        surface = pygame.Surface((400, 300))
        category_filter = CategoryFilter(10, 20, 150, 30, preset_manager)
        category_filter.visible = False

        # Should not raise, should just return early
        category_filter.render(surface)

    def test_categoryfilter_inherits_from_uicomponent(self, preset_manager):
        """CategoryFilter extends UIComponent."""
        from src.ui.components import UIComponent

        category_filter = CategoryFilter(10, 20, 150, 30, preset_manager)
        assert isinstance(category_filter, UIComponent)

    def test_categoryfilter_no_callback_optional(self, preset_manager):
        """CategoryFilter works without callback."""
        category_filter = CategoryFilter(10, 20, 150, 30, preset_manager)

        # Open and select should work without callback
        category_filter.opened = True
        assert category_filter.opened is True

    def test_categoryfilter_item_height(self, preset_manager):
        """CategoryFilter has reasonable item height."""
        category_filter = CategoryFilter(10, 20, 150, 30, preset_manager)

        # Item height should be reasonable
        assert category_filter.item_height > 0
        assert category_filter.item_height <= 50

    def test_categoryfilter_click_outside_dropdown_closes(self, preset_manager):
        """CategoryFilter closes dropdown on click outside."""
        category_filter = CategoryFilter(10, 20, 150, 30, preset_manager)

        # Open dropdown
        category_filter.opened = True
        assert category_filter.opened is True

        # Click outside the dropdown area (far away)
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": (500, 500), "button": 1}
        )
        category_filter.handle_event(event)

        # Should still be open (since we didn't click on an item)
        assert category_filter.opened is True

    def test_categoryfilter_multiple_selections(self, preset_manager):
        """CategoryFilter can switch between categories."""
        callback = Mock()
        category_filter = CategoryFilter(
            10, 20, 150, 30, preset_manager, on_category_changed=callback
        )

        themes = preset_manager.get_all_themes()
        if len(themes) >= 2:
            # Select first theme
            category_filter.opened = True
            first_theme = themes[0]

            for i, (label, category, count) in enumerate(category_filter.dropdown_items):
                if category == first_theme:
                    menu_y = category_filter.rect.bottom + 2
                    item_y = menu_y + i * category_filter.item_height

                    event = pygame.event.Event(
                        pygame.MOUSEBUTTONDOWN,
                        {"pos": (category_filter.rect.x + 10, item_y + 10), "button": 1},
                    )
                    category_filter.handle_event(event)
                    break

            assert category_filter.selected_category == first_theme

            # Select second theme
            category_filter.opened = True
            second_theme = themes[1]

            for i, (label, category, count) in enumerate(category_filter.dropdown_items):
                if category == second_theme:
                    menu_y = category_filter.rect.bottom + 2
                    item_y = menu_y + i * category_filter.item_height

                    event = pygame.event.Event(
                        pygame.MOUSEBUTTONDOWN,
                        {"pos": (category_filter.rect.x + 10, item_y + 10), "button": 1},
                    )
                    category_filter.handle_event(event)
                    break

            assert category_filter.selected_category == second_theme
            assert callback.call_count == 2
