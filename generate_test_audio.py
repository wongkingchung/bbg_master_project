"""Generate simple synthetic WAV files for testing audio_manipulator.py."""

import math
import wave
import struct


def generate_sine_wave(filename: str, frequency: float, duration_ms: int, sample_rate: int = 44100, amplitude: float = 0.5):
    """Generate a sine wave WAV file using the standard library `wave` module."""
    num_samples = int(sample_rate * (duration_ms / 1000.0))
    max_val = 32767  # 16-bit signed int max

    with wave.open(filename, "wb") as wav_file:
        wav_file.setnchannels(1)  # mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)

        for i in range(num_samples):
            t = i / sample_rate
            sample = int(max_val * amplitude * math.sin(2 * math.pi * frequency * t))
            wav_file.writeframes(struct.pack("<h", sample))

    print(f"Generated {filename}: {duration_ms}ms @ {frequency}Hz, {num_samples} samples")


if __name__ == "__main__":
    # Familiar song: 10 seconds of 440 Hz (A4)
    generate_sine_wave("familiar.wav", frequency=440, duration_ms=10_000)
    # Unfamiliar song: 20 seconds of 880 Hz (A5)
    generate_sine_wave("unfamiliar.wav", frequency=880, duration_ms=20_000)
