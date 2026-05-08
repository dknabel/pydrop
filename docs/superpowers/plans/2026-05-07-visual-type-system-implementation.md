# Visual Type System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace 252 generic colored-static presets with 16 focused presets organized into 4 unique visual types, each with its own shader implementation.

**Architecture:** 
- Create new minimal presets.json with 16 presets mapped to 4 visual types (particles, geometric, turbulent, ethereal)
- Implement 4 new shader files, one per visual type, with unique visual forms and audio-responsive behavior
- Update Preset model to include visual_type field
- Update visualizer to route presets to correct shaders based on visual_type
- Archive/remove old preset data

**Tech Stack:** Python (preset management), GLSL (shaders), JSON (preset data)

---

## File Structure

**Files to Create:**
- `src/shaders/particles.glsl` — Particle system shader
- `src/shaders/geometric.glsl` — Geometry deformation shader
- `src/shaders/turbulent.glsl` — Fluid/turbulence shader
- `src/shaders/ethereal.glsl` — Volumetric/atmospheric shader
- `src/presets/presets.json` (new) — 16 minimal presets

**Files to Modify:**
- `src/ui/models.py` — Add visual_type field to Preset
- `src/visualizer.py` — Route presets to correct shaders
- `.gitignore` — Archive old presets backup

**Files to Archive:**
- `src/presets/presets.json` (old) — Backup as presets.json.bak
- `src/presets/*.py` — Archive theme definition files

---

## Tasks

### Task 1: Update Preset Model with Visual Type Field

**Files:**
- Modify: `src/ui/models.py` (Preset class)

- [ ] **Step 1: Add visual_type field to Preset dataclass**

In `src/ui/models.py`, find the Preset class and add the visual_type field after the `difficulty` field:

```python
visual_type: str = "particles"  # Default visual type
```

The updated Preset class fields should be:
```python
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
visual_type: str = "particles"
```

- [ ] **Step 2: Update from_dict() to handle visual_type**

In the `from_dict()` classmethod, add this line when constructing the Preset:

```python
visual_type=data.get('visual_type', 'particles'),
```

Add it as the last parameter before the closing parenthesis in the `cls(...)` call.

- [ ] **Step 3: Test the model**

```bash
python -c "from src.ui.models import Preset; p = Preset(id=0, name='Test', theme='core', description='test', shader='test', visual_type='geometric'); print(f'Preset created with visual_type: {p.visual_type}')"
```

Expected: `Preset created with visual_type: geometric`

- [ ] **Step 4: Commit**

```bash
git add src/ui/models.py
git commit -m "feat: add visual_type field to Preset model"
```

---

### Task 2: Create New Minimal Presets JSON

**Files:**
- Create: `src/presets/presets.json` (new)

- [ ] **Step 1: Create the new presets.json file**

Create `src/presets/presets.json` with these 16 presets:

