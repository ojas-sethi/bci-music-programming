import tkinter as tk
from tkinter import simpledialog
from telnetlib import Telnet
import time
import json
import joblib
from sklearn.preprocessing import StandardScaler

class EEGEmotionRecognitionGUI:
    def __init__(self, master):
        self.master = master
        master.title("Real-Time EEG Emotion Recognition")
        master.geometry("400x300")  # Window size

        # Load model and scaler
        self.model = joblib.load('knn_epoched_model.pkl')
        self.scaler = joblib.load('scaler.pkl')  # Assuming model was trained with data scaled this way

        self.is_recognizing = False
        self.tn = None

        self.start_button = tk.Button(master, text="Start Recognition", command=self.start_recognition)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Recognition", command=self.stop_recognition)
        self.stop_button.pack()

        self.emotion_label = tk.Label(master, text="Emotion: None", font=("Helvetica", 16))
        self.emotion_label.pack(pady=20)

        self.status_label = tk.Label(master, text="Ready")
        self.status_label.pack(pady=10)

    def start_recognition(self):
        self.tn = Telnet('localhost', 13854)
        self.tn.write('{"enableRawOutput": false, "format": "Json"}'.encode('utf-8'))
        self.is_recognizing = True
        self.status_label.config(text="Recognizing...")
        self.recognize_data()

    def stop_recognition(self):
        self.is_recognizing = False
        if self.tn:
            self.tn.close()
        self.status_label.config(text="Recognition stopped.")
        self.emotion_label.config(text="Emotion: None")

    def recognize_data(self):
        if self.is_recognizing:
            try:
                line = self.tn.read_until(b'\r')
                decoded_line = line.decode('utf-8').strip()
                json_data = json.loads(decoded_line)
                if "eegPower" in json_data:
                    features = self.extract_features(json_data)
                    self.predict_emotion(features)
            except json.JSONDecodeError:
                print("Failed to decode:", decoded_line)
            self.master.after(1000, self.recognize_data)  # Call this method again after 1000 ms

    def extract_features(self, json_data):
        # Assuming 'eegPower' data directly correlates with the feature names used during training
        features = [
            json_data['eegPower']['delta'], json_data['eegPower']['theta'], 
            json_data['eegPower']['lowAlpha'], json_data['eegPower']['highAlpha'],
            json_data['eegPower']['lowBeta'], json_data['eegPower']['highBeta'],
            json_data['eegPower']['lowGamma'], json_data['eegPower']['highGamma']
        ]
        features_array = [features]
        # Scale features as the model expects
        scaled_features = self.scaler.transform(features_array)
        return scaled_features

    def predict_emotion(self, features):
        prediction = self.model.predict(features)[0]
        # Map predictions to emotions
        emotion = {1: "Positive", 0: "Neutral", -1: "Negative"}.get(prediction, "Unknown")
        self.emotion_label.config(text=f"Emotion: {emotion}")

root = tk.Tk()
my_gui = EEGEmotionRecognitionGUI(root)
root.mainloop()
