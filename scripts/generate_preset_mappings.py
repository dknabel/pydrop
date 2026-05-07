"""Generate audio dimension mappings for each preset theme."""

# Audio mapping templates for each theme
# Maps audio dimension (amplitude/bass/mid/treble) to visual control (scale/rotation/glow/etc)
AUDIO_MAPPINGS = {
    "abstract": {"amplitude": "glow", "bass": "scale", "mid": "rotation", "treble": "color_shift"},
    "alchemical": {"amplitude": "intensity", "bass": "scale", "mid": "rotation", "treble": "sparkle"},
    "atmospheric": {"amplitude": "opacity", "bass": "sway", "mid": "color_shift", "treble": "glow"},
    "bioluminescent": {"amplitude": "glow", "bass": "scale", "mid": "pulse", "treble": "color_shift"},
    "celestial": {"amplitude": "brightness", "bass": "sway", "mid": "rotation", "treble": "twinkle"},
    "chromatic": {"amplitude": "intensity", "bass": "color_shift", "mid": "rotation", "treble": "glow"},
    "core": {"amplitude": "intensity", "bass": "scale", "mid": "rotation", "treble": "glow"},
    "cosmic": {"amplitude": "brightness", "bass": "scale", "mid": "rotation", "treble": "twinkle"},
    "crystalline": {"amplitude": "glow", "bass": "scale", "mid": "rotation", "treble": "sparkle"},
    "digital": {"amplitude": "intensity", "bass": "scale", "mid": "rotation", "treble": "pulse"},
    "dimensional": {"amplitude": "depth", "bass": "scale", "mid": "rotation", "treble": "color_shift"},
    "ethereal": {"amplitude": "opacity", "bass": "sway", "mid": "glow", "treble": "color_shift"},
    "infernal": {"amplitude": "heat", "bass": "intensity", "mid": "rotation", "treble": "spark_emission"},
    "kinetic": {"amplitude": "speed", "bass": "scale", "mid": "rotation", "treble": "particle_density"},
    "liquids": {"amplitude": "flow_intensity", "bass": "wave_height", "mid": "ripple_frequency", "treble": "color_shift"},
    "mechanical": {"amplitude": "speed", "bass": "scale", "mid": "rotation", "treble": "grinding"},
    "metamorphic": {"amplitude": "transform_rate", "bass": "scale", "mid": "rotation", "treble": "morph_intensity"},
    "organic": {"amplitude": "growth_rate", "bass": "scale", "mid": "sway", "treble": "color_shift"},
    "psychedelic": {"amplitude": "intensity", "bass": "scale", "mid": "kaleidoscope_rotation", "treble": "color_shift"},
    "quantum": {"amplitude": "probability_intensity", "bass": "scale", "mid": "rotation", "treble": "quantum_flicker"},
    "resonant": {"amplitude": "resonance", "bass": "fundamental", "mid": "harmonic", "treble": "overtone"},
    "retro_aero": {"amplitude": "brightness", "bass": "scale", "mid": "rotation", "treble": "glow"},
    "synesthetic": {"amplitude": "intensity", "bass": "color_a", "mid": "color_b", "treble": "color_c"},
    "temporal": {"amplitude": "time_flow", "bass": "past_intensity", "mid": "present_intensity", "treble": "future_intensity"},
}

def get_mapping(theme: str) -> dict:
    """Get audio mapping for a theme."""
    return AUDIO_MAPPINGS.get(theme, AUDIO_MAPPINGS["core"])

if __name__ == "__main__":
    import json
    import sys
    from pathlib import Path

    # Add project root to path
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from src.presets.color_palettes import get_colors

    # Load current presets.json
    presets_file = Path("src/presets/presets.json")
    with open(presets_file, 'r') as f:
        presets = json.load(f)

    # Add colors and audio_mapping to each preset
    for preset in presets:
        theme = preset.get('theme', 'core')
        preset['colors'] = list(get_colors(theme))
        preset['audio_mapping'] = get_mapping(theme)

    # Write back
    with open(presets_file, 'w') as f:
        json.dump(presets, f, indent=2)

    print(f"Updated {len(presets)} presets with colors and audio mappings")
