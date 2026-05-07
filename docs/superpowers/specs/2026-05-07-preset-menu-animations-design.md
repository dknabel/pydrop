# Preset Menu & 250 New Animations Design

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Expand the audio visualizer from 12 presets to 252 presets organized into 25 themed categories, with a visual toggle menu system and persistent playlist management.

**Architecture:** Modular preset structure organized by theme (10 presets per theme), with a toggle overlay menu for browsing/reordering and a playlist manager for saving/loading custom sequences.

**Tech Stack:** Python (Pygame/OpenGL), GLSL fragment shaders, JSON for playlist persistence, filesystem storage at `~/.audiovisualizer/playlists/`.

---

## Overview

### Current State
- 12 presets with keyboard navigation (SPACE/LEFT arrow)
- Single `src/presets.py` file
- Hard-coded shader loading in `src/visualizer.py`

### Final State
- 252 total presets (12 core + 240 new)
- 25 theme groups organized in `src/presets/` directory
- Visual toggle menu (press 'M') showing all presets by theme
- Playlist manager for saving/loading custom sequences
- Drag-to-reorder in menu, click to select, right-click for playlist actions

---

## Theme Categories (25 Groups × 10 Presets Each)

| Theme | Description |
|-------|-------------|
| Core | 12 existing presets (Waveform, Particles, Aurora, etc.) |
| Cosmic | Starfields, nebulas, galaxies, warp tunnels, black holes |
| Organic | Flowing water, cellular automata, biological growth, swirling vortices |
| Retro Aero | Glossy orbs, bubbly shapes, blue/green gradients, bouncing balls |
| Digital | Digital rain, glitch variations, scanlines, geometric grids |
| Abstract | Noise flows, mathematical patterns, sine/cosine harmonics |
| Liquids | Water surfaces, splashing, fluid dynamics, viscosity |
| Crystalline | Crystals, ice formations, geometric lattices, mineral structures |
| Psychedelic | Trippy spirals, color morphing, kaleidoscopic variations |
| Atmospheric | Clouds, fog, weather patterns, storms, rain |
| Mechanical | Gears, machinery, moving parts, industrial effects |
| Bioluminescent | Glowing organisms, neon effects, light trails |
| Quantum | Subatomic particles, quantum fluctuations, probability clouds |
| Temporal | Time effects, aging, decay, timelines |
| Dimensional | Portals, rifts, dimensional shifts, perspective warping |
| Ethereal | Ghostly, spirits, transparency, ephemeral |
| Infernal | Fire, lava, heat distortion, volcanic |
| Celestial | Planets, moons, heavenly bodies, solar systems |
| Metamorphic | Shape-shifting, morphing, transformations |
| Synesthetic | Sensory fusion, mixed perception, cross-modal visualization |
| Crystallized | Frozen effects, ice, mineral growth, crystallization |
| Resonant | Sound visualization, harmonic waves, frequency patterns |
| Chromatic | Color theory, spectrum gradients, light refraction |
| Kinetic | Motion, velocity, movement patterns, trajectories |
| Alchemical | Transformation, alchemy, transmutation effects |

---

## File Structure

### Python Presets
```
src/presets/
├── __init__.py                  (exports all presets as single list)
├── core.py                      (12 existing presets)
├── cosmic.py                    (10 new presets)
├── organic.py                   (10 new presets)
├── retro_aero.py                (10 new presets)
├── digital.py                   (10 new presets)
├── abstract.py                  (10 new presets)
├── liquids.py                   (10 new presets)
├── crystalline.py               (10 new presets)
├── psychedelic.py               (10 new presets)
├── atmospheric.py               (10 new presets)
├── mechanical.py                (10 new presets)
├── bioluminescent.py            (10 new presets)
├── quantum.py                   (10 new presets)
├── temporal.py                  (10 new presets)
├── dimensional.py               (10 new presets)
├── ethereal.py                  (10 new presets)
├── infernal.py                  (10 new presets)
├── celestial.py                 (10 new presets)
├── metamorphic.py               (10 new presets)
├── synesthetic.py               (10 new presets)
├── crystallized.py              (10 new presets)
├── resonant.py                  (10 new presets)
├── chromatic.py                 (10 new presets)
├── kinetic.py                   (10 new presets)
└── alchemical.py                (10 new presets)
```

### New Core Modules
```
src/
├── menu_system.py               (visual toggle overlay)
├── playlist_manager.py          (save/load/manage playlists)
├── visualizer.py                (modified to load from preset modules)
└── ...
```

### Shaders
```
shaders/
├── (12 existing core shaders in root)
├── cosmic/                      (10 new shaders)
├── organic/                     (10 new shaders)
├── retro_aero/                  (10 new shaders)
├── digital/                     (10 new shaders)
├── abstract/                    (10 new shaders)
├── liquids/                     (10 new shaders)
├── crystalline/                 (10 new shaders)
├── psychedelic/                 (10 new shaders)
├── atmospheric/                 (10 new shaders)
├── mechanical/                  (10 new shaders)
├── bioluminescent/              (10 new shaders)
├── quantum/                     (10 new shaders)
├── temporal/                    (10 new shaders)
├── dimensional/                 (10 new shaders)
├── ethereal/                    (10 new shaders)
├── infernal/                    (10 new shaders)
├── celestial/                   (10 new shaders)
├── metamorphic/                 (10 new shaders)
├── synesthetic/                 (10 new shaders)
├── crystallized/                (10 new shaders)
├── resonant/                    (10 new shaders)
├── chromatic/                   (10 new shaders)
├── kinetic/                     (10 new shaders)
└── alchemical/                  (10 new shaders)
```

