# Preset Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enhance all 24 presets with cohesive color palettes, per-preset audio dimension mappings, and dynamic multi-dimensional audio reactivity.

**Architecture:** 
- Extend Preset model to include `colors` (RGB palette) and `audio_mapping` (audio dimension → visual control assignments)
- Create a color palette registry mapping theme names to curated RGB colors
- Update all 252 presets in presets.json with color and audio_mapping data
- Enhance audio engine to expose multi-dimensional audio (bass/mid/treble/amplitude) consistently
- Update shader uniforms to accept mapped audio dimensions for dynamic animation

**Tech Stack:** Python (preset model, JSON generation), JSON (preset data), GLSL (shader uniforms for audio reactivity)

---

## File Structure

**Files to Create:**
- `src/presets/color_palettes.py` — Color palette registry for all themes

**Files to Modify:**
- `src/ui/models.py` — Add `colors` and `audio_mapping` fields to Preset dataclass
- `src/presets/presets.json` — Add color and audio_mapping data to all 252 presets
- `src/audio_engine.py` — Ensure bass/mid/treble/amplitude are accessible
- `src/visualizer.py` — Pass audio mappings to shader uniforms

---

## Tasks

### Task 1: Create Color Palette Registry

**Files:**
- Create: `src/presets/color_palettes.py`

- [ ] **Step 1: Create color_palettes.py with theme-to-palette mapping**

```python
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
```

- [ ] **Step 2: Commit the color palette registry**

```bash
git add src/presets/color_palettes.py
git commit -m "feat: add color palette registry for all 24 themes"
```

---

### Task 2: Extend Preset Model with Colors and Audio Mapping

**Files:**
- Modify: `src/ui/models.py` (Preset class, lines 9-67)

- [ ] **Step 1: Update Preset dataclass to include colors and audio_mapping**

Replace the Preset class definition (lines 9-66) with:

```python
@dataclass
class Preset:
    """Built-in preset metadata with audio reactivity configuration.

    Represents a preset that comes with the application. Contains metadata
    about the preset such as theme, shader path, color palette, and audio
    dimension mappings for dynamic animation control.

    Attributes:
        id: Unique integer identifier for the preset
        name: Display name of the preset
        theme: Theme category (e.g., 'core', 'cyberpunk')
        description: Human-readable description of the preset
        shader: Path to the shader file used by this preset
        tags: List of tags for categorization (default: [])
        difficulty: Difficulty level: 'easy', 'medium', 'hard' (default: 'medium')
        colors: List of 4 RGB tuples defining the color palette
        audio_mapping: Dict mapping audio dimensions to visual controls
    """

    id: int
    name: str
    theme: str
    description: str
    shader: str
    tags: List[str] = field(default_factory=list)
    difficulty: str = "medium"
    colors: List[tuple] = field(default_factory=lambda: [(100, 100, 100), (150, 150, 150), (200, 200, 200), (180, 180, 180)])
    audio_mapping: Dict[str, str] = field(default_factory=lambda: {
        "amplitude": "intensity",
        "bass": "scale",
        "mid": "rotation",
        "treble": "glow"
    })

    def to_dict(self) -> Dict[str, Any]:
        """Convert preset to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the preset
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Preset":
        """Create preset from dictionary.

        Args:
            data: Dictionary containing preset data

        Returns:
            Preset instance

        Raises:
            ValueError: If required fields are missing
        """
        try:
            colors = data.get('colors', [(100, 100, 100), (150, 150, 150), (200, 200, 200), (180, 180, 180)])
            # Convert color lists to tuples if needed
            colors = [tuple(c) if isinstance(c, list) else c for c in colors]
            
            return cls(
                id=data['id'],
                name=data['name'],
                theme=data['theme'],
                description=data['description'],
                shader=data['shader'],
                tags=data.get('tags', []),
                difficulty=data.get('difficulty', 'medium'),
                colors=colors,
                audio_mapping=data.get('audio_mapping', {
                    "amplitude": "intensity",
                    "bass": "scale",
                    "mid": "rotation",
                    "treble": "glow"
                })
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")
```

- [ ] **Step 2: Verify the Preset class changes compile**

```bash
cd /home/drew/Documents/audiovisualizerpy
python -c "from src.ui.models import Preset; print('Preset model updated successfully')"
```

Expected: `Preset model updated successfully`

- [ ] **Step 3: Commit the model changes**

```bash
git add src/ui/models.py
git commit -m "feat: extend Preset model with colors and audio_mapping fields"
```

---

### Task 3: Generate Audio Mappings for All Presets

**Files:**
- Create: `scripts/generate_preset_mappings.py` (temporary build script)

- [ ] **Step 1: Create a script to assign audio mappings per theme**

```python
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
    from pathlib import Path
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
```

- [ ] **Step 2: Run the script to update presets.json**

```bash
cd /home/drew/Documents/audiovisualizerpy
python scripts/generate_preset_mappings.py
```

Expected: `Updated 252 presets with colors and audio mappings`

- [ ] **Step 3: Verify a few presets were updated correctly**

```bash
python -c "
import json
with open('src/presets/presets.json') as f:
    p = json.load(f)
    for i in [0, 50, 100, 150, 200, 251]:
        print(f\"Preset {i}: {p[i]['name']}\")
        print(f\"  colors: {p[i]['colors'][:2]}\")
        print(f\"  audio_mapping: {p[i]['audio_mapping']}\")
"
```

