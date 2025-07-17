import librosa
import numpy as np

def get_bpm(file_path):
    """Analyze the BPM for a single audio file using librosa."""
    try:
        y, sr = librosa.load(file_path, sr=44100, mono=True)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        # Safely convert tempo to float
        if isinstance(tempo, (np.ndarray, list)):
            tempo = tempo[0]

        return round(float(tempo), 2)
    except Exception as e:
        print(f"Failed to analyze BPM for {file_path}: {e}")
        return 0.0

if __name__ == "__main__":
    path = r"C:\Users\john2\Downloads\test3\converted_to_mp3\converted_to_wav\ddd.wav"
    bpm = get_bpm(path)
    print(f"BPM of {path}: {bpm}")
