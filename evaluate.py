import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import librosa
from jiwer import wer
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

matplotlib.use('Agg')

TEST_DATA_DIR = 'test_data'
TRANSCRIPTIONS_FILE = os.path.join(TEST_DATA_DIR, 'transcriptions.txt')

try:
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    print("Model and processor loaded.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

def calculate_pitch(audio_file):
    try:
        y, sr = librosa.load(audio_file)
        f0 = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
        return np.median(f0[f0 > 0])
    except Exception as e:
        print(f"Error calculating pitch for {audio_file}: {e}")
        return None

def evaluate_audio(audio_path, true_transcription):
    try:
        audio_data, sr = librosa.load(audio_path, sr=16000, mono=True)
        pitch = calculate_pitch(audio_path)
        
        input_values = processor(audio_data, sampling_rate=16000, return_tensors="pt").input_values
        
        with torch.no_grad():
            logits = model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)
        transcribed_text = processor.batch_decode(predicted_ids)[0].lower()
        
        error_rate = wer(true_transcription, transcribed_text)
        
        return pitch, error_rate, transcribed_text
    except Exception as e:
        print(f"Error processing {audio_path}: {e}")
        return None, None, None

def run_experiment():
    pitches = []
    wer_scores = []
    
    with open(TRANSCRIPTIONS_FILE, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        try:
            filename, transcription = line.strip().split(',', 1)
            audio_path = os.path.join(TEST_DATA_DIR, filename)
            
            if not os.path.exists(audio_path):
                print(f"Warning: Audio file not found: {audio_path}")
                continue
            
            print(f"Evaluating {filename}...")
            pitch, wer_score, transcribed_text = evaluate_audio(audio_path, transcription)
            
            if pitch is not None and wer_score is not None:
                pitches.append(pitch)
                wer_scores.append(wer_score)
                print(f"  Pitch: {pitch:.2f} Hz, WER: {wer_score:.2f}, Transcription: {transcribed_text}\n")
            
        except Exception as e:
            print(f"Error reading line: {line.strip()}. Error: {e}")
    
    if not pitches:
        print("No valid data points collected. Please check your audio files and transcription file.")
        return

    plt.figure(figsize=(10, 6))
    plt.scatter(pitches, wer_scores, color='blue', s=100, alpha=0.7)
    
    plt.title('ASR Performance vs. Pitch')
    plt.xlabel('Average Pitch (Hz)')
    plt.ylabel('Word Error Rate (WER)')
    plt.grid(True)
    
    output_image_path = "asr_performance_vs_pitch.png"
    plt.savefig(output_image_path)
    print(f"Graph saved to {output_image_path}")

if __name__ == '__main__':
    run_experiment()