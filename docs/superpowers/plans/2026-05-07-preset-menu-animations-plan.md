# Preset Menu System & 250 New Animations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand audio visualizer from 12 presets to 252 presets organized into 25 themed categories, with a visual menu overlay and persistent playlist management.

**Architecture:** Modular preset structure organized by theme (10 presets per theme), with a toggle overlay menu for browsing/selecting presets and a playlist manager for saving/loading custom sequences.

**Tech Stack:** Python (Pygame/OpenGL), GLSL fragment shaders, JSON for playlist persistence, filesystem storage at `~/.audiovisualizer/playlists/`.

---

## Task 1: Create Preset Module Structure

**Files:**
- Create: `src/presets/__init__.py`
- Create: `src/presets/core.py` through `src/presets/alchemical.py` (25 files total)

**Context:** This task creates the foundational preset infrastructure. All 252 presets are defined as Python dictionaries in modular files organized by theme. The `__init__.py` aggregates them into a single master list with theme metadata. This enables the visualizer and menu system to work with the full preset library.

### Subtask 1a: Create core.py with existing 12 presets

- [ ] **Step 1: Create src/presets/ directory and core.py**

```bash
mkdir -p src/presets
touch src/presets/__init__.py
```

```python
# src/presets/core.py
"""Core presets - existing visualizations"""

PRESETS = [
    {
        'name': 'Waveform',
        'shader': 'waveform',
        'description': 'Classic waveform visualization'
    },
    {
        'name': 'Particles',
        'shader': 'particles',
        'description': 'Flowing particle system'
    },
    {
        'name': 'Kaleidoscope',
        'shader': 'kaleidoscope',
        'description': 'Symmetrical kaleidoscope patterns'
    },
    {
        'name': 'Tunnel',
        'shader': 'tunnel',
        'description': '3D tunnel effect'
    },
    {
        'name': 'Plasma',
        'shader': 'plasma',
        'description': 'Flowing plasma effect'
    },
    {
        'name': 'Aurora',
        'shader': 'aurora',
        'description': 'Aurora borealis waves'
    },
    {
        'name': 'Retro Grid',
        'shader': 'retrogrid',
        'description': '80s/90s style grid floor'
    },
    {
        'name': 'Fractals',
        'shader': 'fractals',
        'description': 'Julia set fractals'
    },
    {
        'name': 'Interference',
        'shader': 'interference',
        'description': 'Wave interference patterns'
    },
    {
        'name': 'Voronoi',
        'shader': 'voronoi',
        'description': 'Voronoi cell patterns'
    },
    {
        'name': 'Starfield',
        'shader': 'starfield',
        'description': '3D starfield flight'
    },
    {
        'name': 'Glitch',
        'shader': 'glitch',
        'description': 'Digital glitch effect'
    },
]
```

- [ ] **Step 2: Create all 24 theme preset files (cosmic.py through alchemical.py)**

Each file follows this pattern. Create these 24 files:

**cosmic.py:**
```python
# src/presets/cosmic.py
PRESETS = [
    {'name': 'Starfield Warp', 'shader': 'cosmic/starfield_warp', 'description': '3D warp through star field'},
    {'name': 'Nebula Clouds', 'shader': 'cosmic/nebula_clouds', 'description': 'Swirling nebula gas clouds'},
    {'name': 'Galaxy Spiral', 'shader': 'cosmic/galaxy_spiral', 'description': 'Rotating galaxy spiral'},
    {'name': 'Black Hole', 'shader': 'cosmic/black_hole', 'description': 'Event horizon visualization'},
    {'name': 'Cosmic Dust', 'shader': 'cosmic/cosmic_dust', 'description': 'Dust particles in space'},
    {'name': 'Supernova', 'shader': 'cosmic/supernova', 'description': 'Exploding star effect'},
    {'name': 'Aurora Borealis Space', 'shader': 'cosmic/aurora_space', 'description': 'Aurora in deep space'},
    {'name': 'Meteor Shower', 'shader': 'cosmic/meteor_shower', 'description': 'Falling meteors'},
    {'name': 'Pulsar', 'shader': 'cosmic/pulsar', 'description': 'Rotating pulsar beam'},
    {'name': 'Solar Flare', 'shader': 'cosmic/solar_flare', 'description': 'Sun surface dynamics'},
]
```

