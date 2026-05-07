# Menu System - Remaining Tasks (4-14) Quick Guide

**Status:** Tasks 1-3 complete. Foundation in place (TextRenderer, data models, preset loading).

**Remaining:** 11 tasks to complete the menu system. Estimated effort: ~20-30 hours of development.

---

## Task 4: FavoritesManager with File Persistence

**Location:** `src/ui/presets_data.py` (new class)

**What it does:** Manages favorite presets with automatic JSON persistence.

**Key methods:**
- `__init__(favorites_file=None)` - Load from ~/.audiovisualizer/favorites.json
- `add(preset_id)`, `remove(preset_id)`, `toggle(preset_id) -> bool`
- `is_favorite(preset_id) -> bool`
- `save()` - Write to file
- `load()` - Read from file

**Tests needed:**
- Save/load round-trip
- Toggle behavior
- File creation if missing
- Handle corrupt JSON

**Time:** 1-2 hours

---

## Task 5: UI Component Base Classes

**Location:** `src/ui/components.py` (new file)

**Classes needed:**
```python
class UIComponent:
    """Base class for all UI elements"""
    def __init__(self, x, y, width, height)
    def render(self, surface)
    def handle_event(self, event)
    def contains_point(self, x, y) -> bool

class Button(UIComponent):
    """Clickable button"""
    def __init__(self, x, y, width, height, label, callback)
    
class Slider(UIComponent):
    """Value slider (0-1 range)"""
    def __init__(self, x, y, width, height, min_val, max_val, initial)
    @property
    def value -> float
    
class TextInput(UIComponent):
    """Text entry field"""
    def __init__(self, x, y, width, height, placeholder, max_length)
    @property
    def text -> str
    
class Modal(UIComponent):
    """Overlay dialog"""
    def __init__(self, x, y, width, height, title)
    def add_component(component: UIComponent)
```

**Time:** 2-3 hours

---

## Task 6: Search Bar Component

**Location:** `src/ui/menu_components.py` (new file)

**What it does:** Text input with real-time preset filtering.

**Key logic:**
- Input takes user query
- Calls `preset_manager.search(query)` 
- Updates grid with filtered results
- Case-insensitive substring matching

**Integration:** Works with Task 9 (Preset Grid)

**Time:** 1.5-2 hours

---

## Task 7: Category Filter Dropdown

**What it does:** Dropdown showing themes + "Custom" + "All"

**Key logic:**
- Dropdown opens on click
- Shows list: "All" + theme list sorted (core first)
- Clicking theme filters grid
- Shows count: "Cosmic (10)"

**Integration:** Works with Task 9 (Preset Grid)

**Time:** 2-3 hours

---

## Task 8: Favorites Toggle Button

**What it does:** Star icon to toggle favorite status.

**Key logic:**
- Click toggles current preset favorite
- Icon filled/unfilled based on state
- Calls `favorites_manager.toggle(preset_id)`
- Auto-saves to file

**Integration:** Lives in Task 10 (Details Panel)

**Time:** 1 hour

---

## Task 9: Preset Grid Display

**What it does:** Main grid showing presets (5 cols × 4 rows visible)

**Key features:**
- Render 20 presets per page in grid
- Each card shows: color block + name + difficulty indicator
- Selected preset highlighted with blue border
- Hover effect: brightness increase
- Mouse wheel scrolling
- Click to select preset

**Data needed from Tasks 6-7:**
- Filtered preset list from search
- Filtered preset list from category

**Time:** 3-4 hours

---

## Task 10: Selected Preset Details Panel

**Location:** Right sidebar of menu

**What it shows:**
- Full name (large text)
- Theme (small label)
- Description (multi-line)
- 4 action buttons: [Play] [Edit] [Mix] [Add to Playlist]
- Heart icon (favorite toggle) - Task 8

**Time:** 2-3 hours

---

## Task 11: Parameter Editor Modal

