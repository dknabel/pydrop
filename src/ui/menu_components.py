"""Specialized menu UI components for the preset system.

Provides higher-level UI components built on the base component classes
for use in the menu system, particularly for preset management.
"""

from src.ui.components import UIComponent, TextInput, Button, Slider, Modal
from src.ui.presets_data import PresetManager
from src.ui.models import Preset, CustomPreset, FavoritesManager
from typing import List, Callable, Optional, Tuple, Dict, Union
import pygame
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class SearchBar(TextInput):
    """Text input for searching presets with real-time filtering.

    A specialized TextInput that searches presets as the user types.
    Calls a callback function with filtered results on each keystroke.
    Implements case-insensitive substring matching across preset names,
    descriptions, and tags.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        preset_manager: PresetManager,
        on_search_changed: Optional[Callable[[List[Preset]], None]] = None,
    ):
        """Initialize search bar.

        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            width: Width in pixels
            height: Height in pixels
            preset_manager: PresetManager instance for searching
            on_search_changed: Callback function called with filtered results
                on each search. Called with list of Preset objects.
                Default is None (no callback).

        Raises:
            No exceptions - handles all initialization gracefully
        """
        super().__init__(
            x, y, width, height, placeholder="Search presets...", max_length=100
        )
        self.preset_manager = preset_manager
        self.on_search_changed = on_search_changed
        self.search_results: List[Preset] = []

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle input and trigger search on each event.

        Calls parent handle_event to process keyboard/mouse input,
        then performs search to update results and invoke callback.

        Args:
            event: pygame.event.Event to handle

        Raises:
            No exceptions - logs any errors gracefully
        """
        try:
            super().handle_event(event)
            self._perform_search()
        except Exception as e:
            logger.error(f"SearchBar event handling failed: {e}")

    def _perform_search(self) -> None:
        """Perform search and call callback with results.

        Executes the search using PresetManager.search() and updates
        the search_results. If text is empty, returns all presets.
        Calls the on_search_changed callback with the results.

        Raises:
            No exceptions - logs any errors gracefully
        """
        try:
            if self.text.strip() == "":
                # Empty search returns all presets
                self.search_results = self.preset_manager.builtin_presets.copy()
            else:
                # Search using PresetManager.search()
                self.search_results = self.preset_manager.search(self.text)

            # Call callback with results
            if self.on_search_changed:
                self.on_search_changed(self.search_results)
        except Exception as e:
            logger.error(f"SearchBar search failed: {e}")
            self.search_results = []

    def clear(self) -> None:
        """Clear search text and results.

        Resets the search text to empty string and refreshes search
        results (which will return all presets). Invokes callback with
        the full preset list.

        Raises:
            No exceptions - logs any errors gracefully
        """
        try:
            self._text = ""
            self._perform_search()
        except Exception as e:
            logger.error(f"SearchBar clear failed: {e}")