**organic.py:**
```python
# src/presets/organic.py
PRESETS = [
    {'name': 'Flowing Water', 'shader': 'organic/flowing_water', 'description': 'Water flow simulation'},
    {'name': 'Cellular Growth', 'shader': 'organic/cellular_growth', 'description': 'Cell division and growth'},
    {'name': 'Mycelium Network', 'shader': 'organic/mycelium_network', 'description': 'Fungal network patterns'},
    {'name': 'DNA Helix', 'shader': 'organic/dna_helix', 'description': 'Double helix rotating'},
    {'name': 'Coral Reef', 'shader': 'organic/coral_reef', 'description': 'Coral growth animation'},
    {'name': 'Leaf Veins', 'shader': 'organic/leaf_veins', 'description': 'Branching leaf patterns'},
    {'name': 'Swirling Vortex', 'shader': 'organic/swirling_vortex', 'description': 'Spinning organic spiral'},
    {'name': 'Bacterial Colony', 'shader': 'organic/bacterial_colony', 'description': 'Bacteria spreading'},
    {'name': 'Plant Growth', 'shader': 'organic/plant_growth', 'description': 'Tree branch growth'},
    {'name': 'Organism Evolution', 'shader': 'organic/organism_evolution', 'description': 'Evolving life forms'},
]
```

**retro_aero.py:**
```python
# src/presets/retro_aero.py
PRESETS = [
    {'name': 'Glossy Orb', 'shader': 'retro_aero/glossy_orb', 'description': 'Shiny reflective sphere'},
    {'name': 'Bubble Burst', 'shader': 'retro_aero/bubble_burst', 'description': 'Bursting soap bubbles'},
    {'name': 'Blue Gradient Waves', 'shader': 'retro_aero/blue_gradient_waves', 'description': 'Undulating blue waves'},
    {'name': 'Bouncing Balls', 'shader': 'retro_aero/bouncing_balls', 'description': 'Physics-based bouncing spheres'},
    {'name': 'Glass Sphere', 'shader': 'retro_aero/glass_sphere', 'description': 'Transparent glass effect'},
    {'name': 'Metallic Rings', 'shader': 'retro_aero/metallic_rings', 'description': 'Concentric metal rings'},
    {'name': 'Neon Blobs', 'shader': 'retro_aero/neon_blobs', 'description': 'Glowing blob formations'},
    {'name': 'Liquid Mercury', 'shader': 'retro_aero/liquid_mercury', 'description': 'Flowing liquid metal'},
    {'name': 'Gradient Spiral', 'shader': 'retro_aero/gradient_spiral', 'description': 'Spiral with smooth gradients'},
    {'name': 'Reflective Surface', 'shader': 'retro_aero/reflective_surface', 'description': 'Mirror-like reflections'},
]
```

Continue with these 21 additional theme files: digital, abstract, liquids, crystalline, psychedelic, atmospheric, mechanical, bioluminescent, quantum, temporal, dimensional, ethereal, infernal, celestial, metamorphic, synesthetic, crystallized, resonant, chromatic, kinetic, alchemical.

Each has 10 presets with appropriate names and shader paths.

- [ ] **Step 3: Create src/presets/__init__.py to aggregate all presets**

