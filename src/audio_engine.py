"""Audio input and analysis engine"""

import sounddevice as sd
import numpy as np
from scipy.signal import windows
from collections import deque
import threading
import time

class AudioEngine:
    def __init__(self, sample_rate=44100, block_size=2048, device=None):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.running = False

        # Find loopback device if not specified
        if device is None:
            device = self._find_loopback_device()

        self.device = device
        self.actual_sample_rate = self._get_device_sample_rate(device)

        # Audio buffers
        self.audio_buffer = deque(maxlen=self.actual_sample_rate)  # 1 second buffer
        self.lock = threading.Lock()

        # Analysis data
        self.frequency_data = np.zeros(512)
        self.waveform_data = np.zeros(block_size)
        self.amplitude = 0.0
        self.bass = 0.0
        self.mid = 0.0
        self.treble = 0.0

    @staticmethod
    def _find_loopback_device():
        """Find the best loopback/system audio device available"""
        devices = sd.query_devices()

        # Priority order for loopback devices
        priority_names = ['Chromium', 'loopback', 'stereo mix', 'monitor', 'cava', 'pulse']

        for priority_name in priority_names:
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0 and priority_name.lower() in device['name'].lower():
                    return i

        # Fallback: use first input device with stereo capability
        for i, device in enumerate(devices):
            if device['max_input_channels'] >= 2:
                return i

        # Last resort: default device
        return None

    @staticmethod
    def _get_device_sample_rate(device):
        """Get the actual sample rate for a device"""
        dev_info = sd.query_devices(device)
        return int(dev_info['default_samplerate'])

    def audio_callback(self, indata, frames, time_info, status):
        """Callback for audio stream"""
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

        # Calculate amplitude (RMS) - boost sensitivity
        raw_amplitude = float(np.sqrt(np.mean(audio_data ** 2)))
        self.amplitude = min(raw_amplitude * 5.0, 1.0)  # Boost and clamp
        
        # FFT for frequency analysis
        fft = np.fft.fft(audio_data * windows.hann(len(audio_data)))
        magnitude = np.abs(fft[:len(fft)//2])
        
        # Downsample to 512 bins
        if len(magnitude) > 512:
            self.frequency_data = np.array([
                np.max(magnitude[int(i*len(magnitude)/512):int((i+1)*len(magnitude)/512)])
                for i in range(512)
            ])
        else:
            self.frequency_data = magnitude
        
        # Normalize and boost
        if np.max(self.frequency_data) > 0:
            self.frequency_data = self.frequency_data / np.max(self.frequency_data)
        # Boost sensitivity
        self.frequency_data = np.power(self.frequency_data, 0.5) * 2.0
        
        # Extract frequency bands
        self.bass = np.mean(self.frequency_data[:50])
        self.mid = np.mean(self.frequency_data[50:200])
        self.treble = np.mean(self.frequency_data[200:])

    def start_capture(self):
        """Start audio capture from system audio loopback"""
        self.running = True
        self.stream = None
        try:
            self.stream = sd.InputStream(
                device=self.device,
                samplerate=self.actual_sample_rate,
                blocksize=self.block_size,
                channels=1,
                callback=self.audio_callback,
                latency='low'
            )
            self.stream.start()
            while self.running:
                time.sleep(0.01)
        except Exception as e:
            pass
        finally:
            self.running = False
            if self.stream is not None:
                try:
                    self.stream.stop()
                    self.stream.close()
                except:
                    pass

    def stop_capture(self):
        """Stop audio capture"""
        self.running = False
        # Give stream time to close gracefully
        time.sleep(0.1)

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
