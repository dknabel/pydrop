# In-App Menu System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the broken pygame font-based menu with a PIL/Pillow-rendered text system providing preset browsing, search/filter, custom presets, and mix-and-match functionality.

**Architecture:** PIL/Pillow renders text to images, pygame displays them as overlays. Menu is completely separate from Visualizer (only communicates via `current_preset_idx`). Presets stored as JSON, custom presets in user home directory.

**Tech Stack:** PIL/Pillow (text), Pygame (display), JSON (storage), Python pathlib/json (I/O)

---

## Task 1: Create TextRenderer Class (PIL Text Bridge)

**Files:**
- Create: `src/ui/__init__.py`
- Create: `src/ui/text_renderer.py`
- Create: `tests/ui/__init__.py`
- Create: `tests/ui/test_text_renderer.py`

- [ ] **Step 1: Write failing test for TextRenderer initialization**

```python
# tests/ui/test_text_renderer.py
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
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /home/drew/Documents/audiovisualizerpy
python -m pytest tests/ui/test_text_renderer.py::test_text_renderer_init -v
```

Expected: `FAILED - ModuleNotFoundError: No module named 'src.ui'`

- [ ] **Step 3: Create UI package structure**

```python
# src/ui/__init__.py
"""UI components for menu system"""

from .text_renderer import TextRenderer

__all__ = ['TextRenderer']
```

- [ ] **Step 4: Implement TextRenderer class**

```python
# src/ui/text_renderer.py
"""PIL-based text rendering for pygame"""

from PIL import Image, ImageDraw, ImageFont
import pygame
from pathlib import Path

class TextRenderer:
    """Renders text using PIL, returns pygame-compatible surfaces"""
    
    def __init__(self, font_name=None, font_size_normal=14, font_size_bold=16, font_size_small=10):
        """
        Initialize TextRenderer
        
        Args:
            font_name: System font name or path (uses default if None)
            font_size_normal: Normal text size (pixels)
            font_size_bold: Bold text size (pixels)
            font_size_small: Small text size (pixels)
        """
        self.font_size_normal = font_size_normal
        self.font_size_bold = font_size_bold
        self.font_size_small = font_size_small
        self.font_name = font_name or "sans-serif"
        
        # Load fonts with fallback
        try:
            self.font_normal = ImageFont.truetype(self._get_font_path(), font_size_normal)
            self.font_bold = ImageFont.truetype(self._get_font_path(), font_size_bold)
            self.font_small = ImageFont.truetype(self._get_font_path(), font_size_small)
        except:
            # Fallback to default font if system font not found
            self.font_normal = ImageFont.load_default()
            self.font_bold = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
        
        # Rendering cache: {(text, color, size): (surface, rect)}
        self.cache = {}
    
    def _get_font_path(self):
        """Get system font path"""
        # Try common font locations
        font_paths = [
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),  # Linux
            Path("/System/Library/Fonts/Helvetica.ttc"),  # macOS
            Path("C:\\Windows\\Fonts\\arial.ttf"),  # Windows
        ]
        for path in font_paths:
            if path.exists():
                return str(path)
        return self.font_name
    
    def render(self, text, color=(220, 220, 230), size='normal'):
        """
        Render text to pygame-compatible surface
        
        Args:
            text: String to render
            color: RGB tuple (r, g, b)
            size: 'normal', 'bold', or 'small'
        
        Returns:
            (pygame.Surface, pygame.Rect) tuple
        """
        # Check cache first
        cache_key = (text, color, size)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Select font
        if size == 'bold':
            font = self.font_bold
        elif size == 'small':
            font = self.font_small
        else:
            font = self.font_normal
        
        # Render with PIL
        # Create image large enough for text
        temp_img = Image.new('RGBA', (1000, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(temp_img)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Create final image with exact size
        img = Image.new('RGBA', (text_width + 4, text_height + 4), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((2, 2), text, fill=color, font=font)
        
        # Convert to pygame surface
        mode = img.mode
        size_tuple = img.size
        data = img.tobytes()
        
        py_surface = pygame.image.fromstring(data, size_tuple, mode)
        rect = py_surface.get_rect()
        
        # Cache result
        self.cache[cache_key] = (py_surface, rect)
        return py_surface, rect
    
    def clear_cache(self):
        """Clear rendering cache (useful for memory management)"""
        self.cache.clear()
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
python -m pytest tests/ui/test_text_renderer.py -v
```

