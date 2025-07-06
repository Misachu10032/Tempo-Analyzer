import os
from pydub import AudioSegment
import numpy as np
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


def process_folder(folder_path):
    results = []

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if not os.path.isfile(file_path):
            continue

        mp3_path = convert_to_mp3(file_path)
        if not mp3_path:
            continue

        bpm = get_bpm(mp3_path)
        results.append((os.path.basename(file), bpm))

    return results
