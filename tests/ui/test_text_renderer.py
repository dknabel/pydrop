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


def test_text_renderer_render_normal_size():
    """TextRenderer renders text with normal font size"""
    renderer = TextRenderer()
    surface, rect = renderer.render("Test", (255, 255, 255), size='normal')
    assert surface is not None
    assert rect is not None
    assert rect.width > 0
    assert rect.height > 0


def test_text_renderer_render_bold_size():
    """TextRenderer renders text with bold font size"""
    renderer = TextRenderer()
    surface, rect = renderer.render("Bold Test", (255, 255, 255), size='bold')
    assert surface is not None
    assert rect is not None
    assert rect.width > 0
    assert rect.height > 0


def test_text_renderer_render_small_size():
    """TextRenderer renders text with small font size"""
    renderer = TextRenderer()
    surface, rect = renderer.render("Small", (255, 255, 255), size='small')
    assert surface is not None
    assert rect is not None
    assert rect.width > 0
    assert rect.height > 0


def test_text_renderer_invalid_color_values_out_of_range():
    """TextRenderer raises ValueError for RGB values outside [0, 255]"""
    renderer = TextRenderer()
    with pytest.raises(ValueError, match="RGB values must be in range"):
        renderer.render("Test", (256, 255, 255))

    with pytest.raises(ValueError, match="RGB values must be in range"):
        renderer.render("Test", (255, -1, 255))

    with pytest.raises(ValueError, match="RGB values must be in range"):
        renderer.render("Test", (255, 255, 300))


def test_text_renderer_invalid_color_non_integer():
    """TextRenderer raises ValueError for non-integer RGB values"""
    renderer = TextRenderer()
    with pytest.raises(ValueError, match="RGB values must be in range"):
        renderer.render("Test", (255.5, 255, 255))

    with pytest.raises(ValueError, match="RGB values must be in range"):
        renderer.render("Test", ("255", 255, 255))


def test_text_renderer_valid_edge_case_colors():
    """TextRenderer handles valid edge case color values"""
    renderer = TextRenderer()
    # Test minimum valid value
    surface, rect = renderer.render("Test", (0, 0, 0))
    assert surface is not None

    # Test maximum valid value
    surface, rect = renderer.render("Test", (255, 255, 255))
    assert surface is not None

    # Test mixed values
    surface, rect = renderer.render("Test", (0, 128, 255))
    assert surface is not None


def test_text_renderer_cache_behavior():
    """TextRenderer caches results for identical parameters"""
    renderer = TextRenderer()
    surface1, rect1 = renderer.render("Test", (255, 255, 255), size='normal')
    surface2, rect2 = renderer.render("Test", (255, 255, 255), size='normal')

    # Should be the exact same objects from cache
    assert surface1 is surface2
    assert rect1 is rect2


def test_text_renderer_cache_different_sizes():
    """TextRenderer caches separately for different font sizes"""
    renderer = TextRenderer()
    surface_normal, _ = renderer.render("Test", (255, 255, 255), size='normal')
    surface_small, _ = renderer.render("Test", (255, 255, 255), size='small')
    surface_bold, _ = renderer.render("Test", (255, 255, 255), size='bold')

    # Should be different objects
    assert surface_normal is not surface_small
    assert surface_normal is not surface_bold
    assert surface_small is not surface_bold


def test_text_renderer_cache_different_colors():
    """TextRenderer caches separately for different colors"""
    renderer = TextRenderer()
    surface_white, _ = renderer.render("Test", (255, 255, 255))
    surface_red, _ = renderer.render("Test", (255, 0, 0))

    # Should be different objects
    assert surface_white is not surface_red


def test_text_renderer_empty_string():
    """TextRenderer handles empty strings"""
    renderer = TextRenderer()
    surface, rect = renderer.render("", (255, 255, 255))
    assert surface is not None
    assert rect is not None


def test_text_renderer_special_characters():
    """TextRenderer handles special characters"""
    renderer = TextRenderer()
    special_text = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    surface, rect = renderer.render(special_text, (255, 255, 255))
    assert surface is not None
    assert rect is not None


def test_text_renderer_unicode_characters():
    """TextRenderer handles unicode characters"""
    renderer = TextRenderer()
    unicode_text = "Hello 世界 🎵"
    surface, rect = renderer.render(unicode_text, (255, 255, 255))
    assert surface is not None
    assert rect is not None


def test_text_renderer_clear_cache():
    """TextRenderer can clear its cache"""
    renderer = TextRenderer()
    surface1, _ = renderer.render("Test", (255, 255, 255))
    renderer.clear_cache()
    surface2, _ = renderer.render("Test", (255, 255, 255))

    # After cache clear, should be different objects
    assert surface1 is not surface2
