# 🎙️ Speech-to-Text Application

A **full-stack web application** for converting speech into text using a **Flask backend** and a **modern frontend**.  
Powered by **Hugging Face Wav2Vec2** for high-accuracy transcription.  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)
![Torch](https://img.shields.io/badge/PyTorch-2.x-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Features

- 🎤 **Real-time Audio Transcription** – Record from microphone and transcribe instantly.  
- 🌐 **Full-Stack Architecture** – Flask backend + responsive frontend (HTML/CSS/JS).  
- 🔊 **Audio Visualization** – See live input levels while recording.  
- 📂 **History Tracking** – Save & view past transcription results.  
- ⬇️ **Audio Playback & Download** – Replay or download your recordings.  
- 🧠 **Pre-trained AI Model** – Hugging Face **Wav2Vec2** ensures high transcription accuracy.  

---

## 🛠️ Requirements

- **Python 3.8+**  
- **pip** (Python package manager)  
- Recommended: **Virtual Environment**  

---

## 🚀 Setup & Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/BSTushar/major_proj.git
cd major_proj
```

### Step 2: Create & Activate Virtual Environment

```bash
# Create environment
python -m venv venv

# Activate it
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install Flask librosa soundfile transformers torch
```

> ⚡ If you run into errors installing `torch`, check the [official PyTorch installation guide](https://pytorch.org/get-started/locally/) for your system.

### Step 4: Run the Application

```bash
python run.py
```

Expected output:

```
 * Running on http://127.0.0.1:5000
```

---

## 🌐 Usage

1. Open your browser at **http://127.0.0.1:5000**  
2. Click **🎙️ Record** → Speak into your microphone.  
3. Click **🛑 Stop** → Wait for transcription to appear.  
4. Play back, download, or save your results.  

---

## 📂 Project Structure

```
major_proj/
├── backend/
│   ├── app.py              # Flask app logic
│   └── run.py              # Server runner script
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css   # Styling
│   │   └── js/
│   │       └── script.js   # Frontend logic
│   └── index.html          # User interface
├── .gitignore              # Ignore venv, __pycache__, etc.
└── README.md               # Project documentation
```

## ⚠️ Troubleshooting

- **Mic not working?**  
  Make sure your browser has microphone permissions enabled.  

- **Torch installation failed?**  
  Install according to your OS & CUDA version → [PyTorch Guide](https://pytorch.org/get-started/locally/).  

- **Server not starting?**  
  Ensure you activated your virtual environment and installed dependencies.  

---

## 🤝 Contributing

Contributions are welcome!  

1. Fork the repo 🍴  
2. Create a new branch (`feature-xyz`)  
3. Commit your changes  
4. Open a Pull Request  

---

## 📜 License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and share.  

---

## 👨‍💻 Author

**B.S. Tushar**  
🔗 [GitHub Profile](https://github.com/BSTushar)  

---
