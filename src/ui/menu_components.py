"""Specialized menu UI components for the preset system.

Provides higher-level UI components built on the base component classes
for use in the menu system, particularly for preset management.
"""

from src.ui.components import UIComponent, TextInput
from src.ui.presets_data import PresetManager
from src.ui.models import Preset
from typing import List, Callable, Optional, Tuple, Dict
import pygame
import logging

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
