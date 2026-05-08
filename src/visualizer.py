"""Main visualizer with GLSL shader rendering"""

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os
from .shader_manager import ShaderManager
from .ui.presets_data import PresetManager

class Visualizer:
    def __init__(self, width, height, audio_engine=None):
        self.width = width
        self.height = height

        # Presets - load from PresetManager (presets.json)
        self.preset_manager = PresetManager()
        self.presets = [{'name': p.name, 'shader': p.shader, 'visual_type': p.visual_type, 'audio_mapping': p.audio_mapping}
                        for p in self.preset_manager.builtin_presets]
        self.preset_objects = {p.name: p for p in self.preset_manager.builtin_presets}
        self.current_preset_idx = 0 if self.presets else 0

        # Audio engine for getting audio dimensions
        self.audio_engine = audio_engine

        # Setup OpenGL
        glClearColor(0.05, 0.05, 0.08, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)

        # Shader manager
        self.shader_manager = ShaderManager()
        self.load_shaders()

        # Fullscreen quad for rendering
        self.setup_quad()

        # Time
        self.time = 0.0

    def load_shaders(self):
        """Load all shader presets including themed shaders"""
        shader_dir = os.path.join(os.path.dirname(__file__), 'shaders')

        # Map visual types to shader files (for new presets without 'shader' field)
        shader_map = {
            'particles': 'particles',
            'geometric': 'geometric',
            'turbulent': 'turbulent',
            'ethereal': 'ethereal'
        }

        for preset in self.presets:
            # Option 1: Use existing shader field if present
            if 'shader' in preset and preset['shader']:
                shader_name = preset['shader']  # Use the original shader field (e.g., 'kinetic/particle_stream')
            else:
                # Option 2: Only fall back to visual_type routing for presets without a shader field
                visual_type = preset.get('visual_type', 'particles')
                shader_name = shader_map.get(visual_type, 'particles')

            shader_file = os.path.join(shader_dir, shader_name + '.glsl')

            if os.path.exists(shader_file):
                try:
                    with open(shader_file, 'r') as f:
                        fragment_shader = f.read()
                    self.shader_manager.add_shader(preset['name'], fragment_shader)
                except Exception as e:
                    pass

    def setup_quad(self):
        """Setup fullscreen quad for rendering"""
        vertices = np.array([
            [-1, -1, 0],
            [1, -1, 0],
            [1, 1, 0],
            [-1, 1, 0]
        ], dtype=np.float32)
        
        indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
        
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        
        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        
        pos_loc = 0
        glVertexAttribPointer(pos_loc, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
        glEnableVertexAttribArray(pos_loc)
        
        self.index_count = len(indices)

    def update(self, audio_data):
        """Update visualizer with audio data"""
        self.audio_data = audio_data
        self.time += 0.016  # Assume 60 FPS

    def next_preset(self):
        """Switch to next preset, skipping broken shaders"""
        attempts = 0
        while attempts < len(self.presets):
            self.current_preset_idx = (self.current_preset_idx + 1) % len(self.presets)
            preset = self.presets[self.current_preset_idx]
            shader = self.shader_manager.get_shader(preset['name'])
            if shader is not None and shader.program is not None:
                break
            attempts += 1

    def prev_preset(self):
        """Switch to previous preset, skipping broken shaders"""
        attempts = 0
        while attempts < len(self.presets):
            self.current_preset_idx = (self.current_preset_idx - 1) % len(self.presets)
            preset = self.presets[self.current_preset_idx]
            shader = self.shader_manager.get_shader(preset['name'])
            if shader is not None and shader.program is not None:
                break
            attempts += 1

    def render(self):
        """Render visualization"""
        preset = self.presets[self.current_preset_idx]
        shader = self.shader_manager.get_shader(preset['name'])

        if shader is None or shader.program is None:
            return

        glUseProgram(shader.program)

        # Set uniforms
        shader.set_uniform_1f('iTime', self.time)
        shader.set_uniform_2f('iResolution', self.width, self.height)
        shader.set_uniform_1f('iAmplitude', self.audio_data['amplitude'])
        shader.set_uniform_1f('iBass', self.audio_data['bass'])
        shader.set_uniform_1f('iMid', self.audio_data['mid'])
        shader.set_uniform_1f('iTreble', self.audio_data['treble'])

        # Set color uniforms from preset
        try:
            preset_obj = self.preset_objects.get(preset['name'])
            if preset_obj and preset_obj.colors:
                # Convert colors from 0-255 to 0.0-1.0 range
                colors = preset_obj.colors
                if len(colors) >= 4:
                    for i in range(4):
                        r, g, b = colors[i]
                        shader.set_uniform_3f(f'color{i}', r/255.0, g/255.0, b/255.0)
        except Exception as e:
            pass

        # Apply audio mappings to shader uniforms for dynamic reactivity
        if self.audio_engine is not None:
            audio_dims = self.audio_engine.get_audio_dimensions()
            audio_mapping = preset.get('audio_mapping', {})

            # Apply audio mappings to shader uniforms
            for audio_dim, visual_control in audio_mapping.items():
                audio_value = audio_dims.get(audio_dim, 0.0)

                # Set appropriate uniform based on visual control name
                if visual_control == "intensity":
                    shader.set_uniform_1f('intensity', audio_value)
                elif visual_control == "scale":
                    shader.set_uniform_1f('scale', 1.0 + audio_value * 0.5)
                elif visual_control == "rotation":
                    shader.set_uniform_1f('rotation_speed', audio_value * 2.0)
                elif visual_control == "glow":
                    shader.set_uniform_1f('glow_intensity', audio_value)

        # Bind texture for frequency data
        freq_texture = self.create_texture_from_array(self.audio_data['frequency'])
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_1D, freq_texture)
        shader.set_uniform_1i('iFrequency', 0)

        # Render quad
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.index_count, GL_UNSIGNED_INT, None)

        glDeleteTextures([freq_texture])

    def create_texture_from_array(self, data):
        """Create OpenGL texture from numpy array"""
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_1D, texture)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glTexImage1D(GL_TEXTURE_1D, 0, GL_R32F, len(data), 0, GL_RED, GL_FLOAT, data.astype(np.float32))
        
        return texture


import ctypes