Expected: Shows updated presets with colors and audio_mapping fields

- [ ] **Step 4: Commit the presets.json update**

```bash
git add src/presets/presets.json scripts/generate_preset_mappings.py
git commit -m "feat: add colors and audio mappings to all 252 presets"
```

---

### Task 4: Update Audio Engine to Expose Multi-Dimensional Audio

**Files:**
- Modify: `src/audio_engine.py` (ensure amplitude, bass, mid, treble are consistently named properties)

- [ ] **Step 1: Verify audio dimensions are accessible**

Check that the AudioEngine class has these properties accessible:
- `self.amplitude` (overall volume)
- `self.bass` (low frequencies)
- `self.mid` (mid frequencies)
- `self.treble` (high frequencies)

If already present, skip to step 2. If not, they're in `_analyze_audio()` and already set as instance variables, so they're accessible.

- [ ] **Step 2: Create a method to get all audio dimensions as a dict**

Add this method to AudioEngine class in `src/audio_engine.py` after the `_analyze_audio` method:

```python
def get_audio_dimensions(self) -> dict:
    """Get all audio dimensions as a dictionary.
    
    Returns:
        Dict with keys: 'amplitude', 'bass', 'mid', 'treble'
        Values are floats in range [0.0, 1.0]
    """
    return {
        'amplitude': self.amplitude,
        'bass': self.bass,
        'mid': self.mid,
        'treble': self.treble
    }
```

- [ ] **Step 3: Verify compilation**

```bash
python -c "from src.audio_engine import AudioEngine; print('AudioEngine updated')"
```

Expected: `AudioEngine updated`

- [ ] **Step 4: Commit the audio engine changes**

```bash
git add src/audio_engine.py
git commit -m "feat: add get_audio_dimensions() method to AudioEngine"
```

---

### Task 5: Update Visualizer to Use Audio Mappings

**Files:**
- Modify: `src/visualizer.py` (rendering loop, shader uniform setup)

- [ ] **Step 1: Find where presets are applied in visualizer.py**

Search for where the preset is used:

```bash
grep -n "preset\|shader\|uniform" /home/drew/Documents/audiovisualizerpy/src/visualizer.py | head -20
```

Look for the rendering section that sets shader uniforms.

- [ ] **Step 2: Add audio mapping to the render call**

When setting up shader uniforms, add code to apply audio mappings. The exact location depends on current structure, but it should be near where other uniforms are set. Add:

```python
# Get audio dimensions
audio_dims = self.audio_manager.get_audio_dimensions()

# Get preset's audio mapping
preset = self.get_preset(self.current_preset_name)
audio_mapping = preset.get('audio_mapping', {})

# Map audio dimensions to shader uniforms based on preset's mapping
for audio_dim, visual_control in audio_mapping.items():
    audio_value = audio_dims.get(audio_dim, 0.0)
    
    # Set appropriate uniform based on visual control name
    if visual_control == "intensity":
        glUniform1f(glGetUniformLocation(shader, "intensity"), audio_value)
    elif visual_control == "scale":
        glUniform1f(glGetUniformLocation(shader, "scale"), 1.0 + audio_value * 0.5)
    elif visual_control == "rotation":
        glUniform1f(glGetUniformLocation(shader, "rotation_speed"), audio_value * 2.0)
    elif visual_control == "glow":
        glUniform1f(glGetUniformLocation(shader, "glow_intensity"), audio_value)
    # Add more mappings as needed...
```

- [ ] **Step 3: Get the current visualizer structure and update it properly**

Read the visualizer.py render method to understand the exact structure, then update appropriately based on the current code.

```bash
grep -A 30 "def.*render\|def updateFrame" /home/drew/Documents/audiovisualizerpy/src/visualizer.py | head -50
```

- [ ] **Step 4: Commit visualizer changes**

```bash
git add src/visualizer.py
git commit -m "feat: apply audio mappings to shader uniforms for dynamic reactivity"
```

---

### Task 6: Test Preset Enhancement

**Files:**
- Test: Run the application and verify presets work with colors and audio reactivity

- [ ] **Step 1: Run the application**

```bash
cd /home/drew/Documents/audiovisualizerpy
timeout 5 python main.py || true
```

Expected: App starts without errors

- [ ] **Step 2: Verify presets load successfully**

```bash
python -c "
from src.ui.presets_data import PresetManager
pm = PresetManager()
print(f'Loaded {len(pm.builtin_presets)} presets')
p = pm.builtin_presets[0]
print(f'First preset: {p.name}')
print(f'  Colors: {p.colors}')
print(f'  Audio mapping: {p.audio_mapping}')
"
```

Expected: Shows preset with colors and audio_mapping

- [ ] **Step 3: Commit final changes and push to GitHub**

```bash
git add -A
git commit -m "test: verify preset enhancements load correctly"
git push origin master
```

---

## Success Criteria

- ✓ All 252 presets have color palettes matching their theme
- ✓ All presets have audio dimension mappings defined
- ✓ Preset model extends to include colors and audio_mapping
- ✓ Audio engine exposes amplitude/bass/mid/treble consistently
- ✓ Visualizer applies audio mappings to control animation dynamically
- ✓ Application loads without errors
- ✓ Changes committed and pushed to GitHub