### Playlist Storage
```
~/.audiovisualizer/
└── playlists/
    ├── chill_vibes.json
    ├── party_mode.json
    ├── high_energy.json
    └── (user-saved playlists)
```

---

## Preset Definition Format

Each theme file contains a list of preset dictionaries:

```python
PRESETS = [
    {
        'name': 'Starfield Warp',
        'shader': 'cosmic/starfield_warp',
        'description': '3D warp through star field'
    },
    {
        'name': 'Nebula Clouds',
        'shader': 'cosmic/nebula_clouds',
        'description': 'Swirling nebula gas clouds'
    },
    # ... 8 more presets
]
```

The `__init__.py` in presets directory collects all theme presets into a single master list with theme metadata added:

```python
PRESETS = [
    {
        'name': 'Waveform',
        'shader': 'waveform',
        'description': 'Classic waveform visualization',
        'theme': 'Core'
    },
    {
        'name': 'Starfield Warp',
        'shader': 'cosmic/starfield_warp',
        'description': '3D warp through star field',
        'theme': 'Cosmic'
    },
    # ... 250 more presets
]
```

---

## Menu System (`src/menu_system.py`)

### Behavior
- **Trigger:** Press 'M' to toggle menu overlay on/off
- **Display:** Semi-transparent overlay showing presets organized by theme in a scrollable grid/list
- **Current state:** Highlights currently playing preset
- **Current playlist:** Shows active playlist name at top (if any)

### Interactions
- **Click preset:** Jump immediately to that preset
- **Drag preset:** Reorder preset within current theme group (or custom sequence)
- **Right-click preset:** 
  - Option to add/remove from current playlist
  - Option to add to new playlist
- **Keyboard navigation:** Arrow keys to navigate, Enter to select, ESC to close

### Visual Design
- Semi-transparent dark background (e.g., `rgba(0, 0, 0, 0.8)`)
- Presets shown as clickable cards with name and theme label
- Current preset highlighted (e.g., with colored border or glow)
- Current playlist indicator at top
- Scroll support for viewing all 252 presets
- Close button or ESC key to dismiss

---

## Playlist Manager (`src/playlist_manager.py`)

### Playlist Format (JSON)
```json
{
  "name": "Chill Vibes",
  "presets": [
    "Waveform",
    "Aurora",
    "Organic Flow",
    "Resonant Wave",
    "Ethereal Mist"
  ]
}
```

### Features
- **Create playlist:** From menu, save current reordered preset sequence with a name
- **Load playlist:** Menu shows saved playlists; click to activate
- **Save location:** `~/.audiovisualizer/playlists/` (auto-created on first run)
- **Playback mode:** When playlist active, SPACE cycles through playlist's presets in order (not the full 252)
- **In-memory state:** User can reorder presets at any time, then save as new playlist or overwrite existing

### Persistence
- Playlists stored as JSON files in `~/.audiovisualizer/playlists/`
- Load all saved playlists on app startup
- Allow delete/rename operations on playlists from menu

---

## Integration with Existing Code

### `main.py` Changes
- Add 'M' key handler to toggle menu visibility
- Integrate playlist cycling: if playlist active, SPACE cycles through playlist presets instead of all 252
- LEFT arrow still goes to previous preset (respects playlist if active)

### `visualizer.py` Changes
- Replace hard-coded `PRESETS = [...]` with import from `src.presets`
- Update `load_shaders()` to handle themed shader directories
- Accept preset list from playlist manager when active

### `shader_manager.py`
- No changes needed (already handles relative paths)

### `audio_engine.py`
- No changes needed

---

## Implementation Order

1. **Preset modules** - Create all 25 theme files with preset definitions
2. **Shader files** - Create all 240 new GLSL shaders (10 per theme)
3. **Preset loader** - Create `src/presets/__init__.py` to collect and export all presets
4. **Menu system** - Implement `src/menu_system.py` with toggle overlay
5. **Playlist manager** - Implement `src/playlist_manager.py` with save/load logic
6. **Integration** - Update `main.py`, `visualizer.py` to use new preset structure
7. **Testing** - Verify menu interaction, playlist save/load, shader loading

---

## Success Criteria

- [ ] All 252 presets load without errors
- [ ] Menu toggles with 'M' key and displays all presets organized by theme
- [ ] Click to select a preset immediately switches to it
- [ ] Drag to reorder presets in menu
- [ ] Create, save, and load custom playlists
- [ ] SPACE cycles through active playlist (or all presets if no playlist)
- [ ] All 240 new shaders render without visual artifacts
- [ ] Playlists persist across app restarts
- [ ] No performance degradation with 252 presets

---

## Notes

- Each GLSL shader will be responsively audio-reactive using existing uniforms (iTime, iAmplitude, iBass, iMid, iTreble, iFrequency)
- Retro Aero presets will emphasize glossy, rounded, blue/green aesthetic
- All other themes will feature diverse visual styles and advanced shader techniques
- Playlist manager will gracefully handle missing shader files (display warning but continue)
