import os
import numpy as np
import speech_recognition as sr
import librosa
from sklearn.mixture import GaussianMixture

# Directory where voice samples are stored
voice_samples_dir = "VoiceRec\samp"

# Function to extract MFCC features from an audio file
def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

# Load voice samples and create a GMM model for each individual
def train_models(voice_samples_dir):
    models = {}
    for filename in os.listdir(voice_samples_dir):
        if filename.endswith(".wav"):
            name = filename.split(".")[0]
            file_path = os.path.join(voice_samples_dir, filename)
            features = extract_features(file_path)
            models[name] = GaussianMixture(n_components=1, covariance_type='diag', n_init=3)
            models[name].fit(features.reshape(-1, 1))
    return models

# Recognize the speaker from the audio input
def recognize_speaker(models, audio_features):
    scores = {}
    for name, model in models.items():
        try:
            score = model.score(audio_features.reshape(-1, 1))
            scores[name] = score
        except Exception as e:
            print(f"Error scoring model for {name}: {e}")
    if not scores:
        raise ValueError("No scores available. Ensure models are correctly trained and audio features are valid.")
    return max(scores, key=scores.get)

# Initialize recognizer class
recognizer = sr.Recognizer()

# Train models with pre-recorded samples
models = train_models(voice_samples_dir)
if not models:
    raise ValueError("No models were trained. Ensure there are valid .wav files in the voice_samples directory.")

# Function to recognize voice input from the microphone
def recognize_voice_from_mic():
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source, timeout=3,phrase_time_limit=3)
        print("rec..")
        audio_data = audio.get_wav_data()

        # Save the audio input for feature extraction
        with open("current_audio.wav", "wb") as f:
            f.write(audio_data)

        # Extract features from the current audio
        features = extract_features("current_audio.wav")

        # Recognize the speaker
        name = recognize_speaker(models, features)
        print(f"Hello, {name}!")

# Call the function to recognize voice input
recognize_voice_from_mic()
