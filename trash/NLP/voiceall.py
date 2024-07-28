import os
import numpy as np
import speech_recognition as sr
import librosa
from sklearn.mixture import GaussianMixture
from pydub import AudioSegment

# Directory where voice samples are stored
voice_samples_dir = "VoiceRec\samp"

# Function to convert MP3 to WAV if necessary and return the file path
def convert_to_wav(file_path):
    if file_path.endswith(".mp3"):
        sound = AudioSegment.from_mp3(file_path)
        file_path_wav = file_path.replace(".mp3", ".wav")
        sound.export(file_path_wav, format="wav")
        return file_path_wav
    return file_path

# Function to extract MFCC features from an audio file
def extract_features(file_path):
    file_path = convert_to_wav(file_path)
    y, sr = librosa.load(file_path, sr=None, duration=2.5)  # Load only the first 2.5 seconds
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

# Load voice samples and create a GMM model for each individual
def train_models(voice_samples_dir):
    models = {}
    for filename in os.listdir(voice_samples_dir):
        if filename.endswith(".wav") or filename.endswith(".mp3"):
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
    raise ValueError("No models were trained. Ensure there are valid .wav or .mp3 files in the voice_samples directory.")

# Function to recognize voice input from the microphone
def recognize_voice_from_mic():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        print("Say something!")
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)  # Set a timeout and phrase time limit of 3 seconds
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return

        # Check if the audio contains speech
        try:
            if recognizer.recognize_google(audio, show_all=True) == {}:
                print("No speech detected. Please try again.")
                return
        except sr.UnknownValueError:
            print("No speech detected or unrecognized speech. Please try again.")
            return

        audio_data = audio.get_wav_data()

        # Save the audio input for feature extraction
        with open("current_audio.wav", "wb") as f:
            f.write(audio_data)

        # Extract features from the current audio
        features = extract_features("current_audio.wav")

        # Recognize the speaker
        try:
            name = recognize_speaker(models, features)
            print(f"Hello, {name}!")
        except ValueError as e:
            print(e)

# Call the function to recognize voice input
recognize_voice_from_mic()
