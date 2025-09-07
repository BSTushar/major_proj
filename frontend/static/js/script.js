// Get DOM elements
const recordButton = document.getElementById('recordButton');
const stopButton = document.getElementById('stopButton');
const audioVisualizer = document.getElementById('audioVisualizer');
const statusText = document.getElementById('status');
const loadingSpinner = document.getElementById('loadingSpinner');
const transcriptionText = document.getElementById('transcriptionText');
const audioPlayer = document.getElementById('audioPlayer');
const downloadAudioLink = document.getElementById('downloadAudio');
const audioPlaybackSection = document.querySelector('.audio-playback');
const historyList = document.getElementById('historyList');

// Variables for audio recording
let mediaRecorder;
let audioChunks = [];
let audioContext;
let analyser;
let source;
let dataArray;
let canvasContext;
let animationFrameId;

// Visualizer setup
const canvas = audioVisualizer;
canvasContext = canvas.getContext('2d');

// Helper function to update the UI status
function setStatus(message, isError = false) {
    statusText.textContent = message;
    statusText.style.color = isError ? 'var(--accent-color-secondary)' : 'var(--text-color-secondary)';
}

// Event listeners for buttons
recordButton.addEventListener('click', () => {
    startRecording();
});

stopButton.addEventListener('click', () => {
    stopRecording();
});

// Function to start recording audio
async function startRecording() {
    setStatus('Requesting microphone access...');
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Reset audio chunks and recorder
        audioChunks = [];
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });

        // Setup audio context for the visualizer
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        source = audioContext.createMediaStreamSource(stream);
        source.connect(analyser);
        analyser.fftSize = 256;
        const bufferLength = analyser.frequencyBinomialCount;
        dataArray = new Uint8Array(bufferLength);
        
        // Handle recorded audio data
        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        // Handle recorder stopping
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            transcribeAudio(audioBlob);
            
            // Show audio playback controls
            const audioUrl = URL.createObjectURL(audioBlob);
            audioPlayer.src = audioUrl;
            downloadAudioLink.href = audioUrl;
            audioPlaybackSection.style.display = 'block';
        };

        // Start recording and update UI
        mediaRecorder.start();
        recordButton.disabled = true;
        stopButton.disabled = false;
        setStatus('Recording...');
        audioVisualizer.style.display = 'block';
        drawVisualizer();

    } catch (err) {
        setStatus(`Error: Could not get microphone access.`, true);
        console.error('Error accessing microphone:', err);
    }
}

// Function to stop recording
function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        stopButton.disabled = true;
        recordButton.disabled = false;
        setStatus('Processing...');
        
        // Stop the visualizer animation
        cancelAnimationFrame(animationFrameId);
        audioVisualizer.style.display = 'none';
        
        // Stop all audio tracks
        if (source) {
            source.mediaStream.getAudioTracks().forEach(track => track.stop());
        }
    }
}

// Function to send audio to the backend for transcription
async function transcribeAudio(audioBlob) {
    loadingSpinner.style.display = 'block';
    
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');

    try {
        const response = await fetch('/transcribe', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            transcriptionText.textContent = data.transcription;
            addToHistory(data.transcription);
            setStatus('Transcription complete!');
        } else {
            setStatus(`Transcription failed: ${data.error}`, true);
            transcriptionText.textContent = 'Error during transcription.';
        }
    } catch (err) {
        setStatus(`Transcription failed: ${err.message}`, true);
        console.error('Transcription error:', err);
        transcriptionText.textContent = 'An unexpected error occurred.';
    } finally {
        loadingSpinner.style.display = 'none';
    }
}

// Function to draw the audio visualizer
function drawVisualizer() {
    animationFrameId = requestAnimationFrame(drawVisualizer);
    
    analyser.getByteFrequencyData(dataArray);

    canvasContext.clearRect(0, 0, canvas.width, canvas.height);

    const barWidth = (canvas.width / dataArray.length) * 2.5;
    let barHeight;
    let x = 0;

    for (let i = 0; i < dataArray.length; i++) {
        barHeight = dataArray[i] / 2;
        
        canvasContext.fillStyle = `rgb(${barHeight + 100}, 50, 50)`;
        canvasContext.fillRect(x, canvas.height - barHeight / 2, barWidth, barHeight);

        x += barWidth + 1;
    }
}

// Function to add transcription to history
function addToHistory(transcription) {
    const listItem = document.createElement('li');
    listItem.textContent = transcription;
    historyList.prepend(listItem);
}