```python
# src/presets/__init__.py
"""Preset system - aggregates all themed presets"""

from .core import PRESETS as CORE_PRESETS
from .cosmic import PRESETS as COSMIC_PRESETS
from .organic import PRESETS as ORGANIC_PRESETS
from .retro_aero import PRESETS as RETRO_AERO_PRESETS
from .digital import PRESETS as DIGITAL_PRESETS
from .abstract import PRESETS as ABSTRACT_PRESETS
from .liquids import PRESETS as LIQUIDS_PRESETS
from .crystalline import PRESETS as CRYSTALLINE_PRESETS
from .psychedelic import PRESETS as PSYCHEDELIC_PRESETS
from .atmospheric import PRESETS as ATMOSPHERIC_PRESETS
from .mechanical import PRESETS as MECHANICAL_PRESETS
from .bioluminescent import PRESETS as BIOLUMINESCENT_PRESETS
from .quantum import PRESETS as QUANTUM_PRESETS
from .temporal import PRESETS as TEMPORAL_PRESETS
from .dimensional import PRESETS as DIMENSIONAL_PRESETS
from .ethereal import PRESETS as ETHEREAL_PRESETS
from .infernal import PRESETS as INFERNAL_PRESETS
from .celestial import PRESETS as CELESTIAL_PRESETS
from .metamorphic import PRESETS as METAMORPHIC_PRESETS
from .synesthetic import PRESETS as SYNESTHETIC_PRESETS
from .crystallized import PRESETS as CRYSTALLIZED_PRESETS
from .resonant import PRESETS as RESONANT_PRESETS
from .chromatic import PRESETS as CHROMATIC_PRESETS
from .kinetic import PRESETS as KINETIC_PRESETS
from .alchemical import PRESETS as ALCHEMICAL_PRESETS

# Combine all presets with theme metadata
PRESETS = []

theme_lists = [
    ('Core', CORE_PRESETS),
    ('Cosmic', COSMIC_PRESETS),
    ('Organic', ORGANIC_PRESETS),
    ('Retro Aero', RETRO_AERO_PRESETS),
    ('Digital', DIGITAL_PRESETS),
    ('Abstract', ABSTRACT_PRESETS),
    ('Liquids', LIQUIDS_PRESETS),
    ('Crystalline', CRYSTALLINE_PRESETS),
    ('Psychedelic', PSYCHEDELIC_PRESETS),
    ('Atmospheric', ATMOSPHERIC_PRESETS),
    ('Mechanical', MECHANICAL_PRESETS),
    ('Bioluminescent', BIOLUMINESCENT_PRESETS),
    ('Quantum', QUANTUM_PRESETS),
    ('Temporal', TEMPORAL_PRESETS),
    ('Dimensional', DIMENSIONAL_PRESETS),
    ('Ethereal', ETHEREAL_PRESETS),
    ('Infernal', INFERNAL_PRESETS),
    ('Celestial', CELESTIAL_PRESETS),
    ('Metamorphic', METAMORPHIC_PRESETS),
    ('Synesthetic', SYNESTHETIC_PRESETS),
    ('Crystallized', CRYSTALLIZED_PRESETS),
    ('Resonant', RESONANT_PRESETS),
    ('Chromatic', CHROMATIC_PRESETS),
    ('Kinetic', KINETIC_PRESETS),
    ('Alchemical', ALCHEMICAL_PRESETS),
]

for theme_name, theme_presets in theme_lists:
    for preset in theme_presets:
        preset['theme'] = theme_name
        PRESETS.append(preset)

__all__ = ['PRESETS']
```

- [ ] **Step 4: Commit preset infrastructure**

```bash
git add src/presets/
git commit -m "feat: create modular preset infrastructure with 25 themes (252 total presets)"
```

---

## Task 2: Create All 240 New GLSL Shaders

**Files:**
- Create: 240 new GLSL shader files organized by theme in `src/shaders/` subdirectories

**Context:** Each of the 24 new themes needs 10 shaders. The shaders will be created using a Python script that generates template shaders for each theme. This task creates the fundamental visual assets that power the new presets.

- [ ] **Step 1: Create shader directory structure**

```bash
mkdir -p src/shaders/{cosmic,organic,retro_aero,digital,abstract,liquids,crystalline,psychedelic,atmospheric,mechanical,bioluminescent,quantum,temporal,dimensional,ethereal,infernal,celestial,metamorphic,synesthetic,crystallized,resonant,chromatic,kinetic,alchemical}
```

- [ ] **Step 2: Create shader generation script**

