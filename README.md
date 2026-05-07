# Audio Visualizer (Python)

A Milkdrop-style audio visualization application for desktop, built with Python, Pygame, and GLSL shaders.

## Features

- Real-time audio visualization using GLSL fragment shaders
- Multiple visualization presets
- Audio-reactive parameters (amplitude, frequency bands)
- Smooth, organic animations
- Microphone input support

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

- **SPACE** - Next preset
- **LEFT ARROW** - Previous preset
- **ESC** - Exit

## Architecture

- `main.py` - Application entry point
- `src/audio_engine.py` - Audio capture and analysis
- `src/visualizer.py` - Main visualization renderer
- `src/shader_manager.py` - GLSL shader compilation and management
- `src/presets.py` - Visualization presets
- `src/shaders/` - GLSL fragment shaders

## Shaders

Each preset corresponds to a GLSL fragment shader that processes audio data in real-time:

- `waveform.glsl` - Classic waveform visualization
- `particles.glsl` - Flowing particle system
- `kaleidoscope.glsl` - Symmetrical kaleidoscope patterns
