const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const statusText = document.getElementById('status');
const transcriptionText = document.getElementById('transcriptionText');

let mediaRecorder;
let audioChunks = [];

startBtn.addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm;codecs=opus' });
        audioChunks = [];
        
        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            sendAudioToServer(audioBlob);
        };

        mediaRecorder.start();
        startBtn.disabled = true;
        stopBtn.disabled = false;
        statusText.textContent = "Recording...";
        transcriptionText.textContent = "";
        
    } catch (err) {
        console.error('Error accessing microphone:', err);
        statusText.textContent = "Error: Could not access microphone.";
    }
});

stopBtn.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        startBtn.disabled = false;
        stopBtn.disabled = true;
        statusText.textContent = "Processing audio...";
    }
});

async function sendAudioToServer(audioBlob) {
    try {
        const response = await fetch('/transcribe', {
            method: 'POST',
            body: audioBlob,
            headers: { 'Content-Type': 'audio/webm' }
        });

        if (response.ok) {
            const data = await response.json();
            transcriptionText.textContent = data.transcription;
            statusText.textContent = "Transcription complete.";
        } else {
            console.error('Server error:', response.statusText);
            statusText.textContent = "Transcription failed.";
        }
    } catch (error) {
        console.error('Error sending audio:', error);
        statusText.textContent = "An error occurred.";
    }
}
