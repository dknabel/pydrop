"""Preset module - aggregates all 252 presets from 25 themes"""

from . import core
from . import cosmic
from . import organic
from . import retro_aero
from . import digital
from . import abstract
from . import liquids
from . import crystalline
from . import psychedelic
from . import atmospheric
from . import mechanical
from . import bioluminescent
from . import quantum
from . import temporal
from . import dimensional
from . import ethereal
from . import infernal
from . import celestial
from . import metamorphic
from . import synesthetic
from . import crystallized
from . import resonant
from . import chromatic
from . import kinetic
from . import alchemical


def _add_theme(presets_list, theme_name):
    """Add theme metadata to all presets in a list."""
    for preset in presets_list:
        preset['theme'] = theme_name
    return presets_list


# Aggregate all presets with theme metadata
PRESETS = (
    _add_theme(core.PRESETS, 'core') +
    _add_theme(cosmic.PRESETS, 'cosmic') +
    _add_theme(organic.PRESETS, 'organic') +
    _add_theme(retro_aero.PRESETS, 'retro_aero') +
    _add_theme(digital.PRESETS, 'digital') +
    _add_theme(abstract.PRESETS, 'abstract') +
    _add_theme(liquids.PRESETS, 'liquids') +
    _add_theme(crystalline.PRESETS, 'crystalline') +
    _add_theme(psychedelic.PRESETS, 'psychedelic') +
    _add_theme(atmospheric.PRESETS, 'atmospheric') +
    _add_theme(mechanical.PRESETS, 'mechanical') +
    _add_theme(bioluminescent.PRESETS, 'bioluminescent') +
    _add_theme(quantum.PRESETS, 'quantum') +
    _add_theme(temporal.PRESETS, 'temporal') +
    _add_theme(dimensional.PRESETS, 'dimensional') +
    _add_theme(ethereal.PRESETS, 'ethereal') +
    _add_theme(infernal.PRESETS, 'infernal') +
    _add_theme(celestial.PRESETS, 'celestial') +
    _add_theme(metamorphic.PRESETS, 'metamorphic') +
    _add_theme(synesthetic.PRESETS, 'synesthetic') +
    _add_theme(crystallized.PRESETS, 'crystallized') +
    _add_theme(resonant.PRESETS, 'resonant') +
    _add_theme(chromatic.PRESETS, 'chromatic') +
    _add_theme(kinetic.PRESETS, 'kinetic') +
    _add_theme(alchemical.PRESETS, 'alchemical')
)

__all__ = ['PRESETS']
