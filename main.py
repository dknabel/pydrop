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
import logging

from src.audio_engine import AudioEngine
from src.visualizer import Visualizer
from src.ui.menu_system import MenuSystem
from src.ui.presets_data import PresetManager
from src.ui.models import FavoritesManager
from src.playlist_manager import PlaylistManager

logger = logging.getLogger(__name__)

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

        # Preset and Favorites managers
        self.preset_manager = PresetManager()
        self.favorites_manager = FavoritesManager()

        # Menu system
        self.menu = MenuSystem(
            x=10, y=10, width=width-20, height=height-20,
            preset_manager=self.preset_manager,
            favorites_manager=self.favorites_manager,
            on_preset_selected=self._on_preset_selected,
            on_custom_preset_saved=self._on_custom_preset_saved
        )

        # Playlist manager
        self.playlist_manager = PlaylistManager()
        self.playlist_index = 0

        # FPS clock
        self.clock = pygame.time.Clock()
        self.fps = 60

        # Start audio capture in background thread
        self.audio_thread = threading.Thread(target=self.audio_engine.start_capture, daemon=True)
        self.audio_thread.start()

    def handle_events(self):
        """Handle all input events."""
        for event in pygame.event.get():
            try:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.menu.visible:
                            self.menu.toggle()
                        else:
                            self.running = False
                    elif event.key == pygame.K_m:
                        self.menu.toggle()
                    elif not self.menu.visible:
                        # Only handle preset navigation if menu is closed
                        if event.key == pygame.K_SPACE:
                            # If playlist is active, cycle through playlist presets
                            if self.playlist_manager.current_playlist:
                                self._next_playlist_preset()
                            else:
                                self.visualizer.next_preset()
                        elif event.key == pygame.K_LEFT:
                            self.visualizer.prev_preset()
                        elif event.key == pygame.K_RIGHT:
                            self.visualizer.next_preset()
                        elif event.key == pygame.K_PAGEUP:
                            self.visualizer.prev_preset()
                        elif event.key == pygame.K_PAGEDOWN:
                            self.visualizer.next_preset()

                # Handle menu events
                self.menu.handle_event(event)

            except Exception as e:
                logger.error(f"Error handling event: {e}")

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

        # Render menu overlay if visible
        if self.menu.visible:
            self._render_menu_overlay()

        # Swap buffers
        pygame.display.flip()

    def _on_preset_selected(self, preset_id: int) -> None:
        """Handle preset selection from menu.

        Args:
            preset_id: ID of the selected preset
        """
        try:
            # Find preset by ID
            for i, preset in enumerate(self.preset_manager.builtin_presets):
                if preset.id == preset_id:
                    self.visualizer.current_preset_idx = i
                    logger.info(f"Preset selected: {preset.name}")
                    break
        except Exception as e:
            logger.error(f"Error selecting preset: {e}")

    def _on_custom_preset_saved(self, custom_preset) -> None:
        """Handle custom preset creation.

        Args:
            custom_preset: The newly created CustomPreset object
        """
        try:
            logger.info(f"Custom preset saved: {custom_preset.name}")
            # Could update visualizer to use the custom preset
        except Exception as e:
            logger.error(f"Error saving custom preset: {e}")

    def _render_menu_overlay(self):
        """Render 2D menu overlay on top of OpenGL content"""
        import ctypes

        # Create a pygame surface for the menu
        menu_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.menu.render(menu_surface)

        # Convert pygame surface to OpenGL texture
        texture_data = pygame.image.tostring(menu_surface, "RGBA", True)

        # Create a texture from the menu surface
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        # Save current GL state
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        # Switch to orthographic projection for 2D
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Setup for 2D rendering
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Use fixed pipeline
        glUseProgram(0)

        # Enable texturing
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)

        # Render fullscreen quad with the texture
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex2f(0, 0)
        glTexCoord2f(1, 1)
        glVertex2f(self.width, 0)
        glTexCoord2f(1, 0)
        glVertex2f(self.width, self.height)
        glTexCoord2f(0, 0)
        glVertex2f(0, self.height)
        glEnd()

        # Clean up
        glDisable(GL_TEXTURE_2D)
        glDeleteTextures([texture])

        # Restore GL state
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)
        
        self.cleanup()

    def _next_playlist_preset(self):
        """Cycle to the next preset in the active playlist."""
        current_presets = self.playlist_manager.get_current_presets()
        if current_presets:
            self.playlist_index = (self.playlist_index + 1) % len(current_presets)
            preset_name = current_presets[self.playlist_index]

            # Find preset index in main list
            for i, preset in enumerate(self.visualizer.presets):
                if preset['name'] == preset_name:
                    self.visualizer.current_preset_idx = i
                    print(f"Playlist: {preset_name}")
                    break

    def cleanup(self):
        self.audio_engine.stop_capture()
        # Wait for audio thread to finish gracefully
        self.audio_thread.join(timeout=1.0)
        pygame.quit()

if __name__ == '__main__':
    app = AudioVisualizerApp()
    app.run()
