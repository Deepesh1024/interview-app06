import io
import tempfile
import moviepy.editor as mp
import whisper
import json
import streamlit as st

class VideoTranscriber:
    def __init__(self, video_file, output_audio_path, output_json_path):
        self.video_file = video_file  # Video file uploaded in memory
        self.output_audio_path = output_audio_path
        self.output_json_path = output_json_path
        self.model = whisper.load_model("small")

    def extract_audio(self):
        """Extract audio from video file and save it."""
        # Create a temporary file in memory from the uploaded video file
        with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
            temp_video_file.write(self.video_file.read())
            temp_video_file_path = temp_video_file.name

        # Use the temporary file path for VideoFileClip
        video_clip = mp.VideoFileClip(temp_video_file_path)
        audio = video_clip.audio
        audio.write_audiofile(self.output_audio_path)

    def transcribe(self):
        """Transcribe audio and save the results to the JSON file."""
        self.extract_audio()  # Extract audio before transcribing
        results = self.model.transcribe(self.output_audio_path, verbose=True)
        transcription_output = []
        data = ""
        for segment in results['segments']:
            start = segment['start']
            end = segment['end']
            text = segment['text']
            
            # Print the transcription to console
            print(f"[{start:.2f}s - {end:.2f}s] {text}")
            data += f"[{start:.2f}s - {end:.2f}s] {text}"

            # Append the segment information to the list
            transcription_output.append({
                'start': start,
                'end': end,
                'text': text
            })

        # Write the transcription results to a JSON file
        with open(self.output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(transcription_output, json_file, ensure_ascii=False, indent=4)

        print(f"Transcription results saved to {self.output_json_path}")
        return data

# # Streamlit UI to upload video file
# uploaded_video = st.file_uploader("Choose a video...", type=["mp4", "mov", "avi", "mkv"])

# if uploaded_video is not None:
#     st.write("Transcribing Video...")
#     # Initialize the transcriber with the uploaded video file
#     transcriber = VideoTranscriber(uploaded_video, "audio.wav", "transcription_output.json")
#     transcriber.transcribe()  # Start transcription
