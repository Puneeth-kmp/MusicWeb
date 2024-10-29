import os
import streamlit as st

# Supported audio file formats
SUPPORTED_FORMATS = ['.mp3', '.wav', '.ogg']

# Function to get a list of audio files from the uploaded files
def get_local_audio_files(uploaded_files):
    audio_files = []
    for uploaded_file in uploaded_files:
        if os.path.splitext(uploaded_file.name)[1].lower() in SUPPORTED_FORMATS:
            audio_files.append(uploaded_file)
    return audio_files

# Streamlit UI logic
st.title("Local Audio Player")

# File uploader to select audio files
uploaded_files = st.file_uploader("Choose audio files", accept_multiple_files=True, type=SUPPORTED_FORMATS)

if uploaded_files:
    st.write("Available songs:")
    audio_files = get_local_audio_files(uploaded_files)
    selected_file = st.selectbox("Select a song to play", audio_files, format_func=lambda x: x.name)

    if selected_file:
        st.audio(selected_file)
else:
    st.warning("No audio files uploaded.")
