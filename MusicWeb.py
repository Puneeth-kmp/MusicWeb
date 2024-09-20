import streamlit as st
from pytube import YouTube
from pydub import AudioSegment
from pydub.playback import play
import os

# Define the path for saving the audio files
DOWNLOAD_PATH = "downloads"

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

# Streamlit app layout
st.title("YouTube Audio Downloader")
youtube_url = st.text_input("Paste the YouTube link:")

# Function to download audio
def download_audio(youtube_url):
    try:
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(output_path=DOWNLOAD_PATH)
        base, ext = os.path.splitext(audio_file)
        new_file = base + '.mp3'
        os.rename(audio_file, new_file)
        return new_file, yt.title
    except Exception as e:
        st.error(f"Error downloading audio: {str(e)}")
        return None, None

# Button to trigger download
if st.button("Download Audio"):
    if youtube_url:
        audio_file, title = download_audio(youtube_url)
        if audio_file:
            st.success(f"Downloaded '{title}' successfully!")
            st.audio(audio_file)
    else:
        st.warning("Please paste a valid YouTube link.")

# Optional playback button
if st.button("Play Audio"):
    if audio_file:
        # Load and play the downloaded audio
        audio = AudioSegment.from_mp3(audio_file)
        play(audio)
    else:
        st.warning("No audio file to play.")
