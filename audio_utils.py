import sys
import os
import shutil
import numpy as np
import librosa
from pydub import AudioSegment

# Optional: If you're using PyInstaller and need to bundle ffmpeg
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and PyInstaller """
#     base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
#     return os.path.join(base_path, relative_path)

# AudioSegment.converter = resource_path("ffmpeg.exe")
# print(f"Resolved ffmpeg path: {AudioSegment.converter}")

def convert_to_mp3(input_path):
    if input_path.lower().endswith(".mp3"):
        return input_path

    output_path = os.path.splitext(input_path)[0] + ".mp3"
    try:
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="mp3")
        return output_path
    except Exception as e:
        print(f"Conversion failed for {input_path}: {e}")
        return None

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


def batch_analyze_bpm(folder_path, progress_callback=None):
    """Analyze BPM for only WAV files in a given folder."""
    results = []
    audio_extensions = ('.wav',)  # Only WAV files for analysis

    files = [f for f in os.listdir(folder_path)
             if os.path.isfile(os.path.join(folder_path, f)) and
             os.path.splitext(f)[1].lower() in audio_extensions]

    total = len(files)

    for i, file in enumerate(files):
        file_path = os.path.join(folder_path, file)

        bpm = get_bpm(file_path)
        results.append((os.path.basename(file), bpm))

        if progress_callback:
            progress_callback(i + 1, total)

    return results

def batch_convert_to_mp3(source_folder, progress_callback=None):
    output_folder = os.path.join(source_folder, "converted_to_mp3")
    os.makedirs(output_folder, exist_ok=True)

    supported_extensions = (".mp3", ".wav", ".mp4", ".flac", ".m4a", ".aac", ".ogg")
    files = [
        f for f in os.listdir(source_folder)
        if os.path.isfile(os.path.join(source_folder, f)) and
           os.path.splitext(f)[1].lower() in supported_extensions
    ]

    total = len(files)

    for i, file in enumerate(files):
        file_path = os.path.join(source_folder, file)

        try:
            ext = os.path.splitext(file)[1].lower()
            if ext == ".mp3":
                shutil.copy(file_path, os.path.join(output_folder, file))
            else:
                audio = AudioSegment.from_file(file_path)
                output_file = os.path.splitext(file)[0] + ".mp3"
                output_path = os.path.join(output_folder, output_file)
                audio.export(output_path, format="mp3")
        except Exception as e:
            print(f"Failed to process {file}: {e}")

        if progress_callback:
            progress_callback(i + 1, total)

def batch_convert_to_wav(source_folder, progress_callback=None):
    output_folder = os.path.join(source_folder, "converted_to_wav")
    os.makedirs(output_folder, exist_ok=True)

    supported_extensions = (".mp3", ".wav", ".mp4", ".flac", ".m4a", ".aac", ".ogg")
    files = [
        f for f in os.listdir(source_folder)
        if os.path.isfile(os.path.join(source_folder, f)) and
           os.path.splitext(f)[1].lower() in supported_extensions
    ]

    total = len(files)

    for i, file in enumerate(files):
        file_path = os.path.join(source_folder, file)
        output_file = os.path.splitext(file)[0] + ".wav"
        output_path = os.path.join(output_folder, output_file)

        try:
            audio = AudioSegment.from_file(file_path)

            # Normalize format for librosa: mono, 44.1kHz
            audio = audio.set_channels(1).set_frame_rate(44100)

            audio.export(output_path, format="wav")
        except Exception as e:
            print(f"Failed to convert {file} to WAV: {e}")

        if progress_callback:
            progress_callback(i + 1, total)