Expected: `PASSED (2 passed)`

- [ ] **Step 6: Commit**

```bash
git add src/ui/ tests/ui/
git commit -m "feat: add TextRenderer class for PIL-based text rendering

- PIL/Pillow-based text rendering avoiding pygame.font circular imports
- Render text to pygame-compatible surfaces
- Cache rendered text for performance
- Fallback to system fonts with graceful degradation
- Support normal, bold, and small text sizes"
```

---

## Task 2: Create Preset Data Models

**Files:**
- Create: `src/ui/models.py`
- Create: `tests/ui/test_models.py`

- [ ] **Step 1: Write failing tests for preset models**

```python
# tests/ui/test_models.py
import pytest
from src.ui.models import Preset, CustomPreset, FavoritesManager
import json

def test_preset_creation():
    """Preset can be created and accessed"""
    preset = Preset(
        id=0,
        name="Waveform",
        theme="core",
        description="Classic oscillating waveform",
        shader="core/waveform",
        tags=["classic", "simple"],
        difficulty="easy"
    )
    assert preset.id == 0
    assert preset.name == "Waveform"
    assert preset.theme == "core"

def test_preset_to_dict():
    """Preset converts to dictionary"""
    preset = Preset(0, "Test", "core", "desc", "shader", [], "easy")
    data = preset.to_dict()
    assert data['id'] == 0
    assert data['name'] == "Test"
    assert isinstance(data, dict)

def test_custom_preset_creation():
    """CustomPreset can be created with parameters"""
    custom = CustomPreset(
        id="custom_001",
        name="My Neon",
        base_preset=45,
        parameters={"bass_sensitivity": 2.0}
    )
    assert custom.id == "custom_001"
    assert custom.parameters["bass_sensitivity"] == 2.0

def test_favorites_manager():
    """FavoritesManager tracks favorites"""
    mgr = FavoritesManager()
    mgr.add(5)
    mgr.add("custom_001")
    assert mgr.is_favorite(5)
    assert mgr.is_favorite("custom_001")
    assert not mgr.is_favorite(999)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m pytest tests/ui/test_models.py -v
```

Expected: `FAILED - ModuleNotFoundError: No module named 'src.ui.models'`

- [ ] **Step 3: Implement data models**

```python
# src/ui/models.py
"""Data models for presets, custom presets, and favorites"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class Preset:
    """Built-in preset metadata"""
    id: int
    name: str
    theme: str
    description: str
    shader: str
    tags: List[str] = field(default_factory=list)
    difficulty: str = "medium"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Preset':
        """Create from dictionary"""
        return cls(**data)

@dataclass
class CustomPreset:
    """User-created preset with parameters"""
    id: str  # e.g., "custom_001"
    name: str
    base_preset: int  # ID of preset this is based on
    parameters: Dict[str, float] = field(default_factory=dict)
    mix_preset: Optional[int] = None  # If created by mixing two presets
    created: str = field(default_factory=lambda: datetime.now().isoformat())
    modified: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CustomPreset':
        """Create from dictionary"""
        return cls(**data)

class FavoritesManager:
    """Manages favorite presets"""
    
    def __init__(self):
        self.favorites: set = set()
    
    def add(self, preset_id) -> None:
        """Add preset to favorites"""
        self.favorites.add(preset_id)
    
    def remove(self, preset_id) -> None:
        """Remove preset from favorites"""
        self.favorites.discard(preset_id)
    
    def toggle(self, preset_id) -> bool:
        """Toggle favorite status, return new state"""
        if self.is_favorite(preset_id):
            self.remove(preset_id)
            return False
        else:
            self.add(preset_id)
            return True
    
    def is_favorite(self, preset_id) -> bool:
        """Check if preset is favorite"""
        return preset_id in self.favorites
    
    def to_list(self) -> List:
        """Convert to list for JSON serialization"""
        return list(self.favorites)
    
    def from_list(self, favorites_list: List) -> None:
        """Load from list"""
        self.favorites = set(favorites_list)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
python -m pytest tests/ui/test_models.py -v
```

