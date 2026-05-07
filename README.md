# PyDrop

A Milkdrop-style audio visualization application for desktop, built with Python, Pygame, and GLSL shaders. Features 252 presets across 25 themed categories with real-time system audio capture and visualization.

## Features

- **252 Visualization Presets** organized into 25 themed categories
- Real-time audio visualization using GLSL fragment shaders
- Audio-reactive parameters (amplitude, frequency bands: bass, mid, treble)
- System audio loopback capture (Windows/Mac/Linux compatible)
- Interactive preset menu with theme browsing
- Custom playlist creation and management
- Smooth, organic animations with audio synchronization

## Preset Themes

The visualizer includes 252 presets organized into the following 25 themes:

- **Core** (12) - Classic presets (Waveform, Particles, Aurora, etc.)
- **Cosmic** (10) - Starfields, nebulas, galaxies, warps
- **Organic** (10) - Flowing water, cellular growth, life forms
- **Retro Aero** (10) - Glossy orbs, bubbles, blue gradients (90s/2000s aesthetic)
- **Digital** (10) - Digital rain, glitch, scanlines, circuits
- **Abstract** (10) - Noise flows, fractals, harmonic patterns
- **Liquids** (10) - Water surfaces, splashing, fluid dynamics
- **Crystalline** (10) - Crystals, ice, geometric lattices
- **Psychedelic** (10) - Trippy spirals, kaleidoscopic morphs
- **Atmospheric** (10) - Clouds, fog, storms, weather effects
- **Mechanical** (10) - Gears, pistons, machinery
- **Bioluminescent** (10) - Glowing organisms, neon trails
- **Quantum** (10) - Electron orbits, wave functions, particles
- **Temporal** (10) - Time effects, aging, decay
- **Dimensional** (10) - Portals, rifts, perspective shifts
- **Ethereal** (10) - Ghosts, spirits, transparency
- **Infernal** (10) - Lava, fire, heat distortion
- **Celestial** (10) - Planets, moons, stars
- **Metamorphic** (10) - Shape-shifting, morphing, transformations
- **Synesthetic** (10) - Sensory fusion, cross-modal visualization
- **Crystallized** (10) - Frozen landscapes, ice, crystallization
- **Resonant** (10) - Sound visualization, harmonic waves
- **Chromatic** (10) - Color theory, gradients, light refraction
- **Kinetic** (10) - Motion, velocity, trajectories
- **Alchemical** (10) - Transformation, alchemy, transmutation

## Installation

```bash
cd audiovisualizerpy
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

### Controls

- **SPACE** - Next preset (or next in active playlist)
- **LEFT ARROW** - Previous preset
- **M** - Toggle preset menu (click to select, arrow keys to navigate)
- **UP/DOWN ARROWS** - Navigate menu selections
- **ENTER** - Confirm menu selection
- **ESC** - Exit

### Playlists

Create custom preset sequences and save them:

```python
from src.playlist_manager import PlaylistManager

pm = PlaylistManager()
pm.save_playlist("Chill Vibes", ["Waveform", "Aurora", "Floating Water"])
pm.activate_playlist("Chill Vibes")

# Press SPACE to cycle through playlist presets
```

Playlists are saved to `~/.audiovisualizer/playlists/` and persist across sessions.

## Architecture

- `main.py` - Application entry point and event loop
- `src/audio_engine.py` - System audio loopback capture and real-time analysis
- `src/visualizer.py` - OpenGL rendering and shader integration
- `src/shader_manager.py` - GLSL shader compilation and management
- `src/menu_system.py` - Interactive preset menu with mouse/keyboard controls
- `src/playlist_manager.py` - Playlist creation, saving, and management
- `src/presets/` - Modular preset system (25 theme modules)
- `src/shaders/` - 252 GLSL fragment shaders organized by theme

## Shaders

Each preset corresponds to a GLSL fragment shader that processes audio data in real-time:

- **All 252 shaders** respond to audio uniforms:
  - `iTime` - Animation time
  - `iAmplitude` - Overall audio amplitude (RMS)
  - `iBass` - Low-frequency band (0-50Hz)
  - `iMid` - Mid-frequency band (50-200Hz)
  - `iTreble` - High-frequency band (200Hz+)
  - `iFrequency` - Full frequency spectrum texture (sampler1D)

Shaders are organized by theme in `src/shaders/`:
- Core shaders in root directory (waveform.glsl, particles.glsl, etc.)
- Themed shaders in subdirectories (cosmic/starfield_warp.glsl, digital/digital_rain.glsl, etc.)
