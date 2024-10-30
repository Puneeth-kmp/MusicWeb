import streamlit as st
import os
from pathlib import Path
import time
import random

# Set page configuration
st.set_page_config(page_title="Music Player", layout="wide")

# Directory to save uploaded audio files
UPLOAD_DIR = "uploaded_audio_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Supported audio file formats
SUPPORTED_FORMATS = ['.mp3', '.wav', '.ogg']

# Custom CSS with enhanced button styling
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
    
    /* Controls container */
    .controls-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin: 10px 0;
    }
    
    /* Control buttons */
    .control-button {
        background-color: #1DB954;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    
    .control-button:hover {
        background-color: #1ed760;
    }
    
    /* Active state for shuffle/repeat buttons */
    .control-button.active {
        background-color: #1ed760;
        border: 2px solid white;
    }
    
    /* Playlist item */
    .playlist-item {
        padding: 10px;
        margin: 5px 0;
        background-color: #282828;
        border-radius: 5px;
        cursor: pointer;
    }
    
    .playlist-item:hover {
        background-color: #383838;
    }
    
    .playlist-item.playing {
        border-left: 4px solid #1DB954;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False
if 'shuffle_on' not in st.session_state:
    st.session_state.shuffle_on = False
if 'repeat_on' not in st.session_state:
    st.session_state.repeat_on = False
if 'auto_play' not in st.session_state:
    st.session_state.auto_play = True
if 'last_played' not in st.session_state:
    st.session_state.last_played = None

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

def play_next():
    """Play next song based on current playback mode"""
    audio_files = get_saved_audio_files()
    if not audio_files:
        return

    if st.session_state.shuffle_on:
        st.session_state.current_index = random.randint(0, len(audio_files) - 1)
    else:
        st.session_state.current_index = (st.session_state.current_index + 1) % len(audio_files)
    
    st.session_state.is_playing = True
    st.experimental_rerun()

def play_previous():
    """Play previous song"""
    audio_files = get_saved_audio_files()
    if not audio_files:
        return

    if st.session_state.shuffle_on:
        st.session_state.current_index = random.randint(0, len(audio_files) - 1)
    else:
        st.session_state.current_index = (st.session_state.current_index - 1) % len(audio_files)
    
    st.session_state.is_playing = True
    st.experimental_rerun()

def toggle_play():
    """Toggle play/pause state"""
    st.session_state.is_playing = not st.session_state.is_playing
    st.experimental_rerun()

def toggle_shuffle():
    """Toggle shuffle mode"""
    st.session_state.shuffle_on = not st.session_state.shuffle_on
    st.experimental_rerun()

def toggle_repeat():
    """Toggle repeat mode"""
    st.session_state.repeat_on = not st.session_state.repeat_on
    st.experimental_rerun()

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
        time.sleep(1)
        st.experimental_rerun()

# Player Section
st.markdown("### Now Playing")
audio_files = get_saved_audio_files()

if audio_files:
    # Ensure current_index is valid
    if st.session_state.current_index >= len(audio_files):
        st.session_state.current_index = 0
    
    current_file = audio_files[st.session_state.current_index]
    
    # Create columns for player layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Audio player
        audio_player = st.audio(current_file, format='audio/mp3')
        
        # Player controls
        controls_col1, controls_col2, controls_col3, controls_col4, controls_col5 = st.columns(5)
        
        with controls_col1:
            st.button("⏮️ Previous", on_click=play_previous, key="prev_button")
        
        with controls_col2:
            play_text = "⏸️ Pause" if st.session_state.is_playing else "▶️ Play"
            st.button(play_text, on_click=toggle_play, key="play_button")
        
        with controls_col3:
            st.button("⏭️ Next", on_click=play_next, key="next_button")
        
        with controls_col4:
            shuffle_text = "🔀 Shuffle (On)" if st.session_state.shuffle_on else "🔀 Shuffle"
            st.button(shuffle_text, on_click=toggle_shuffle, key="shuffle_button")
        
        with controls_col5:
            repeat_text = "🔁 Repeat (On)" if st.session_state.repeat_on else "🔁 Repeat"
            st.button(repeat_text, on_click=toggle_repeat, key="repeat_button")
    
    with col2:
        # Display current song info
        st.markdown("#### Current Track")
        st.markdown(f"**{format_filename(current_file)}**")
        
        # Display playback mode
        if st.session_state.shuffle_on:
            st.markdown("🔀 Shuffle On")
        if st.session_state.repeat_on:
            st.markdown("🔁 Repeat On")
    
    # Playlist section
    st.markdown("### Playlist")
    for idx, file in enumerate(audio_files):
        is_current = idx == st.session_state.current_index
        status = "🎵 " if is_current else "   "
        if st.button(
            f"{status}{format_filename(file)}",
            key=f"playlist_{idx}",
            help="Click to play"
        ):
            st.session_state.current_index = idx
            st.session_state.is_playing = True
            st.experimental_rerun()

    # Auto-play next song
    if st.session_state.last_played != current_file:
        st.session_state.last_played = current_file
        if st.session_state.auto_play:
            time.sleep(0.1)  # Small delay to ensure audio element is loaded
            play_next()

else:
    st.warning("No audio files found. Upload some music to get started!")

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ using Streamlit",
    unsafe_allow_html=True
)
