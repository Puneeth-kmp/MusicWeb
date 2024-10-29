import os
import streamlit as st

# Supported audio file formats
SUPPORTED_FORMATS = ['.mp3', '.wav', '.ogg']

# Function to get a list of audio files from the selected directory
def get_local_audio_files(directory):
    audio_files = []
    if not os.path.exists(directory):
        st.error(f"The directory {directory} does not exist.")
        return audio_files

    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1].lower() in SUPPORTED_FORMATS:
                    audio_files.append(os.path.join(root, file))
    except Exception as e:
        st.error(f"Error reading audio files: {str(e)}")
    return audio_files

# Streamlit UI logic
st.title("Local Audio Player")

# Text input to enter the directory path
directory = st.text_input("Enter the directory path")

if directory:
    st.write(f"Selected directory: {directory}")

    # List and play local audio files from the selected folder
    audio_files = get_local_audio_files(directory)

    if audio_files:
        st.write("Available songs:")
        selected_file = st.selectbox("Select a song to play", audio_files)

        if selected_file:
            st.audio(selected_file)
    else:
        st.warning("No audio files found in the specified directory.")
else:
    st.warning("Please enter a directory path.")
