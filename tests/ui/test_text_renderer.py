import pytest
from src.ui.text_renderer import TextRenderer


def test_text_renderer_init():
    """TextRenderer initializes with default font"""
    renderer = TextRenderer()
    assert renderer.font_size_normal == 14
    assert renderer.font_size_bold == 16
    assert renderer.font_size_small == 10


def test_text_renderer_render():
    """TextRenderer renders text to pygame-compatible surface"""
    renderer = TextRenderer()
    surface, rect = renderer.render("Test", (255, 255, 255))
    assert surface is not None
    assert rect is not None
    assert rect.width > 0
    assert rect.height > 0
