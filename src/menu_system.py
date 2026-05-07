"""Menu system for preset selection and browsing"""

import pygame
import math


class PresetMenu:
    """Visual toggle menu overlay for preset selection"""

    def __init__(self, presets, width=1280, height=720):
        self.presets = presets
        self.width = width
        self.height = height
        self.visible = False
        self.selected_index = 0

        # Menu styling
        self.bg_color = (20, 20, 30, 200)  # Semi-transparent dark background
        self.card_bg_color = (40, 40, 50)
        self.card_border_color = (80, 80, 100)
        self.card_selected_color = (100, 150, 255)
        self.text_color = (220, 220, 230)
        self.theme_text_color = (150, 150, 170)

        # Grid layout
        self.card_width = 120
        self.card_height = 80
        self.padding = 10
        self.margin = 20

        # Calculate grid dimensions
        self.cols = max(1, (width - 2 * self.margin) // (self.card_width + self.padding))
        self.rows = max(1, math.ceil(len(presets) / self.cols))

        # Scrolling
        self.scroll_offset = 0
        self.max_scroll = max(0, (self.rows * (self.card_height + self.padding)) - (height - 2 * self.margin))

        # Font - lazy initialized to avoid pygame initialization issues
        self.font_name = None
        self.font_theme = None
        self._fonts_initialized = False

    def toggle(self):
        """Toggle menu visibility"""
        self.visible = not self.visible
        if self.visible:
            # Reset scroll when opening menu
            self.scroll_offset = 0

    def handle_event(self, event):
        """
        Handle events when menu is visible.
        Returns selected preset index if a preset was clicked, None otherwise.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                preset_idx = self._get_preset_at_position(event.pos)
                if preset_idx is not None:
                    return preset_idx

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - self.cols)
                self._scroll_to_selected()
            elif event.key == pygame.K_DOWN:
                self.selected_index = min(len(self.presets) - 1, self.selected_index + self.cols)
                self._scroll_to_selected()
            elif event.key == pygame.K_LEFT:
                self.selected_index = max(0, self.selected_index - 1)
                self._scroll_to_selected()
            elif event.key == pygame.K_RIGHT:
                self.selected_index = min(len(self.presets) - 1, self.selected_index + 1)
                self._scroll_to_selected()
            elif event.key == pygame.K_RETURN:
                return self.selected_index

        elif event.type == pygame.MOUSEWHEEL:
            # Handle mouse wheel scrolling
            self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset - event.y * 20))

        return None

    def _scroll_to_selected(self):
        """Auto-scroll to keep selected item visible"""
        selected_row = self.selected_index // self.cols
        item_y = selected_row * (self.card_height + self.padding) - self.scroll_offset

        if item_y < self.margin:
            self.scroll_offset = max(0, selected_row * (self.card_height + self.padding) - self.margin)
        elif item_y + self.card_height > self.height - self.margin:
            self.scroll_offset = min(
                self.max_scroll,
                selected_row * (self.card_height + self.padding) + self.card_height - (self.height - 2 * self.margin)
            )

    def _get_preset_at_position(self, pos):
        """Get preset index from mouse coordinates"""
        x, y = pos

        # Check if click is within the menu area
        if x < self.margin or x > self.width - self.margin:
            return None

        # Adjust for scroll offset
        adjusted_y = y + self.scroll_offset - self.margin

        if adjusted_y < 0 or adjusted_y > self.rows * (self.card_height + self.padding):
            return None

        # Calculate grid position
        col = (x - self.margin) // (self.card_width + self.padding)
        row = adjusted_y // (self.card_height + self.padding)

        # Bounds checking
        if col >= self.cols or row >= self.rows:
            return None

        preset_idx = row * self.cols + col
        if preset_idx < len(self.presets):
            return preset_idx

        return None

    def render(self, surface):
        """Render the menu overlay"""
        if not self.visible:
            return

        # Initialize fonts on first render (deferred to avoid circular imports)
        if not self._fonts_initialized:
            self._fonts_initialized = True

        # Create a surface for the menu with alpha support
        menu_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Draw semi-transparent background
        pygame.draw.rect(menu_surface, self.bg_color, (0, 0, self.width, self.height))

        # Draw title (text only - skip font rendering to avoid pygame circular import in Python 3.14)
        # Visual indicator instead: thicker border at top
        pygame.draw.line(menu_surface, self.card_selected_color, (0, 30), (self.width, 30), 3)

        # Create a clipping region for the preset grid
        grid_area = pygame.Rect(
            self.margin,
            self.margin + 40,
            self.width - 2 * self.margin,
            self.height - 2 * self.margin - 40
        )

        # Draw preset cards
        for i, preset in enumerate(self.presets):
            row = i // self.cols
            col = i % self.cols

            x = self.margin + col * (self.card_width + self.padding)
            y = self.margin + 40 + row * (self.card_height + self.padding) - self.scroll_offset

            # Skip if outside visible area
            if y + self.card_height < self.margin + 40 or y > self.height - self.margin:
                continue

            # Draw card
            card_rect = pygame.Rect(x, y, self.card_width, self.card_height)

            # Determine card color
            if i == self.selected_index:
                # Highlight selected card
                pygame.draw.rect(menu_surface, self.card_selected_color, card_rect, 2)
                pygame.draw.rect(menu_surface, (self.card_selected_color[0], self.card_selected_color[1], self.card_selected_color[2], 50), card_rect)
            else:
                pygame.draw.rect(menu_surface, self.card_border_color, card_rect, 1)
                pygame.draw.rect(menu_surface, self.card_bg_color, card_rect)

            # Draw index number inside the card (simple text replacement)
            # Calculate how many digits the index has
            preset_num = str(i + 1)
            x_pos = x + self.card_width // 2 - 5
            y_pos = y + self.card_height // 2 - 10

            # Draw number as simple geometric indicators instead of text
            # Draw a bar proportional to the index position (0-252)
            bar_width = int((i / len(self.presets)) * (self.card_width - 4))
            pygame.draw.rect(menu_surface, self.theme_text_color, (x + 2, y + self.card_height - 8, bar_width, 4))

        # Draw scroll indicator if needed
        if self.max_scroll > 0:
            scroll_percent = self.scroll_offset / self.max_scroll
            scroll_bar_height = 20
            scroll_bar_y = self.margin + 40 + scroll_percent * (self.height - 2 * self.margin - 40 - scroll_bar_height)
            pygame.draw.rect(menu_surface, self.card_selected_color, (self.width - 10, scroll_bar_y, 5, scroll_bar_height))

        # Blit to main surface
        surface.blit(menu_surface, (0, 0))
