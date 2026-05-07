"""UI Component base classes for the menu system."""

from abc import ABC, abstractmethod
import pygame
import logging
from typing import Optional, Callable, List

logger = logging.getLogger(__name__)


class UIComponent(ABC):
    """Base class for all UI elements.

    Provides common functionality for all UI components including positioning,
    visibility, and event handling.
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        """Initialize component with position and size.

        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            width: Width in pixels
            height: Height in pixels
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """Render component to surface.

        Args:
            surface: pygame.Surface to render to
        """
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame event.

        Args:
            event: pygame.event.Event to handle
        """
        pass

    def contains_point(self, x: int, y: int) -> bool:
        """Check if point is within component bounds.

        Args:
            x: X coordinate to check
            y: Y coordinate to check

        Returns:
            True if point is within bounds, False otherwise
        """
        return self.rect.collidepoint(x, y)


class Button(UIComponent):
    """Clickable button with callback.

    A rectangular button that triggers a callback function when clicked.
    Supports hover and press state tracking.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        label: str,
        callback: Callable[[], None],
    ):
        """Initialize button.

        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            width: Width in pixels
            height: Height in pixels
            label: Button text label
            callback: Function to call on click
        """
        super().__init__(x, y, width, height)
        self.label = label
        self.callback = callback
        self.hovered = False
        self.pressed = False

    def render(self, surface: pygame.Surface) -> None:
        """Render button to surface.

        Args:
            surface: pygame.Surface to render to
        """
        if not self.visible:
            return

        # Draw button background with color based on hover state
        color = (120, 180, 255) if self.hovered else (80, 120, 200)
        pygame.draw.rect(surface, color, self.rect)

        # Draw button border
        pygame.draw.rect(surface, (200, 220, 255), self.rect, 2)

        # Draw button label
        try:
            from src.ui.text_renderer import TextRenderer
            renderer = TextRenderer()
            text_surf, text_rect = renderer.render(
                self.label, (220, 220, 230), size='normal'
            )
            # Center text on button
            text_x = self.rect.centerx - text_rect.width // 2
            text_y = self.rect.centery - text_rect.height // 2
            surface.blit(text_surf, (text_x, text_y))
        except Exception as e:
            pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle mouse events.

        Args:
            event: pygame.event.Event to handle
        """
        try:
            if event.type == pygame.MOUSEMOTION:
                if hasattr(event, 'pos'):
                    self.hovered = self.contains_point(event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hasattr(event, 'button') and hasattr(event, 'pos'):
                    if event.button == 1 and self.contains_point(event.pos[0], event.pos[1]):
                        self.pressed = True
                        try:
                            self.callback()
                        except Exception as e:
                            logger.error(f"Button callback failed: {e}")
            elif event.type == pygame.MOUSEBUTTONUP:
                self.pressed = False
        except Exception as e:
            logger.error(f"Button event handling failed: {e}")


class Slider(UIComponent):
    """Value slider for continuous input.

    A horizontal slider that allows selecting a value within a min-max range.
    Supports dragging to adjust the value.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        min_val: float = 0.0,
        max_val: float = 1.0,
        initial: float = 0.5,
    ):
        """Initialize slider.

        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            width: Width in pixels
            height: Height in pixels
            min_val: Minimum slider value (default 0.0)
            max_val: Maximum slider value (default 1.0)
            initial: Initial slider value (default 0.5)
        """
        super().__init__(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        if self.min_val >= self.max_val:
            logger.warning("Slider min_val >= max_val, setting max_val to min_val + 1")
            self.max_val = self.min_val + 1
        self._value = max(self.min_val, min(self.max_val, initial))
        self.dragging = False

    @property
    def value(self) -> float:
        """Get current slider value.

        Returns:
            Current slider value
        """
        return self._value

    @value.setter
    def value(self, val: float) -> None:
        """Set slider value.

        Args:
            val: Value to set (will be clamped to [min_val, max_val])
        """
        self._value = max(self.min_val, min(self.max_val, val))

    def render(self, surface: pygame.Surface) -> None:
        """Render slider to surface.

        Args:
            surface: pygame.Surface to render to
        """
        if not self.visible:
            return

        # Draw slider track (horizontal line)
        track_y = self.rect.centery
        pygame.draw.line(
            surface, (100, 100, 120), (self.rect.left, track_y), (self.rect.right, track_y), 2
        )

        # Draw slider handle (circle at current value position)
        normalized = (self._value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.left + normalized * self.rect.width
        pygame.draw.circle(surface, (100, 150, 255), (int(handle_x), track_y), 5)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle mouse events for dragging.

        Args:
            event: pygame.event.Event to handle
        """
        try:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hasattr(event, 'button') and hasattr(event, 'pos'):
                    if event.button == 1 and self.contains_point(event.pos[0], event.pos[1]):
                        self.dragging = True
                        self._update_value_from_position(event.pos[0])
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if hasattr(event, 'pos'):
                    if self.dragging:
                        self._update_value_from_position(event.pos[0])
        except Exception as e:
            logger.error(f"Slider event handling failed: {e}")

    def _update_value_from_position(self, x: int) -> None:
        """Update value based on mouse X position.

        Args:
            x: Mouse X coordinate
        """
        normalized = (x - self.rect.left) / self.rect.width
        normalized = max(0, min(1, normalized))
        self._value = self.min_val + normalized * (self.max_val - self.min_val)


class TextInput(UIComponent):
    """Text entry field with keyboard input support.

    An input field that accepts keyboard input when focused. Supports text
    selection, deletion, and maximum length enforcement.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        placeholder: str = "",
        max_length: int = 100,
    ):
        """Initialize text input.

        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            width: Width in pixels
            height: Height in pixels
            placeholder: Placeholder text (default "")
            max_length: Maximum characters (default 100)
        """
        super().__init__(x, y, width, height)
        self.placeholder = placeholder
        self.max_length = max_length
        self._text = ""
        self.focused = False

    @property
    def text(self) -> str:
        """Get current text.

        Returns:
            Current text content
        """
        return self._text

    @text.setter
    def text(self, val: str) -> None:
        """Set text input value.

        Args:
            val: Text to set (will be truncated to max_length)
        """
        self._text = val[:self.max_length]

    def render(self, surface: pygame.Surface) -> None:
        """Render text input to surface.

        Args:
            surface: pygame.Surface to render to
        """
        if not self.visible:
            return

        # Draw input background with color based on focus state
        color = (60, 70, 80) if self.focused else (40, 50, 60)
        pygame.draw.rect(surface, color, self.rect)

        # Draw input border
        border_color = (100, 150, 200) if self.focused else (80, 100, 120)
        pygame.draw.rect(surface, border_color, self.rect, 2)

        # Draw text or placeholder
        text_to_display = self._text if self._text else self.placeholder
        text_color = (220, 220, 230) if self._text else (150, 150, 170)

        # Simple text rendering using pygame font as fallback
        try:
            from src.ui.text_renderer import TextRenderer
            renderer = TextRenderer()
            text_surf, text_rect = renderer.render(text_to_display, text_color, size='normal')
            text_x = self.rect.x + 5
            text_y = self.rect.centery - text_rect.height // 2
            surface.blit(text_surf, (text_x, text_y))
        except Exception as e:
            pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle mouse and keyboard events.

        Args:
            event: pygame.event.Event to handle
        """
        try:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hasattr(event, 'button') and hasattr(event, 'pos'):
                    if event.button == 1:
                        self.focused = self.contains_point(event.pos[0], event.pos[1])
            elif event.type == pygame.KEYDOWN and self.focused:
                if event.key == pygame.K_BACKSPACE:
                    self._text = self._text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.focused = False
                elif hasattr(event, 'unicode') and len(self._text) < self.max_length:
                    if event.unicode.isprintable() and ord(event.unicode) < 128:
                        self._text += event.unicode
        except Exception as e:
            logger.error(f"TextInput event handling failed: {e}")


class Modal(UIComponent):
    """Overlay dialog for displaying content on top of main interface.

    A modal dialog that can contain other UI components and displays
    a semi-transparent overlay behind it.
    """

    def __init__(self, x: int, y: int, width: int, height: int, title: str = ""):
        """Initialize modal.

        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            width: Width in pixels
            height: Height in pixels
            title: Modal title (default "")
        """
        super().__init__(x, y, width, height)
        self.title = title
        self.components: List['UIComponent'] = []
        self.visible = False

    def add_component(self, component: "UIComponent") -> None:
        """Add a component to the modal.

        Args:
            component: UIComponent to add
        """
        self.components.append(component)

    def render(self, surface: pygame.Surface) -> None:
        """Render modal and all contained components.

        Args:
            surface: pygame.Surface to render to
        """
        if not self.visible:
            return

        # Draw semi-transparent overlay
        overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        # Draw modal background
        pygame.draw.rect(surface, (30, 40, 60), self.rect)
        pygame.draw.rect(surface, (100, 150, 255), self.rect, 3)

        # Draw title bar
        title_rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, 30)
        pygame.draw.rect(surface, (50, 70, 100), title_rect)

        # Render all components
        for component in self.components:
            component.render(surface)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events for all components in modal.

        Only passes events to modal components if modal is visible.

        Args:
            event: pygame.event.Event to handle
        """
        if not self.visible:
            return

        # Pass events to all modal components
        for component in self.components:
            component.handle_event(event)
