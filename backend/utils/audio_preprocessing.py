import os
import tempfile
import numpy as np
import librosa
from pydub import AudioSegment
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

MAX_SEQ_LENGTH = 300
NUM_MFCCS = 40

def preprocess_audio_for_inference(audio_file_path, scaler):
    try:
        audio = AudioSegment.from_file(audio_file_path)
        wav_path = tempfile.mktemp(suffix=".wav")
        audio.export(wav_path, format="wav")
        
        audio_data, sr = librosa.load(wav_path, sr=16000, mono=True)
        
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=NUM_MFCCS)
        
        mfccs_padded = pad_sequences([mfccs.T], maxlen=MAX_SEQ_LENGTH, dtype='float32', padding='post', truncating='post')
        
        mfccs_scaled = scaler.transform(mfccs_padded.reshape(-1, mfccs_padded.shape[-1])).reshape(mfccs_padded.shape)
        
        os.remove(wav_path)
        
        return mfccs_scaled
    except Exception as e:
        print(f"Error during audio preprocessing: {e}")
        return None
