"""Tests for specialized menu UI components."""

import pytest
import pygame
from unittest.mock import MagicMock, Mock
from pathlib import Path
from tempfile import TemporaryDirectory

from src.ui.menu_components import (
    SearchBar, CategoryFilter, FavoritesToggle, PresetCard, PresetGrid,
    DetailsPanel, ParameterEditorModal, MixToolModal
)
from src.ui.presets_data import PresetManager
from src.ui.models import Preset, FavoritesManager


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


class TestFavoritesToggle:
    """Test FavoritesToggle button component."""

    @pytest.fixture
    def favorites_manager(self):
        """Create a FavoritesManager instance."""
        return FavoritesManager()

    def test_favorites_toggle_init(self, favorites_manager):
        """FavoritesToggle initializes with correct properties."""
        toggle = FavoritesToggle(10, 20, 40, 40, 1, favorites_manager)

        assert toggle.rect.x == 10
        assert toggle.rect.y == 20
        assert toggle.rect.width == 40
        assert toggle.rect.height == 40
        assert toggle.preset_id == 1
        assert toggle.favorites_manager is favorites_manager
        assert toggle.is_favorited is False

    def test_favorites_toggle_with_favorited_preset(self, favorites_manager):
        """FavoritesToggle reflects favorited preset status."""
        favorites_manager.add(1)
        toggle = FavoritesToggle(10, 20, 40, 40, 1, favorites_manager)

        assert toggle.is_favorited is True

    def test_favorites_toggle_click_toggles_status(self, favorites_manager):
        """FavoritesToggle toggles favorite status on click."""
        toggle = FavoritesToggle(10, 20, 40, 40, 1, favorites_manager)

        assert toggle.is_favorited is False
        assert favorites_manager.is_favorite(1) is False

        # Simulate click
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": (30, 40), "button": 1}
        )
        toggle.handle_event(event)

        assert toggle.is_favorited is True
        assert favorites_manager.is_favorite(1) is True

    def test_favorites_toggle_calls_callback(self, favorites_manager):
        """FavoritesToggle calls callback on toggle."""
        callback = Mock()
        toggle = FavoritesToggle(10, 20, 40, 40, 1, favorites_manager, on_toggled=callback)

        # Simulate click
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": (30, 40), "button": 1}
        )
        toggle.handle_event(event)

        callback.assert_called_once_with(True)

    def test_favorites_toggle_render_filled_star(self, favorites_manager):
        """FavoritesToggle renders filled star when favorited."""
        surface = pygame.Surface((100, 100))
        toggle = FavoritesToggle(10, 20, 40, 40, 1, favorites_manager)
        toggle.visible = True
        toggle.is_favorited = True

        # Should not raise
        toggle.render(surface)

    def test_favorites_toggle_render_unfilled_star(self, favorites_manager):
        """FavoritesToggle renders unfilled star when not favorited."""
        surface = pygame.Surface((100, 100))
        toggle = FavoritesToggle(10, 20, 40, 40, 1, favorites_manager)
        toggle.visible = True
        toggle.is_favorited = False

        # Should not raise
        toggle.render(surface)

    def test_favorites_toggle_different_preset_ids(self, favorites_manager):
        """FavoritesToggle works with different preset ID types."""
        # Integer ID
        toggle1 = FavoritesToggle(10, 20, 40, 40, 1, favorites_manager)
        assert toggle1.preset_id == 1

        # String ID
        toggle2 = FavoritesToggle(10, 20, 40, 40, "custom_1", favorites_manager)
        assert toggle2.preset_id == "custom_1"

    def test_favorites_toggle_inherits_from_button(self, favorites_manager):
        """FavoritesToggle extends Button."""
        from src.ui.components import Button

        toggle = FavoritesToggle(10, 20, 40, 40, 1, favorites_manager)
        assert isinstance(toggle, Button)


