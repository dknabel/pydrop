"""GLSL Shader management"""

from OpenGL.GL import *
import numpy as np

VERTEX_SHADER = """
#version 330 core
layout(location = 0) in vec3 position;
void main() {
    gl_Position = vec4(position, 1.0);
}
"""

class Shader:
    def __init__(self, name, fragment_source):
        self.name = name
        self.program = self.compile_program(VERTEX_SHADER, fragment_source)
        self.uniforms = {}

    def compile_program(self, vertex_src, fragment_src):
        """Compile vertex and fragment shaders"""
        vertex = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex, vertex_src)
        glCompileShader(vertex)
        
        if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
            print(f"Vertex shader compile error: {glGetShaderInfoLog(vertex)}")
            return None
        
        fragment = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment, fragment_src)
        glCompileShader(fragment)
        
        if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
            print(f"Fragment shader compile error: {glGetShaderInfoLog(fragment)}")
            return None
        
        program = glCreateProgram()
        glAttachShader(program, vertex)
        glAttachShader(program, fragment)
        glLinkProgram(program)
        
        if not glGetProgramiv(program, GL_LINK_STATUS):
            print(f"Program link error: {glGetProgramInfoLog(program)}")
            return None
        
        glDeleteShader(vertex)
        glDeleteShader(fragment)
        
        return program

    def set_uniform_1f(self, name, value):
        """Set float uniform"""
        if self.program:
            loc = glGetUniformLocation(self.program, name)
            if loc != -1:
                glUniform1f(loc, value)

    def set_uniform_2f(self, name, x, y):
        """Set vec2 uniform"""
        if self.program:
            loc = glGetUniformLocation(self.program, name)
            if loc != -1:
                glUniform2f(loc, x, y)

    def set_uniform_1i(self, name, value):
        """Set int uniform"""
        if self.program:
            loc = glGetUniformLocation(self.program, name)
            if loc != -1:
                glUniform1i(loc, value)


class ShaderManager:
    def __init__(self):
        self.shaders = {}

    def add_shader(self, name, fragment_source):
        """Add a shader preset"""
        shader = Shader(name, fragment_source)
        self.shaders[name] = shader

    def get_shader(self, name):
        """Get shader by name"""
        return self.shaders.get(name)