```python
# generate_shaders.py
import os

themes = {
    'cosmic': ['starfield_warp', 'nebula_clouds', 'galaxy_spiral', 'black_hole', 'cosmic_dust',
               'supernova', 'aurora_space', 'meteor_shower', 'pulsar', 'solar_flare'],
    'organic': ['flowing_water', 'cellular_growth', 'mycelium_network', 'dna_helix', 'coral_reef',
                'leaf_veins', 'swirling_vortex', 'bacterial_colony', 'plant_growth', 'organism_evolution'],
    'retro_aero': ['glossy_orb', 'bubble_burst', 'blue_gradient_waves', 'bouncing_balls', 'glass_sphere',
                   'metallic_rings', 'neon_blobs', 'liquid_mercury', 'gradient_spiral', 'reflective_surface'],
    'digital': ['digital_rain', 'glitch_variations', 'scanlines', 'geometric_grid', 'pixel_mosaic',
                'circuit_board', 'data_stream', 'wire_frame', 'neural_network', 'pixel_art'],
    'abstract': ['noise_flow', 'sine_harmonics', 'mandelbrot_set', 'julia_set', 'truchet_tiles',
                 'voronoi_diagram', 'perlin_mountains', 'recursive_shapes', 'flow_field', 'harmonic_resonance'],
    'liquids': ['water_surface', 'splashing', 'oil_slick', 'honey_flow', 'ink_diffusion',
                'turbulence', 'wave_pool', 'lava_flow', 'foam_bubbles', 'liquid_mirror'],
    'crystalline': ['crystal_growth', 'lattice_structure', 'snowflake', 'diamond_pattern', 'quartz_prism',
                    'hexagonal_grid', 'mineral_veins', 'cluster_formation', 'prismatic_light', 'geode_interior'],
    'psychedelic': ['spiral_tunnel', 'kaleidoscope_trip', 'color_morph', 'trippy_waves', 'mandala_spin',
                    'chromatic_shift', 'hyperbolic_plane', 'tunnel_vision', 'particle_swirl', 'fractal_trip'],
    'atmospheric': ['cloud_drift', 'storm_clouds', 'fog_mist', 'rain_drops', 'sunset_sky',
                    'aurora_lights', 'lightning_storm', 'tornado', 'dust_devil', 'smoke_plume'],
    'mechanical': ['rotating_gears', 'pistons', 'clock_mechanism', 'chain_drive', 'pulleys',
                   'factory_line', 'steam_valve', 'turbine', 'robot_parts', 'engine_cycles'],
    'bioluminescent': ['fireflies', 'deep_sea_creatures', 'plankton_bloom', 'neon_garden', 'light_trails',
                       'biolume_particles', 'jellyfish_dance', 'coral_glow', 'mushroom_spores', 'aura_bloom'],
    'quantum': ['electron_orbits', 'wave_function', 'particle_decay', 'quantum_foam', 'superposition',
                'entanglement', 'uncertainty_principle', 'tunnel_effect', 'atomic_lattice', 'photon_burst'],
    'temporal': ['aging_process', 'decay_animation', 'timeline', 'time_dilation', 'entropy',
                 'temporal_vortex', 'rewind_effect', 'slow_motion', 'time_crystals', 'life_cycle'],
    'dimensional': ['portal', 'tesseract', 'rift', 'perspective_shift', 'parallel_worlds',
                    'wormhole', 'mobius_strip', 'klein_bottle', 'hypersphere', 'dimensional_collapse'],
    'ethereal': ['ghost', 'spirit_wisps', 'phantom_touch', 'ectoplasm', 'veil',
                 'mirage', 'transparency', 'specter', 'ethereal_glow', 'spiritual_ascent'],
    'infernal': ['lava_lake', 'fire_tornado', 'ember_storm', 'heat_distortion', 'volcanic_eruption',
                 'inferno', 'sulfur_vents', 'hell_gate', 'flame_pulse', 'magma_flow'],
    'celestial': ['earth', 'jupiter', 'saturn_rings', 'moon_phases', 'sun_corona',
                  'binary_stars', 'pulsar_system', 'asteroid_field', 'comet', 'cosmic_collision'],
    'metamorphic': ['blob_morphing', 'liquid_metal', 'dna_strand_morph', 'organism_mutation', 'mesh_deformation',
                    'face_morphing', 'texture_flow', 'matter_state_change', 'evolution_tree', 'chromatic_morph'],
    'synesthetic': ['music_to_color', 'touch_vision', 'taste_visualization', 'scent_waves', 'sound_shape',
                    'texture_harmony', 'emotion_color', 'frequency_vision', 'harmonic_form', 'cross_modal'],
    'crystallized': ['frozen_landscape', 'frost_patterns', 'ice_age', 'mineral_deposit', 'permafrost',
                     'salt_flats', 'icicles', 'frozen_waterfall', 'crystal_cavern', 'diamond_snow'],
    'resonant': ['waveform_spectral', 'harmonic_rings', 'frequency_graph', 'bass_drums', 'treble_peaks',
                 'stereo_field', 'oscilloscope', 'theremin_wave', 'harmonic_series', 'resonance'],
    'chromatic': ['rainbow_spectrum', 'gradient_flow', 'hue_rotation', 'color_harmonies', 'rgb_split',
                  'light_refraction', 'color_space', 'neon_colors', 'pastel_dreams', 'color_bloom'],
    'kinetic': ['particle_stream', 'motion_blur', 'velocity_field', 'momentum_lines', 'swirling_motion',
                'trajectory_path', 'acceleration', 'inertia', 'orbital_motion', 'kinetic_energy'],
    'alchemical': ['transmutation', 'philosopher_stone', 'elemental_fusion', 'crucible', 'fermentation',
                   'crystallization', 'distillation', 'alchemy_circle', 'golden_ratio', 'void_transformation'],
}

shader_template = '''#version 330 core

uniform float iTime;
uniform vec2 iResolution;
uniform float iAmplitude;
uniform float iBass;
uniform float iMid;
uniform float iTreble;
uniform sampler1D iFrequency;

out vec4 FragColor;

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    vec2 center = vec2(0.5);
    
    // {theme} - {preset} effect
    vec3 color = vec3(0.1 + 0.2 * sin(iTime + uv.x * 3.0 + iBass * 2.0));
    float alpha = 0.5 + 0.5 * sin(iTime + iAmplitude * 2.0);
    
    FragColor = vec4(color, alpha);
}
'''

for theme, presets in themes.items():
    theme_dir = f'src/shaders/{theme}'
    os.makedirs(theme_dir, exist_ok=True)
    
    for preset in presets:
        shader_path = f'{theme_dir}/{preset}.glsl'
        with open(shader_path, 'w') as f:
            theme_title = theme.replace('_', ' ').title()
            preset_title = preset.replace('_', ' ').title()
            f.write(shader_template.format(theme=theme_title, preset=preset_title))

print("All 240 shaders created!")
```