Expected: `PASSED (4 passed)`

- [ ] **Step 5: Commit**

```bash
git add src/ui/models.py tests/ui/test_models.py
git commit -m "feat: add preset data models

- Preset: built-in preset metadata with to_dict/from_dict
- CustomPreset: user-created preset with parameters
- FavoritesManager: track favorited presets
- Support serialization to/from JSON"
```

---

## Task 3: Create Preset Data Loading

**Files:**
- Create: `src/ui/presets_data.py`
- Create: `src/presets/presets.json` (partial - expand later)
- Create: `tests/ui/test_presets_data.py`

- [ ] **Step 1: Create presets.json with existing preset data**

```python
# Convert existing presets to JSON
# src/presets/presets.json - Start with core presets as example
[
  {"id": 0, "name": "Waveform", "theme": "core", "description": "Classic oscillating waveform", "shader": "core/waveform", "tags": ["classic", "waves"], "difficulty": "easy"},
  {"id": 1, "name": "Particles", "theme": "core", "description": "Particle system", "shader": "core/particles", "tags": ["particles"], "difficulty": "easy"},
  ...
  // Add all 252 existing presets here
]
```

- [ ] **Step 2: Write failing tests for preset loading**

```python
# tests/ui/test_presets_data.py
import pytest
from src.ui.presets_data import PresetManager
import tempfile
from pathlib import Path

def test_preset_manager_load_builtin():
    """PresetManager loads built-in presets from JSON"""
    mgr = PresetManager()
    presets = mgr.load_builtin_presets()
    assert len(presets) > 0
    assert presets[0].id == 0
    assert presets[0].name == "Waveform"

def test_preset_manager_get_by_id():
    """PresetManager retrieves preset by ID"""
    mgr = PresetManager()
    preset = mgr.get_preset(0)
    assert preset.id == 0
    assert preset.name == "Waveform"

def test_preset_manager_search():
    """PresetManager searches presets by query"""
    mgr = PresetManager()
    results = mgr.search("wave")
    assert len(results) > 0
    assert any(p.name.lower() == "waveform" for p in results)

def test_preset_manager_filter_by_category():
    """PresetManager filters by theme"""
    mgr = PresetManager()
    results = mgr.filter_by_theme("core")
    assert len(results) > 0
    assert all(p.theme == "core" for p in results)
```

- [ ] **Step 3: Run test to verify it fails**

```bash
python -m pytest tests/ui/test_presets_data.py::test_preset_manager_load_builtin -v
```

Expected: `FAILED - ModuleNotFoundError`

- [ ] **Step 4: Implement PresetManager**

