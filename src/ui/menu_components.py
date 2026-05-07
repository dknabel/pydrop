"""Specialized menu UI components for the preset system.

Provides higher-level UI components built on the base component classes
for use in the menu system, particularly for preset management.
"""

from src.ui.components import UIComponent, TextInput
from src.ui.presets_data import PresetManager
from src.ui.models import Preset
from typing import List, Callable, Optional
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
