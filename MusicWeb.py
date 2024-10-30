import os
import streamlit as st

# Directory to save uploaded audio files
UPLOAD_DIR = "uploaded_audio_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Supported audio file formats
SUPPORTED_FORMATS = ['.mp3', '.wav', '.ogg']

# Function to save uploaded files
def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Function to get a list of saved audio files
def get_saved_audio_files():
    audio_files = []
    for root, dirs, files in os.walk(UPLOAD_DIR):
        for file in files:
            if os.path.splitext(file)[1].lower() in SUPPORTED_FORMATS:
                audio_files.append(os.path.join(root, file))
    return audio_files

# Streamlit UI logic
st.set_page_config(page_title="Music Player", layout="wide")
st.title("🎶 Local Music Player")

# CSS for styling
st.markdown("""
<style>
    body {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .header {
        text-align: center;
        padding: 20px;
    }
    .upload-area {
        border: 2px dashed #1DB954;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .audio-player {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    }
    .song-title {
        font-size: 18px;
        font-weight: bold;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# File uploader to select audio files
st.markdown("<div class='upload-area'>", unsafe_allow_html=True)
uploaded_files = st.file_uploader("Choose your favorite songs", accept_multiple_files=True, type=SUPPORTED_FORMATS)
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        save_uploaded_file(uploaded_file)
    st.success("Files uploaded successfully!")

# List and play saved audio files
audio_files = get_saved_audio_files()

if audio_files:
    st.write("Available Songs:")
    selected_file = st.selectbox("Select a song to play", audio_files, format_func=lambda x: os.path.basename(x))

    if selected_file:
        st.markdown("<div class='audio-player'>", unsafe_allow_html=True)
        st.audio(selected_file)
        st.markdown(f"<div class='song-title'>Now Playing: {os.path.basename(selected_file)}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.warning("No audio files found.")
