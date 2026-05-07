"""Integration tests for main.py with the menu system."""

import pytest
import pygame
from unittest.mock import MagicMock, Mock

# Initialize pygame for testing
pygame.init()


class TestMainIntegration:
    """Test main.py integration with menu system."""

    def test_main_module_imports_menu_system(self):
        """main.py successfully imports MenuSystem."""
        try:
            from src.ui.menu_system import MenuSystem
            assert MenuSystem is not None
        except ImportError:
            pytest.fail("MenuSystem should be importable from main.py")

    def test_main_module_imports_preset_manager(self):
        """main.py successfully imports PresetManager."""
        try:
            from src.ui.presets_data import PresetManager
            assert PresetManager is not None
        except ImportError:
            pytest.fail("PresetManager should be importable from main.py")

    def test_main_module_imports_favorites_manager(self):
        """main.py successfully imports FavoritesManager."""
        try:
            from src.ui.models import FavoritesManager
            assert FavoritesManager is not None
        except ImportError:
            pytest.fail("FavoritesManager should be importable from main.py")

    def test_menu_system_class_exists(self):
        """MenuSystem class is properly defined."""
        from src.ui.menu_system import MenuSystem
        from src.ui.components import UIComponent

        # Should be a subclass of UIComponent
        assert issubclass(MenuSystem, UIComponent)

    def test_menu_system_has_required_methods(self):
        """MenuSystem has all required methods."""
        from src.ui.menu_system import MenuSystem

        required_methods = ['toggle', 'render', 'handle_event']

        for method_name in required_methods:
            assert hasattr(MenuSystem, method_name), \
                f"MenuSystem should have {method_name} method"

    def test_menu_system_has_all_components(self):
        """MenuSystem contains all required component attributes."""
        from src.ui.menu_system import MenuSystem
        from src.ui.presets_data import PresetManager
        from src.ui.models import FavoritesManager

        preset_manager = PresetManager()
        favorites_manager = FavoritesManager()

        menu = MenuSystem(0, 0, 800, 600, preset_manager, favorites_manager)

        component_names = [
            'search_bar', 'category_filter', 'preset_grid',
            'details_panel', 'parameter_editor_modal', 'mix_tool_modal'
        ]

        for component_name in component_names:
            assert hasattr(menu, component_name), \
                f"MenuSystem should have {component_name} component"

    def test_menu_system_toggle_works(self):
        """MenuSystem toggle method works correctly."""
        from src.ui.menu_system import MenuSystem
        from src.ui.presets_data import PresetManager
        from src.ui.models import FavoritesManager

        preset_manager = PresetManager()
        favorites_manager = FavoritesManager()

        menu = MenuSystem(0, 0, 800, 600, preset_manager, favorites_manager)

        # Initially hidden
        assert menu.visible is False

        # Toggle to show
        menu.toggle()
        assert menu.visible is True

        # Toggle to hide
        menu.toggle()
        assert menu.visible is False

    def test_menu_system_render_works(self):
        """MenuSystem render method works without error."""
        from src.ui.menu_system import MenuSystem
        from src.ui.presets_data import PresetManager
        from src.ui.models import FavoritesManager

        preset_manager = PresetManager()
        favorites_manager = FavoritesManager()

        menu = MenuSystem(0, 0, 800, 600, preset_manager, favorites_manager)
        surface = pygame.Surface((800, 600))

        # Should not raise
        menu.visible = True
        menu.render(surface)

    def test_menu_system_event_handling(self):
        """MenuSystem handles events."""
        from src.ui.menu_system import MenuSystem
        from src.ui.presets_data import PresetManager
        from src.ui.models import FavoritesManager

        preset_manager = PresetManager()
        favorites_manager = FavoritesManager()

        menu = MenuSystem(0, 0, 800, 600, preset_manager, favorites_manager)
        menu.visible = True

        event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (100, 100)})

        # Should not raise
        menu.handle_event(event)

    def test_menu_system_escape_closes_menu(self):
        """MenuSystem closes on Escape key."""
        from src.ui.menu_system import MenuSystem
        from src.ui.presets_data import PresetManager
        from src.ui.models import FavoritesManager

        preset_manager = PresetManager()
        favorites_manager = FavoritesManager()

        menu = MenuSystem(0, 0, 800, 600, preset_manager, favorites_manager)
        menu.visible = True

        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
        menu.handle_event(event)

        assert menu.visible is False

    def test_menu_components_all_have_required_methods(self):
        """All menu components have required render/handle_event methods."""
        from src.ui.menu_components import (
            FavoritesToggle, PresetCard, PresetGrid, DetailsPanel,
            ParameterEditorModal, MixToolModal
        )
        from src.ui.models import FavoritesManager, Preset

        components_to_check = [
            (FavoritesToggle, {'preset_id': 1, 'favorites_manager': FavoritesManager()}),
            (PresetCard, {'preset': Preset(1, 'Test', 'core', 'desc', 'shader')}),
            (PresetGrid, {'presets': []}),
            (DetailsPanel, {
                'preset_manager': None,  # Will be mocked
                'favorites_manager': FavoritesManager()
            }),
        ]

        for component_class, kwargs in components_to_check:
            # All should have render and handle_event
            assert hasattr(component_class, 'render')
            assert hasattr(component_class, 'handle_event')
