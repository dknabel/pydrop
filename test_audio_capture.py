#!/usr/bin/env python3
"""Test system audio capture"""

import sys
sys.path.insert(0, 'src')

from audio_engine import AudioEngine
import time
import numpy as np

def test_system_audio():
    engine = AudioEngine(block_size=2048)

    print(f"Device: {engine.device}")
    print(f"Sample Rate: {engine.actual_sample_rate}")
    print(f"Block Size: {engine.block_size}")

    # Start capturing
    import threading
    capture_thread = threading.Thread(target=engine.start_capture, daemon=True)
    capture_thread.start()

    print("\nListening for 10 seconds...")
    print("Play some music or system audio to test capture.")
    print("-" * 60)

    for i in range(10):
        time.sleep(1)
        analysis = engine.get_analysis()
        amp = analysis['amplitude']
        bass = analysis['bass']
        mid = analysis['mid']
        treble = analysis['treble']

        status = "🔊" if amp > 0.1 else "  "
        print(f"{status} Sec {i+1}: amp={amp:.2f}, bass={bass:.2f}, mid={mid:.2f}, treble={treble:.2f}")

    engine.stop_capture()
    print("-" * 60)
    print("Test complete!")

if __name__ == '__main__':
    test_system_audio()
