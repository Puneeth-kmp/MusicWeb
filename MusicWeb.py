import os
import streamlit as st
from tkinter import Tk, filedialog

# Function to select folder using tkinter
def select_folder():
    root = Tk()
    root.withdraw()  # Hide the main tkinter window
    folder_path = filedialog.askdirectory()  # Open the folder dialog
    root.destroy()  # Close the tkinter window
    return folder_path

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

# Button to select folder
if st.button("Select Folder"):
    folder_path = select_folder()
    if folder_path:
        st.write(f"Selected directory: {folder_path}")

        # List and play local audio files from the selected folder
        audio_files = get_local_audio_files(folder_path)

        if audio_files:
            st.write("Available songs:")
            selected_file = st.selectbox("Select a song to play", audio_files)

            if selected_file:
                st.audio(selected_file)
        else:
            st.warning("No audio files found in the specified directory.")
    else:
        st.warning("No folder selected.")
