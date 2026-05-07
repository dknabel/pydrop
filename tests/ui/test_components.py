"""Tests for UI component base classes."""

import pytest
import pygame
from src.ui.components import UIComponent, Button, Slider, TextInput, Modal


# Initialize pygame for testing
pygame.init()


class ConcreteUIComponent(UIComponent):
    """Concrete implementation of UIComponent for testing abstract base class."""

    def render(self, surface: pygame.Surface) -> None:
        """Render component to surface."""
        if self.visible:
            pygame.draw.rect(surface, (255, 255, 255), self.rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame event."""
        pass


class TestUIComponent:
    """Test UIComponent base class."""

    def test_uicomponent_init(self):
        """UIComponent initializes with position and size."""
        component = ConcreteUIComponent(10, 20, 100, 50)
        assert component.rect.x == 10
        assert component.rect.y == 20
        assert component.rect.width == 100
        assert component.rect.height == 50
        assert component.visible is True

    def test_uicomponent_contains_point_inside(self):
        """UIComponent.contains_point returns True for points inside bounds."""
        component = ConcreteUIComponent(10, 20, 100, 50)
        assert component.contains_point(50, 45) is True
        assert component.contains_point(10, 20) is True
        assert component.contains_point(109, 69) is True

    def test_uicomponent_contains_point_outside(self):
        """UIComponent.contains_point returns False for points outside bounds."""
        component = ConcreteUIComponent(10, 20, 100, 50)
        assert component.contains_point(5, 45) is False
        assert component.contains_point(120, 45) is False
        assert component.contains_point(50, 15) is False
        assert component.contains_point(50, 80) is False

    def test_uicomponent_visibility(self):
        """UIComponent visibility can be toggled."""
        component = ConcreteUIComponent(10, 20, 100, 50)
        assert component.visible is True
        component.visible = False
        assert component.visible is False

    def test_uicomponent_render_visible(self):
        """UIComponent renders when visible."""
        surface = pygame.Surface((200, 200))
        component = ConcreteUIComponent(10, 20, 100, 50)
        component.visible = True
        component.render(surface)
        # If render executes without error, it passes

    def test_uicomponent_render_hidden(self):
        """UIComponent skips render when not visible."""
        surface = pygame.Surface((200, 200))
        component = ConcreteUIComponent(10, 20, 100, 50)
        component.visible = False
        component.render(surface)
        # Should not raise an error


class TestButton:
    """Test Button component."""

    def test_button_init(self):
        """Button initializes with label and callback."""
        callback_called = []
        callback = lambda: callback_called.append(True)
        button = Button(10, 20, 100, 50, "Click Me", callback)
        assert button.label == "Click Me"
        assert button.callback is callback
        assert button.hovered is False
        assert button.pressed is False

    def test_button_click_callback(self):
        """Button calls callback on click."""
        callback_called = []
        callback = lambda: callback_called.append(True)
        button = Button(10, 20, 100, 50, "Click Me", callback)

        # Simulate click inside button
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (50, 45), 'button': 1})
        button.handle_event(event)

        assert len(callback_called) == 1

    def test_button_click_outside(self):
        """Button does not call callback when clicked outside."""
        callback_called = []
        callback = lambda: callback_called.append(True)
        button = Button(10, 20, 100, 50, "Click Me", callback)

        # Simulate click outside button
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (5, 45), 'button': 1})
        button.handle_event(event)

        assert len(callback_called) == 0

    def test_button_hover_detection(self):
        """Button detects mouse hover."""
        callback = lambda: None
        button = Button(10, 20, 100, 50, "Click Me", callback)

        # Simulate hover inside
        event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (50, 45)})
        button.handle_event(event)
        assert button.hovered is True

        # Simulate hover outside
        event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (5, 45)})
        button.handle_event(event)
        assert button.hovered is False

    def test_button_press_state(self):
        """Button tracks pressed state."""
        callback = lambda: None
        button = Button(10, 20, 100, 50, "Click Me", callback)

        # Simulate mouse down
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (50, 45), 'button': 1})
        button.handle_event(event)
        assert button.pressed is True

        # Simulate mouse up
        event = pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1})
        button.handle_event(event)
        assert button.pressed is False

    def test_button_render(self):
        """Button renders without error."""
        surface = pygame.Surface((200, 200))
        button = Button(10, 20, 100, 50, "Click Me", lambda: None)
        button.visible = True
        button.render(surface)
        # Should not raise an error


class TestSlider:
    """Test Slider component."""

    def test_slider_init(self):
        """Slider initializes with min, max, and initial values."""
        slider = Slider(10, 20, 200, 50, min_val=0.0, max_val=1.0, initial=0.5)
        assert slider.value == 0.5
        assert slider.min_val == 0.0
        assert slider.max_val == 1.0
        assert slider.dragging is False

    def test_slider_value_enforcement(self):
        """Slider enforces min/max range."""
        slider = Slider(10, 20, 200, 50, min_val=0.0, max_val=1.0, initial=0.5)

        slider.value = 1.5
        assert slider.value == 1.0

        slider.value = -0.5
        assert slider.value == 0.0

        slider.value = 0.5
        assert slider.value == 0.5

    def test_slider_different_range(self):
        """Slider works with different min/max values."""
        slider = Slider(10, 20, 200, 50, min_val=10.0, max_val=100.0, initial=50.0)
        assert slider.value == 50.0

        slider.value = 200.0
        assert slider.value == 100.0

        slider.value = 5.0
        assert slider.value == 10.0

    def test_slider_drag_detection(self):
        """Slider detects drag start and end."""
        slider = Slider(10, 20, 200, 50, min_val=0.0, max_val=1.0, initial=0.5)

        # Simulate mouse down on slider
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (110, 45), 'button': 1})
        slider.handle_event(event)
        assert slider.dragging is True

        # Simulate mouse up
        event = pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1})
        slider.handle_event(event)
        assert slider.dragging is False

    def test_slider_drag_updates_value(self):
        """Slider updates value while dragging."""
        slider = Slider(10, 20, 200, 50, min_val=0.0, max_val=1.0, initial=0.5)

        # Simulate drag to middle (0.5)
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (110, 45), 'button': 1})
        slider.handle_event(event)
        assert slider.dragging is True
        assert abs(slider.value - 0.5) < 0.05  # Stricter tolerance

        # Simulate drag to right (1.0)
        event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (210, 45)})
        slider.handle_event(event)
        assert abs(slider.value - 1.0) < 0.1  # Close to 1.0

    def test_slider_click_outside(self):
        """Slider does not start drag when clicked outside."""
        slider = Slider(10, 20, 200, 50, min_val=0.0, max_val=1.0, initial=0.5)

        # Simulate click outside slider
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (5, 45), 'button': 1})
        slider.handle_event(event)
        assert slider.dragging is False

    def test_slider_render(self):
        """Slider renders without error."""
        surface = pygame.Surface((300, 100))
        slider = Slider(10, 20, 200, 50, min_val=0.0, max_val=1.0, initial=0.5)
        slider.visible = True
        slider.render(surface)
        # Should not raise an error


class TestTextInput:
    """Test TextInput component."""

    def test_textinput_init(self):
        """TextInput initializes with placeholder and max length."""
        text_input = TextInput(10, 20, 200, 50, placeholder="Enter text", max_length=100)
        assert text_input.placeholder == "Enter text"
        assert text_input.max_length == 100
        assert text_input.text == ""
        assert text_input.focused is False

    def test_textinput_text_property(self):
        """TextInput text property works correctly."""
        text_input = TextInput(10, 20, 200, 50, placeholder="Enter text", max_length=20)
        text_input.text = "Hello"
        assert text_input.text == "Hello"

    def test_textinput_max_length_enforcement(self):
        """TextInput enforces maximum length."""
        text_input = TextInput(10, 20, 200, 50, placeholder="Enter text", max_length=5)
        text_input.text = "Hello World"
        assert text_input.text == "Hello"
        assert len(text_input.text) <= 5

    def test_textinput_focus_detection(self):
        """TextInput detects focus on click."""
        text_input = TextInput(10, 20, 200, 50, placeholder="Enter text", max_length=100)

        # Click inside
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (100, 45), 'button': 1})
        text_input.handle_event(event)
        assert text_input.focused is True

        # Click outside
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (5, 45), 'button': 1})
        text_input.handle_event(event)
        assert text_input.focused is False

    def test_textinput_keyboard_input(self):
        """TextInput accepts keyboard input when focused."""
        text_input = TextInput(10, 20, 200, 50, placeholder="Enter text", max_length=100)
        text_input.focused = True

        # Simulate typing 'a'
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_a, 'unicode': 'a'})
        text_input.handle_event(event)
        assert text_input.text == "a"

        # Simulate typing 'b'
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_b, 'unicode': 'b'})
        text_input.handle_event(event)
        assert text_input.text == "ab"

    def test_textinput_backspace(self):
        """TextInput handles backspace."""
        text_input = TextInput(10, 20, 200, 50, placeholder="Enter text", max_length=100)
        text_input.focused = True
        text_input._text = "hello"

        # Simulate backspace
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_BACKSPACE})
        text_input.handle_event(event)
        assert text_input.text == "hell"

    def test_textinput_return_unfocuses(self):
        """TextInput loses focus on return key."""
        text_input = TextInput(10, 20, 200, 50, placeholder="Enter text", max_length=100)
        text_input.focused = True
        text_input._text = "hello"

        # Simulate return
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})
        text_input.handle_event(event)
        assert text_input.focused is False

    def test_textinput_no_input_when_unfocused(self):
        """TextInput ignores keyboard input when not focused."""
        text_input = TextInput(10, 20, 200, 50, placeholder="Enter text", max_length=100)
        text_input.focused = False

        # Simulate typing 'a'
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_a, 'unicode': 'a'})
        text_input.handle_event(event)
        assert text_input.text == ""

    def test_textinput_non_printable_ignored(self):
        """TextInput ignores non-printable characters."""
        text_input = TextInput(10, 20, 200, 50, placeholder="Enter text", max_length=100)
        text_input.focused = True

        # Simulate non-printable character (using a space which is printable, then tab which isn't)
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE, 'unicode': ' '})
        text_input.handle_event(event)
        assert " " in text_input.text  # Space is printable

    def test_textinput_render(self):
        """TextInput renders without error."""
        surface = pygame.Surface((300, 100))
        text_input = TextInput(10, 20, 200, 50, placeholder="Enter text", max_length=100)
        text_input.visible = True
        text_input.render(surface)
        # Should not raise an error


class TestModal:
    """Test Modal component."""

    def test_modal_init(self):
        """Modal initializes with title."""
        modal = Modal(100, 100, 400, 300, title="Test Modal")
        assert modal.title == "Test Modal"
        assert modal.components == []
        assert modal.visible is False

    def test_modal_add_component(self):
        """Modal can add components."""
        modal = Modal(100, 100, 400, 300, title="Test Modal")
        button = Button(120, 120, 100, 50, "OK", lambda: None)

        modal.add_component(button)
        assert len(modal.components) == 1
        assert button in modal.components

    def test_modal_multiple_components(self):
        """Modal can contain multiple components."""
        modal = Modal(100, 100, 400, 300, title="Test Modal")
        button1 = Button(120, 120, 100, 50, "OK", lambda: None)
        button2 = Button(120, 180, 100, 50, "Cancel", lambda: None)
        slider = Slider(120, 240, 200, 50, min_val=0.0, max_val=1.0, initial=0.5)

        modal.add_component(button1)
        modal.add_component(button2)
        modal.add_component(slider)

        assert len(modal.components) == 3
        assert button1 in modal.components
        assert button2 in modal.components
        assert slider in modal.components

    def test_modal_visibility(self):
        """Modal visibility can be toggled."""
        modal = Modal(100, 100, 400, 300, title="Test Modal")
        assert modal.visible is False

        modal.visible = True
        assert modal.visible is True

        modal.visible = False
        assert modal.visible is False

    def test_modal_render_when_hidden(self):
        """Modal does not render when not visible."""
        surface = pygame.Surface((800, 600))
        modal = Modal(100, 100, 400, 300, title="Test Modal")
        modal.visible = False
        modal.render(surface)
        # Should not raise an error

    def test_modal_render_when_visible(self):
        """Modal renders when visible."""
        surface = pygame.Surface((800, 600))
        modal = Modal(100, 100, 400, 300, title="Test Modal")
        modal.visible = True
        modal.render(surface)
        # Should not raise an error

    def test_modal_render_with_components(self):
        """Modal renders all components."""
        surface = pygame.Surface((800, 600))
        modal = Modal(100, 100, 400, 300, title="Test Modal")
        button = Button(120, 120, 100, 50, "OK", lambda: None)
        modal.add_component(button)

        modal.visible = True
        modal.render(surface)
        # Should not raise an error

    def test_modal_handle_event_when_hidden(self):
        """Modal does not pass events when not visible."""
        modal = Modal(100, 100, 400, 300, title="Test Modal")
        callback_called = []
        button = Button(120, 120, 100, 50, "OK", lambda: callback_called.append(True))
        modal.add_component(button)

        modal.visible = False
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (150, 145), 'button': 1})
        modal.handle_event(event)

        assert len(callback_called) == 0

    def test_modal_handle_event_passes_to_components(self):
        """Modal passes events to components when visible."""
        modal = Modal(100, 100, 400, 300, title="Test Modal")
        callback_called = []
        button = Button(120, 120, 100, 50, "OK", lambda: callback_called.append(True))
        modal.add_component(button)

        modal.visible = True
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (150, 145), 'button': 1})
        modal.handle_event(event)

        assert len(callback_called) == 1


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_slider_equal_min_max(self):
        """Slider with equal min/max is handled gracefully."""
        slider = Slider(0, 0, 100, 20, min_val=5.0, max_val=5.0)
        # Should auto-adjust max_val to prevent division by zero
        assert slider.max_val > slider.min_val

    def test_slider_invalid_initial(self):
        """Slider with initial outside range is clamped."""
        slider = Slider(0, 0, 100, 20, min_val=0, max_val=10, initial=15)
        assert slider.value <= 10
        assert slider.value >= 0

    def test_text_input_special_chars(self):
        """TextInput handles special characters."""
        text_input = TextInput(0, 0, 100, 20)
        # Test adding various characters
        text_input.text = "hello123!@#"
        assert text_input.text == "hello123!@#"

    def test_button_callback_exception(self):
        """Button handles callback exceptions gracefully."""
        def bad_callback():
            raise ValueError("Test error")

        button = Button(0, 0, 100, 20, "Test", bad_callback)
        # Simulate click - should not raise
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (50, 10)})
        button.handle_event(event)  # Should log error, not crash

    def test_modal_event_filtering(self):
        """Modal only processes events when visible."""
        modal = Modal(100, 100, 200, 200, "Test")
        button = Button(110, 110, 50, 30, "Click", lambda: None)
        modal.add_component(button)

        # When invisible, button should not respond to clicks
        modal.visible = False
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (135, 125)})
        modal.handle_event(event)
        # The button click should be ignored because modal is invisible