class CategoryFilter(UIComponent):
    """Dropdown for filtering presets by theme/category.

    A dropdown menu that displays all available themes plus an "All" option
    at the top. Shows the count of presets for each category. Clicking a
    category triggers a callback with the selected category name.
    The "core" theme is always listed first among the themes.

    Attributes:
        preset_manager: PresetManager instance for accessing presets and themes
        opened: Whether the dropdown menu is currently open
        selected_category: Currently selected category name
        categories: Dictionary mapping category names to preset counts
        dropdown_items: List of (label, category, count) tuples for display
        item_height: Height in pixels of each dropdown item
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        preset_manager: PresetManager,
        text_renderer: Optional["TextRenderer"] = None,
        on_category_changed: Optional[Callable[[str], None]] = None,
    ):
        """Initialize category filter dropdown.

        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            width: Width in pixels
            height: Height in pixels
            preset_manager: PresetManager instance for accessing presets
            text_renderer: TextRenderer for rendering text (optional, not used yet)
            on_category_changed: Callback function called with selected category name
                when a category is selected. Default is None (no callback).

        Raises:
            No exceptions - handles all initialization gracefully
        """
        super().__init__(x, y, width, height)
        self.preset_manager = preset_manager
        self.text_renderer = text_renderer
        self.on_category_changed = on_category_changed

        # Dropdown state
        self.opened = False
        self.selected_category = "All"

        # Build categories list with counts
        self.categories = self._build_categories()
        self.dropdown_items = self._build_dropdown_items()

        # Sizing
        self.item_height = 25

    def _build_categories(self) -> Dict[str, int]:
        """Build dictionary of categories with preset counts.

        Creates a mapping of category names to the number of presets
        in each category. Includes "All" which represents all presets
        combined.

        Returns:
            Dictionary mapping category name to preset count
        """
        categories = {}

        # Get all themes from preset manager
        themes = self.preset_manager.get_all_themes()

        for theme in themes:
            count = len(self.preset_manager.filter_by_theme(theme))
            categories[theme] = count

        # Add "All" category with total count
        total_count = len(self.preset_manager.builtin_presets)
        categories["All"] = total_count

        return categories

    def _build_dropdown_items(self) -> List[Tuple[str, str, int]]:
        """Build list of dropdown items: (label, category, count).

        Creates the list of items to display in the dropdown menu.
        "All" is always first, followed by themes sorted alphabetically
        with "core" coming before other themes.

        Returns:
            List of tuples (label, category_name, count) for each item
        """
        items = []

        # Add "All" first
        items.append(("All", "All", self.categories.get("All", 0)))

        # Add all themes sorted, with "core" first
        themes = sorted([k for k in self.categories.keys() if k != "All"])
        if "core" in themes:
            themes.remove("core")
            themes = ["core"] + themes

        for theme in themes:
            count = self.categories.get(theme, 0)
            # Format theme name: replace underscores with spaces and title case
            label = theme.replace("_", " ").title()
            items.append((label, theme, count))

        return items

    def render(self, surface: pygame.Surface) -> None:
        """Render dropdown button and menu if open.

        Args:
            surface: pygame.Surface to render to
        """
        if not self.visible:
            return

        # Draw main button background
        button_color = (80, 120, 200) if self.opened else (60, 100, 180)
        pygame.draw.rect(surface, button_color, self.rect)
        pygame.draw.rect(surface, (100, 150, 255), self.rect, 2)

        # Draw dropdown arrow
        arrow_x = self.rect.right - 15
        arrow_y = self.rect.centery
        pygame.draw.polygon(
            surface,
            (220, 220, 230),
            [
                (arrow_x, arrow_y - 3),
                (arrow_x + 6, arrow_y - 3),
                (arrow_x + 3, arrow_y + 3),
            ],
        )

        # Render dropdown menu if open
        if self.opened:
            self._render_dropdown_menu(surface)

    def _render_dropdown_menu(self, surface: pygame.Surface) -> None:
        """Render the dropdown menu items.

        Args:
            surface: pygame.Surface to render to
        """
        menu_y = self.rect.bottom + 2

        for i, (label, category, count) in enumerate(self.dropdown_items):
            item_rect = pygame.Rect(
                self.rect.x, menu_y + i * self.item_height, self.rect.width, self.item_height
            )

            # Highlight selected item
            if category == self.selected_category:
                pygame.draw.rect(surface, (100, 140, 200), item_rect)
            else:
                pygame.draw.rect(surface, (50, 70, 100), item_rect)

            pygame.draw.rect(surface, (80, 100, 150), item_rect, 1)

            # Text rendering with count
            # Note: Full TextRenderer integration would happen in full implementation
            # For now, we just render the rectangles

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle click events to open/close dropdown and select items.

        Args:
            event: pygame.event.Event to handle
        """
        try:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and hasattr(event, "pos"):
                    x, y = event.pos

                    if self.rect.collidepoint(x, y):
                        # Click on main button toggles dropdown
                        self.opened = not self.opened
                    elif self.opened:
                        # Click on dropdown item
                        self._handle_dropdown_click(x, y)
        except Exception as e:
            logger.error(f"CategoryFilter event handling failed: {e}")

    def _handle_dropdown_click(self, x: int, y: int) -> None:
        """Handle click on dropdown menu item.

        Checks if click is within any dropdown item rect and updates
        selected_category and calls the callback if applicable.

        Args:
            x: X coordinate of click
            y: Y coordinate of click
        """
        menu_y = self.rect.bottom + 2

        for i, (label, category, count) in enumerate(self.dropdown_items):
            item_rect = pygame.Rect(
                self.rect.x, menu_y + i * self.item_height, self.rect.width, self.item_height
            )

            if item_rect.collidepoint(x, y):
                self.selected_category = category
                self.opened = False

                # Call callback with selected category
                if self.on_category_changed:
                    try:
                        self.on_category_changed(category)
                    except Exception as e:
                        logger.error(f"Category filter callback failed: {e}")
                break