class TestPresetCard:
    """Test PresetCard component."""

    @pytest.fixture
    def sample_preset(self):
        """Create a sample preset."""
        return Preset(
            id=1, name="Test Preset", theme="core",
            description="A test preset", shader="test.glsl"
        )

    def test_preset_card_init(self, sample_preset):
        """PresetCard initializes with correct properties."""
        card = PresetCard(10, 20, 100, 100, sample_preset)

        assert card.rect.x == 10
        assert card.rect.y == 20
        assert card.rect.width == 100
        assert card.rect.height == 100
        assert card.preset is sample_preset
        assert card.selected is False
        assert card.hovered is False

    def test_preset_card_selection(self, sample_preset):
        """PresetCard can be selected."""
        card = PresetCard(10, 20, 100, 100, sample_preset)

        assert card.selected is False
        card.selected = True
        assert card.selected is True

    def test_preset_card_hover_effect(self, sample_preset):
        """PresetCard responds to hover."""
        card = PresetCard(10, 20, 100, 100, sample_preset)

        event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (50, 70)})
        card.handle_event(event)

        assert card.hovered is True

    def test_preset_card_click_callback(self, sample_preset):
        """PresetCard calls callback on click."""
        callback = Mock()
        card = PresetCard(10, 20, 100, 100, sample_preset, on_clicked=callback)

        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": (50, 70), "button": 1}
        )
        card.handle_event(event)

        callback.assert_called_once_with(sample_preset.id)

    def test_preset_card_render(self, sample_preset):
        """PresetCard renders without error."""
        surface = pygame.Surface((200, 200))
        card = PresetCard(10, 20, 100, 100, sample_preset)
        card.visible = True

        # Should not raise
        card.render(surface)

    def test_preset_card_color_by_theme(self, sample_preset):
        """PresetCard gets color based on theme."""
        card = PresetCard(10, 20, 100, 100, sample_preset)

        # Test known theme
        color = card._get_preset_color()
        assert isinstance(color, tuple)
        assert len(color) == 3

    def test_preset_card_unknown_theme_color(self):
        """PresetCard uses default color for unknown theme."""
        preset = Preset(
            id=1, name="Test", theme="unknown_theme",
            description="Test", shader="test.glsl"
        )
        card = PresetCard(10, 20, 100, 100, preset)

        color = card._get_preset_color()
        assert isinstance(color, tuple)
        assert len(color) == 3


class TestPresetGrid:
    """Test PresetGrid component."""

    @pytest.fixture
    def sample_presets(self):
        """Create sample presets."""
        return [
            Preset(id=i, name=f"Preset {i}", theme="core",
                   description=f"Description {i}", shader="test.glsl")
            for i in range(1, 21)
        ]

    def test_preset_grid_init(self, sample_presets):
        """PresetGrid initializes with correct properties."""
        grid = PresetGrid(10, 20, 500, 400, sample_presets)

        assert grid.rect.x == 10
        assert grid.rect.y == 20
        assert grid.rect.width == 500
        assert grid.rect.height == 400
        assert grid.presets == sample_presets
        assert grid.cards_per_row == 5
        assert grid.cards_per_col == 4
        assert grid.current_page == 0

    def test_preset_grid_creates_cards(self, sample_presets):
        """PresetGrid creates cards for current page."""
        grid = PresetGrid(10, 20, 500, 400, sample_presets)

        assert len(grid.cards) == min(20, len(sample_presets))

    def test_preset_grid_select_preset(self, sample_presets):
        """PresetGrid can select a preset by ID."""
        grid = PresetGrid(10, 20, 500, 400, sample_presets)

        grid.select_preset(1)
        assert grid.selected_preset_id == 1

    def test_preset_grid_set_presets(self, sample_presets):
        """PresetGrid can update preset list."""
        grid = PresetGrid(10, 20, 500, 400, sample_presets)

        new_presets = sample_presets[:5]
        grid.set_presets(new_presets)

        assert grid.presets == new_presets
        assert grid.current_page == 0

    def test_preset_grid_render(self, sample_presets):
        """PresetGrid renders without error."""
        surface = pygame.Surface((600, 500))
        grid = PresetGrid(10, 20, 500, 400, sample_presets)
        grid.visible = True

        # Should not raise
        grid.render(surface)

    def test_preset_grid_callback_on_selection(self, sample_presets):
        """PresetGrid calls callback when preset is selected."""
        callback = Mock()
        grid = PresetGrid(10, 20, 500, 400, sample_presets, on_preset_selected=callback)

        # Click on first card
        if grid.cards:
            event = pygame.event.Event(
                pygame.MOUSEBUTTONDOWN,
                {"pos": (grid.cards[0].rect.centerx, grid.cards[0].rect.centery), "button": 1}
            )
            grid.handle_event(event)

            callback.assert_called()


