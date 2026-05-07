# Web-Based In-App Menu System Design

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:writing-plans (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the broken pygame font-based menu with a PIL/Pillow-rendered text system that provides full preset browsing, search, custom preset creation, and mix-and-match functionality.

**Architecture:** Text rendering via PIL/Pillow to images, displayed as pygame Surface overlays. Menu communicates directly with Visualizer instance via method calls. Presets stored as JSON with metadata. Custom presets live in local files with import/export.

**Tech Stack:** PIL/Pillow (text rendering), Pygame (display), JSON (persistence), Python standard library (file I/O)

---

## 1. Text Rendering System (PIL Bridge)

**Problem:** pygame.font has circular import issues in Python 3.14. Solution: Use PIL/Pillow to render text, convert to pygame-compatible images.

**TextRenderer class** (`src/ui/text_renderer.py`):
- Initialize with font name, sizes (normal, bold, small)
- `render(text, color, size='normal')` → returns (surface, rect) compatible with pygame.blit()
- Cache rendered text to avoid re-rendering same string every frame
- Support for different font sizes: normal (14px), bold (16px), small (10px)

**Color palette:**
- Text: (220, 220, 230) - light gray
- Labels: (150, 150, 170) - muted gray
- Accent: (100, 150, 255) - blue
- Success: (100, 255, 100) - green
- Warning: (255, 150, 100) - orange

---

## 2. Menu Data Structure

**Preset metadata** (JSON format):
```json
{
  "id": 0,
  "name": "Waveform",
  "theme": "core",
  "description": "Classic oscillating waveform",
  "shader": "core/waveform",
  "tags": ["classic", "simple", "waves"],
  "difficulty": "easy"
}
```

**Custom preset format** (saved locally):
```json
{
  "id": "custom_001",
  "name": "My Neon Plasma",
  "base_preset": 45,
  "mix_preset": 78,
  "parameters": {
    "color_hue": 0.8,
    "color_saturation": 1.2,
    "animation_speed": 1.5,
    "bass_sensitivity": 2.0,
    "mid_sensitivity": 1.8,
    "treble_sensitivity": 1.2
  },
  "created": "2026-05-07T18:30:00",
  "modified": "2026-05-07T18:35:00"
}
```

**Favorites list** (`~/.audiovisualizer/favorites.json`):
```json
{
  "favorites": [5, 12, 47, 152, "custom_001"]
}
```

---

## 3. Menu UI Components

### Search Bar
- Top-left, spans 40% of width
- Real-time filtering as user types
- Shows "Search presets..." placeholder
- Case-insensitive substring match on name + description + tags

### Category Filter
- Dropdown/selector showing all 25 themes + "Custom" + "All"
- Updates grid instantly
- Shows count: "Cosmic (10)"

### Favorites Toggle
- Star icon, top-right
- When active, shows only favorited presets
- Works with category filter and search

### Preset Grid
- Displays 5 columns × 4 rows visible (20 presets per page)
- Scrollable with mouse wheel or Page Up/Down
- Each card shows:
  - Theme color block (left 25%)
  - Preset name (left 75%, white text)
  - Difficulty indicator (small bar at bottom: easy/medium/hard)
- Selected preset highlighted with blue border
- Hover effect: slight brightness increase

### Right Sidebar (Selected Preset Details)
- Shows full name, theme, description
- 4 action buttons stacked:
  - [Play] - Preview in realtime (press Enter key equivalent)
  - [Edit] - Open parameter editor
  - [Mix] - Select another preset to combine with
  - [Add to Playlist] - Choose playlist or create new
- Heart icon to toggle favorite

### Parameter Editor (Overlay Modal)
- 6 sliders for audio reactivity:
  - Bass sensitivity (0.0 - 3.0)
  - Mid sensitivity (0.0 - 3.0)
  - Treble sensitivity (0.0 - 3.0)
  - Color hue shift (-180 - 180)
  - Color saturation (-1.0 - 2.0)
  - Animation speed (0.5 - 2.0)
- Live preview of changes in background
- [Save] [Cancel] buttons
- Input: text box to enter custom preset name

### Mix Tool (Modal)
- Shows currently selected preset on left
- "Mix with:" dropdown showing recent presets
- Blend slider (0% base / 100% other)
- Live preview
- [Save as Custom] [Cancel]

---

## 4. Data Storage

**Built-in presets:**
- `src/presets/presets.json` - All 252+ presets with metadata
- Format: Array of preset objects
- Incrementally expand from 252 → ~1000 over time

**Custom presets:**
- `~/.audiovisualizer/custom_presets/` directory
- One JSON file per custom preset: `custom_001.json`, etc.
- Indexed by creation timestamp for IDs

**Favorites:**
- `~/.audiovisualizer/favorites.json`
- Simple array of preset IDs and custom preset IDs

**Playlists:**
- Existing: `~/.audiovisualizer/playlists/`
- Extended to support custom preset IDs

---

## 5. Menu Integration

**MenuSystem class** (`src/ui/menu_system.py`):
- Initialize with Visualizer instance + TextRenderer
- `toggle()` - Show/hide menu
- `handle_event(event)` - Process keyboard/mouse
- `render(surface)` - Draw to pygame surface
- `get_selected_preset()` - Return current selection

**Key methods:**
- `search(query)` - Filter presets by text
- `filter_by_category(theme)` - Show only one theme
- `toggle_favorites()` - Show only liked presets
- `select_preset(preset_id)` - Set selection
- `save_custom_preset(name, parameters)` - Create custom
- `mix_presets(preset1_id, preset2_id, blend)` - Mix two presets
- `export_preset(preset_id, filepath)` - Save as JSON
- `import_preset(filepath)` - Load custom preset

---

## 6. Integration with Visualizer

**Minimal coupling:**
- MenuSystem takes Visualizer as constructor argument
- Calls only: `visualizer.current_preset_idx = X` to change presets
- No menu-specific code in Visualizer
- Visualizer unaware of menu complexity

**Event flow:**
```
User presses M
  → main.py calls menu.toggle()
  → MenuSystem.render() draws to surface
  → MenuSystem.handle_event() processes input
  → On selection: menu sets visualizer.current_preset_idx
  → Visualizer renders selected shader
```

---

## 7. File Structure

```
src/
├── ui/
│   ├── __init__.py
│   ├── text_renderer.py     # PIL text → pygame image bridge
│   ├── menu_system.py       # Main menu controller (refactored)
│   ├── menu_components.py   # UI element classes
│   └── presets_data.py      # Preset loading/caching
├── presets/
│   ├── __init__.py
│   └── presets.json         # All preset metadata (new)
└── utils/
    └── preset_validator.py  # Validate all shaders compile

~/.audiovisualizer/
├── custom_presets/
│   ├── custom_001.json
│   ├── custom_002.json
│   └── ...
├── favorites.json           # List of favorited preset IDs
└── playlists/               # (existing)
```

---

## 8. Error Handling

**Shader validation:**
- On startup: test-render each preset shader
- Log failures: "Preset #47 (Julia Set): shader failed to compile"
- Gracefully skip broken presets in menu
- Show warning badge on broken presets

**File I/O:**
- Handle missing custom preset files gracefully
- Auto-create ~/.audiovisualizer/ directories if missing
- Validate JSON format before loading

**Text rendering:**
- Fallback to system fonts if preferred font missing
- Scale text size if needed for different display resolutions

---

## 9. Testing Strategy

- Unit tests for TextRenderer (text rendering, caching)
- Unit tests for MenuSystem (filtering, selection, favorites)
- Integration test: menu ↔ visualizer communication
- Shader validation test: render sample of each preset
- UI tests: mouse/keyboard interaction, search, mix tool

---

## 10. Future Extensibility

- **Import themes:** Users can download preset packs
- **Cloud sync:** Optional sync custom presets to account
- **Preset ratings:** Community feedback on presets
- **Template system:** Create presets from templates (coming later)
