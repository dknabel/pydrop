"""Main visualizer with GLSL shader rendering"""

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os
from .shader_manager import ShaderManager
from .presets import PRESETS

class Visualizer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Setup OpenGL
        glClearColor(0.05, 0.05, 0.08, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        
        # Shader manager
        self.shader_manager = ShaderManager()
        self.load_shaders()
        
        # Presets
        self.presets = PRESETS
        self.current_preset_idx = 0
        
        # Fullscreen quad for rendering
        self.setup_quad()
        
        # Time
        self.time = 0.0

    def load_shaders(self):
        """Load all shader presets"""
        shader_dir = os.path.join(os.path.dirname(__file__), 'shaders')
        for preset in self.presets:
            shader_file = os.path.join(shader_dir, preset['shader'] + '.glsl')
            if os.path.exists(shader_file):
                with open(shader_file, 'r') as f:
                    fragment_shader = f.read()
                self.shader_manager.add_shader(preset['name'], fragment_shader)

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
        """Switch to next preset"""
        self.current_preset_idx = (self.current_preset_idx + 1) % len(self.presets)
        print(f"Preset: {self.presets[self.current_preset_idx]['name']}")

    def prev_preset(self):
        """Switch to previous preset"""
        self.current_preset_idx = (self.current_preset_idx - 1) % len(self.presets)
        print(f"Preset: {self.presets[self.current_preset_idx]['name']}")

    def render(self):
        """Render visualization"""
        preset = self.presets[self.current_preset_idx]
        shader = self.shader_manager.get_shader(preset['name'])
        
        if shader is None:
            return
        
        glUseProgram(shader.program)
        
        # Set uniforms
        shader.set_uniform_1f('iTime', self.time)
        shader.set_uniform_2f('iResolution', self.width, self.height)
        shader.set_uniform_1f('iAmplitude', self.audio_data['amplitude'])
        shader.set_uniform_1f('iBass', self.audio_data['bass'])
        shader.set_uniform_1f('iMid', self.audio_data['mid'])
        shader.set_uniform_1f('iTreble', self.audio_data['treble'])
        
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