```json
[
  {
    "id": 0,
    "name": "Kinetic",
    "theme": "kinetic",
    "visual_type": "particles",
    "description": "Fast, dense particle clouds responding to rhythm",
    "shader": "particles",
    "tags": ["particles", "energetic"],
    "difficulty": "medium",
    "colors": [[160, 80, 60], [180, 70, 50], [200, 140, 30], [140, 70, 50]],
    "audio_mapping": {"amplitude": "intensity", "bass": "density", "mid": "speed", "treble": "spread"}
  },
  {
    "id": 1,
    "name": "Resonant",
    "theme": "resonant",
    "visual_type": "particles",
    "description": "Particles arranged in harmonic patterns",
    "shader": "particles",
    "tags": ["particles", "harmonic"],
    "difficulty": "medium",
    "colors": [[180, 150, 190], [150, 170, 140], [180, 140, 160], [170, 160, 180]],
    "audio_mapping": {"amplitude": "resonance", "bass": "fundamental", "mid": "harmonic", "treble": "overtone"}
  },
  {
    "id": 2,
    "name": "Digital",
    "theme": "digital",
    "visual_type": "particles",
    "description": "Sharp, geometric particle behavior",
    "shader": "particles",
    "tags": ["particles", "digital"],
    "difficulty": "medium",
    "colors": [[140, 160, 140], [230, 230, 230], [180, 180, 200], [160, 160, 180]],
    "audio_mapping": {"amplitude": "intensity", "bass": "scale", "mid": "rotation", "treble": "pulse"}
  },
  {
    "id": 3,
    "name": "Temporal",
    "theme": "temporal",
    "visual_type": "particles",
    "description": "Particles flowing through time-based patterns",
    "shader": "particles",
    "tags": ["particles", "temporal"],
    "difficulty": "medium",
    "colors": [[160, 140, 180], [180, 160, 140], [200, 140, 80], [140, 120, 160]],
    "audio_mapping": {"amplitude": "time_flow", "bass": "past_intensity", "mid": "present_intensity", "treble": "future_intensity"}
  },
  {
    "id": 4,
    "name": "Crystalline",
    "theme": "crystalline",
    "visual_type": "geometric",
    "description": "Ice-like lattice structures with smooth deformation",
    "shader": "geometric",
    "tags": ["geometric", "crystalline"],
    "difficulty": "medium",
    "colors": [[200, 190, 220], [200, 200, 210], [230, 230, 240], [180, 190, 220]],
    "audio_mapping": {"amplitude": "glow", "bass": "scale", "mid": "rotation", "treble": "sparkle"}
  },
  {
    "id": 5,
    "name": "Mechanical",
    "theme": "mechanical",
    "visual_type": "geometric",
    "description": "Industrial grid and gear-like forms",
    "shader": "geometric",
    "tags": ["geometric", "mechanical"],
    "difficulty": "medium",
    "colors": [[100, 110, 120], [180, 190, 200], [60, 70, 80], [140, 150, 160]],
    "audio_mapping": {"amplitude": "speed", "bass": "scale", "mid": "rotation", "treble": "grinding"}
  },
  {
    "id": 6,
    "name": "Dimensional",
    "theme": "dimensional",
    "visual_type": "geometric",
    "description": "Tesseract and higher-dimensional geometry",
    "shader": "geometric",
    "tags": ["geometric", "dimensional"],
    "difficulty": "medium",
    "colors": [[200, 120, 80], [180, 100, 100], [150, 100, 150], [100, 80, 150]],
    "audio_mapping": {"amplitude": "depth", "bass": "scale", "mid": "rotation", "treble": "color_shift"}
  },
  {
    "id": 7,
    "name": "Abstract",
    "theme": "abstract",
    "visual_type": "geometric",
    "description": "Minimalist geometric arrangements",
    "shader": "geometric",
    "tags": ["geometric", "abstract"],
    "difficulty": "medium",
    "colors": [[200, 200, 200], [100, 100, 100], [150, 140, 170], [220, 220, 220]],
    "audio_mapping": {"amplitude": "glow", "bass": "scale", "mid": "rotation", "treble": "color_shift"}
  },
  {
    "id": 8,
    "name": "Infernal",
    "theme": "infernal",
    "visual_type": "turbulent",
    "description": "Chaotic flame-like turbulence with heat motion",
    "shader": "turbulent",
    "tags": ["turbulent", "infernal"],
    "difficulty": "hard",
    "colors": [[180, 20, 80], [200, 90, 30], [50, 40, 40], [220, 60, 90]],
    "audio_mapping": {"amplitude": "heat", "bass": "intensity", "mid": "rotation", "treble": "spark_emission"}
  },
  {
    "id": 9,
    "name": "Psychedelic",
    "theme": "psychedelic",
    "visual_type": "turbulent",
    "description": "Colorful swirling patterns with hypnotic motion",
    "shader": "turbulent",
    "tags": ["turbulent", "psychedelic"],
    "difficulty": "hard",
    "colors": [[200, 120, 180], [160, 110, 160], [150, 140, 140], [180, 150, 200]],
    "audio_mapping": {"amplitude": "intensity", "bass": "scale", "mid": "kaleidoscope_rotation", "treble": "color_shift"}
  },
  {
    "id": 10,
    "name": "Quantum",
    "theme": "quantum",
    "visual_type": "turbulent",
    "description": "Probabilistic field turbulence with quantum artifacts",
    "shader": "turbulent",
    "tags": ["turbulent", "quantum"],
    "difficulty": "hard",
    "colors": [[60, 80, 160], [180, 160, 200], [200, 190, 230], [80, 100, 180]],
    "audio_mapping": {"amplitude": "probability_intensity", "bass": "scale", "mid": "rotation", "treble": "quantum_flicker"}
  },
  {
    "id": 11,
    "name": "Synesthetic",
    "theme": "synesthetic",
    "visual_type": "turbulent",
    "description": "Multi-sensory interpretation of audio as turbulence",
    "shader": "turbulent",
    "tags": ["turbulent", "synesthetic"],
    "difficulty": "hard",
    "colors": [[220, 140, 130], [200, 180, 220], [80, 80, 180], [200, 160, 80]],
    "audio_mapping": {"amplitude": "intensity", "bass": "color_a", "mid": "color_b", "treble": "color_c"}
  },
  {
    "id": 12,
    "name": "Celestial",
    "theme": "celestial",
    "visual_type": "ethereal",
    "description": "Star-like particles in gaseous clouds",
    "shader": "ethereal",
    "tags": ["ethereal", "celestial"],
    "difficulty": "easy",
    "colors": [[40, 50, 120], [180, 170, 200], [240, 230, 200], [100, 100, 180]],
    "audio_mapping": {"amplitude": "brightness", "bass": "sway", "mid": "rotation", "treble": "twinkle"}
  },
  {
    "id": 13,
    "name": "Bioluminescent",
    "theme": "bioluminescent",
    "visual_type": "ethereal",
    "description": "Glowing organisms in ethereal space",
    "shader": "ethereal",
    "tags": ["ethereal", "bioluminescent"],
    "difficulty": "easy",
    "colors": [[180, 150, 200], [150, 180, 100], [120, 180, 180], [200, 180, 220]],
    "audio_mapping": {"amplitude": "glow", "bass": "scale", "mid": "pulse", "treble": "color_shift"}
  },
  {
    "id": 14,
    "name": "Alchemical",
    "theme": "alchemical",
    "visual_type": "ethereal",
    "description": "Mystical transmutation of light and color",
    "shader": "ethereal",
    "tags": ["ethereal", "alchemical"],
    "difficulty": "easy",
    "colors": [[75, 30, 120], [218, 165, 32], [184, 115, 51], [180, 50, 100]],
    "audio_mapping": {"amplitude": "intensity", "bass": "scale", "mid": "rotation", "treble": "sparkle"}
  },
  {
    "id": 15,
    "name": "Cosmic",
    "theme": "cosmic",
    "visual_type": "ethereal",
    "description": "Deep space with cosmic dust and nebulae",
    "shader": "ethereal",
    "tags": ["ethereal", "cosmic"],
    "difficulty": "easy",
    "colors": [[30, 40, 80], [180, 90, 50], [200, 140, 30], [60, 70, 120]],
    "audio_mapping": {"amplitude": "brightness", "bass": "scale", "mid": "rotation", "treble": "twinkle"}
  }
]
```

