"""Tests for the menu system integration."""

import pytest
import pygame
from unittest.mock import MagicMock, Mock

from src.ui.menu_system import MenuSystem
from src.ui.presets_data import PresetManager
from src.ui.models import FavoritesManager

# Initialize pygame for testing
pygame.init()


class TestMenuSystem:
    """Test MenuSystem integration component."""

    @pytest.fixture
    def setup(self):
        """Create required fixtures."""
        preset_manager = PresetManager()
        favorites_manager = FavoritesManager()
        return preset_manager, favorites_manager

    def test_menu_system_init(self, setup):
        """MenuSystem initializes with correct properties."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )

        assert menu.rect.x == 0
        assert menu.rect.y == 0
        assert menu.rect.width == 1000
        assert menu.rect.height == 600
        assert menu.preset_manager is preset_manager
        assert menu.favorites_manager is favorites_manager
        assert menu.visible is False

    def test_menu_system_has_all_components(self, setup):
        """MenuSystem contains all required components."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )

        assert menu.search_bar is not None
        assert menu.category_filter is not None
        assert menu.preset_grid is not None
        assert menu.details_panel is not None
        assert menu.parameter_editor_modal is not None
        assert menu.mix_tool_modal is not None

    def test_menu_system_toggle_visibility(self, setup):
        """MenuSystem can toggle visibility."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )

        assert menu.visible is False
        menu.toggle()
        assert menu.visible is True
        menu.toggle()
        assert menu.visible is False

    def test_menu_system_render_when_visible(self, setup):
        """MenuSystem renders when visible."""
        preset_manager, favorites_manager = setup
        surface = pygame.Surface((1200, 700))
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )
        menu.visible = True

        # Should not raise
        menu.render(surface)

    def test_menu_system_does_not_render_when_hidden(self, setup):
        """MenuSystem doesn't render when hidden."""
        preset_manager, favorites_manager = setup
        surface = pygame.Surface((1200, 700))
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )
        menu.visible = False

        # Should not raise, should just return early
        menu.render(surface)

    def test_menu_system_handles_escape_key(self, setup):
        """MenuSystem closes on Escape key."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )
        menu.visible = True

        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
        menu.handle_event(event)

        assert menu.visible is False

    def test_menu_system_search_results_callback(self, setup):
        """MenuSystem handles search results changes."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )

        # Trigger search with some results
        initial_preset_count = len(menu.preset_grid.presets)

        # Search should filter results
        menu.search_bar._text = "test"
        menu.search_bar._perform_search()

        # Grid should be updated
        assert len(menu.preset_grid.presets) <= initial_preset_count

    def test_menu_system_category_filter_callback(self, setup):
        """MenuSystem handles category filter changes."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )

        themes = preset_manager.get_all_themes()
        if themes:
            theme = themes[0]
            menu._on_category_changed(theme)

            # Grid should be updated with filtered presets
            assert menu.preset_grid.presets is not None

    def test_menu_system_preset_selection_callback(self, setup):
        """MenuSystem handles preset selection."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )

        if preset_manager.builtin_presets:
            preset_id = preset_manager.builtin_presets[0].id
            menu._on_preset_selected(preset_id)

            assert menu.preset_grid.selected_preset_id == preset_id
            assert menu.details_panel.preset is not None

    def test_menu_system_edit_preset_opens_modal(self, setup):
        """MenuSystem opens parameter editor on edit."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )

        menu._on_edit_preset(1)

        assert menu.parameter_editor_modal.visible is True
        assert menu.parameter_editor_modal.base_preset_id == 1

    def test_menu_system_mix_preset_opens_modal(self, setup):
        """MenuSystem opens mix tool on mix."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )

        menu._on_mix_presets(1)

        assert menu.mix_tool_modal.visible is True
        assert menu.mix_tool_modal.base_preset_id == 1

    def test_menu_system_play_preset_closes_menu(self, setup):
        """MenuSystem closes menu when playing preset."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )
        menu.visible = True

        menu._on_play_preset(1)

        assert menu.visible is False

    def test_menu_system_with_external_callbacks(self, setup):
        """MenuSystem calls external callbacks."""
        preset_manager, favorites_manager = setup
        on_preset_selected = Mock()
        on_custom_preset_saved = Mock()

        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager,
            on_preset_selected=on_preset_selected,
            on_custom_preset_saved=on_custom_preset_saved
        )

        if preset_manager.builtin_presets:
            preset_id = preset_manager.builtin_presets[0].id
            menu._on_preset_selected(preset_id)

            on_preset_selected.assert_called_once_with(preset_id)

    def test_menu_system_add_to_playlist(self, setup):
        """MenuSystem handles add to playlist."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )

        # Should not raise
        menu._on_add_to_playlist(1)

    def test_menu_system_modal_cancellation(self, setup):
        """MenuSystem closes modals on cancel."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )

        menu.parameter_editor_modal.visible = True
        menu.mix_tool_modal.visible = True

        menu._on_modal_cancelled()

        assert menu.parameter_editor_modal.visible is False
        assert menu.mix_tool_modal.visible is False

    def test_menu_system_inherits_from_uicomponent(self, setup):
        """MenuSystem extends UIComponent."""
        from src.ui.components import UIComponent

        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )

        assert isinstance(menu, UIComponent)

    def test_menu_system_parameter_save_creates_custom_preset(self, setup):
        """MenuSystem creates custom preset on parameter save."""
        preset_manager, favorites_manager = setup
        on_custom_preset_saved = Mock()

        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager,
            on_custom_preset_saved=on_custom_preset_saved
        )

        menu._on_parameters_saved("My Custom", {"bass_sensitivity": 2.0})

        # Custom preset should be created and callback called
        assert on_custom_preset_saved.called

    def test_menu_system_blend_save_creates_blended_preset(self, setup):
        """MenuSystem creates blended preset on mix save."""
        preset_manager, favorites_manager = setup
        on_custom_preset_saved = Mock()

        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager,
            on_custom_preset_saved=on_custom_preset_saved
        )

        menu._on_blend_saved(1, 2, 0.5, "Blended")

        # Custom preset should be created and callback called
        assert on_custom_preset_saved.called

    def test_menu_system_current_filtered_presets(self, setup):
        """MenuSystem tracks current filtered presets."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )

        # Initially should have all presets
        assert len(menu.current_filtered_presets) > 0
        assert menu.current_filtered_presets == preset_manager.builtin_presets

    def test_menu_system_event_handling(self, setup):
        """MenuSystem handles events when visible."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )
        menu.visible = True

        # Should not raise
        event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (100, 100)})
        menu.handle_event(event)

    def test_menu_system_ignores_events_when_hidden(self, setup):
        """MenuSystem ignores events when not visible."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )
        menu.visible = False

        # Should not raise, should just return early
        event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (100, 100)})
        menu.handle_event(event)

    def test_menu_system_all_category_filters(self, setup):
        """MenuSystem handles 'All' category filter."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )

        menu._on_category_changed("All")

        # Should show all presets
        assert len(menu.preset_grid.presets) == len(preset_manager.builtin_presets)

    def test_menu_system_specific_theme_filter(self, setup):
        """MenuSystem filters by specific theme."""
        preset_manager, favorites_manager = setup
        menu = MenuSystem(
            0, 0, 1000, 600, preset_manager, favorites_manager
        )

        themes = preset_manager.get_all_themes()
        if themes:
            theme = themes[0]
            expected_count = len(preset_manager.filter_by_theme(theme))
            menu._on_category_changed(theme)

            # Grid should have the correct number of filtered presets
            assert len(menu.preset_grid.presets) == expected_count
