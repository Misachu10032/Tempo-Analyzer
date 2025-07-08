from madmom.features.beats import RNNBeatProcessor, DBNBeatTrackingProcessor
import numpy as np
import librosa
import matplotlib.pyplot as plt

def detect_tempo_madmom(audio_path):
    # Load audio to get SR and duration
    y, sr = librosa.load(audio_path, sr=None)

    # Step 1: Generate beat activations using RNN
    act = RNNBeatProcessor()(audio_path)

    # Step 2: Use DBN (Dynamic Bayesian Network) to track beat positions
    proc = DBNBeatTrackingProcessor(fps=100, min_bpm=40, max_bpm=200)
    beats = proc(act)

    # Convert beat intervals to obtain tempo
    intervals = np.diff(beats)
    avg_interval = np.mean(intervals)
    tempo = 60.0 / avg_interval

    print(f"Detected Tempo: {tempo:.2f} BPM")



# Example usage:
detect_tempo_madmom(r"C:\Users\john2\Downloads\test3\aaa.mp3")