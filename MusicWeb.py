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
st.title("🎵 Local Audio Player")
st.markdown("""
<style>
    .main {
        background-color: #f0f0f5;
        padding: 20px;
        border-radius: 10px;
    }
    h1 {
        color: #4CAF50;
    }
    .audio-player {
        margin-top: 20px;
        padding: 10px;
        background-color: #ffffff;
        border-radius: 5px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# File uploader to select audio files
uploaded_files = st.file_uploader("Choose audio files", accept_multiple_files=True, type=SUPPORTED_FORMATS)

if uploaded_files:
    for uploaded_file in uploaded_files:
        save_uploaded_file(uploaded_file)
    st.success("Files uploaded successfully!")

# List and play saved audio files
audio_files = get_saved_audio_files()

if audio_files:
    st.write("Available songs:")
    selected_file = st.selectbox("Select a song to play", audio_files, format_func=lambda x: os.path.basename(x))

    if selected_file:
        st.markdown(f"<div class='audio-player'><h3>Now Playing: {os.path.basename(selected_file)}</h3></div>", unsafe_allow_html=True)
        st.audio(selected_file)
else:
    st.warning("No audio files found.")