- [ ] **Step 2: Verify the JSON is valid**

```bash
python -c "import json; json.load(open('src/presets/presets.json')); print('✓ Valid JSON')"
```

Expected: `✓ Valid JSON`

- [ ] **Step 3: Verify presets load correctly**

```bash
python -c "
from src.ui.presets_data import PresetManager
pm = PresetManager()
print(f'Loaded {len(pm.builtin_presets)} presets')
for vtype in ['particles', 'geometric', 'turbulent', 'ethereal']:
    count = len([p for p in pm.builtin_presets if p.visual_type == vtype])
    print(f'{vtype}: {count} presets')
"
```

Expected:
```
Loaded 16 presets
particles: 4 presets
geometric: 4 presets
turbulent: 4 presets
ethereal: 4 presets
```

- [ ] **Step 4: Backup old presets and commit**

```bash
mv src/presets/presets.json.old src/presets/presets.json.bak 2>/dev/null || true
git add src/presets/presets.json
git commit -m "feat: create new minimal presets.json with 16 presets across 4 visual types"
```

---

### Task 3: Implement Particles Shader

**Files:**
- Create: `src/shaders/particles.glsl`

- [ ] **Step 1: Create particles.glsl shader**

Create `src/shaders/particles.glsl`:

```glsl
#version 330 core

uniform float time;
uniform float amplitude;
uniform float bass;
uniform float mid;
uniform float treble;

// Color uniforms
uniform vec3 color0;
uniform vec3 color1;
uniform vec3 color2;
uniform vec3 color3;

in vec2 uv;
out vec4 fragColor;

// Pseudo-random function
float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

// Particle system shader
void main() {
    vec2 pos = uv;
    
    // Particle density controlled by bass
    float density = 0.1 + bass * 0.5;
    
    // Particle speed controlled by mid
    float speed = mid * 2.0;
    
    // Particle spread controlled by treble
    float spread = 0.1 + treble * 0.3;
    
    // Generate particles using noise
    vec2 particlePos = pos + vec2(sin(time * speed + pos.y * 10.0), cos(time * speed + pos.x * 10.0)) * spread;
    
    float particle = random(floor(particlePos * density)) * 0.5 + 0.5;
    particle = smoothstep(0.3, 0.7, particle);
    
    // Apply distance falloff
    float dist = length(particlePos - pos);
    particle *= exp(-dist * dist * 5.0);
    
    // Color based on particle position and time
    vec3 color = mix(
        mix(color0, color1, sin(time * 0.5 + particlePos.x * 3.0) * 0.5 + 0.5),
        mix(color2, color3, cos(time * 0.3 + particlePos.y * 3.0) * 0.5 + 0.5),
        particle
    );
    
    // Final color with amplitude controlling intensity
    fragColor = vec4(color * particle * amplitude, particle * amplitude);
}
```

