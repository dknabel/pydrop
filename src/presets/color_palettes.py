"""Color palettes for preset themes - RGB tuples with semantic meaning."""

# Each theme maps to a palette of 4-5 colors:
# (primary, secondary, accent1, accent2, [accent3])
THEME_PALETTES = {
    "abstract": {
        "name": "Grayscale with Soft Lavender",
        "colors": [(200, 200, 200), (100, 100, 100), (150, 140, 170), (220, 220, 220)]
    },
    "alchemical": {
        "name": "Deep Purple, Gold, Copper",
        "colors": [(75, 30, 120), (218, 165, 32), (184, 115, 51), (180, 50, 100)]
    },
    "atmospheric": {
        "name": "Soft Periwinkle, Misty Gray, Cool White",
        "colors": [(180, 170, 200), (180, 180, 190), (220, 220, 230), (150, 150, 170)]
    },
    "bioluminescent": {
        "name": "Soft Violet, Muted Lime, Soft Teal",
        "colors": [(180, 150, 200), (150, 180, 100), (120, 180, 180), (200, 180, 220)]
    },
    "celestial": {
        "name": "Deep Purple-Blue, Soft Lavender, Warm Cream",
        "colors": [(40, 50, 120), (180, 170, 200), (240, 230, 200), (100, 100, 180)]
    },
    "chromatic": {
        "name": "Soft Pastels: Dusty Rose, Sage, Periwinkle, Butter",
        "colors": [(220, 170, 170), (170, 190, 160), (200, 190, 220), (240, 230, 180)]
    },
    "core": {
        "name": "Warm Gray, Soft Gold, Sage Green",
        "colors": [(160, 150, 140), (200, 180, 120), (140, 160, 130), (180, 170, 160)]
    },
    "cosmic": {
        "name": "Deep Indigo, Rust, Deep Gold",
        "colors": [(30, 40, 80), (180, 90, 50), (200, 140, 30), (60, 70, 120)]
    },
    "crystalline": {
        "name": "Icy Lavender, Silver, Cool White",
        "colors": [(200, 190, 220), (200, 200, 210), (230, 230, 240), (180, 190, 220)]
    },
    "digital": {
        "name": "Crisp Sage, Cool White, Soft Purple-Gray",
        "colors": [(140, 160, 140), (230, 230, 230), (180, 180, 200), (160, 160, 180)]
    },
    "dimensional": {
        "name": "Warm Terracotta → Cool Violet (gradient)",
        "colors": [(200, 120, 80), (180, 100, 100), (150, 100, 150), (100, 80, 150)]
    },
    "ethereal": {
        "name": "Pale Lavender, Soft Peach, Cool White",
        "colors": [(220, 200, 230), (230, 190, 170), (240, 240, 240), (200, 190, 210)]
    },
    "infernal": {
        "name": "Deep Magenta-Red, Burnt Orange, Charcoal",
        "colors": [(180, 20, 80), (200, 90, 30), (50, 40, 40), (220, 60, 90)]
    },
    "kinetic": {
        "name": "Warm Sienna, Deep Rust, Gold",
        "colors": [(160, 80, 60), (180, 70, 50), (200, 140, 30), (140, 70, 50)]
    },
    "liquids": {
        "name": "Ocean Blue, Teal, Seafoam",
        "colors": [(30, 100, 180), (50, 150, 180), (100, 180, 160), (80, 160, 140)]
    },
    "mechanical": {
        "name": "Gunmetal, Cool Silver, Dark Slate",
        "colors": [(100, 110, 120), (180, 190, 200), (60, 70, 80), (140, 150, 160)]
    },
    "metamorphic": {
        "name": "Earthy Brown → Soft Violet",
        "colors": [(140, 100, 70), (160, 110, 130), (180, 120, 160), (120, 80, 140)]
    },
    "organic": {
        "name": "Moss Green, Warm Brown, Terracotta",
        "colors": [(80, 120, 70), (140, 110, 80), (180, 110, 80), (100, 140, 90)]
    },
    "psychedelic": {
        "name": "Soft Magenta, Dusty Purple, Sage",
        "colors": [(200, 120, 180), (160, 110, 160), (150, 140, 140), (180, 150, 200)]
    },
    "quantum": {
        "name": "Cool Indigo, Soft Violet, Pale Periwinkle",
        "colors": [(60, 80, 160), (180, 160, 200), (200, 190, 230), (80, 100, 180)]
    },
    "resonant": {
        "name": "Soft Purple, Sage, Warm Mauve",
        "colors": [(180, 150, 190), (150, 170, 140), (180, 140, 160), (170, 160, 180)]
    },
    "retro_aero": {
        "name": "Teal, Warm Gold, Soft Lavender, Cream",
        "colors": [(80, 160, 180), (200, 170, 80), (200, 180, 220), (240, 230, 210)]
    },
    "synesthetic": {
        "name": "Multi-tone: Coral, Lavender, Indigo, Gold",
        "colors": [(220, 140, 130), (200, 180, 220), (80, 80, 180), (200, 160, 80)]
    },
    "temporal": {
        "name": "Cool Violet-Gray → Warm Ochre",
        "colors": [(160, 140, 180), (180, 160, 140), (200, 140, 80), (140, 120, 160)]
    },
}

def get_palette(theme: str) -> dict:
    """Get color palette for a theme.

    Args:
        theme: Theme name (e.g., 'core', 'infernal')

    Returns:
        Dictionary with 'name' and 'colors' (list of RGB tuples)
    """
    return THEME_PALETTES.get(theme, THEME_PALETTES["core"])

def get_colors(theme: str) -> list:
    """Get just the RGB colors for a theme.

    Args:
        theme: Theme name

    Returns:
        List of (R, G, B) tuples
    """
    return get_palette(theme)["colors"]
