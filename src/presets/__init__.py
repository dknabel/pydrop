"""Preset module - now uses presets.json for all 252 presets from 25 themes

Previously this module aggregated presets from individual theme Python files.
Now all presets are loaded from src/presets/presets.json via PresetManager.
The core presets are defined in core.py and loaded into the JSON file.
"""

from . import core
from .core import PRESETS

__all__ = ['core', 'PRESETS']