**What it does:** Overlay for editing custom preset parameters.

**Sliders (6 total):**
- Bass sensitivity (0.0 - 3.0)
- Mid sensitivity (0.0 - 3.0)
- Treble sensitivity (0.0 - 3.0)
- Color hue (-180 - 180)
- Color saturation (-1.0 - 2.0)
- Animation speed (0.5 - 2.0)

**Features:**
- Real-time preview in background
- Input field for custom preset name
- [Save] [Cancel] buttons

**Data flow:**
1. User clicks [Edit] on a preset
2. Modal opens with current values
3. User adjusts sliders
4. [Save] creates CustomPreset with parameters
5. Calls `preset_manager.save_custom_preset(custom)`

**Time:** 4-5 hours

---

## Task 12: Mix Tool Modal

**What it does:** Combine two presets by blending parameters.

**Features:**
- Show base preset on left
- Dropdown to select "Mix with:" preset
- Slider for blend (0% base / 100% other)
- Live preview
- [Save as Custom] [Cancel] buttons

**Logic:**
1. Blend parameters: `blended = base * (1-blend) + other * blend`
2. Create CustomPreset with blended parameters
3. Save to file

**Time:** 2-3 hours

---

## Task 13: Menu Container & Integration

**What it does:** Main MenuSystem class that ties everything together.

**Key components:**
- Search bar (Task 6)
- Category filter (Task 7)
- Favorites toggle
- Preset grid (Task 9)
- Selected preset details (Task 10)
- Parameter editor modal (Task 11)
- Mix tool modal (Task 12)

**Key methods:**
```python
class MenuSystem:
    def __init__(self, visualizer, preset_manager, favorites_manager)
    def toggle() - Show/hide menu
    def render(surface) - Draw all components
    def handle_event(event) - Process input
    def select_preset(preset_id) - Update visualizer
```

**Integration with Visualizer:**
- Only interaction: `visualizer.current_preset_idx = preset_id`
- Call from: Grid click, [Play] button, keyboard Enter

**Time:** 3-4 hours

---

## Task 14: Event Handling & Main Integration

**What it does:** Wire menu into main application.

**Changes needed in `main.py`:**
```python
from src.ui.menu_system import MenuSystem

class AudioVisualizerApp:
    def __init__(self):
        # ... existing code ...
        self.menu = MenuSystem(self.visualizer, preset_manager, favorites_manager)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.key == pygame.K_m:
                self.menu.toggle()
            if self.menu.visible:
                self.menu.handle_event(event)
    
    def render(self):
        # ... render visualizer ...
        if self.menu.visible:
            self.menu.render(menu_surface)
            # Blend menu_surface onto main surface
```

**Keyboard shortcuts:**
- M: Toggle menu
- Arrow keys: Navigate grid
- Enter: Select preset
- Page Up/Down: Scroll grid
- Esc: Close menu (if open), else exit app

**Mouse support:**
- Click preset: Select
- Wheel: Scroll grid
- Click buttons: Trigger actions

**Time:** 2-3 hours

---

## Testing Strategy for Tasks 4-14

**Unit tests per task:**
- Each task should have `tests/ui/test_<component>.py`
- Test rendering (surfaces created)
- Test events (keyboard/mouse)
- Test state changes

**Integration tests:**
- Menu with visualizer communication
- Full menu flow: search → select → preview
- Custom preset creation and save
- Favorites persistence

**Manual testing checklist:**
- [ ] Menu opens/closes with M key
- [ ] Search filters presets in real-time
- [ ] Category filter works
- [ ] Click preset selects it
- [ ] Details panel shows correct info
- [ ] [Edit] opens parameter editor
- [ ] Sliders update live preview
- [ ] [Save] creates custom preset
- [ ] [Mix] opens and blends correctly
- [ ] Favorites persist across sessions
- [ ] [Add to Playlist] works
- [ ] Arrow keys navigate
- [ ] Mouse wheel scrolls

