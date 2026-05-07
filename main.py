#!/usr/bin/env python3
"""
Audio Visualizer - Milkdrop-style audio visualization for desktop
"""

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import sounddevice as sd
from scipy import signal
import threading
import time

from src.audio_engine import AudioEngine
from src.visualizer import Visualizer

class AudioVisualizerApp:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.running = True
        
        # Initialize Pygame and OpenGL
        pygame.init()
        pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption("Audio Visualizer")
        
        # Audio engine
        self.audio_engine = AudioEngine()
        
        # Visualizer
        self.visualizer = Visualizer(width, height)
        
        # FPS clock
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Start audio capture in background thread
        self.audio_thread = threading.Thread(target=self.audio_engine.start_capture, daemon=True)
        self.audio_thread.start()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.visualizer.next_preset()
                elif event.key == pygame.K_LEFT:
                    self.visualizer.prev_preset()

    def update(self):
        # Get audio analysis data
        audio_data = self.audio_engine.get_analysis()
        
        # Update visualizer with audio data
        self.visualizer.update(audio_data)

    def render(self):
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Render visualization
        self.visualizer.render()
        
        # Swap buffers
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)
        
        self.cleanup()

    def cleanup(self):
        self.audio_engine.stop_capture()
        pygame.quit()

if __name__ == '__main__':
    app = AudioVisualizerApp()
    app.run()
