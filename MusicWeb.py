import yt_dlp
import os
import streamlit as st

DOWNLOAD_PATH = "./downloads"

def download_audio(youtube_url):
    try:
        # Set options for yt-dlp to extract audio
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
        }
        audio_file = None
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            audio_file = ydl.prepare_filename(info_dict)
            audio_file = audio_file.replace('.webm', '.mp3')  # Adjust extension if necessary

        # Return the file and the video title
        return audio_file, info_dict.get('title', 'Unknown title')
    except Exception as e:
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
            st.audio(audio_file)
        else:
            st.error("Failed to download audio. Please check the video link.")
    else:
        st.error("Please enter a valid YouTube URL.")