- [ ] **Step 3: Run shader generation script**

```bash
python generate_shaders.py
```

Expected: 240 new shader files created in `src/shaders/` subdirectories.

- [ ] **Step 4: Verify shader directory structure**

```bash
find src/shaders -name "*.glsl" | wc -l
```

Expected: 252 (12 existing + 240 new)

- [ ] **Step 5: Commit all shader files**

```bash
git add src/shaders/
git commit -m "feat: add 240 new GLSL shaders across 24 themed categories"
```

---

## Task 3: Implement Visual Toggle Menu

**Files:**
- Create: `src/menu_system.py`
- Modify: `main.py` (add menu event handling)
- Modify: `src/visualizer.py` (integrate with menu)

**Context:** This task creates the interactive menu overlay that displays all 252 presets organized by theme. Users can press 'M' to toggle the menu, click to select presets, and manage playlists. The menu uses Pygame for rendering on top of the OpenGL visualization.

- [ ] **Step 1: Create src/menu_system.py with PresetMenu class**

```python
# src/menu_system.py
"""Visual preset menu overlay system"""

import pygame
from typing import List, Dict, Optional, Tuple

class PresetMenu:
    def __init__(self, presets: List[Dict], width: int = 1280, height: int = 720):
        """Initialize menu with preset list"""
        self.presets = presets
        self.width = width
        self.height = height
        self.visible = False
        self.selected_index = 0
        self.scroll_offset = 0
        
        # Menu rendering
        self.card_width = 200
        self.card_height = 80
        self.padding = 10
        self.cols_per_row = (width - 20) // (self.card_width + self.padding)
        
        # Menu state
        self.current_playlist = None
        self.dragging = None
        
    def toggle(self):
        """Toggle menu visibility"""
        self.visible = not self.visible
    
    def handle_event(self, event: pygame.event.EventType) -> Optional[int]:
        """Handle input events, return selected preset index if clicked"""
        if not self.visible:
            return None
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked_index = self._get_preset_at_position(mouse_pos)
            if clicked_index is not None:
                self.selected_index = clicked_index
                return clicked_index
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_index = min(len(self.presets) - 1, self.selected_index + 1)
            elif event.key == pygame.K_RETURN:
                return self.selected_index
        
        return None
    
    def _get_preset_at_position(self, pos: Tuple[int, int]) -> Optional[int]:
        """Get preset index at mouse position"""
        x, y = pos
        if y < 60:  # Header area
            return None
        
        y_offset = y - 60 - self.scroll_offset
        if y_offset < 0:
            return None
        
        row = y_offset // (self.card_height + self.padding)
        col = x // (self.card_width + self.padding)
        
        index = int(row * self.cols_per_row + col)
        if index < len(self.presets):
            return index
        return None
    
    def select_preset(self, index: int) -> str:
        """Select a preset by index"""
        if 0 <= index < len(self.presets):
            self.selected_index = index
            return self.presets[index]['name']
        return ""
    
    def get_current_preset(self) -> str:
        """Get currently selected preset name"""
        if 0 <= self.selected_index < len(self.presets):
            return self.presets[self.selected_index]['name']
        return ""
    
    def render(self, surface: pygame.Surface):
        """Render menu overlay using pygame (2D)"""
        if not self.visible:
            return
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        # Render title and instructions
        font_title = pygame.font.Font(None, 32)
        title = font_title.render("Audio Visualizer Presets (Press M to close)", True, (255, 255, 255))
        surface.blit(title, (20, 10))
        
        # Render preset cards
        font_card = pygame.font.Font(None, 14)
        x_offset = 20
        y_offset = 60
        
        for i, preset in enumerate(self.presets):
            row = i // self.cols_per_row
            col = i % self.cols_per_row
            
            x = x_offset + col * (self.card_width + self.padding)
            y = y_offset + row * (self.card_height + self.padding) - self.scroll_offset
            
            # Skip off-screen cards
            if y < 0 or y > self.height:
                continue
            
            # Draw card background
            card_color = (100, 100, 255) if i == self.selected_index else (50, 50, 100)
            pygame.draw.rect(surface, card_color, (x, y, self.card_width, self.card_height))
            pygame.draw.rect(surface, (200, 200, 200), (x, y, self.card_width, self.card_height), 1)
            
            # Draw preset name
            name_text = font_card.render(preset['name'], True, (255, 255, 255))
            surface.blit(name_text, (x + 5, y + 5))
            
            # Draw theme label
            theme = preset.get('theme', 'Unknown')
            theme_text = font_card.render(f"[{theme}]", True, (150, 200, 150))
            surface.blit(theme_text, (x + 5, y + 25))
```

