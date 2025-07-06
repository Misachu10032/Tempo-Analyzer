import librosa

def analyze_bpm(audio_path):
    try:
        y, sr = librosa.load(audio_path,sr=None)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        # Just make sure it's a float
        return float(tempo)

    except Exception as e:
        print(f"Error analyzing BPM for {audio_path}: {e}")
        return None
