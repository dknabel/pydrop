# Preset Refinement Design

**Date:** 2026-05-07  
**Scope:** Enhance all 24 presets with improved audio reactivity, cohesive color schemes, and unique animation mappings

## Overview

Refine the audio visualizer's preset system to move away from generic, neon-heavy designs toward visually pleasing, musically responsive animations. Each preset will have:

1. **Unique Color Palette** — Cohesive, non-neon color scheme tailored to the theme
2. **Audio Dimension Mapping** — Custom assignment of bass/mid/treble/amplitude to visual controls
3. **Dynamic Animation Response** — Faster reactions to audio changes, smoother transitions

## Color Palettes by Theme

| Theme | Colors |
|-------|--------|
| Abstract | Grayscale with soft lavender accents |
| Alchemical | Deep purple, gold, copper |
| Atmospheric | Soft periwinkle, misty gray, cool white |
| Bioluminescent | Soft violet, muted lime, soft teal |
| Celestial | Deep purple-blue, soft lavender, warm cream |
| Chromatic | Soft pastels: dusty rose, sage, periwinkle, butter |
| Core | Warm gray, soft gold, sage green |
| Cosmic | Deep indigo, rust, deep gold |
| Crystalline | Icy lavender, silver, cool white |
| Digital | Crisp sage, cool white, soft purple-gray |
| Dimensional | Warm terracotta → cool violet gradient |
| Ethereal | Pale lavender, soft peach, cool white |
| Infernal | Deep magenta-red, burnt orange, charcoal |
| Kinetic | Warm sienna, deep rust, gold |
| Liquids | Ocean blue, teal, seafoam |
| Mechanical | Gunmetal, cool silver, dark slate |
| Metamorphic | Earthy brown → soft violet |
| Organic | Moss green, warm brown, terracotta |
| Psychedelic | Soft magenta, dusty purple, sage |
| Quantum | Cool indigo, soft violet, pale periwinkle |
| Resonant | Soft purple, sage, warm mauve |
| Retro Aero | Teal, warm gold, soft lavender, cream |
| Synesthetic | Multi-tone: coral, lavender, indigo, gold |
| Temporal | Cool violet-gray → warm ochre |

## Audio Dimension Mapping

Each preset will define how audio dimensions control visuals. Mappings will be chosen per-preset to match the theme:

- **Audio Dimensions:** Amplitude (overall volume), Bass (low frequencies), Mid (mid frequencies), Treble (high frequencies)
- **Visual Controls:** Scale/size, rotation speed, glow/brightness, particle density, color shift, transparency, sway/movement

Example mappings:
- **Kinetic**: Bass → scale, Mid → rotation, Treble → particle density, Amplitude → overall intensity
- **Ethereal**: Amplitude → glow, Bass → gentle sway, Mid → color shift, Treble → transparency
- **Infernal**: Bass → heat/intensity, Mid → rotation speed, Treble → spark emission, Amplitude → overall brightness

## Animation Behavior

- **Dynamic Response:** Animations react immediately to audio changes (no lag)
- **Multi-Dimensional:** Use multiple audio dimensions simultaneously for richer, more complex animations
- **Smooth Transitions:** Avoid jarring jumps; use interpolation for fluid motion
- **Balanced Reactivity:** Ensure animations are responsive without being overwhelming

## Implementation Scope

- Modify each of 24 preset files to include color definitions and audio mappings
- Update animation logic to use multi-dimensional audio input
- Ensure backward compatibility with existing rendering system
- No new visualization primitives or features; purely configuration and behavior refinement

## Success Criteria

- ✓ Each preset has a visually distinct color palette
- ✓ Animations respond dynamically to multiple audio dimensions
- ✓ No neon/harsh color schemes; all palettes are visually pleasing
- ✓ Each theme has a unique audio-to-visual mapping

## Out of Scope

- Adding new animation effects
- UI changes
- Refactoring rendering system
- New preset categories
