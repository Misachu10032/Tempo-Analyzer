import librosa
import matplotlib.pyplot as plt
import numpy as np

def plot_fft(audio_path):
    # Load the audio file
    y, sr = librosa.load(audio_path, sr=None)

    # Perform Fast Fourier Transform (FFT)
    D = np.fft.fft(y)

    # Compute the corresponding frequencies for the FFT result
    freqs = np.fft.fftfreq(len(D), 1 / sr)

    # Take the positive half of the spectrum (real frequencies)
    D = np.abs(D[:len(D)//2])
    freqs = freqs[:len(freqs)//2]

    # Plot frequency vs. amplitude
    plt.figure(figsize=(12, 6))
    plt.plot(freqs, D)
    plt.title("Frequency vs. Amplitude (FFT)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()

    # Show the plot
    plt.show()

# Example usage:
audio_path = r"C:\Users\john2\Downloads\bbb.mp4"  # Replace with your song path
plot_fft(audio_path)
