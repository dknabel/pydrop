"""Menu system for preset selection and browsing"""

import pygame
import math


class PresetMenu:
    """Visual toggle menu overlay for preset selection organized by theme"""

    def __init__(self, presets, width=1280, height=720):
        self.presets = presets
        self.width = width
        self.height = height
        self.visible = False
        self.selected_index = 0

        # Menu styling
        self.bg_color = (20, 20, 30, 200)
        self.card_bg_color = (40, 40, 50)
        self.card_border_color = (80, 80, 100)
        self.card_selected_color = (100, 150, 255)
        self.text_color = (220, 220, 230)
        self.theme_text_color = (150, 150, 170)
        self.category_header_color = (80, 120, 200)

        # Grid layout
        self.card_width = 100
        self.card_height = 70
        self.padding = 8
        self.margin = 20
        self.category_height = 25

        # Calculate grid dimensions
        self.cols = max(1, (width - 2 * self.margin) // (self.card_width + self.padding))

        # Group presets by theme
        self.categories = self._group_by_theme()
        self._build_grid_layout()

        # Scrolling
        self.scroll_offset = 0
        self.max_scroll = max(0, self.total_height - (height - 2 * self.margin))

        # Font - lazy initialized to avoid pygame initialization issues
        self.font_name = None
        self.font_theme = None
        self._fonts_initialized = False

    def _group_by_theme(self):
        """Group presets by their theme"""
        categories = {}
        for i, preset in enumerate(self.presets):
            theme = preset.get('theme', 'Unknown')
            if theme not in categories:
                categories[theme] = []
            categories[theme].append((i, preset))

        # Sort by theme name but keep Core first
        sorted_categories = {}
        if 'Core' in categories:
            sorted_categories['Core'] = categories.pop('Core')

        for theme in sorted(categories.keys()):
            sorted_categories[theme] = categories[theme]

        return sorted_categories

    def _build_grid_layout(self):
        """Calculate total height needed for all categories and presets"""
        self.total_height = 0
        for theme, presets in self.categories.items():
            self.total_height += self.category_height  # Header
            rows = math.ceil(len(presets) / self.cols)
            self.total_height += rows * (self.card_height + self.padding)
            self.total_height += self.padding  # Space between categories

    def _get_preview_color(self, index):
        """Generate a preview color based on preset index and shader type"""
        preset = self.presets[index]
        shader = preset.get('shader', '')

        # Color schemes based on theme
        theme = preset.get('theme', 'Unknown')
        theme_colors = {
            'Cosmic': (30, 60, 100),
            'Organic': (60, 100, 60),
            'Retro Aero': (100, 150, 200),
            'Digital': (100, 100, 150),
            'Abstract': (120, 80, 120),
            'Liquids': (60, 120, 180),
            'Crystalline': (150, 200, 255),
            'Psychedelic': (200, 100, 200),
            'Atmospheric': (100, 150, 180),
            'Mechanical': (100, 100, 100),
            'Bioluminescent': (150, 255, 150),
            'Quantum': (200, 100, 255),
            'Temporal': (255, 200, 100),
            'Dimensional': (200, 150, 255),
            'Ethereal': (180, 150, 200),
            'Infernal': (255, 100, 50),
            'Celestial': (255, 200, 100),
            'Metamorphic': (150, 200, 150),
            'Synesthetic': (200, 150, 200),
            'Crystallized': (200, 220, 255),
            'Resonant': (200, 200, 100),
            'Chromatic': (200, 150, 100),
            'Kinetic': (255, 150, 100),
            'Alchemical': (200, 150, 100),
            'Core': (100, 120, 150),
        }

        return theme_colors.get(theme, (80, 80, 100))

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
        # Find the Y position of the selected preset in the category-based layout
        target_y = 0
        found = False

        for theme, theme_presets in self.categories.items():
            target_y += self.category_height

            for local_idx, (preset_idx, preset) in enumerate(theme_presets):
                if preset_idx == self.selected_index:
                    row = local_idx // self.cols
                    target_y += row * (self.card_height + self.padding)
                    found = True
                    break

            if found:
                break

            rows = math.ceil(len(theme_presets) / self.cols)
            target_y += rows * (self.card_height + self.padding) + self.padding

        if not found:
            return

        # Adjust scroll to keep selected item visible
        item_y = target_y - self.scroll_offset

        if item_y < self.margin + 40:
            self.scroll_offset = max(0, target_y - (self.margin + 40))
        elif item_y + self.card_height > self.height - self.margin:
            self.scroll_offset = min(
                self.max_scroll,
                target_y + self.card_height - (self.height - 2 * self.margin)
            )

    def _get_preset_at_position(self, pos):
        """Get preset index from mouse coordinates"""
        x, y = pos

        # Check if click is within the menu area
        if x < self.margin or x > self.width - self.margin:
            return None

        # Adjust for scroll offset
        adjusted_y = y + self.scroll_offset - self.margin - 40  # Account for title bar

        if adjusted_y < 0:
            return None

        # Iterate through categories to find which preset was clicked
        y_offset = 0
        for theme, theme_presets in self.categories.items():
            # Category header
            y_offset += self.category_height

            # Presets in this category
            for local_idx, (preset_idx, preset) in enumerate(theme_presets):
                col = local_idx % self.cols
                row = local_idx // self.cols

                preset_y = y_offset + row * (self.card_height + self.padding)
                preset_x = self.margin + col * (self.card_width + self.padding)

                # Check if click is on this preset card
                if (adjusted_y >= preset_y and
                    adjusted_y < preset_y + self.card_height and
                    x >= preset_x and
                    x < preset_x + self.card_width):
                    return preset_idx

            # Space between categories
            rows = math.ceil(len(theme_presets) / self.cols)
            y_offset += rows * (self.card_height + self.padding) + self.padding

        return None

    def _draw_preview(self, surface, x, y, preset_idx):
        """Draw a visual preview rectangle for the preset"""
        preview_width = self.card_width - 4
        preview_height = 35

        # Get theme-based color
        color = self._get_preview_color(preset_idx)

        # Draw main colored preview rectangle with border
        pygame.draw.rect(surface, color, (x + 2, y + 2, preview_width, preview_height))
        pygame.draw.rect(surface, self.text_color, (x + 2, y + 2, preview_width, preview_height), 1)

        # Draw pattern based on shader type
        shader = self.presets[preset_idx].get('shader', '')
        pattern_color = tuple(min(255, c + 60) for c in color)

        # Draw horizontal gradient/pattern lines
        for i in range(0, preview_height, 4):
            intensity = int((i / preview_height) * 100)
            line_color = tuple(min(255, c + intensity // 3) for c in color)
            pygame.draw.line(surface, line_color, (x + 5, y + 2 + i), (x + preview_width - 3, y + 2 + i), 1)

    def render(self, surface):
        """Render the menu overlay organized by theme"""
        if not self.visible:
            return

        # Initialize fonts on first render (deferred to avoid circular imports)
        if not self._fonts_initialized:
            self._fonts_initialized = True
            try:
                # Import freetype lazily to avoid circular import at module level
                from pygame import freetype
                self.font_name = freetype.Font(None, 10)
                self.font_category = freetype.Font(None, 12)
            except Exception as e:
                self.font_name = None
                self.font_category = None

        # Create a surface for the menu with alpha support
        menu_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Draw semi-transparent background
        pygame.draw.rect(menu_surface, self.bg_color, (0, 0, self.width, self.height))

        # Draw title bar
        pygame.draw.line(menu_surface, self.card_selected_color, (0, 30), (self.width, 30), 3)

        # Draw presets organized by theme
        y_offset = self.margin + 40

        for theme, theme_presets in self.categories.items():
            # Draw category header
            header_y = y_offset - self.scroll_offset

            if header_y > self.margin and header_y < self.height - self.margin:
                pygame.draw.rect(menu_surface, self.category_header_color, (self.margin, header_y, self.width - 2 * self.margin, self.category_height))
                # Theme label (visual indicator with colored bar)
                color = self._get_preview_color(next((idx for idx, (_, p) in enumerate(theme_presets) if p.get('theme') == theme), 0))
                pygame.draw.rect(menu_surface, color, (self.margin + 5, header_y + 5, 10, self.category_height - 10))

                # Draw category name
                if self.font_category:
                    name_surface, _ = self.font_category.render(theme, self.text_color)
                    menu_surface.blit(name_surface, (self.margin + 20, header_y + 4))

            y_offset += self.category_height

            # Draw presets in this category
            for local_idx, (preset_idx, preset) in enumerate(theme_presets):
                col = local_idx % self.cols
                row = local_idx // self.cols

                x = self.margin + col * (self.card_width + self.padding)
                y = y_offset + row * (self.card_height + self.padding) - self.scroll_offset

                # Skip if outside visible area
                if y + self.card_height < self.margin + 40 or y > self.height - self.margin:
                    continue

                # Draw card
                card_rect = pygame.Rect(x, y, self.card_width, self.card_height)

                # Determine card color
                if preset_idx == self.selected_index:
                    # Highlight selected card
                    pygame.draw.rect(menu_surface, self.card_selected_color, card_rect, 2)
                    pygame.draw.rect(menu_surface, (self.card_selected_color[0], self.card_selected_color[1], self.card_selected_color[2], 50), card_rect)
                else:
                    pygame.draw.rect(menu_surface, self.card_border_color, card_rect, 1)
                    pygame.draw.rect(menu_surface, self.card_bg_color, card_rect)

                # Draw preview color bar
                self._draw_preview(menu_surface, x, y, preset_idx)

                # Draw preset name
                if self.font_name:
                    preset_name = preset.get('name', 'Preset')
                    # Truncate name if too long
                    if len(preset_name) > 10:
                        preset_name = preset_name[:9] + '.'
                    name_surface, name_rect = self.font_name.render(preset_name, self.text_color)
                    # Center text below preview
                    name_x = x + (self.card_width - name_rect.width) // 2
                    menu_surface.blit(name_surface, (name_x, y + 40))

            # Space between categories
            rows = math.ceil(len(theme_presets) / self.cols)
            y_offset += rows * (self.card_height + self.padding) + self.padding

        # Draw scroll indicator if needed
        if self.max_scroll > 0:
            scroll_percent = self.scroll_offset / self.max_scroll
            scroll_bar_height = 20
            scroll_bar_y = self.margin + 40 + scroll_percent * (self.height - 2 * self.margin - 40 - scroll_bar_height)
            pygame.draw.rect(menu_surface, self.card_selected_color, (self.width - 10, scroll_bar_y, 5, scroll_bar_height))

        # Blit to main surface
        surface.blit(menu_surface, (0, 0))