```python
# src/ui/presets_data.py
"""Preset data loading and management"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from src.ui.models import Preset, CustomPreset

class PresetManager:
    """Load, search, and manage presets"""
    
    def __init__(self):
        self.builtin_presets: List[Preset] = []
        self.custom_presets: Dict[str, CustomPreset] = {}
        self.presets_file = Path(__file__).parent.parent / "presets" / "presets.json"
        self.custom_dir = Path.home() / ".audiovisualizer" / "custom_presets"
        
        # Load on initialization
        self.load_builtin_presets()
        self.load_custom_presets()
    
    def load_builtin_presets(self) -> List[Preset]:
        """Load built-in presets from JSON"""
        try:
            with open(self.presets_file, 'r') as f:
                data = json.load(f)
            self.builtin_presets = [Preset.from_dict(p) for p in data]
            return self.builtin_presets
        except FileNotFoundError:
            print(f"Warning: presets.json not found at {self.presets_file}")
            return []
    
    def load_custom_presets(self) -> Dict[str, CustomPreset]:
        """Load custom presets from user directory"""
        self.custom_dir.mkdir(parents=True, exist_ok=True)
        self.custom_presets = {}
        
        for preset_file in self.custom_dir.glob("*.json"):
            try:
                with open(preset_file, 'r') as f:
                    data = json.load(f)
                custom = CustomPreset.from_dict(data)
                self.custom_presets[custom.id] = custom
            except Exception as e:
                print(f"Warning: Failed to load custom preset {preset_file}: {e}")
        
        return self.custom_presets
    
    def get_preset(self, preset_id: int) -> Optional[Preset]:
        """Get built-in preset by ID"""
        try:
            return self.builtin_presets[preset_id]
        except IndexError:
            return None
    
    def get_custom_preset(self, preset_id: str) -> Optional[CustomPreset]:
        """Get custom preset by ID"""
        return self.custom_presets.get(preset_id)
    
    def search(self, query: str) -> List[Preset]:
        """Search presets by name, description, or tags"""
        query_lower = query.lower()
        results = []
        
        for preset in self.builtin_presets:
            if (query_lower in preset.name.lower() or
                query_lower in preset.description.lower() or
                any(query_lower in tag.lower() for tag in preset.tags)):
                results.append(preset)
        
        return results
    
    def filter_by_theme(self, theme: str) -> List[Preset]:
        """Get all presets of a theme"""
        return [p for p in self.builtin_presets if p.theme == theme]
    
    def get_all_themes(self) -> List[str]:
        """Get list of all themes"""
        themes = list(set(p.theme for p in self.builtin_presets))
        # Sort with 'core' first
        if 'core' in themes:
            themes.remove('core')
            themes = ['core'] + sorted(themes)
        else:
            themes.sort()
        return themes
    
    def save_custom_preset(self, custom: CustomPreset) -> None:
        """Save custom preset to file"""
        self.custom_dir.mkdir(parents=True, exist_ok=True)
        preset_file = self.custom_dir / f"{custom.id}.json"
        
        with open(preset_file, 'w') as f:
            json.dump(custom.to_dict(), f, indent=2)
        
        self.custom_presets[custom.id] = custom
    
    def delete_custom_preset(self, preset_id: str) -> None:
        """Delete custom preset"""
        if preset_id in self.custom_presets:
            preset_file = self.custom_dir / f"{preset_id}.json"
            preset_file.unlink()
            del self.custom_presets[preset_id]
```

- [ ] **Step 5: Create initial presets.json**

First, convert existing preset definitions to JSON format. Parse the current preset system and export to JSON:

```bash
# Create script to convert existing presets to JSON
python << 'EOF'
import json
from pathlib import Path
from src.presets import PRESETS

# Convert to list of dicts with all fields
presets_data = []
for preset in PRESETS:
    presets_data.append({
        "id": len(presets_data),
        "name": preset.get('name', f'Preset {len(presets_data)}'),
        "theme": preset.get('theme', 'unknown'),
        "description": preset.get('description', ''),
        "shader": preset.get('shader', ''),
        "tags": preset.get('tags', []),
        "difficulty": preset.get('difficulty', 'medium')
    })

# Save to JSON
output_path = Path("src/presets/presets.json")
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, 'w') as f:
    json.dump(presets_data, f, indent=2)

print(f"Exported {len(presets_data)} presets to {output_path}")
EOF
```

- [ ] **Step 6: Run tests to verify they pass**

```bash
python -m pytest tests/ui/test_presets_data.py -v
```

Expected: `PASSED (all tests)`

- [ ] **Step 7: Commit**

```bash
git add src/ui/presets_data.py src/presets/presets.json tests/ui/test_presets_data.py
git commit -m "feat: add PresetManager for data loading and searching

- Load built-in presets from JSON
- Load custom presets from ~/.audiovisualizer/custom_presets/
- Search by name, description, or tags
- Filter by theme/category
- Save/delete custom presets"
```

---

## Task 4: Create Favorites Manager

**Files:**
- Modify: `src/ui/presets_data.py` (add favorites methods)
- Create: `tests/ui/test_favorites.py`

- [ ] **Step 1: Write failing tests for favorites persistence**