class FavoritesToggle(Button):
    """Star icon button for toggling preset favorite status.

    A specialized button that displays as a filled or unfilled star depending
    on whether the preset is favorited. Clicking toggles the favorite status
    and automatically saves via FavoritesManager.

    Attributes:
        preset_id: ID of the preset this button controls
        favorites_manager: FavoritesManager instance for managing favorites
        is_favorited: Whether the preset is currently favorited
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        preset_id: Union[int, str],
        favorites_manager: FavoritesManager,
        on_toggled: Optional[Callable[[bool], None]] = None,
    ):
        """Initialize favorites toggle button.

        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            width: Width in pixels
            height: Height in pixels
            preset_id: ID of the preset (int for built-in, str for custom)
            favorites_manager: FavoritesManager instance
            on_toggled: Optional callback called with new favorite state (True/False)

        Raises:
            No exceptions - handles all initialization gracefully
        """
        def toggle_favorite() -> None:
            try:
                self.is_favorited = self.favorites_manager.toggle(self.preset_id)
                if on_toggled:
                    on_toggled(self.is_favorited)
            except Exception as e:
                logger.error(f"FavoritesToggle toggle failed: {e}")

        super().__init__(x, y, width, height, "★", toggle_favorite)
        self.preset_id = preset_id
        self.favorites_manager = favorites_manager
        self.is_favorited = favorites_manager.is_favorite(preset_id)
        self.on_toggled = on_toggled

    def render(self, surface: pygame.Surface) -> None:
        """Render star button with filled or unfilled star based on favorite status.

        Args:
            surface: pygame.Surface to render to
        """
        if not self.visible:
            return

        # Draw button background
        button_color = (200, 180, 80) if self.hovered else (180, 160, 60)
        pygame.draw.rect(surface, button_color, self.rect)
        pygame.draw.rect(surface, (220, 200, 100), self.rect, 2)

        # Draw star (filled if favorited, unfilled otherwise)
        self._draw_star(surface, self.is_favorited)

    def _draw_star(self, surface: pygame.Surface, filled: bool) -> None:
        """Draw a 5-point star in the button center.

        Args:
            surface: pygame.Surface to render to
            filled: Whether to draw a filled or outline star
        """
        import math

        center_x = self.rect.centerx
        center_y = self.rect.centery
        size = min(self.rect.width, self.rect.height) // 3

        # Calculate 5-point star points
        points = []
        for i in range(10):
            angle_deg = (i * 36 - 90)
            angle_rad = math.radians(angle_deg)
            radius = size if i % 2 == 0 else size // 2
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            points.append((int(x), int(y)))

        if filled:
            if len(points) >= 3:
                pygame.draw.polygon(surface, (255, 200, 0), points)
        else:
            if len(points) >= 3:
                pygame.draw.polygon(surface, (255, 200, 0), points, 2)


class PresetCard(UIComponent):
    """Visual card representing a single preset in the grid.

    Displays a preset with a color block, name, and difficulty level.
    Supports selection (blue border) and hover effects (brightness increase).
    Can be clicked to select the preset.

    Attributes:
        preset: The Preset object this card represents
        selected: Whether this card is currently selected
        hovered: Whether the mouse is over this card
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        preset: Preset,
        on_clicked: Optional[Callable[[int], None]] = None,
    ):
        """Initialize preset card.

        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            width: Width in pixels
            height: Height in pixels
            preset: Preset object to display
            on_clicked: Optional callback called with preset ID when clicked

        Raises:
            No exceptions - handles all initialization gracefully
        """
        super().__init__(x, y, width, height)
        self.preset = preset
        self.selected = False
        self.hovered = False
        self.on_clicked = on_clicked

    def render(self, surface: pygame.Surface) -> None:
        """Render preset card with color block, name, and difficulty.

        Args:
            surface: pygame.Surface to render to
        """
        if not self.visible:
            return

        # Draw card background
        bg_color = (50, 70, 100)
        pygame.draw.rect(surface, bg_color, self.rect)

        # Draw selection border (blue if selected)
        if self.selected:
            pygame.draw.rect(surface, (100, 150, 255), self.rect, 3)
        else:
            pygame.draw.rect(surface, (80, 100, 150), self.rect, 1)

        # Draw color block (top half of card)
        color_height = self.rect.height // 2
        color_rect = pygame.Rect(
            self.rect.x + 5, self.rect.y + 5,
            self.rect.width - 10, color_height - 10
        )
        # Use theme-based color or default
        color = self._get_preset_color()
        pygame.draw.rect(surface, color, color_rect)

        # Apply hover brightness increase
        if self.hovered:
            overlay = pygame.Surface(self.rect.size)
            overlay.set_alpha(30)
            overlay.fill((255, 255, 255))
            surface.blit(overlay, self.rect)

    def _get_preset_color(self) -> Tuple[int, int, int]:
        """Get a color for the preset based on its theme.

        Returns:
            RGB tuple for the preset color
        """
        theme_colors = {
            "core": (100, 150, 255),
            "cyberpunk": (200, 50, 150),
            "nature": (100, 200, 100),
            "fire": (255, 100, 50),
            "water": (50, 150, 200),
        }
        return theme_colors.get(self.preset.theme, (100, 100, 150))

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle mouse events for selection and hover.

        Args:
            event: pygame.event.Event to handle
        """
        try:
            if event.type == pygame.MOUSEMOTION:
                if hasattr(event, 'pos'):
                    self.hovered = self.contains_point(event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hasattr(event, 'pos') and hasattr(event, 'button'):
                    if event.button == 1 and self.contains_point(event.pos[0], event.pos[1]):
                        if self.on_clicked:
                            try:
                                self.on_clicked(self.preset.id)
                            except Exception as e:
                                logger.error(f"PresetCard click callback failed: {e}")
        except Exception as e:
            logger.error(f"PresetCard event handling failed: {e}")


class PresetGrid(UIComponent):
    """Grid display of preset cards with selection and scrolling.

    Displays presets in a 5×4 grid (20 per page). Supports mouse wheel scrolling
    for pagination, selection (blue border), and hover effects. Clicking a card
    selects it and calls a callback.

    Attributes:
        presets: List of Preset objects to display
        cards_per_row: Number of cards horizontally (default 5)
        cards_per_col: Number of cards vertically (default 4)
        selected_preset_id: ID of currently selected preset
        current_page: Current page index for pagination
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        presets: List[Preset],
        cards_per_row: int = 5,
        cards_per_col: int = 4,
        on_preset_selected: Optional[Callable[[int], None]] = None,
    ):
        """Initialize preset grid.

        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            width: Width in pixels
            height: Height in pixels
            presets: List of Preset objects to display
            cards_per_row: Number of cards per row (default 5)
            cards_per_col: Number of cards per column (default 4)
            on_preset_selected: Optional callback called with preset ID when selected

        Raises:
            No exceptions - handles all initialization gracefully
        """
        super().__init__(x, y, width, height)
        self.presets = presets
        self.cards_per_row = cards_per_row
        self.cards_per_col = cards_per_col
        self.on_preset_selected = on_preset_selected
        self.selected_preset_id: Optional[int] = None
        self.current_page = 0

        # Create cards
        self.cards = self._create_cards()

    def _create_cards(self) -> List[PresetCard]:
        """Create PresetCard objects for current page.

        Returns:
            List of PresetCard objects for current page
        """
        cards = []
        cards_per_page = self.cards_per_row * self.cards_per_col
        start_idx = self.current_page * cards_per_page
        end_idx = start_idx + cards_per_page

        # Calculate card dimensions
        card_width = (self.rect.width - 10) // self.cards_per_row - 5
        card_height = (self.rect.height - 10) // self.cards_per_col - 5

        for i, preset in enumerate(self.presets[start_idx:end_idx]):
            row = i // self.cards_per_row
            col = i % self.cards_per_row

            card_x = self.rect.x + 5 + col * (card_width + 5)
            card_y = self.rect.y + 5 + row * (card_height + 5)

            def make_callback(preset_id: int) -> Callable[[int], None]:
                def on_card_clicked(pid: int) -> None:
                    self.selected_preset_id = pid
                    if self.on_preset_selected:
                        try:
                            self.on_preset_selected(pid)
                        except Exception as e:
                            logger.error(f"PresetGrid selection callback failed: {e}")
                return on_card_clicked

            card = PresetCard(
                card_x, card_y, card_width, card_height, preset,
                on_clicked=make_callback(preset.id)
            )
            if preset.id == self.selected_preset_id:
                card.selected = True
            cards.append(card)

        return cards

    def set_presets(self, presets: List[Preset]) -> None:
        """Update the presets to display.

        Args:
            presets: New list of Preset objects to display
        """
        try:
            self.presets = presets
            self.current_page = 0
            self.cards = self._create_cards()
        except Exception as e:
            logger.error(f"PresetGrid set_presets failed: {e}")

    def select_preset(self, preset_id: int) -> None:
        """Select a preset by ID.

        Args:
            preset_id: ID of preset to select
        """
        try:
            self.selected_preset_id = preset_id
            for card in self.cards:
                card.selected = (card.preset.id == preset_id)
        except Exception as e:
            logger.error(f"PresetGrid select_preset failed: {e}")

    def render(self, surface: pygame.Surface) -> None:
        """Render grid background and all preset cards.

        Args:
            surface: pygame.Surface to render to
        """
        if not self.visible:
            return

        # Draw grid background
        pygame.draw.rect(surface, (30, 40, 60), self.rect)
        pygame.draw.rect(surface, (80, 100, 150), self.rect, 2)

        # Render all cards
        for card in self.cards:
            card.render(surface)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events for grid interaction (selection, scrolling).

        Args:
            event: pygame.event.Event to handle
        """
        try:
            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                # Pass to all cards
                for card in self.cards:
                    card.handle_event(event)

            elif event.type == pygame.MOUSEWHEEL and hasattr(event, 'y'):
                # Handle scrolling for pagination
                cards_per_page = self.cards_per_row * self.cards_per_col
                max_pages = (len(self.presets) + cards_per_page - 1) // cards_per_page

                if event.y > 0:  # Scroll up - previous page
                    self.current_page = max(0, self.current_page - 1)
                else:  # Scroll down - next page
                    self.current_page = min(max_pages - 1, self.current_page + 1)

                self.cards = self._create_cards()

        except Exception as e:
            logger.error(f"PresetGrid event handling failed: {e}")


class DetailsPanel(UIComponent):
    """Right sidebar panel showing selected preset information and controls.

    Displays the currently selected preset with full details and action buttons.
    Shows preset name, theme, description, and buttons for Play, Edit, Mix, and
    Add to Playlist. Includes a heart icon for toggling favorites.

    Attributes:
        preset: The currently selected Preset object
        favorites_manager: FavoritesManager instance
        components: List of UI components in this panel
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        preset_manager: PresetManager,
        favorites_manager: FavoritesManager,
        on_play: Optional[Callable[[int], None]] = None,
        on_edit: Optional[Callable[[int], None]] = None,
        on_mix: Optional[Callable[[int], None]] = None,
        on_add_to_playlist: Optional[Callable[[int], None]] = None,
    ):
        """Initialize details panel.

        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            width: Width in pixels
            height: Height in pixels
            preset_manager: PresetManager instance
            favorites_manager: FavoritesManager instance
            on_play: Optional callback when Play button clicked
            on_edit: Optional callback when Edit button clicked
            on_mix: Optional callback when Mix button clicked
            on_add_to_playlist: Optional callback when Add to Playlist clicked

        Raises:
            No exceptions - handles all initialization gracefully
        """
        super().__init__(x, y, width, height)
        self.preset_manager = preset_manager
        self.favorites_manager = favorites_manager
        self.preset: Optional[Preset] = None
        self.on_play = on_play
        self.on_edit = on_edit
        self.on_mix = on_mix
        self.on_add_to_playlist = on_add_to_playlist

        # Create buttons
        button_width = (width - 20) // 2
        button_height = 35
        button_y = height - 150

        self.play_button = Button(
            x + 10, button_y, button_width, button_height, "Play",
            lambda: self._trigger_callback(self.on_play)
        )
        self.edit_button = Button(
            x + 10 + button_width + 5, button_y, button_width, button_height, "Edit",
            lambda: self._trigger_callback(self.on_edit)
        )
        self.mix_button = Button(
            x + 10, button_y + 45, button_width, button_height, "Mix",
            lambda: self._trigger_callback(self.on_mix)
        )
        self.playlist_button = Button(
            x + 10 + button_width + 5, button_y + 45, button_width, button_height, "Playlist",
            lambda: self._trigger_callback(self.on_add_to_playlist)
        )

        # Create favorites toggle
        self.favorites_toggle = FavoritesToggle(
            x + width - 50, y + 10, 40, 40, 0, favorites_manager
        )

        self.components = [
            self.play_button, self.edit_button, self.mix_button,
            self.playlist_button, self.favorites_toggle
        ]

    def _trigger_callback(self, callback: Optional[Callable[[int], None]]) -> None:
        """Trigger a callback with current preset ID.

        Args:
            callback: Callback function to trigger
        """
        try:
            if callback and self.preset:
                callback(self.preset.id)
        except Exception as e:
            logger.error(f"DetailsPanel callback failed: {e}")

    def set_preset(self, preset: Preset) -> None:
        """Set the preset to display.

        Args:
            preset: Preset object to display
        """
        try:
            self.preset = preset
            self.favorites_toggle.preset_id = preset.id
            self.favorites_toggle.is_favorited = self.favorites_manager.is_favorite(preset.id)
        except Exception as e:
            logger.error(f"DetailsPanel set_preset failed: {e}")

    def render(self, surface: pygame.Surface) -> None:
        """Render panel with preset details and buttons.

        Args:
            surface: pygame.Surface to render to
        """
        if not self.visible or self.preset is None:
            return

        # Draw panel background
        pygame.draw.rect(surface, (30, 40, 60), self.rect)
        pygame.draw.rect(surface, (80, 100, 150), self.rect, 2)

        # Draw preset details (would include text rendering)
        # For now, just render components
        for component in self.components:
            component.render(surface)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events for all panel components.

        Args:
            event: pygame.event.Event to handle
        """
        if not self.visible or self.preset is None:
            return

        try:
            for component in self.components:
                component.handle_event(event)
        except Exception as e:
            logger.error(f"DetailsPanel event handling failed: {e}")


class ParameterEditorModal(Modal):
    """Modal dialog for editing custom preset parameters.

    Displays 6 sliders for editing:
    - Bass sensitivity (0.0-3.0)
    - Mid sensitivity (0.0-3.0)
    - Treble sensitivity (0.0-3.0)
    - Color hue (-180 to 180)
    - Color saturation (-1.0 to 2.0)
    - Animation speed (0.5-2.0)

    Also includes a text input for custom preset name and Save/Cancel buttons.

    Attributes:
        parameters: Dictionary of parameter values
        base_preset_id: ID of the base preset
        sliders: Dictionary of parameter name to Slider objects
        name_input: TextInput for custom preset name
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        base_preset_id: int,
        on_save: Optional[Callable[[str, Dict[str, float]], None]] = None,
        on_cancel: Optional[Callable[[], None]] = None,
    ):
        """Initialize parameter editor modal.

        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            width: Width in pixels
            height: Height in pixels
            base_preset_id: ID of the base preset
            on_save: Optional callback called with (name, parameters) when saved
            on_cancel: Optional callback called when cancelled

        Raises:
            No exceptions - handles all initialization gracefully
        """
        super().__init__(x, y, width, height, title="Edit Preset Parameters")
        self.base_preset_id = base_preset_id
        self.on_save = on_save
        self.on_cancel = on_cancel

        # Initialize parameters with defaults
        self.parameters: Dict[str, float] = {
            "bass_sensitivity": 1.0,
            "mid_sensitivity": 1.0,
            "treble_sensitivity": 1.0,
            "color_hue": 0.0,
            "color_saturation": 0.0,
            "animation_speed": 1.0,
        }

        # Create sliders
        slider_y = y + 40
        slider_width = width - 40
        self.sliders: Dict[str, Slider] = {}

        slider_configs = [
            ("bass_sensitivity", "Bass", 0.0, 3.0, 1.0),
            ("mid_sensitivity", "Mid", 0.0, 3.0, 1.0),
            ("treble_sensitivity", "Treble", 0.0, 3.0, 1.0),
            ("color_hue", "Hue", -180.0, 180.0, 0.0),
            ("color_saturation", "Saturation", -1.0, 2.0, 0.0),
            ("animation_speed", "Speed", 0.5, 2.0, 1.0),
        ]

        for i, (param_name, label, min_val, max_val, initial) in enumerate(slider_configs):
            slider = Slider(
                x + 20, slider_y + i * 50, slider_width, 20,
                min_val=min_val, max_val=max_val, initial=initial
            )
            self.sliders[param_name] = slider
            self.add_component(slider)
            self.parameters[param_name] = initial

        # Create name input
        name_input_y = slider_y + len(slider_configs) * 50
        self.name_input = TextInput(
            x + 20, name_input_y, slider_width, 30,
            placeholder="Custom preset name", max_length=100
        )
        self.add_component(self.name_input)

        # Create Save/Cancel buttons
        button_width = (slider_width - 10) // 2
        button_y = name_input_y + 50

        save_button = Button(
            x + 20, button_y, button_width, 30, "Save",
            self._on_save_clicked
        )
        cancel_button = Button(
            x + 20 + button_width + 10, button_y, button_width, 30, "Cancel",
            self._on_cancel_clicked
        )

        self.add_component(save_button)
        self.add_component(cancel_button)

    def _on_save_clicked(self) -> None:
        """Handle Save button click."""
        try:
            # Update parameters from sliders
            for param_name, slider in self.sliders.items():
                self.parameters[param_name] = slider.value

            if self.on_save:
                self.on_save(self.name_input.text, self.parameters)
            self.visible = False
        except Exception as e:
            logger.error(f"ParameterEditorModal save failed: {e}")

    def _on_cancel_clicked(self) -> None:
        """Handle Cancel button click."""
        try:
            if self.on_cancel:
                self.on_cancel()
            self.visible = False
        except Exception as e:
            logger.error(f"ParameterEditorModal cancel failed: {e}")

    def set_parameters(self, parameters: Dict[str, float]) -> None:
        """Set parameter values.

        Args:
            parameters: Dictionary of parameter values
        """
        try:
            for param_name, value in parameters.items():
                if param_name in self.sliders:
                    self.sliders[param_name].value = value
                    self.parameters[param_name] = value
        except Exception as e:
            logger.error(f"ParameterEditorModal set_parameters failed: {e}")


