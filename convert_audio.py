import os
from pydub import AudioSegment

def convert_to_wav(input_path, output_path):
    """Converts an audio file to a standard WAV format."""
    try:
        audio = AudioSegment.from_file(input_path, format="webm")
        audio.export(output_path, format="wav")
        print(f"Successfully converted {os.path.basename(input_path)} to {os.path.basename(output_path)}")
    except Exception as e:
        print(f"Error converting {os.path.basename(input_path)}: {e}")

if __name__ == "__main__":
    test_data_dir = "test_data"
    audio_files = ["normal.wav", "high_pitch.wav", "low_pitch.wav"]
    
    for filename in audio_files:
        input_path = os.path.join(test_data_dir, filename)
        output_filename = filename.replace(".wav", "_converted.wav")
        output_path = os.path.join(test_data_dir, output_filename)
        
        if os.path.exists(input_path):
            convert_to_wav(input_path, output_path)
        else:
            print(f"File not found: {input_path}")