```python
# tests/ui/test_favorites.py
import pytest
import tempfile
from pathlib import Path
from src.ui.presets_data import FavoritesManager

def test_favorites_save_and_load():
    """Favorites can be saved to file and loaded"""
    with tempfile.TemporaryDirectory() as tmpdir:
        fav_file = Path(tmpdir) / "favorites.json"
        
        mgr = FavoritesManager(fav_file)
        mgr.add(5)
        mgr.add(12)
        mgr.save()
        
        # Load in new manager
        mgr2 = FavoritesManager(fav_file)
        assert mgr2.is_favorite(5)
        assert mgr2.is_favorite(12)
        assert not mgr2.is_favorite(99)

def test_favorites_toggle():
    """Toggle favorite status"""
    with tempfile.TemporaryDirectory() as tmpdir:
        mgr = FavoritesManager(Path(tmpdir) / "fav.json")
        
        assert mgr.toggle(5) == True  # Add
        assert mgr.toggle(5) == False  # Remove
        assert mgr.toggle(5) == True  # Add again
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m pytest tests/ui/test_favorites.py -v
```

Expected: `FAILED`

- [ ] **Step 3: Add FavoritesManager class to presets_data.py**

```python
# Add to src/ui/presets_data.py

class FavoritesManager:
    """Manage favorite presets with file persistence"""
    
    def __init__(self, favorites_file: Path = None):
        if favorites_file is None:
            favorites_file = Path.home() / ".audiovisualizer" / "favorites.json"
        self.favorites_file = favorites_file
        self.favorites = set()
        self.load()
    
    def load(self) -> None:
        """Load favorites from file"""
        if self.favorites_file.exists():
            try:
                with open(self.favorites_file, 'r') as f:
                    data = json.load(f)
                self.favorites = set(data.get('favorites', []))
            except Exception as e:
                print(f"Warning: Failed to load favorites: {e}")
    
    def save(self) -> None:
        """Save favorites to file"""
        self.favorites_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.favorites_file, 'w') as f:
            json.dump({'favorites': list(self.favorites)}, f, indent=2)
    
    def add(self, preset_id) -> None:
        """Add to favorites"""
        self.favorites.add(preset_id)
    
    def remove(self, preset_id) -> None:
        """Remove from favorites"""
        self.favorites.discard(preset_id)
    
    def toggle(self, preset_id) -> bool:
        """Toggle, return new state"""
        if self.is_favorite(preset_id):
            self.remove(preset_id)
            return False
        else:
            self.add(preset_id)
            return True
    
    def is_favorite(self, preset_id) -> bool:
        """Check if favorite"""
        return preset_id in self.favorites
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
python -m pytest tests/ui/test_favorites.py -v
```

Expected: `PASSED`

- [ ] **Step 5: Commit**

```bash
git add src/ui/presets_data.py tests/ui/test_favorites.py
git commit -m "feat: add FavoritesManager for persistent favorites

- Save/load favorites from ~/.audiovisualizer/favorites.json
- Add/remove/toggle favorite status
- Persistent across sessions"
```

---

## Task 5-14: Remaining Implementation Tasks

Due to length constraints, here's the outline for remaining tasks:

**Task 5:** Create UI component base classes (Button, Slider, TextInput, Modal)
**Task 6:** Implement Search Bar component
**Task 7:** Implement Category Filter dropdown
**Task 8:** Implement Preset Grid display
**Task 9:** Implement Selected Preset Details panel
**Task 10:** Implement Parameter Editor modal
**Task 11:** Implement Mix Tool modal
**Task 12:** Integrate Menu with Visualizer
**Task 13:** Add keyboard/mouse event handling
**Task 14:** Add validation and error handling

*[Each task follows same TDD pattern: failing test → implementation → pass test → commit]*

---

## Integration Checklist

- [ ] Menu disabled in main.py (old pygame menu removed)
- [ ] New MenuSystem imported and initialized
- [ ] Menu M toggle key working
- [ ] Preset selection updates visualizer
- [ ] Custom presets persist across sessions
- [ ] All tests passing

---

## Testing Commands

```bash
# Run all UI tests
pytest tests/ui/ -v

# Run specific component tests
pytest tests/ui/test_text_renderer.py -v
pytest tests/ui/test_presets_data.py -v

# Coverage report
pytest tests/ui/ --cov=src/ui --cov-report=html
```