- [ ] **Step 2: Verify shader syntax**

Check shader compiles by examining file:
```bash
wc -l src/shaders/particles.glsl
```

Expected: ~60 lines of valid GLSL

- [ ] **Step 3: Commit**

```bash
git add src/shaders/particles.glsl
git commit -m "feat: implement particles shader with audio-responsive density, speed, and spread"
```

---

### Task 4: Implement Geometric Shader

**Files:**
- Create: `src/shaders/geometric.glsl`

- [ ] **Step 1: Create geometric.glsl shader**

Create `src/shaders/geometric.glsl`:

```glsl
#version 330 core

uniform float time;
uniform float amplitude;
uniform float bass;
uniform float mid;
uniform float treble;

// Color uniforms
uniform vec3 color0;
uniform vec3 color1;
uniform vec3 color2;
uniform vec3 color3;

in vec2 uv;
out vec4 fragColor;

// Grid and geometric patterns
void main() {
    vec2 pos = uv * 10.0;  // Scale for grid
    
    // Scale controlled by bass
    float scale = 1.0 + bass * 0.5;
    pos /= scale;
    
    // Rotation controlled by mid
    float angle = mid * time * 2.0;
    mat2 rot = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
    pos = rot * pos;
    
    // Create grid pattern
    vec2 grid = fract(pos);
    vec2 gridDist = min(grid, 1.0 - grid);
    float gridLine = min(gridDist.x, gridDist.y);
    
    // Add detail controlled by treble
    float detail = treble * 0.3;
    gridLine = smoothstep(detail + 0.01, detail - 0.01, gridLine);
    
    // Glow effect
    float glow = exp(-length(grid - 0.5) * length(grid - 0.5) * 5.0);
    
    // Color interpolation
    vec3 color = mix(
        mix(color0, color1, pos.x),
        mix(color2, color3, pos.y),
        0.5
    );
    
    // Final output
    float brightness = (gridLine + glow * 0.5) * amplitude;
    fragColor = vec4(color * brightness, brightness);
}
```

- [ ] **Step 2: Verify shader syntax**

```bash
wc -l src/shaders/geometric.glsl
```

Expected: ~50 lines of valid GLSL

- [ ] **Step 3: Commit**

```bash
git add src/shaders/geometric.glsl
git commit -m "feat: implement geometric shader with scale, rotation, and detail control"
```

---

### Task 5: Implement Turbulent Shader

**Files:**
- Create: `src/shaders/turbulent.glsl`

- [ ] **Step 1: Create turbulent.glsl shader**

Create `src/shaders/turbulent.glsl`:

