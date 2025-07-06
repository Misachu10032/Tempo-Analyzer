import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
import madmom
import numpy as np
import openpyxl
from madmom.features.beats import RNNBeatProcessor, DBNBeatTrackingProcessor


def convert_to_mp3(input_path):
    if input_path.lower().endswith(".mp3"):
        return input_path  # already mp3

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
        proc = madmom.audio.signal.FramedSignal(file_path, num_channels=1)
        beat_proc = RNNBeatProcessor()(file_path)
        act = DBNBeatTrackingProcessor(fps=100)(beat_proc)
        if len(act) < 2:
            return 0.0
        intervals = np.diff(act)
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


def export_to_excel(data, output_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["File Name", "BPM"])
    for row in data:
        ws.append(row)
    wb.save(output_path)


class BPMAnalyzerApp:
    def __init__(self, master):
        self.master = master
        master.title("BPM Analyzer")

        self.label = tk.Label(master, text="Select a folder containing audio files:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(master, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=5)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return

        messagebox.showinfo("Processing", "Analyzing audio files. This may take a while...")

        data = process_folder(folder_path)
        output_excel = os.path.join(folder_path, "bpm_output.xlsx")
        export_to_excel(data, output_excel)

        messagebox.showinfo("Done", f"Analysis complete!\nExcel saved at:\n{output_excel}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BPMAnalyzerApp(root)
    root.mainloop()