---

## Architecture Diagram (Tasks 4-14)

```
MenuSystem (Task 13)
├── SearchBar (Task 6)
├── CategoryFilter (Task 7)
├── PresetGrid (Task 9)
│   └── Each card triggers [Play] → visualizer.current_preset_idx
├── DetailsPanel (Task 10)
│   ├── [Play] button
│   ├── [Edit] button → ParameterEditorModal (Task 11)
│   ├── [Mix] button → MixToolModal (Task 12)
│   ├── [Add to Playlist] button
│   └── Heart icon (Task 8)
├── ParameterEditorModal (Task 11)
├── MixToolModal (Task 12)
└── main.py integration (Task 14)
    └── Listens for M key → menu.toggle()
    └── Routes events → menu.handle_event()
    └── Renders menu surface
    └── Updates visualizer on selection
```

---

## Dependencies Between Tasks

```
Task 4  (FavoritesManager) - Standalone
Task 5  (UIComponent base) - Dependency for Tasks 6-12
Task 6  (SearchBar) - Needs Tasks 4-5
Task 7  (CategoryFilter) - Needs Tasks 4-5
Task 8  (Favorites toggle) - Needs Tasks 4-5
Task 9  (PresetGrid) - Needs Tasks 4-7
Task 10 (DetailsPanel) - Needs Tasks 4-8
Task 11 (ParamEditor) - Needs Tasks 4-5, 10
Task 12 (MixTool) - Needs Tasks 4-5, 10
Task 13 (MenuSystem) - Needs Tasks 4-12
Task 14 (Integration) - Needs Task 13
```

**Build order:** 4 → 5 → 6,7,8 (parallel) → 9 → 10 → 11,12 (parallel) → 13 → 14

---

## Quick Wins for Minimal Menu

If you want a working menu quickly, focus on:
1. Task 4 (FavoritesManager) - 1-2 hrs
2. Task 5 (UI base classes) - 2-3 hrs
3. Task 9 (Preset grid) - 3-4 hrs
4. Task 10 (Details) - 2-3 hrs
5. Task 13 (Container) - 3-4 hrs
6. Task 14 (Integration) - 2-3 hrs

**Result:** Basic menu showing presets, clicking to select. No modals/editing.
**Time:** ~15-20 hours
**Then add:** Tasks 6-8, 11-12 for full features (another 10+ hours)

---

## Debugging Notes

**Common issues:**
- Menu not rendering: Check `menu.visible` flag
- Clicks not registering: Verify `handle_event()` receives pygame events
- Presets not loading: Check presets.json path and JSON format
- Custom presets not saving: Verify ~/.audiovisualizer/custom_presets/ directory exists
- Text not visible: Check TextRenderer caching and surface blitting

**Performance:**
- Cache rendered text aggressively (Task 1 already does this)
- Don't re-render grid every frame if nothing changed
- Use dirty rect updates for menu surface

---

## File Summary

**New files to create (Tasks 4-14):**
- `src/ui/presets_data.py` - FavoritesManager (Task 4)
- `src/ui/components.py` - UI base classes (Task 5)
- `src/ui/menu_components.py` - Specific components (Tasks 6-12)
- `src/ui/menu_system.py` - Menu container (Task 13, refactor from old)
- `tests/ui/test_*.py` - Tests for each task
- Update `main.py` - Integration (Task 14)

**Total new code:** ~2000-2500 lines implementation + ~1000-1500 lines tests

---

## Next Steps

1. **For implementation:** Follow tasks 4-14 in dependency order using same subagent pattern
2. **For quick testing:** Create Tasks 4, 5, 9, 10, 13, 14 first (MVP)
3. **For full features:** Complete all 14 tasks then add validation/error handling

All foundation work (Tasks 1-3) is complete and tested. Tasks 4-14 are pure feature implementation with clear dependencies and testable pieces.