class MixToolModal(Modal):
    """Modal dialog for blending two presets together.

    Shows a base preset on the left and a dropdown to select a preset to
    mix with. A slider controls the blend ratio (0% base / 100% other).
    Includes Save as Custom and Cancel buttons.

    Attributes:
        base_preset_id: ID of the base preset
        mix_preset_id: ID of the preset to mix with
        blend_ratio: Blend ratio (0.0 = base only, 1.0 = mix only)
        preset_manager: PresetManager instance
        blend_slider: Slider for adjusting blend ratio
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        base_preset_id: int,
        preset_manager: PresetManager,
        on_save: Optional[Callable[[int, int, float, str], None]] = None,
        on_cancel: Optional[Callable[[], None]] = None,
    ):
        """Initialize mix tool modal.

        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            width: Width in pixels
            height: Height in pixels
            base_preset_id: ID of the base preset
            preset_manager: PresetManager instance for accessing presets
            on_save: Optional callback with (base_id, mix_id, blend_ratio, name)
            on_cancel: Optional callback when cancelled

        Raises:
            No exceptions - handles all initialization gracefully
        """
        super().__init__(x, y, width, height, title="Mix Presets")
        self.base_preset_id = base_preset_id
        self.mix_preset_id: Optional[int] = None
        self.blend_ratio = 0.5
        self.preset_manager = preset_manager
        self.on_save = on_save
        self.on_cancel = on_cancel

        # Create blend slider
        slider_y = y + 80
        self.blend_slider = Slider(
            x + 20, slider_y, width - 40, 20,
            min_val=0.0, max_val=1.0, initial=0.5
        )
        self.add_component(self.blend_slider)

        # Create name input
        name_input_y = slider_y + 80
        self.name_input = TextInput(
            x + 20, name_input_y, width - 40, 30,
            placeholder="Blended preset name", max_length=100
        )
        self.add_component(self.name_input)

        # Create Save/Cancel buttons
        button_width = (width - 50) // 2
        button_y = name_input_y + 50

        save_button = Button(
            x + 20, button_y, button_width, 30, "Save",
            self._on_save_clicked
        )
        cancel_button = Button(
            x + 20 + button_width + 10, button_y, button_width, 30, "Cancel",
            self._on_cancel_clicked
        )

        self.add_component(save_button)
        self.add_component(cancel_button)

    def _on_save_clicked(self) -> None:
        """Handle Save button click."""
        try:
            self.blend_ratio = self.blend_slider.value
            if self.on_save and self.mix_preset_id is not None:
                self.on_save(
                    self.base_preset_id, self.mix_preset_id,
                    self.blend_ratio, self.name_input.text
                )
            self.visible = False
        except Exception as e:
            logger.error(f"MixToolModal save failed: {e}")

    def _on_cancel_clicked(self) -> None:
        """Handle Cancel button click."""
        try:
            if self.on_cancel:
                self.on_cancel()
            self.visible = False
        except Exception as e:
            logger.error(f"MixToolModal cancel failed: {e}")

    def set_mix_preset(self, preset_id: int) -> None:
        """Set the preset to mix with.

        Args:
            preset_id: ID of the preset to mix with
        """
        try:
            self.mix_preset_id = preset_id
        except Exception as e:
            logger.error(f"MixToolModal set_mix_preset failed: {e}")