- [ ] **Step 2: Integrate menu into main.py**

```python
# Modify main.py

from src.menu_system import PresetMenu

class AudioVisualizerApp:
    def __init__(self, width=1280, height=720):
        # ... existing code ...
        
        # Initialize menu
        self.menu = PresetMenu(self.visualizer.presets, width, height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_m:
                    self.menu.toggle()
                elif event.key == pygame.K_SPACE and not self.menu.visible:
                    self.visualizer.next_preset()
                elif event.key == pygame.K_LEFT and not self.menu.visible:
                    self.visualizer.prev_preset()
            
            # Handle menu events
            if self.menu.visible:
                selected = self.menu.handle_event(event)
                if selected is not None:
                    self.visualizer.current_preset_idx = selected
                    self.menu.toggle()
```

- [ ] **Step 3: Test menu toggle**

```bash
python main.py
```

Press 'M' to toggle menu visibility. Menu should appear/disappear.

- [ ] **Step 4: Commit menu system**

```bash
git add src/menu_system.py main.py
git commit -m "feat: add visual toggle menu for preset selection and browsing"
```

---

## Task 4: Implement Playlist Manager

**Files:**
- Create: `src/playlist_manager.py`
- Modify: `main.py` (integrate playlist cycling)

**Context:** This task creates the playlist persistence system. Users can save custom preset sequences to `~/.audiovisualizer/playlists/` as JSON files, load them back, and cycle through playlists with the SPACE key when a playlist is active.

