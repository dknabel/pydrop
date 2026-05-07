"""Text rendering using PIL/Pillow to avoid pygame.font circular imports"""

import os
from typing import Tuple, Optional, Dict
from PIL import Image, ImageDraw, ImageFont
import pygame


class TextRenderer:
    """Renders text to pygame-compatible surfaces using PIL/Pillow.

    This avoids circular import issues with pygame.font and provides
    better font handling and caching for menu rendering.
    """

    def __init__(
        self,
        font_path: Optional[str] = None,
        bold_font_path: Optional[str] = None,
        font_size_normal: int = 14,
        font_size_bold: int = 16,
        font_size_small: int = 10,
    ):
        """Initialize TextRenderer with font paths and sizes.

        Args:
            font_path: Path to regular font file. If None, uses system fonts.
            bold_font_path: Path to bold font file. If None, uses system fonts or regular font.
            font_size_normal: Size for normal text (default 14px)
            font_size_bold: Size for bold text (default 16px)
            font_size_small: Size for small text (default 10px)
        """
        self.font_size_normal = font_size_normal
        self.font_size_bold = font_size_bold
        self.font_size_small = font_size_small

        self.font_path = font_path
        self.bold_font_path = bold_font_path

        # Cache for rendered text: (text, color, size) -> (surface, rect)
        self._cache: Dict[Tuple[str, Tuple[int, int, int], str], Tuple[pygame.Surface, pygame.Rect]] = {}

        # Initialize fonts
        self._load_fonts()

    def _load_fonts(self) -> None:
        """Load fonts with fallback to system fonts."""
        self.fonts = {}

        # Try to load regular font
        if self.font_path and os.path.exists(self.font_path):
            try:
                self.fonts['normal'] = ImageFont.truetype(self.font_path, self.font_size_normal)
                self.fonts['small'] = ImageFont.truetype(self.font_path, self.font_size_small)
            except Exception as e:
                print(f"Failed to load font from {self.font_path}: {e}")
                self.fonts['normal'] = self._get_default_font(self.font_size_normal)
                self.fonts['small'] = self._get_default_font(self.font_size_small)
        else:
            self.fonts['normal'] = self._get_default_font(self.font_size_normal)
            self.fonts['small'] = self._get_default_font(self.font_size_small)

        # Try to load bold font
        if self.bold_font_path and os.path.exists(self.bold_font_path):
            try:
                self.fonts['bold'] = ImageFont.truetype(self.bold_font_path, self.font_size_bold)
            except Exception as e:
                print(f"Failed to load bold font from {self.bold_font_path}: {e}")
                self.fonts['bold'] = self._get_default_font(self.font_size_bold)
        else:
            self.fonts['bold'] = self._get_default_font(self.font_size_bold)

    def _get_default_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Get default system font with fallback."""
        # Try common system font paths
        font_paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Linux
            '/System/Library/Fonts/Helvetica.ttc',  # macOS
            'C:\\Windows\\Fonts\\arial.ttf',  # Windows
        ]

        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except Exception:
                    continue

        # Fallback to default font
        return ImageFont.load_default()

    def render(
        self,
        text: str,
        color: Tuple[int, int, int] = (255, 255, 255),
        size: str = 'normal',
    ) -> Tuple[pygame.Surface, pygame.Rect]:
        """Render text to a pygame surface.

        Args:
            text: Text to render
            color: RGB color tuple (default white)
            size: Font size: 'normal', 'bold', or 'small' (default 'normal')

        Returns:
            Tuple of (pygame.Surface, pygame.Rect) for blit operations
        """
        # Validate size argument
        if size not in ('normal', 'bold', 'small'):
            size = 'normal'

        # Check cache
        cache_key = (text, color, size)
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Get font
        font = self.fonts.get(size, self.fonts['normal'])

        # Create PIL image for text measurement and rendering
        # First, get the bounding box to determine image size
        dummy_image = Image.new('RGBA', (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_image)
        bbox = dummy_draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Add padding
        padding = 4
        image_width = max(text_width + 2 * padding, 1)
        image_height = max(text_height + 2 * padding, 1)

        # Create actual image for rendering
        pil_image = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(pil_image)

        # Draw text centered with padding
        draw.text(
            (padding - bbox[0], padding - bbox[1]),
            text,
            font=font,
            fill=(*color, 255),  # Add full alpha
        )

        # Convert PIL image to pygame surface
        # PIL RGBA to pygame surface
        pil_image = pil_image.convert('RGBA')
        raw_str = pil_image.tobytes('raw', 'RGBA')
        pygame_surface = pygame.image.fromstring(
            raw_str,
            pil_image.size,
            'RGBA',
        )

        # Create rect for blit operations
        rect = pygame_surface.get_rect()

        # Cache result
        result = (pygame_surface, rect)
        self._cache[cache_key] = result

        return result

    def clear_cache(self) -> None:
        """Clear the render cache."""
        self._cache.clear()
