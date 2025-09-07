import os
import tempfile
import librosa
from flask import Flask, request, jsonify, render_template
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')
STATIC_DIR = os.path.join(FRONTEND_DIR, 'static')
TEMPLATE_DIR = FRONTEND_DIR

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)

try:
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    print("Pre-trained Wav2Vec2 model and processor loaded successfully.")
except Exception as e:
    print(f"Error loading pre-trained model: {e}")
    processor = None
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_endpoint():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file found'}), 400
    
    audio_file = request.files['audio']
    temp_file_path = tempfile.mktemp()
    audio_file.save(temp_file_path)
    
    if model is None or processor is None:
        return jsonify({'error': 'Model not loaded. Please check server logs.'}), 500

    try:
        audio_data, sr = librosa.load(temp_file_path, sr=16000, mono=True)
        
        input_values = processor(audio_data, sampling_rate=16000, return_tensors="pt", padding=True).input_values
        
        with torch.no_grad():
            logits = model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)
        
        transcription = processor.batch_decode(predicted_ids)[0].lower()
            
        return jsonify({'transcription': transcription})
    
    except Exception as e:
        print(f"An unexpected error occurred during transcription: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500
        
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