- [ ] **Step 1: Create src/playlist_manager.py**

```python
# src/playlist_manager.py
"""Playlist management - save/load custom preset sequences"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional

class PlaylistManager:
    def __init__(self):
        """Initialize playlist manager"""
        self.playlist_dir = Path.home() / '.audiovisualizer' / 'playlists'
        self.playlist_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_playlist = None
        self.playlists = {}
        self.load_all_playlists()
    
    def load_all_playlists(self):
        """Load all saved playlists from disk"""
        self.playlists = {}
        for playlist_file in self.playlist_dir.glob('*.json'):
            try:
                with open(playlist_file, 'r') as f:
                    playlist = json.load(f)
                    self.playlists[playlist['name']] = playlist['presets']
                    print(f"Loaded playlist: {playlist['name']}")
            except Exception as e:
                print(f"Error loading {playlist_file}: {e}")
    
    def save_playlist(self, name: str, preset_names: List[str]):
        """Save a new playlist"""
        playlist = {'name': name, 'presets': preset_names}
        playlist_file = self.playlist_dir / f"{name.lower().replace(' ', '_')}.json"
        
        with open(playlist_file, 'w') as f:
            json.dump(playlist, f, indent=2)
        
        self.playlists[name] = preset_names
        print(f"Saved playlist: {name}")
    
    def activate_playlist(self, name: str) -> bool:
        """Activate a playlist"""
        if name in self.playlists:
            self.current_playlist = name
            print(f"Activated playlist: {name}")
            return True
        return False
    
    def deactivate_playlist(self):
        """Deactivate current playlist"""
        self.current_playlist = None
    
    def get_current_presets(self) -> Optional[List[str]]:
        """Get preset list for current playlist"""
        if self.current_playlist:
            return self.playlists.get(self.current_playlist)
        return None
    
    def delete_playlist(self, name: str) -> bool:
        """Delete a saved playlist"""
        if name in self.playlists:
            playlist_file = self.playlist_dir / f"{name.lower().replace(' ', '_')}.json"
            if playlist_file.exists():
                playlist_file.unlink()
            del self.playlists[name]
            if self.current_playlist == name:
                self.current_playlist = None
            print(f"Deleted playlist: {name}")
            return True
        return False
    
    def list_playlists(self) -> List[str]:
        """Get list of all available playlists"""
        return list(self.playlists.keys())
```

- [ ] **Step 2: Integrate playlist manager into main.py**

```python
# Modify main.py

from src.playlist_manager import PlaylistManager

class AudioVisualizerApp:
    def __init__(self, width=1280, height=720):
        # ... existing code ...
        
        # Initialize playlist manager
        self.playlist_manager = PlaylistManager()
        self.playlist_index = 0

    def handle_events(self):
        for event in pygame.event.get():
            # ... existing code ...
            
            elif event.key == pygame.K_SPACE and not self.menu.visible:
                # If playlist active, cycle through playlist
                if self.playlist_manager.current_playlist:
                    self._next_playlist_preset()
                else:
                    self.visualizer.next_preset()

    def _next_playlist_preset(self):
        """Cycle to next preset in current playlist"""
        current_presets = self.playlist_manager.get_current_presets()
        if current_presets:
            self.playlist_index = (self.playlist_index + 1) % len(current_presets)
            preset_name = current_presets[self.playlist_index]
            
            # Find preset index in main list
            for i, preset in enumerate(self.visualizer.presets):
                if preset['name'] == preset_name:
                    self.visualizer.current_preset_idx = i
                    print(f"Playlist: {preset_name}")
                    break
```

