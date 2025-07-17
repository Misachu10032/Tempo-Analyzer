import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import os
import threading
import logging

from audio_utils import batch_analyze_bpm, batch_convert_to_mp3, batch_convert_to_wav
from excel_exporter import export_to_excel

logging.basicConfig(level=logging.DEBUG)

class BPMAnalyzerApp:
    def __init__(self, master):
        self.master = master
        master.title("BPM Analyzer")

        self.label = tk.Label(master, text="Select a folder containing audio files:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(master, text="Select Folder and Analyze BPM", command=self.analyze_bpm)
        self.select_button.pack(pady=5)

        self.convert_button = tk.Button(master, text="Batch Convert to MP3", command=self.batch_convert)
        self.convert_button.pack(pady=5)

        self.wav_convert_button = tk.Button(master, text="Batch Convert to WAV", command=self.batch_convert_to_wav)
        self.wav_convert_button.pack(pady=5)

        self.status_label = tk.Label(master, text="", fg="blue")
        self.status_label.pack(pady=5)

        self.progress = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

    def reset_progress(self, message=""):
        self.progress["value"] = 0
        self.progress["maximum"] = 100
        self.status_label.config(text=message)
        self.master.update_idletasks()

    def update_progress(self, current, total):
        percent = int((current / total) * 100)
        self.progress["value"] = percent
        self.master.update_idletasks()

    def analyze_bpm(self):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            logging.debug("No folder selected for BPM analysis.")
            return

        logging.debug(f"Selected folder for BPM analysis: {folder_path}")
        self.reset_progress("Analyzing audio files...")

        def task():
            try:
                logging.debug("Starting BPM analysis...")
                data = batch_analyze_bpm(folder_path, self.update_progress)
                output_excel = os.path.join(folder_path, "bpm_output.xlsx")
                export_to_excel(data, output_excel)
                logging.debug(f"Exported BPM data to: {output_excel}")
                self.master.after(0, self.analysis_done)
            except Exception as e:
                logging.error(f"Error in BPM analysis: {e}")

        threading.Thread(target=task, daemon=True).start()

    def analysis_done(self):
        self.progress["value"] = 100
        self.status_label.config(text="Analysis complete!")
        self.master.after(5000, lambda: self.status_label.config(text=""))

    def batch_convert(self):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            logging.debug("No folder selected for conversion.")
            return

        logging.debug(f"Selected folder for batch conversion: {folder_path}")
        self.reset_progress("Converting files to MP3. Please wait...")

        def task():
            try:
                logging.debug("Starting batch conversion to MP3...")
                batch_convert_to_mp3(folder_path, self.update_progress)
                logging.debug("Batch conversion completed.")
                self.master.after(0, self.conversion_done)
            except Exception as e:
                logging.error(f"Error in batch conversion: {e}")

        threading.Thread(target=task, daemon=True).start()

    def batch_convert_to_wav(self):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            logging.debug("No folder selected for WAV conversion.")
            return

        logging.debug(f"Selected folder for batch WAV conversion: {folder_path}")
        self.reset_progress("Converting files to WAV. Please wait...")

        def task():
            try:
                logging.debug("Starting batch conversion to WAV...")
                batch_convert_to_wav(folder_path, self.update_progress)
                logging.debug("Batch WAV conversion completed.")
                self.master.after(0, self.conversion_done)
            except Exception as e:
                logging.error(f"Error in batch WAV conversion: {e}")

        threading.Thread(target=task, daemon=True).start()

    def conversion_done(self):
        self.progress["value"] = 100
        self.status_label.config(text="Conversion complete!")
        self.master.after(5000, lambda: self.status_label.config(text=""))

if __name__ == "__main__":
    root = tk.Tk()
    app = BPMAnalyzerApp(root)
    root.mainloop()
