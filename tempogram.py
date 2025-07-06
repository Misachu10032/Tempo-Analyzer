import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def show_tempogram(audio_path):
    # Load audio
    y, sr = librosa.load(audio_path, sr=None)
    
    # Compute onset envelope
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
    
    # Compute the tempogram
    tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr, hop_length=512)
    
    # Get times for x-axis
    times = librosa.frames_to_time(np.arange(tempogram.shape[1]), sr=sr, hop_length=512)

    # Plot the tempogram
    plt.figure(figsize=(12, 6))
    librosa.display.specshow(tempogram, sr=sr, hop_length=512, x_axis='time', y_axis='tempo', cmap='magma')
    plt.colorbar(label='Tempo strength')
    plt.title('Tempogram (Tempo over Time)')
    plt.tight_layout()
    plt.show()
    
    # Optional: Print global tempo estimate
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    print(f"Global estimated tempo: {tempo:.2f} BPM")

# Example usage
audio_path = r"C:\Users\john2\Downloads\bbb.mp4"  # Replace with your file
show_tempogram(audio_path)