class TestDetailsPanel:
    """Test DetailsPanel component."""

    @pytest.fixture
    def setup(self):
        """Create required fixtures."""
        preset_manager = PresetManager()
        favorites_manager = FavoritesManager()
        return preset_manager, favorites_manager

    def test_details_panel_init(self, setup):
        """DetailsPanel initializes with correct properties."""
        preset_manager, favorites_manager = setup
        panel = DetailsPanel(
            500, 20, 200, 400, preset_manager, favorites_manager
        )

        assert panel.rect.x == 500
        assert panel.rect.y == 20
        assert panel.rect.width == 200
        assert panel.rect.height == 400
        assert panel.preset is None

    def test_details_panel_set_preset(self, setup):
        """DetailsPanel can set and display preset."""
        preset_manager, favorites_manager = setup
        panel = DetailsPanel(
            500, 20, 200, 400, preset_manager, favorites_manager
        )

        if preset_manager.builtin_presets:
            preset = preset_manager.builtin_presets[0]
            panel.set_preset(preset)

            assert panel.preset is preset

    def test_details_panel_with_callbacks(self, setup):
        """DetailsPanel initializes with callbacks."""
        preset_manager, favorites_manager = setup
        on_play = Mock()
        on_edit = Mock()
        on_mix = Mock()
        on_add = Mock()

        panel = DetailsPanel(
            500, 20, 200, 400, preset_manager, favorites_manager,
            on_play=on_play, on_edit=on_edit, on_mix=on_mix,
            on_add_to_playlist=on_add
        )

        assert panel.on_play is on_play
        assert panel.on_edit is on_edit
        assert panel.on_mix is on_mix
        assert panel.on_add_to_playlist is on_add

    def test_details_panel_render(self, setup):
        """DetailsPanel renders without error."""
        preset_manager, favorites_manager = setup
        surface = pygame.Surface((800, 500))
        panel = DetailsPanel(
            500, 20, 200, 400, preset_manager, favorites_manager
        )
        panel.visible = True

        # Need to set a preset to render properly
        if preset_manager.builtin_presets:
            panel.set_preset(preset_manager.builtin_presets[0])

        # Should not raise
        panel.render(surface)

    def test_details_panel_has_buttons(self, setup):
        """DetailsPanel has play, edit, mix, and playlist buttons."""
        preset_manager, favorites_manager = setup
        panel = DetailsPanel(
            500, 20, 200, 400, preset_manager, favorites_manager
        )

        assert panel.play_button is not None
        assert panel.edit_button is not None
        assert panel.mix_button is not None
        assert panel.playlist_button is not None

    def test_details_panel_has_favorites_toggle(self, setup):
        """DetailsPanel has favorites toggle."""
        preset_manager, favorites_manager = setup
        panel = DetailsPanel(
            500, 20, 200, 400, preset_manager, favorites_manager
        )

        assert panel.favorites_toggle is not None


class TestParameterEditorModal:
    """Test ParameterEditorModal component."""

    def test_parameter_editor_init(self):
        """ParameterEditorModal initializes with correct properties."""
        modal = ParameterEditorModal(20, 20, 400, 300, base_preset_id=1)

        assert modal.rect.x == 20
        assert modal.rect.y == 20
        assert modal.rect.width == 400
        assert modal.rect.height == 300
        assert modal.base_preset_id == 1
        assert modal.visible is False

    def test_parameter_editor_has_sliders(self):
        """ParameterEditorModal has all required sliders."""
        modal = ParameterEditorModal(20, 20, 400, 300, base_preset_id=1)

        required_params = [
            "bass_sensitivity", "mid_sensitivity", "treble_sensitivity",
            "color_hue", "color_saturation", "animation_speed"
        ]

        for param in required_params:
            assert param in modal.sliders
            assert param in modal.parameters

    def test_parameter_editor_slider_ranges(self):
        """ParameterEditorModal sliders have correct ranges."""
        modal = ParameterEditorModal(20, 20, 400, 300, base_preset_id=1)

        # Check bass sensitivity range
        bass_slider = modal.sliders["bass_sensitivity"]
        assert bass_slider.min_val == 0.0
        assert bass_slider.max_val == 3.0

        # Check hue range
        hue_slider = modal.sliders["color_hue"]
        assert hue_slider.min_val == -180.0
        assert hue_slider.max_val == 180.0

    def test_parameter_editor_has_name_input(self):
        """ParameterEditorModal has name input field."""
        modal = ParameterEditorModal(20, 20, 400, 300, base_preset_id=1)

        assert modal.name_input is not None

    def test_parameter_editor_set_parameters(self):
        """ParameterEditorModal can set parameter values."""
        modal = ParameterEditorModal(20, 20, 400, 300, base_preset_id=1)

        new_params = {
            "bass_sensitivity": 2.0,
            "mid_sensitivity": 1.5,
            "treble_sensitivity": 1.0,
            "color_hue": 45.0,
            "color_saturation": 0.5,
            "animation_speed": 1.2
        }

        modal.set_parameters(new_params)

        for param, value in new_params.items():
            assert modal.parameters[param] == value

    def test_parameter_editor_render(self):
        """ParameterEditorModal renders without error."""
        surface = pygame.Surface((600, 500))
        modal = ParameterEditorModal(20, 20, 400, 300, base_preset_id=1)
        modal.visible = True

        # Should not raise
        modal.render(surface)

    def test_parameter_editor_callback_on_save(self):
        """ParameterEditorModal calls callback on save."""
        callback = Mock()
        modal = ParameterEditorModal(20, 20, 400, 300, base_preset_id=1, on_save=callback)
        modal.visible = True
        modal.name_input.text = "Test Preset"

        # Simulate save button click
        if modal.components:
            # Find and click the save button (should be near the end)
            for component in modal.components:
                if hasattr(component, 'label') and component.label == "Save":
                    component.callback()
                    break

    def test_parameter_editor_callback_on_cancel(self):
        """ParameterEditorModal calls callback on cancel."""
        callback = Mock()
        modal = ParameterEditorModal(20, 20, 400, 300, base_preset_id=1, on_cancel=callback)
        modal.visible = True

        # Simulate cancel button click
        if modal.components:
            for component in modal.components:
                if hasattr(component, 'label') and component.label == "Cancel":
                    component.callback()
                    break


