import os
import io
import librosa
from flask import Flask, request, jsonify, render_template
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
from pydub import AudioSegment
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')
STATIC_DIR = os.path.join(FRONTEND_DIR, 'static')
TEMPLATE_DIR = FRONTEND_DIR

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)

processor = None
model = None

try:
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    print("Pre-trained Wav2Vec2 model and processor loaded successfully.")
except Exception as e:
    print(f"Error loading pre-trained model: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/record')
def record():
    """Renders the dedicated audio recording page."""
    return render_template('record_audio.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if not model or not processor:
        return jsonify({'error': 'Model not loaded. Please check server logs.'}), 500

    audio_data_raw = request.data
    
    temp_webm_file = None
    temp_wav_file = None
    try:
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_webm_file_handler:
            temp_webm_file_handler.write(audio_data_raw)
            temp_webm_file = temp_webm_file_handler.name

        audio_segment = AudioSegment.from_file(temp_webm_file, format="webm")
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav_file_handler:
            audio_segment.export(temp_wav_file_handler.name, format="wav")
            temp_wav_file = temp_wav_file_handler.name

        audio_data, sr = librosa.load(temp_wav_file, sr=16000, mono=True)
            
        input_values = processor(audio_data, sampling_rate=16000, return_tensors="pt").input_values
        
        with torch.no_grad():
            logits = model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)
        
        transcription = processor.batch_decode(predicted_ids)[0].lower()
        
        return jsonify({'transcription': transcription})
    
    except Exception as e:
        print(f"Error during transcription: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500
    finally:
        if temp_webm_file and os.path.exists(temp_webm_file):
            os.remove(temp_webm_file)
        if temp_wav_file and os.path.exists(temp_wav_file):
            os.remove(temp_wav_file)