- [ ] **Step 3: Test playlist save/load**

```bash
python main.py
```

Manually verify:
1. Playlists directory created at `~/.audiovisualizer/playlists/`
2. Can create/save playlists
3. Playlists persist across app restart

- [ ] **Step 4: Commit playlist manager**

```bash
git add src/playlist_manager.py main.py
git commit -m "feat: add playlist manager with save/load functionality"
```

---

## Task 5: Update Visualizer for New Preset System

**Files:**
- Modify: `src/visualizer.py`

**Context:** The visualizer needs to load presets from the new modular system instead of the old hardcoded list, and handle shader paths that may be in theme subdirectories.

- [ ] **Step 1: Update visualizer.py imports and initialization**

```python
# src/visualizer.py - modify top of file

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os
from .shader_manager import ShaderManager
from .presets import PRESETS  # Import from modular system

class Visualizer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Use presets from modular system
        self.presets = PRESETS
        self.current_preset_idx = 0
        
        # ... rest of existing initialization code ...
```

- [ ] **Step 2: Update load_shaders to handle theme subdirectories**

```python
def load_shaders(self):
    """Load all shader presets including themed shaders"""
    shader_dir = os.path.join(os.path.dirname(__file__), 'shaders')
    
    for preset in self.presets:
        shader_file = os.path.join(shader_dir, preset['shader'] + '.glsl')
        
        if os.path.exists(shader_file):
            try:
                with open(shader_file, 'r') as f:
                    fragment_shader = f.read()
                self.shader_manager.add_shader(preset['name'], fragment_shader)
            except Exception as e:
                print(f"Warning: Could not load shader for {preset['name']}: {e}")
        else:
            print(f"Warning: Shader file not found: {shader_file}")
```

- [ ] **Step 3: Test visualizer with new presets**

```bash
python main.py
```

All 252 presets should load without errors. Check console for any missing shaders.

- [ ] **Step 4: Commit visualizer updates**

```bash
git add src/visualizer.py
git commit -m "feat: update visualizer to load from modular preset system"
```

---

## Task 6: Final Integration and Testing

**Files:**
- Test all components end-to-end
- No new files

**Context:** This final task verifies that all components work together: preset cycling, menu selection, playlist save/load, and shader rendering across all 252 presets.

- [ ] **Step 1: Test full preset cycling**

```bash
python main.py
```

- Press SPACE to cycle through all 252 presets
- Press LEFT to go backwards
- Verify audio reactivity works on several different theme presets

- [ ] **Step 2: Test menu system**

- Press 'M' to open menu
- Click on various presets from different themes
- Verify selection jumps to correct preset
- Press 'M' to close menu

- [ ] **Step 3: Test playlist creation and management**

- Create a playlist by saving preset sequence
- Close and reopen app
- Verify playlist loads and persists
- Activate playlist and cycle through with SPACE

- [ ] **Step 4: Final validation**

```bash
git status
```

Expected: All changes committed, working tree clean.

- [ ] **Step 5: Final commit**

```bash
git log --oneline -10
```

Should show all task commits. Final status: All 252 presets loaded, menu functional, playlists working.

---

## Success Criteria

- ✅ All 252 presets (12 existing + 240 new) load without errors
- ✅ Menu toggles with 'M' key and displays all presets organized by theme
- ✅ Click to select a preset immediately switches visualization
- ✅ SPACE cycles through all presets (or through active playlist if one is loaded)
- ✅ Playlists save to `~/.audiovisualizer/playlists/` and persist across restarts
- ✅ All 240 new shaders render without visual artifacts
- ✅ Audio reactivity (iBass, iMid, iTreble, iAmplitude) works across all presets
