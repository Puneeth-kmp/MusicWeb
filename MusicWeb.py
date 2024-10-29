import os
import streamlit as st
from streamlit.components.v1 import html

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

# HTML and JavaScript for folder picker
folder_picker = """
<input type="file" id="folderPicker" webkitdirectory directory multiple>
<script>
    const folderPicker = document.getElementById('folderPicker');
    folderPicker.addEventListener('change', (event) => {
        const files = event.target.files;
        const paths = Array.from(files).map(file => file.webkitRelativePath);
        const uniquePaths = [...new Set(paths.map(path => path.split('/')[0]))];
        const selectedFolder = uniquePaths[0];
        window.parent.postMessage({selectedFolder: selectedFolder}, '*');
    });
</script>
"""

# Display folder picker
html(folder_picker)

# Placeholder for selected directory
selected_directory = st.empty()

# JavaScript to handle folder selection
selected_folder = st.experimental_get_query_params().get('selectedFolder', [None])[0]

if selected_folder:
    selected_directory.write(f"Selected directory: {selected_folder}")

    # List and play local audio files from the selected folder
    audio_files = get_local_audio_files(selected_folder)

    if audio_files:
        st.write("Available songs:")
        selected_file = st.selectbox("Select a song to play", audio_files)

        if selected_file:
            st.audio(selected_file)
    else:
        st.warning("No audio files found in the specified directory.")
else:
    st.warning("Please select a directory.")
