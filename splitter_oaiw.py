# This version uses the standard OpenAI Whisper model to transcribe the audio and split it into sentences.

import os
import ffmpeg
from pydub import AudioSegment
import whisper

# Ensure you have ffmpeg installed in your system and accessible via PATH
# You can download it from https://ffmpeg.org/download.html

# Directory paths
input_dir = 'input'
output_dir = 'oaiw_processed'

# Load Whisper model
model = whisper.load_model("medium")

def convert_mp4_to_wav(mp4_path, wav_path):
    audio = ffmpeg.input(mp4_path)
    audio = ffmpeg.output(audio, wav_path, format='wav')
    ffmpeg.run(audio)

def transcribe_audio(wav_path):
    result = model.transcribe(wav_path)
    return result['segments']

def split_audio_by_sentences(wav_path, segments, output_dir):
    audio = AudioSegment.from_wav(wav_path)
    manifest_lines = []

    for i, segment in enumerate(segments):
        start_ms = segment['start'] * 1000
        end_ms = segment['end'] * 1000
        sentence = segment['text'].strip()
        
        sentence_audio = audio[start_ms:end_ms]
        sentence_filename = f"audio{i+1}.wav"
        sentence_path = os.path.join(output_dir, sentence_filename)
        
        sentence_audio.export(sentence_path, format="wav")
        
        manifest_lines.append(f"{sentence_filename}|0|{sentence}")

    return manifest_lines

def process_mp4_files(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith('.mp4'):
            base_filename = os.path.splitext(filename)[0]
            mp4_path = os.path.join(input_dir, filename)
            wav_dir = os.path.join(output_dir, base_filename)
            wav_path = os.path.join(wav_dir, f"{base_filename}.wav")
            
            os.makedirs(wav_dir, exist_ok=True)
            
            # Convert MP4 to WAV
            convert_mp4_to_wav(mp4_path, wav_path)
            
            # Transcribe audio
            segments = transcribe_audio(wav_path)
            
            # Split audio and create manifest
            manifest_lines = split_audio_by_sentences(wav_path, segments, wav_dir)
            
            # Write manifest file
            manifest_path = os.path.join(wav_dir, "manifest.txt")
            with open(manifest_path, 'w', encoding='utf-8') as manifest_file:
                manifest_file.write("\n".join(manifest_lines))

# Run the processing
process_mp4_files(input_dir, output_dir)

print("Processing complete! UwU 🎉")
