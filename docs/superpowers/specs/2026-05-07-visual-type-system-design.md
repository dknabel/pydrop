# Visual Type System Design

**Date:** 2026-05-07  
**Scope:** Replace 252 generic colored-static presets with 16 focused presets across 4 distinct visual types

## Overview

The current preset system has 252 presets that are all variations of colored static/noise without distinctive visual forms. This design replaces that with a lean, focused system of 16 presets organized into 4 unique visual types, each with its own geometric form and procedural rendering.

## Visual Types

Each visual type has a unique visual character and audio-responsive behavior:

### 1. Particles
**Character:** Fast-moving, energetic, point-cloud based  
**Themes:** Kinetic, Resonant, Digital, Temporal  
**Visual Form:** Moving swarms of particles with varying density, speed, and spread  
**Audio Control:**
- Bass → Particle density
- Mid → Particle speed  
- Treble → Spread/dispersion
- Amplitude → Overall intensity/brightness

### 2. Geometric Structures
**Character:** Sharp, crystalline, structured forms  
**Themes:** Crystalline, Mechanical, Dimensional, Abstract  
**Visual Form:** Procedurally generated 3D geometry (grids, lattices, polyhedra) that deforms in real-time  
**Audio Control:**
- Bass → Scale/size of structures
- Mid → Rotation and deformation
- Treble → Detail/complexity level
- Amplitude → Glow intensity

### 3. Turbulent/Chaotic
**Character:** Intense, swirling, fluid-like dynamics  
**Themes:** Infernal, Psychedelic, Quantum, Synesthetic  
**Visual Form:** Fluid simulation or turbulence fields with swirling motion  
**Audio Control:**
- Bass → Turbulence intensity
- Mid → Swirl/rotation speed
- Treble → Fine detail/noise scale
- Amplitude → Heat/brightness

### 4. Ethereal/Atmospheric
**Character:** Subtle, flowing, volumetric and gentle  
**Themes:** Celestial, Bioluminescent, Alchemical, Cosmic  
**Visual Form:** Volumetric effects with gentle oscillations and drifting motion  
**Audio Control:**
- Bass → Volume/density
- Mid → Oscillation speed
- Treble → Shimmer/sparkle effect
- Amplitude → Glow/luminosity

## Preset Mappings

### Particles (4 presets)
- **Kinetic** — Fast, dense particle clouds responding to rhythm
- **Resonant** — Particles arranged in harmonic patterns
- **Digital** — Sharp, geometric particle behavior
- **Temporal** — Particles flowing through time-based patterns

### Geometric Structures (4 presets)
- **Crystalline** — Ice-like lattice structures with smooth deformation
- **Mechanical** — Industrial grid and gear-like forms
- **Dimensional** — Tesseract and higher-dimensional geometry
- **Abstract** — Minimalist geometric arrangements

### Turbulent/Chaotic (4 presets)
- **Infernal** — Chaotic flame-like turbulence with heat motion
- **Psychedelic** — Colorful swirling patterns with hypnotic motion
- **Quantum** — Probabilistic field turbulence with quantum artifacts
- **Synesthetic** — Multi-sensory interpretation of audio as turbulence

### Ethereal/Atmospheric (4 presets)
- **Celestial** — Star-like particles in gaseous clouds
- **Bioluminescent** — Glowing organisms in ethereal space
- **Alchemical** — Mystical transmutation of light and color
- **Cosmic** — Deep space with cosmic dust and nebulae

## Color Palettes

Each of the 16 themes retains its unique color palette (defined in previous preset enhancement):

- **Particles**: Warm (kinetic/resonant), cool (digital/temporal)
- **Geometric**: Icy/cool (crystalline), metallic (mechanical), gradient (dimensional), minimal (abstract)
- **Turbulent**: Warm intense (infernal), vibrant (psychedelic), cool scientific (quantum), multicolor (synesthetic)
- **Ethereal**: Cool cosmic (celestial), soft glow (bioluminescent), mystical (alchemical), deep space (cosmic)

## Architecture

### Current Structure to Remove
- `src/presets/presets.json` — All 252 presets with shader references
- Shader files that generate colored noise (if modular)
- Preset Python files (abstract.py, alchemical.py, etc.)

### New Structure to Create
- **New `src/presets/presets.json`** — 16 presets mapped to 4 visual types
- **4 new shader files** (one per visual type):
  - `src/shaders/particles.glsl` — Particle system shader
  - `src/shaders/geometric.glsl` — Geometry deformation shader
  - `src/shaders/turbulent.glsl` — Fluid/turbulence shader
  - `src/shaders/ethereal.glsl` — Volumetric/atmospheric shader
- **Updated theme mappings** in presets.json

### Data Model

Each preset in the new `presets.json`:
```json
{
  "id": 0,
  "name": "Kinetic",
  "theme": "kinetic",
  "visual_type": "particles",
  "description": "Fast, dense particle clouds responding to rhythm",
  "shader": "particles",
  "colors": [...],
  "audio_mapping": {...}
}
```

## Implementation Approach

1. **Phase 1: Cleanup**
   - Archive existing presets.json
   - Create new minimal presets.json with 16 presets
   - Update Preset model if needed (add visual_type field)

2. **Phase 2: Shaders**
   - Implement 4 new shader types (particles, geometric, turbulent, ethereal)
   - Each shader handles its audio mappings and unique visual form
   - Test each shader independently

3. **Phase 3: Integration**
   - Update preset manager to load new presets
   - Update visualizer to route presets to correct shaders
   - Verify audio reactivity works per visual type

## Success Criteria

- ✓ 16 presets load without errors
- ✓ Each visual type renders a distinctive form (not colored noise)
- ✓ Audio responsiveness works for each type
- ✓ Color palettes are applied correctly
- ✓ No visual duplication between themes
- ✓ Application runs smoothly with new preset system

## Out of Scope

- Creating hundreds of variations (we're focusing on quality over quantity)
- Mixing visual types within a single preset
- Real-time shader hot-loading or editing
