import streamlit as st
import os
from pathlib import Path
import time

# Set page configuration
st.set_page_config(page_title="Music Player", layout="wide")

# Directory to save uploaded audio files
UPLOAD_DIR = "uploaded_audio_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Supported audio file formats
SUPPORTED_FORMATS = ['.mp3', '.wav', '.ogg']

# Custom CSS
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #121212;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1DB954 !important;
        font-family: 'Arial', sans-serif;
    }
    
    /* File uploader */
    .uploadedFile {
        background-color: #282828 !important;
        border: 2px dashed #1DB954 !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }
    
    /* Audio player container */
    .stAudio {
        background-color: #282828 !important;
        border-radius: 10px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
    }
    
    /* Success message */
    .success {
        padding: 10px;
        border-radius: 5px;
        background-color: rgba(29, 185, 84, 0.1);
        border: 1px solid #1DB954;
        color: #1DB954;
    }
    
    /* Warning message */
    .stWarning {
        background-color: rgba(255, 214, 0, 0.1) !important;
        border: 1px solid #FFD700 !important;
    }
    
    /* Select box */
    .stSelectbox {
        background-color: #282828 !important;
        color: white !important;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #1DB954 !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 5px !important;
        cursor: pointer !important;
    }
    
    .stButton button:hover {
        background-color: #1ed760 !important;
    }
</style>
""", unsafe_allow_html=True)

def save_uploaded_file(uploaded_file):
    """Save uploaded file to directory and return the file path"""
    file_path = Path(UPLOAD_DIR) / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(file_path)

def get_saved_audio_files():
    """Get list of saved audio files"""
    audio_files = []
    for file in Path(UPLOAD_DIR).glob("*"):
        if file.suffix.lower() in SUPPORTED_FORMATS:
            audio_files.append(str(file))
    return sorted(audio_files)

def format_filename(filepath):
    """Format filepath to display name"""
    return Path(filepath).name

# App Header
st.title("🎵 Music Player")
st.markdown("---")

# File Upload Section
st.markdown("### Upload Music")
uploaded_files = st.file_uploader(
    "Choose your favorite songs",
    accept_multiple_files=True,
    type=['mp3', 'wav', 'ogg'],
    help="Supported formats: MP3, WAV, OGG"
)

# Handle file uploads
if uploaded_files:
    with st.spinner("Processing uploads..."):
        for uploaded_file in uploaded_files:
            save_uploaded_file(uploaded_file)
        st.success(f"Successfully uploaded {len(uploaded_files)} file(s)!")
        time.sleep(1)  # Give user time to see the success message
        st.experimental_rerun()  # Refresh to update the playlist

# Player Section
st.markdown("### Now Playing")
audio_files = get_saved_audio_files()

if audio_files:
    # Create columns for player controls
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Song selection
        selected_file = st.selectbox(
            "Select a song",
            audio_files,
            format_func=format_filename,
            key="song_select"
        )
        
        # Audio player
        st.audio(selected_file, format='audio/mp3')
        
    with col2:
        # Display current song info
        st.markdown("#### Current Track")
        st.markdown(f"**{format_filename(selected_file)}**")
        
    # Playlist section
    st.markdown("### Playlist")
    for idx, file in enumerate(audio_files, 1):
        is_playing = file == selected_file
        status = "🎵 " if is_playing else "   "
        st.markdown(
            f"{status}{idx}. {format_filename(file)}",
            unsafe_allow_html=True
        )
else:
    st.warning("No audio files found. Upload some music to get started!")

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ using Streamlit",
    unsafe_allow_html=True
)

# Add session state to maintain player state
if 'playing' not in st.session_state:
    st.session_state.playing = False
