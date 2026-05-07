"""Main menu system for preset management and visualization control.

Integrates all menu components (SearchBar, CategoryFilter, PresetGrid,
DetailsPanel, and modals) into a cohesive menu system that can be
toggled on/off and handles all user interactions.
"""

import pygame
import logging
from typing import List, Optional, Callable

from src.ui.components import UIComponent
from src.ui.menu_components import (
    SearchBar, CategoryFilter, FavoritesToggle, PresetGrid, DetailsPanel,
    ParameterEditorModal, MixToolModal
)
from src.ui.presets_data import PresetManager
from src.ui.models import Preset, CustomPreset, FavoritesManager
from src.ui.text_renderer import TextRenderer

logger = logging.getLogger(__name__)


class MenuSystem(UIComponent):
    """Main menu system containing all components and managing interactions.

    Integrates all UI components (search, filter, grid, details panel, modals)
    into a cohesive system. Handles visibility toggling, event dispatch, and
    communication between components.

    Attributes:
        preset_manager: PresetManager instance
        favorites_manager: FavoritesManager instance
        search_bar: SearchBar component for searching presets
        category_filter: CategoryFilter dropdown for filtering by theme
        preset_grid: PresetGrid displaying available presets
        details_panel: DetailsPanel showing selected preset info
        parameter_editor_modal: Modal for editing parameters
        mix_tool_modal: Modal for mixing presets
        current_filtered_presets: Currently displayed presets (after search/filter)
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        preset_manager: PresetManager,
        favorites_manager: FavoritesManager,
        on_preset_selected: Optional[Callable[[int], None]] = None,
        on_custom_preset_saved: Optional[Callable[[CustomPreset], None]] = None,
    ):
        """Initialize menu system.

        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            width: Width in pixels
            height: Height in pixels
            preset_manager: PresetManager instance
            favorites_manager: FavoritesManager instance
            on_preset_selected: Optional callback when preset is selected
            on_custom_preset_saved: Optional callback when custom preset is saved

        Raises:
            No exceptions - handles all initialization gracefully
        """
        super().__init__(x, y, width, height)
        self.visible = False  # Menu is hidden by default
        self.preset_manager = preset_manager
        self.favorites_manager = favorites_manager
        self.on_preset_selected = on_preset_selected
        self.on_custom_preset_saved = on_custom_preset_saved

        # Initialize text renderer for menu components
        self.text_renderer = TextRenderer()

        # Initialize filtered presets
        self.current_filtered_presets = preset_manager.builtin_presets.copy()

        # Create PresetGrid at top
        grid_y = y + 10
        grid_height = height - 150  # Leave space for search/filter bar at bottom
        self.preset_grid = PresetGrid(
            x + 10, grid_y, width - 230, grid_height,
            presets=self.current_filtered_presets,
            cards_per_row=5,
            cards_per_col=4,
            on_preset_selected=self._on_preset_selected
        )

        # Create DetailsPanel on the right side of grid
        details_x = x + 10 + width - 230 + 10
        self.details_panel = DetailsPanel(
            details_x, grid_y, 200, grid_height,
            preset_manager=preset_manager,
            favorites_manager=favorites_manager,
            on_play=self._on_play_preset,
            on_edit=self._on_edit_preset,
            on_mix=self._on_mix_presets,
            on_add_to_playlist=self._on_add_to_playlist
        )

        # Create SearchBar at bottom
        search_y = y + height - 130
        self.search_bar = SearchBar(
            x + 10, search_y, width - 180, 40,
            preset_manager=preset_manager,
            on_search_changed=self._on_search_results_changed
        )

        # Create CategoryFilter next to SearchBar
        self.category_filter = CategoryFilter(
            x + width - 160, search_y, 150, 40,
            preset_manager=preset_manager,
            text_renderer=self.text_renderer,
            on_category_changed=self._on_category_changed
        )

        # Create ParameterEditorModal
        modal_width = width - 40
        modal_height = height - 40
        modal_x = x + 20
        modal_y = y + 20
        self.parameter_editor_modal = ParameterEditorModal(
            modal_x, modal_y, modal_width, modal_height,
            base_preset_id=0,
            on_save=self._on_parameters_saved,
            on_cancel=self._on_modal_cancelled
        )

        # Create MixToolModal
        self.mix_tool_modal = MixToolModal(
            modal_x, modal_y, modal_width, modal_height,
            base_preset_id=0,
            preset_manager=preset_manager,
            on_save=self._on_blend_saved,
            on_cancel=self._on_modal_cancelled
        )

        # Component list for rendering and event handling
        self.components = [
            self.search_bar, self.category_filter, self.preset_grid,
            self.details_panel, self.parameter_editor_modal, self.mix_tool_modal
        ]

        # Focus tracking for keyboard navigation
        self.focused_component_idx = 0  # Start with search bar

    def toggle(self) -> None:
        """Toggle menu visibility.

        Shows the menu if it's hidden, hides if visible.
        """
        try:
            self.visible = not self.visible
            if self.visible:
                logger.info("Menu system opened")
            else:
                logger.info("Menu system closed")
        except Exception as e:
            logger.error(f"MenuSystem toggle failed: {e}")

    def render(self, surface: pygame.Surface) -> None:
        """Render all visible components.

        Args:
            surface: pygame.Surface to render to
        """
        if not self.visible:
            return

        try:
            # Draw semi-transparent background (40% opacity)
            overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 50))  # Lower alpha for more transparency
            surface.blit(overlay, (0, 0))

            # Render menu container background (semi-transparent)
            menu_bg = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            menu_bg.fill((20, 30, 50, 180))  # 70% opacity menu background
            surface.blit(menu_bg, (self.rect.x, self.rect.y))
            pygame.draw.rect(surface, (80, 100, 150), self.rect, 3)

 # Render component labels
            try:
                # Search label (at bottom)
                search_label_y = self.rect.y + self.rect.height - 130
                search_surf, search_rect = self.text_renderer.render(
                    "Search:", (180, 180, 200), size='small'
                )
                surface.blit(search_surf, (self.rect.x + 10, search_label_y - 25))

                # Category label (at bottom right)
                category_surf, category_rect = self.text_renderer.render(
                    "Category:", (180, 180, 200), size='small'
                )
                surface.blit(category_surf, (self.rect.x + self.rect.width - 160, search_label_y - 25))
            except Exception as e:
                pass

            # Render all components
            for component in self.components:
                if component.visible:
                    component.render(surface)

        except Exception as e:
            logger.error(f"MenuSystem render failed: {e}")

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events for all components.

        Args:
            event: pygame.event.Event to handle
        """
        if not self.visible:
            return

        try:
            # Check for close key (Esc)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.toggle()
                    return

                # Tab to navigate between components
                elif event.key == pygame.K_TAB:
                    if event.mod & pygame.KMOD_SHIFT:
                        # Shift+Tab - go backwards
                        self.focused_component_idx = (self.focused_component_idx - 1) % len(self.components)
                    else:
                        # Tab - go forwards
                        self.focused_component_idx = (self.focused_component_idx + 1) % len(self.components)
                    return

                # Arrow keys for preset grid navigation
                elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    # Route arrow keys to PresetGrid
                    if self.preset_grid.visible:
                        self.preset_grid.handle_event(event)
                    return

                # Enter to select preset from grid
                elif event.key == pygame.K_RETURN:
                    if self.preset_grid.visible and self.preset_grid.selected_preset_id is not None:
                        self._on_preset_selected(self.preset_grid.selected_preset_id)
                    return

            # Pass events to all components
            for component in self.components:
                if component.visible:
                    component.handle_event(event)

        except Exception as e:
            logger.error(f"MenuSystem event handling failed: {e}")

    def _on_search_results_changed(self, results: List[Preset]) -> None:
        """Handle search results update.

        Args:
            results: List of Preset objects matching search query
        """
        try:
            self.current_filtered_presets = results
            self.preset_grid.set_presets(results)
        except Exception as e:
            logger.error(f"MenuSystem search results handler failed: {e}")

    def _on_category_changed(self, category: str) -> None:
        """Handle category filter change.

        Args:
            category: Selected category name
        """
        try:
            if category == "All":
                self.current_filtered_presets = self.preset_manager.builtin_presets.copy()
            else:
                self.current_filtered_presets = self.preset_manager.filter_by_theme(category)

            # Set search scope for the search bar
            self.search_bar.search_scope = self.current_filtered_presets

            # Update search with current filter
            if self.search_bar.text.strip():
                self.search_bar._perform_search(self.current_filtered_presets)
            else:
                self.preset_grid.set_presets(self.current_filtered_presets)

        except Exception as e:
            logger.error(f"MenuSystem category change handler failed: {e}")

    def _on_preset_selected(self, preset_id: int) -> None:
        """Handle preset selection from grid.

        Args:
            preset_id: ID of selected preset
        """
        try:
            # Find the preset
            preset = None
            for p in self.preset_manager.builtin_presets:
                if p.id == preset_id:
                    preset = p
                    break

            if preset:
                self.details_panel.set_preset(preset)
                self.preset_grid.select_preset(preset_id)

                # Call external callback
                if self.on_preset_selected:
                    self.on_preset_selected(preset_id)

        except Exception as e:
            logger.error(f"MenuSystem preset selection handler failed: {e}")

    def _on_play_preset(self, preset_id: int) -> None:
        """Handle play button click.

        Args:
            preset_id: ID of preset to play
        """
        try:
            if self.on_preset_selected:
                self.on_preset_selected(preset_id)
            self.toggle()
        except Exception as e:
            logger.error(f"MenuSystem play handler failed: {e}")

    def _on_edit_preset(self, preset_id: int) -> None:
        """Handle edit button click - opens parameter editor modal.

        Args:
            preset_id: ID of preset to edit
        """
        try:
            self.parameter_editor_modal.base_preset_id = preset_id
            self.parameter_editor_modal.visible = True
        except Exception as e:
            logger.error(f"MenuSystem edit handler failed: {e}")

    def _on_mix_presets(self, preset_id: int) -> None:
        """Handle mix button click - opens mix tool modal.

        Args:
            preset_id: ID of base preset to mix
        """
        try:
            self.mix_tool_modal.base_preset_id = preset_id
            self.mix_tool_modal.visible = True
        except Exception as e:
            logger.error(f"MenuSystem mix handler failed: {e}")

    def _on_add_to_playlist(self, preset_id: int) -> None:
        """Handle add to playlist button click.

        Args:
            preset_id: ID of preset to add
        """
        try:
            logger.info(f"Add preset {preset_id} to playlist")
            # This would integrate with playlist manager
        except Exception as e:
            logger.error(f"MenuSystem add to playlist handler failed: {e}")

    def _on_parameters_saved(self, name: str, parameters: dict) -> None:
        """Handle parameter editor save.

        Args:
            name: Name of custom preset
            parameters: Dictionary of parameter values
        """
        try:
            if not name:
                name = f"Custom Preset {len(self.preset_manager.custom_presets) + 1}"

            # Create custom preset
            custom_preset = CustomPreset(
                id=f"custom_{len(self.preset_manager.custom_presets) + 1}",
                name=name,
                base_preset=self.parameter_editor_modal.base_preset_id,
                parameters=parameters
            )

            # Save to manager
            self.preset_manager.custom_presets[custom_preset.id] = custom_preset
            self.preset_manager.save_custom_preset(custom_preset)

            # Call callback
            if self.on_custom_preset_saved:
                self.on_custom_preset_saved(custom_preset)

        except Exception as e:
            logger.error(f"MenuSystem parameters save handler failed: {e}")

    def _on_blend_saved(self, base_id: int, mix_id: int, blend_ratio: float, name: str) -> None:
        """Handle mix tool save.

        Args:
            base_id: ID of base preset
            mix_id: ID of preset to mix with
            blend_ratio: Blend ratio (0.0 to 1.0)
            name: Name of blended preset
        """
        try:
            if not name:
                name = f"Blended Preset {len(self.preset_manager.custom_presets) + 1}"

            # Create blended custom preset
            custom_preset = CustomPreset(
                id=f"custom_{len(self.preset_manager.custom_presets) + 1}",
                name=name,
                base_preset=base_id,
                mix_preset=mix_id,
                parameters={"blend_ratio": blend_ratio}
            )

            # Save to manager
            self.preset_manager.custom_presets[custom_preset.id] = custom_preset
            self.preset_manager.save_custom_preset(custom_preset)

            # Call callback
            if self.on_custom_preset_saved:
                self.on_custom_preset_saved(custom_preset)

        except Exception as e:
            logger.error(f"MenuSystem blend save handler failed: {e}")

    def _on_modal_cancelled(self) -> None:
        """Handle modal cancellation."""
        try:
            self.parameter_editor_modal.visible = False
            self.mix_tool_modal.visible = False
        except Exception as e:
            logger.error(f"MenuSystem modal cancel handler failed: {e}")
