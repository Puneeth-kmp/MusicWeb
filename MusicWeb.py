import streamlit as st
from pytube import YouTube
import os

# Define a directory to save the downloaded audio
DOWNLOAD_PATH = "./downloads"

def download_audio(youtube_url):
    try:
        # Ensure audio file is set to None by default
        audio_file = None

        # Attempt to create YouTube object
        yt = YouTube(youtube_url)
        
        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Check if audio stream is available
        if not audio_stream:
            st.error("No audio stream found for this video.")
            return None, None
        
        # Download the audio stream
        audio_file = audio_stream.download(output_path=DOWNLOAD_PATH)

        # Rename the downloaded file to an mp3
        base, ext = os.path.splitext(audio_file)
        new_file = base + '.mp3'
        os.rename(audio_file, new_file)

        # Return the downloaded file and the video title
        return new_file, yt.title
    except Exception as e:
        # Handle exceptions and show error message
        st.error(f"Error downloading audio: {str(e)}")
        return None, None

# Streamlit UI logic
st.title("YouTube Audio Downloader")

# Get YouTube URL from the user
youtube_url = st.text_input("Enter YouTube URL", "")

# Create a download button
if st.button("Download Audio"):
    if youtube_url:
        # Attempt to download audio
        audio_file, video_title = download_audio(youtube_url)
        
        # Check if audio_file is properly assigned
        if audio_file:
            st.success(f"Downloaded: {video_title}")
            # Add an option to play the audio (if desired)
            st.audio(audio_file)
        else:
            st.error("Failed to download audio. Please check the video link.")
    else:
        st.error("Please enter a valid YouTube URL.")
