import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

def calculate_bpm_segment(y, sr, start_sample, end_sample):
    segment = y[start_sample:end_sample]
    tempo, _ = librosa.beat.beat_track(y=segment, sr=sr)
    return tempo

def detect_sections_and_bpm(audio_path):
    # Load audio file
    y, sr = librosa.load(audio_path, sr=None)

    # Compute onset envelope
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)

    # Detect onset times
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units='frames', backtrack=False)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    # Estimate tempo in sliding windows
    bpm_list = []
    segment_times = []
    window_size = 5  # seconds
    for i in range(len(onset_times) - window_size):
        segment_start = int(onset_times[i] * sr)
        segment_end = int(onset_times[i + window_size] * sr)
        segment_y = y[segment_start:segment_end]
        tempo, _ = librosa.beat.beat_track(y=segment_y, sr=sr)
        bpm_list.append(tempo)
        segment_times.append(onset_times[i + window_size])  # use end time as reference

    # Prepare BPM data for clustering
    bpm_array = np.array(bpm_list).reshape(-1, 1)
    print("BPM array:\n", bpm_array)

    # Run KMeans to detect 2 clusters (verse and chorus)
    kmeans = KMeans(n_clusters=2, n_init=10, random_state=42)
    kmeans.fit(bpm_array)
    labels = kmeans.labels_

    # Determine which cluster is chorus (faster BPM)
    cluster_0_mean = bpm_array[labels == 0].mean()
    cluster_1_mean = bpm_array[labels == 1].mean()
    chorus_label = 0 if cluster_0_mean > cluster_1_mean else 1
    verse_label = 1 - chorus_label

    verse_bpm = cluster_0_mean if verse_label == 0 else cluster_1_mean
    chorus_bpm = cluster_1_mean if chorus_label == 1 else cluster_0_mean

    print(f"Verse BPM: {verse_bpm:.2f}")
    print(f"Chorus BPM: {chorus_bpm:.2f}")

    # ==========================
    # 🎨 Visualization #1: BPM vs Time (scatter + KMeans)
    # ==========================
    plt.figure(figsize=(10, 5))
    bpm_flat = bpm_array.flatten()

    for i, time in enumerate(segment_times):
        color = 'red' if labels[i] == chorus_label else 'blue'
        plt.scatter(time, bpm_flat[i], color=color)

    # Plot cluster centers
    for center in kmeans.cluster_centers_:
        plt.axhline(y=center[0], color='green', linestyle='--', label=f"Cluster center: {center[0]:.2f} BPM")

    plt.title("BPM Segments and KMeans Clusters (Red = Chorus, Blue = Verse)")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Estimated BPM")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ==========================
    # 🎨 Visualization #2: Waveform with Segment Lines
    # ==========================
    plt.figure(figsize=(12, 6))
    librosa.display.waveshow(y, sr=sr, alpha=0.5)

    for i, time in enumerate(segment_times):
        color = 'r' if labels[i] == chorus_label else 'b'
        plt.axvline(x=time, color=color, linestyle='--')

    plt.title(f"Detected Sections (Verse vs. Chorus) with BPM\nVerse BPM: {verse_bpm:.2f}, Chorus BPM: {chorus_bpm:.2f}")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.show()

# 🔊 Example usage
audio_path = r"C:\Users\john2\Downloads\bbb.mp4"  # Replace with your actual file path
detect_sections_and_bpm(audio_path)