```glsl
#version 330 core

uniform float time;
uniform float amplitude;
uniform float bass;
uniform float mid;
uniform float treble;

// Color uniforms
uniform vec3 color0;
uniform vec3 color1;
uniform vec3 color2;
uniform vec3 color3;

in vec2 uv;
out vec4 fragColor;

// Simplex-like noise approximation
float noise(vec2 p) {
    return sin(p.x * 12.9898 + p.y * 78.233) * 43758.5453;
}

// Turbulent flow field
void main() {
    vec2 pos = uv;
    
    // Turbulence intensity controlled by bass
    float turbIntensity = bass * 2.0;
    
    // Swirl controlled by mid
    float swirl = mid * time;
    vec2 offset = vec2(sin(swirl), cos(swirl)) * turbIntensity;
    
    // Add flowing motion
    pos += offset + vec2(time * 0.1, sin(time * 0.15) * 0.2);
    
    // Multi-octave noise for detail
    float n = 0.0;
    float amp = 1.0;
    for (int i = 0; i < 4; i++) {
        n += amp * abs(sin(noise(pos * (1.0 + float(i) * treble))));
        pos *= 2.0;
        amp *= 0.5;
    }
    
    // Normalize and apply amplitude
    n = n / 2.5;
    n = smoothstep(0.3, 0.7, n);
    
    // Color based on turbulence pattern
    vec3 color = mix(
        mix(color0, color1, n),
        mix(color2, color3, sin(n * 3.14159) * 0.5 + 0.5),
        0.5
    );
    
    // Final output with amplitude control
    fragColor = vec4(color * n * amplitude, n * amplitude);
}
```

- [ ] **Step 2: Verify shader syntax**

```bash
wc -l src/shaders/turbulent.glsl
```

Expected: ~55 lines of valid GLSL

- [ ] **Step 3: Commit**

```bash
git add src/shaders/turbulent.glsl
git commit -m "feat: implement turbulent shader with flowing, swirling motion"
```

---

### Task 6: Implement Ethereal Shader

**Files:**
- Create: `src/shaders/ethereal.glsl`

- [ ] **Step 1: Create ethereal.glsl shader**

Create `src/shaders/ethereal.glsl`:

```glsl
#version 330 core

uniform float time;
uniform float amplitude;
uniform float bass;
uniform float mid;
uniform float treble;

// Color uniforms
uniform vec3 color0;
uniform vec3 color1;
uniform vec3 color2;
uniform vec3 color3;

in vec2 uv;
out vec4 fragColor;

void main() {
    vec2 pos = uv;
    
    // Volumetric density controlled by bass
    float density = 0.1 + bass * 0.3;
    
    // Oscillation speed controlled by mid
    float oscSpeed = mid * 1.5;
    
    // Shimmer/sparkle controlled by treble
    float shimmer = treble * 2.0;
    
    // Create soft, drifting layers
    float layers = 0.0;
    for (int i = 0; i < 3; i++) {
        float layer = sin(pos.y * float(i) + time * oscSpeed) * 0.5 + 0.5;
        layer *= sin(pos.x * float(i) * 0.7 + time * oscSpeed * 0.7) * 0.5 + 0.5;
        layer = smoothstep(0.2, 0.8, layer);
        layers += layer / 3.0;
    }
    
    // Add sparkle/twinkle
    float sparkle = sin(pos.x * 20.0 + time * shimmer) * sin(pos.y * 20.0 + time * shimmer * 0.7);
    sparkle = smoothstep(0.4, 0.6, sparkle + 0.5);
    sparkle *= 0.3;
    
    // Combine layers and sparkle
    float glow = layers + sparkle;
    glow = smoothstep(0.1, 0.9, glow * density);
    
    // Color transition based on position and time
    vec3 color = mix(
        mix(color0, color1, sin(time * 0.3 + pos.x) * 0.5 + 0.5),
        mix(color2, color3, cos(time * 0.2 + pos.y) * 0.5 + 0.5),
        glow
    );
    
    // Soft glow with amplitude control
    float finalGlow = glow * amplitude;
    fragColor = vec4(color * finalGlow, finalGlow * 0.8);
}
```

- [ ] **Step 2: Verify shader syntax**

```bash
wc -l src/shaders/ethereal.glsl
```

Expected: ~60 lines of valid GLSL

- [ ] **Step 3: Commit**

```bash
git add src/shaders/ethereal.glsl
git commit -m "feat: implement ethereal shader with layered, drifting volumetric effects"
```

---

### Task 7: Update Visualizer to Route Presets to Shaders

**Files:**
- Modify: `src/visualizer.py` (shader loading and routing)

- [ ] **Step 1: Find shader loading in visualizer.py**

Search for where shaders are currently loaded:
```bash
grep -n "shader\|glsl\|compile" /home/drew/Documents/audiovisualizerpy/src/visualizer.py | head -20
```

- [ ] **Step 2: Update shader loading to route by visual_type**

