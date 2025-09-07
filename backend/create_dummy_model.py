import os
import numpy as np
import pickle
import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Dropout, Bidirectional, TimeDistributed
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Input

MAX_SEQ_LENGTH = 300
NUM_MFCCS = 40

def create_and_save_dummy_model():
    MODEL_DIR = os.path.join('..', 'backend', 'model')
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    # 1. Create and save a dummy scaler
    scaler = StandardScaler()
    dummy_data = np.random.rand(100, NUM_MFCCS)
    scaler.fit(dummy_data)
    with open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'wb') as f:
        pickle.dump(scaler, f)
    print("Dummy scaler saved.")

    # 2. Create and save a dummy tokenizer
    tokenizer = Tokenizer(char_level=True, lower=True)
    dummy_text = "the quick brown fox jumps over the lazy dog"
    tokenizer.fit_on_texts([dummy_text])
    tokenizer_json = tokenizer.to_json()
    with open(os.path.join(MODEL_DIR, 'tokenizer.json'), 'w') as f:
        f.write(json.dumps(tokenizer_json, indent=4))
    print("Dummy tokenizer saved.")

    # 3. Create and save a dummy GRU-based model with correct input shape
    num_classes = len(tokenizer.word_index) + 1

    model = Sequential()
    model.add(Input(shape=(MAX_SEQ_LENGTH, NUM_MFCCS)))  # Correct 3D input shape
    model.add(Bidirectional(GRU(128, return_sequences=True)))
    model.add(Dropout(0.5))
    model.add(TimeDistributed(Dense(num_classes, activation='softmax')))
    
    model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    model.save(os.path.join(MODEL_DIR, 'cnn_lstm_model.h5'))
    print("Dummy GRU model saved.")

if __name__ == '__main__':
    create_and_save_dummy_model()