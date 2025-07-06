import os
from pydub import AudioSegment
import numpy as np
import shutil
from madmom.features.beats import RNNBeatProcessor, DBNBeatTrackingProcessor


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
    try:
        beat_proc = RNNBeatProcessor()(file_path)
        beats = DBNBeatTrackingProcessor(fps=100)(beat_proc)
        if len(beats) < 2:
            return 0.0
        intervals = np.diff(beats)
        bpm = 60.0 / np.median(intervals)
        return round(bpm, 2)
    except Exception as e:
        print(f"Failed BPM for {file_path}: {e}")
        return 0.0

def batch_analyze_bpm(folder_path, progress_callback=None):
    results = []
    audio_extensions = ('.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg')

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
        f
        for f in os.listdir(source_folder)
        if os.path.isfile(os.path.join(source_folder, f))
        and os.path.splitext(f)[1].lower() in supported_extensions
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

        # Update progress
        if progress_callback:
            progress_callback(i + 1, total)