In the visualizer's shader loading logic, add code to select shader based on preset's visual_type:

```python
# Get the preset and its visual type
preset = self.get_preset(self.current_preset_name)
visual_type = preset.get('visual_type', 'particles')

# Map visual type to shader file
shader_map = {
    'particles': 'particles',
    'geometric': 'geometric',
    'turbulent': 'turbulent',
    'ethereal': 'ethereal'
}

shader_name = shader_map.get(visual_type, 'particles')
shader_file = f'src/shaders/{shader_name}.glsl'

# Load the appropriate shader
shader = self.shader_manager.load_shader(shader_file)
```

- [ ] **Step 3: Test application startup**

```bash
timeout 3 python main.py || true
```

Expected: Application starts without errors about missing shaders

- [ ] **Step 4: Commit**

```bash
git add src/visualizer.py
git commit -m "feat: route presets to correct shader based on visual_type"
```

---

### Task 8: Cleanup Old Preset Data

**Files:**
- Remove: `src/presets/*.py` (old theme files)
- Archive: Old presets.json backup

- [ ] **Step 1: Check what old preset files exist**

```bash
ls src/presets/*.py | grep -v __pycache__ | head -20
```

- [ ] **Step 2: Remove old preset theme files**

```bash
rm -f src/presets/abstract.py src/presets/alchemical.py src/presets/atmospheric.py src/presets/bioluminescent.py src/presets/celestial.py src/presets/chromatic.py src/presets/cosmic.py src/presets/crystalline.py src/presets/crystallized.py src/presets/digital.py src/presets/dimensional.py src/presets/ethereal.py src/presets/infernal.py src/presets/kinetic.py src/presets/liquids.py src/presets/mechanical.py src/presets/metamorphic.py src/presets/organic.py src/presets/psychedelic.py src/presets/quantum.py src/presets/resonant.py src/presets/retro_aero.py src/presets/synesthetic.py src/presets/temporal.py
```

- [ ] **Step 3: Verify only __init__.py remains**

```bash
ls src/presets/*.py
```

Expected: Only `src/presets/__init__.py` remains

- [ ] **Step 4: Commit cleanup**

```bash
git add -A
git commit -m "cleanup: remove old preset theme definition files, archive old presets.json"
```

---

### Task 9: Test New Visual Type System

**Files:**
- Test: Run app and verify new presets load

- [ ] **Step 1: Test application startup**

```bash
timeout 5 python main.py || true
```

Expected: Application starts without errors

- [ ] **Step 2: Verify presets load with visual types**

```bash
python -c "
from src.ui.presets_data import PresetManager
pm = PresetManager()
print(f'✓ Loaded {len(pm.builtin_presets)} presets')
for p in pm.builtin_presets[:5]:
    print(f'  {p.name} ({p.visual_type}): {p.shader}')
"
```

Expected: Shows 16 presets with correct visual_type assignments

- [ ] **Step 3: Verify each visual type has correct themes**

```bash
python -c "
from src.ui.presets_data import PresetManager
pm = PresetManager()
visual_types = {}
for p in pm.builtin_presets:
    vt = p.visual_type
    if vt not in visual_types:
        visual_types[vt] = []
    visual_types[vt].append(p.theme)

for vt in ['particles', 'geometric', 'turbulent', 'ethereal']:
    themes = visual_types.get(vt, [])
    print(f'{vt}: {themes}')
"
```

Expected:
```
particles: ['kinetic', 'resonant', 'digital', 'temporal']
geometric: ['crystalline', 'mechanical', 'dimensional', 'abstract']
turbulent: ['infernal', 'psychedelic', 'quantum', 'synesthetic']
ethereal: ['celestial', 'bioluminescent', 'alchemical', 'cosmic']
```

- [ ] **Step 4: Final commit and push**

```bash
git add -A
git commit -m "test: verify visual type system loads correctly with 16 presets"
git push origin master
```

---

## Success Criteria

- ✓ 16 new presets created and loading
- ✓ 4 new shader files implemented (particles, geometric, turbulent, ethereal)
- ✓ Preset model includes visual_type field
- ✓ Visualizer routes presets to correct shaders
- ✓ Old preset data cleaned up
- ✓ Application runs without errors
- ✓ Each visual type has 4 themes assigned
- ✓ All changes committed and pushed to GitHub
