import tkinter as tk
from tkinter import simpledialog
from telnetlib import Telnet
import time
import json

class EEGDataCaptureGUI:
    def __init__(self, master):
        self.master = master
        master.title("EEG Data Capture")
        master.geometry("400x300")  # Window size

        self.is_capturing = False
        self.filename = "eeg_data.csv"
        self.tn = None
        self.start_time = None
        self.file = None
        self.elapsed_time = 0

        self.label = tk.Label(master, text="Enter the filename for the EEG data:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.start_button = tk.Button(master, text="Start Capture", command=self.start_capture)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Capture", command=self.stop_capture)
        self.stop_button.pack()

        self.status_label = tk.Label(master, text="Ready to capture")
        self.status_label.pack()

        self.timer_label = tk.Label(master, text="00:00:00")
        self.timer_label.pack()

    def update_timer(self):
        if self.is_capturing:
            self.elapsed_time = time.perf_counter() - self.start_time
            elapsed_str = time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time))
            self.timer_label.config(text=elapsed_str)
            self.master.after(1000, self.update_timer)

    def start_capture(self):
        self.filename = self.entry.get() or "eeg_data.csv"
        self.file = open(self.filename, 'w')
        self.file.write(','.join([
            'time', 'attention', 'meditation', 'delta', 'theta', 'lowAlpha', 'highAlpha',
            'lowBeta', 'highBeta', 'lowGamma', 'highGamma', 'blinkStrength', 'poorSignalLevel'
        ]) + '\n')
        
        self.tn = Telnet('localhost', 13854)
        self.tn.write('{"enableRawOutput": false, "format": "Json"}'.encode('utf-8'))
        self.start_time = time.perf_counter()
        self.is_capturing = True
        self.status_label.config(text="Capturing...")
        self.elapsed_time = 0
        self.update_timer()
        self.capture_data()

    def stop_capture(self):
        self.is_capturing = False
        if self.tn:
            self.tn.close()
        if self.file:
            self.file.close()
        self.status_label.config(text="Capture stopped. Data saved to " + self.filename)
        self.timer_label.config(text="00:00:00")

    def capture_data(self):
        if self.is_capturing:
            try:
                line = self.tn.read_until(b'\r')
                print(line)
                decoded_line = line.decode('utf-8').strip()
                json_data = json.loads(decoded_line)
                if "eSense" in json_data and "eegPower" in json_data:
                    self.process_data(json_data)
                    self.status_label.config(text="Capture in progress...")
                else:
                    self.status_label.config(text="Connecting to the headset...")
            except json.JSONDecodeError:
                print("Failed to decode:", decoded_line)
            self.master.after(1000, self.capture_data)

    def process_data(self, json_data):
        esense = json_data['eSense']
        eeg_power = json_data['eegPower']
        poor_signal_level = json_data['poorSignalLevel']
        current_time = time.perf_counter() - self.start_time
        row_data = [
            str(current_time), str(esense['attention']), str(esense['meditation']),
            str(eeg_power['delta']), str(eeg_power['theta']), str(eeg_power['lowAlpha']),
            str(eeg_power['highAlpha']), str(eeg_power['lowBeta']), str(eeg_power['highBeta']),
            str(eeg_power['lowGamma']), str(eeg_power['highGamma']), '0',
            str(poor_signal_level)
        ]
        self.file.write(','.join(row_data) + '\n')

root = tk.Tk()
my_gui = EEGDataCaptureGUI(root)
root.mainloop()
