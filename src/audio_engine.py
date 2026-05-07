"""Audio input and analysis engine"""

import sounddevice as sd
import numpy as np
from scipy import signal
from collections import deque
import threading
import time

class AudioEngine:
    def __init__(self, sample_rate=44100, block_size=2048):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.running = False
        
        # Audio buffers
        self.audio_buffer = deque(maxlen=sample_rate)  # 1 second buffer
        self.lock = threading.Lock()
        
        # Analysis data
        self.frequency_data = np.zeros(512)
        self.waveform_data = np.zeros(block_size)
        self.amplitude = 0.0
        self.bass = 0.0
        self.mid = 0.0
        self.treble = 0.0

    def audio_callback(self, indata, frames, time_info, status):
        """Callback for audio stream"""
        if status:
            print(f"Audio status: {status}")
        
        # Add to buffer
        with self.lock:
            self.audio_buffer.extend(indata[:, 0])
            self._analyze_audio()

    def _analyze_audio(self):
        """Analyze audio data for visualization"""
        if len(self.audio_buffer) < self.block_size:
            return
        
        # Get latest audio block
        audio_data = np.array(list(self.audio_buffer)[-self.block_size:])
        self.waveform_data = audio_data
        
        # Calculate amplitude (RMS)
        self.amplitude = float(np.sqrt(np.mean(audio_data ** 2)))
        
        # FFT for frequency analysis
        fft = np.fft.fft(audio_data * signal.hann(len(audio_data)))
        magnitude = np.abs(fft[:len(fft)//2])
        
        # Downsample to 512 bins
        if len(magnitude) > 512:
            self.frequency_data = np.array([
                np.max(magnitude[int(i*len(magnitude)/512):int((i+1)*len(magnitude)/512)])
                for i in range(512)
            ])
        else:
            self.frequency_data = magnitude
        
        # Normalize
        if np.max(self.frequency_data) > 0:
            self.frequency_data = self.frequency_data / np.max(self.frequency_data)
        
        # Extract frequency bands
        self.bass = np.mean(self.frequency_data[:50])
        self.mid = np.mean(self.frequency_data[50:200])
        self.treble = np.mean(self.frequency_data[200:])

    def start_capture(self):
        """Start audio capture from microphone"""
        self.running = True
        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                blocksize=self.block_size,
                channels=1,
                callback=self.audio_callback,
                latency='low'
            ):
                while self.running:
                    time.sleep(0.01)
        except Exception as e:
            print(f"Audio capture error: {e}")
        finally:
            self.running = False

    def stop_capture(self):
        """Stop audio capture"""
        self.running = False

    def get_analysis(self):
        """Get current audio analysis data"""
        with self.lock:
            return {
                'amplitude': self.amplitude,
                'frequency': self.frequency_data.copy(),
                'waveform': self.waveform_data.copy(),
                'bass': self.bass,
                'mid': self.mid,
                'treble': self.treble,
            }