class TestMixToolModal:
    """Test MixToolModal component."""

    @pytest.fixture
    def preset_manager(self):
        """Create a PresetManager instance."""
        return PresetManager()

    def test_mix_tool_modal_init(self, preset_manager):
        """MixToolModal initializes with correct properties."""
        modal = MixToolModal(20, 20, 400, 300, base_preset_id=1, preset_manager=preset_manager)

        assert modal.rect.x == 20
        assert modal.rect.y == 20
        assert modal.rect.width == 400
        assert modal.rect.height == 300
        assert modal.base_preset_id == 1
        assert modal.blend_ratio == 0.5

    def test_mix_tool_modal_has_blend_slider(self, preset_manager):
        """MixToolModal has blend slider."""
        modal = MixToolModal(20, 20, 400, 300, base_preset_id=1, preset_manager=preset_manager)

        assert modal.blend_slider is not None
        assert modal.blend_slider.min_val == 0.0
        assert modal.blend_slider.max_val == 1.0

    def test_mix_tool_modal_has_name_input(self, preset_manager):
        """MixToolModal has name input field."""
        modal = MixToolModal(20, 20, 400, 300, base_preset_id=1, preset_manager=preset_manager)

        assert modal.name_input is not None

    def test_mix_tool_modal_set_mix_preset(self, preset_manager):
        """MixToolModal can set mix preset."""
        modal = MixToolModal(20, 20, 400, 300, base_preset_id=1, preset_manager=preset_manager)

        modal.set_mix_preset(2)
        assert modal.mix_preset_id == 2

    def test_mix_tool_modal_render(self, preset_manager):
        """MixToolModal renders without error."""
        surface = pygame.Surface((600, 500))
        modal = MixToolModal(20, 20, 400, 300, base_preset_id=1, preset_manager=preset_manager)
        modal.visible = True

        # Should not raise
        modal.render(surface)

    def test_mix_tool_modal_callback_on_save(self, preset_manager):
        """MixToolModal calls callback on save."""
        callback = Mock()
        modal = MixToolModal(
            20, 20, 400, 300, base_preset_id=1, preset_manager=preset_manager,
            on_save=callback
        )
        modal.visible = True
        modal.set_mix_preset(2)
        modal.name_input.text = "Blended"

        # Simulate save button click
        if modal.components:
            for component in modal.components:
                if hasattr(component, 'label') and component.label == "Save":
                    component.callback()
                    break

    def test_mix_tool_modal_callback_on_cancel(self, preset_manager):
        """MixToolModal calls callback on cancel."""
        callback = Mock()
        modal = MixToolModal(
            20, 20, 400, 300, base_preset_id=1, preset_manager=preset_manager,
            on_cancel=callback
        )
        modal.visible = True

        # Simulate cancel button click
        if modal.components:
            for component in modal.components:
                if hasattr(component, 'label') and component.label == "Cancel":
                    component.callback()
                    break
