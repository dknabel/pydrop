# PyDrop

A Milkdrop-style audio visualization application for desktop, built with Python, Pygame, and GLSL shaders. Features 252 presets across 25 themed categories with real-time system audio capture and visualization.

## Features

- **252+ Visualization Presets** organized into 25 themed categories
- Real-time audio visualization using GLSL fragment shaders
- Audio-reactive parameters (amplitude, frequency bands: bass, mid, treble)
- System audio loopback capture (Windows/Mac/Linux compatible)
- **Interactive In-App Menu System:**
  - Search presets by name, description, or tags
  - Filter by theme/category with preset counts
  - Favorites system with persistent storage
  - Create custom presets with parameter editor
  - Mix and blend two presets together
  - 5×4 grid display with selection and scrolling
  - Full keyboard and mouse control
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

**Playback:**
- **SPACE** - Next preset (or next in active playlist)
- **LEFT ARROW** - Previous preset

**Menu (Press M to toggle):**
- **M** - Toggle menu open/close
- **Search Bar** - Type to filter presets by name, description, or tags
- **Category Filter** - Click dropdown to show only presets from one theme
- **Star Icon** - Click to favorite/unfavorite current preset
- **Preset Grid** - Click preset to select, mouse wheel to scroll
- **LEFT/RIGHT ARROWS** - Navigate presets left/right
- **UP/DOWN ARROWS** - Navigate presets up/down  
- **PAGE UP/DOWN** - Scroll grid
- **ENTER** - Select highlighted preset
- **[Edit]** - Open parameter editor to create custom preset
- **[Mix]** - Blend two presets together
- **[Play]** - Preview selected preset
- **[Add to Playlist]** - Add preset to a playlist

**General:**
- **ESC** - Close menu (or exit app)

### Menu System

The interactive in-app menu provides complete preset browsing and customization:

- **Search** - Real-time filtering by preset name, description, or tags
- **Theme Filter** - Browse presets organized by theme with counts (e.g., "Cosmic (10)")
- **Favorites** - Mark presets as favorites and access them instantly (saved to `~/.audiovisualizer/favorites.json`)
- **Custom Presets** - Create and save your own presets:
  - **Parameter Editor**: Adjust 6 audio-reactive parameters:
    - Bass/Mid/Treble Sensitivity (0.0-3.0)
    - Color Hue (-180 to 180)
    - Color Saturation (-1.0 to 2.0)
    - Animation Speed (0.5-2.0)
  - **Mix Tool**: Blend two presets together with adjustable blend ratio
- **Live Preview** - See parameter changes reflected in real-time
- **Persistent Storage** - Custom presets saved to `~/.audiovisualizer/custom_presets/`

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

**Core:**
- `main.py` - Application entry point and event loop
- `src/audio_engine.py` - System audio loopback capture and real-time analysis
- `src/visualizer.py` - OpenGL rendering and shader integration
- `src/shader_manager.py` - GLSL shader compilation and management
- `src/playlist_manager.py` - Playlist creation, saving, and management

**UI Components (New):**
- `src/ui/menu_system.py` - MenuSystem container integrating all UI components
- `src/ui/components.py` - Base UI component classes (UIComponent, Button, Slider, TextInput, Modal)
- `src/ui/menu_components.py` - Specialized menu components:
  - SearchBar - Real-time preset filtering
  - CategoryFilter - Theme selection dropdown
  - PresetGrid - 5×4 preset display with selection
  - DetailsPanel - Selected preset info and action buttons
  - ParameterEditorModal - Custom preset parameter editor
  - MixToolModal - Preset blending tool
  - FavoritesToggle - Favorite/unfavorite button

**Data Models & Management:**
- `src/ui/text_renderer.py` - PIL-based text rendering to pygame surfaces
- `src/ui/models.py` - Data classes (Preset, CustomPreset, FavoritesManager)
- `src/ui/presets_data.py` - PresetManager for loading and searching presets

**Storage:**
- `src/presets/` - Preset metadata and definitions
- `src/shaders/` - 252+ GLSL fragment shaders organized by theme
- `~/.audiovisualizer/` - User data:
  - `favorites.json` - Favorite presets (persisted)
  - `custom_presets/` - User-created presets
  - `playlists/` - User-created playlists

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
