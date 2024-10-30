<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Music Player</title>
    <style>
        :root {
            --primary-color: #1DB954;
            --bg-color: #121212;
            --secondary-bg: #282828;
            --text-primary: #ffffff;
            --text-secondary: #b3b3b3;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        .player-header {
            text-align: center;
            margin-bottom: 2rem;
        }

        .upload-zone {
            border: 2px dashed var(--primary-color);
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
            background-color: var(--secondary-bg);
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .upload-zone:hover {
            border-color: #1ed760;
            background-color: rgba(29, 185, 84, 0.1);
        }

        .upload-zone input[type="file"] {
            display: none;
        }

        .player-container {
            background-color: var(--secondary-bg);
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .visualization {
            height: 200px;
            background-color: var(--bg-color);
            border-radius: 10px;
            margin-bottom: 2rem;
            overflow: hidden;
            position: relative;
        }

        .visualization canvas {
            width: 100%;
            height: 100%;
        }

        .controls {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .control-btn {
            background: none;
            border: none;
            color: var(--text-primary);
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 50%;
            transition: all 0.3s ease;
        }

        .control-btn:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }

        .play-btn {
            background-color: var(--primary-color);
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .play-btn:hover {
            background-color: #1ed760;
            transform: scale(1.05);
        }

        .progress-container {
            width: 100%;
            height: 5px;
            background-color: var(--bg-color);
            border-radius: 5px;
            cursor: pointer;
            margin: 1rem 0;
        }

        .progress-bar {
            height: 100%;
            background-color: var(--primary-color);
            border-radius: 5px;
            width: 0%;
            transition: width 0.1s linear;
        }

        .time-info {
            display: flex;
            justify-content: space-between;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .playlist {
            margin-top: 2rem;
            background-color: var(--secondary-bg);
            border-radius: 10px;
            padding: 1rem;
        }

        .playlist-item {
            display: flex;
            align-items: center;
            padding: 0.75rem;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .playlist-item:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }

        .playlist-item.active {
            background-color: rgba(29, 185, 84, 0.2);
        }

        .playlist-item-title {
            margin-left: 1rem;
            flex-grow: 1;
        }

        .playlist-item-duration {
            color: var(--text-secondary);
        }

        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }

            .controls {
                flex-wrap: wrap;
            }

            .visualization {
                height: 150px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="player-header">
            <h1>🎵 Modern Music Player</h1>
        </div>

        <div class="upload-zone" id="uploadZone">
            <input type="file" id="fileInput" accept="audio/*" multiple>
            <p>Drop your audio files here or click to upload</p>
        </div>

        <div class="player-container">
            <div class="visualization">
                <canvas id="visualizer"></canvas>
            </div>

            <div class="controls">
                <button class="control-btn" id="prevBtn">⏮️</button>
                <button class="control-btn play-btn" id="playBtn">▶️</button>
                <button class="control-btn" id="nextBtn">⏭️</button>
                <button class="control-btn" id="shuffleBtn">🔀</button>
                <button class="control-btn" id="repeatBtn">🔁</button>
            </div>

            <div class="progress-container" id="progressContainer">
                <div class="progress-bar" id="progressBar"></div>
            </div>

            <div class="time-info">
                <span id="currentTime">0:00</span>
                <span id="duration">0:00</span>
            </div>

            <div class="playlist" id="playlist">
                <!-- Playlist items will be added here dynamically -->
            </div>
        </div>
    </div>

    <script>
        class MusicPlayer {
            constructor() {
                this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                this.audioElement = new Audio();
                this.playlist = [];
                this.currentTrack = 0;
                this.isPlaying = false;
                this.isRepeat = false;
                this.isShuffled = false;

                this.initializeAudioNodes();
                this.setupEventListeners();
                this.setupVisualization();
            }

            initializeAudioNodes() {
                this.audioSource = this.audioContext.createMediaElementSource(this.audioElement);
                this.analyser = this.audioContext.createAnalyser();
                this.analyser.fftSize = 256;
                
                this.audioSource.connect(this.analyser);
                this.analyser.connect(this.audioContext.destination);
            }

            setupEventListeners() {
                // Upload zone
                const uploadZone = document.getElementById('uploadZone');
                const fileInput = document.getElementById('fileInput');

                uploadZone.addEventListener('click', () => fileInput.click());
                uploadZone.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    uploadZone.style.borderColor = '#1ed760';
                });
                uploadZone.addEventListener('dragleave', () => {
                    uploadZone.style.borderColor = '#1DB954';
                });
                uploadZone.addEventListener('drop', (e) => {
                    e.preventDefault();
                    uploadZone.style.borderColor = '#1DB954';
                    this.handleFiles(e.dataTransfer.files);
                });
                fileInput.addEventListener('change', (e) => this.handleFiles(e.target.files));

                // Controls
                document.getElementById('playBtn').addEventListener('click', () => this.togglePlay());
                document.getElementById('prevBtn').addEventListener('click', () => this.playPrevious());
                document.getElementById('nextBtn').addEventListener('click', () => this.playNext());
                document.getElementById('shuffleBtn').addEventListener('click', () => this.toggleShuffle());
                document.getElementById('repeatBtn').addEventListener('click', () => this.toggleRepeat());

                // Progress bar
                const progressContainer = document.getElementById('progressContainer');
                progressContainer.addEventListener('click', (e) => {
                    const percent = e.offsetX / progressContainer.offsetWidth;
                    this.audioElement.currentTime = percent * this.audioElement.duration;
                });

                // Audio element events
                this.audioElement.addEventListener('timeupdate', () => this.updateProgress());
                this.audioElement.addEventListener('ended', () => this.handleTrackEnd());
            }

            handleFiles(files) {
                Array.from(files).forEach(file => {
                    if (file.type.startsWith('audio/')) {
                        const track = {
                            file: file,
                            name: file.name,
                            url: URL.createObjectURL(file)
                        };
                        this.playlist.push(track);
                    }
                });
                this.updatePlaylist();
                if (this.playlist.length === files.length) {
                    this.loadTrack(0);
                }
            }

            updatePlaylist() {
                const playlistElement = document.getElementById('playlist');
                playlistElement.innerHTML = '';
                
                this.playlist.forEach((track, index) => {
                    const item = document.createElement('div');
                    item.className = `playlist-item ${index === this.currentTrack ? 'active' : ''}`;
                    item.innerHTML = `
                        <span class="playlist-item-title">${track.name}</span>
                        <span class="playlist-item-duration">--:--</span>
                    `;
                    item.addEventListener('click', () => this.loadTrack(index));
                    playlistElement.appendChild(item);
                });
            }

            loadTrack(index) {
                if (index >= 0 && index < this.playlist.length) {
                    this.currentTrack = index;
                    this.audioElement.src = this.playlist[index].url;
                    this.audioElement.load();
                    this.updatePlaylist();
                    if (this.isPlaying) {
                        this.audioElement.play();
                    }
                }
            }

            togglePlay() {
                if (this.audioContext.state === 'suspended') {
                    this.audioContext.resume();
                }

                if (this.isPlaying) {
                    this.audioElement.pause();
                    document.getElementById('playBtn').textContent = '▶️';
                } else {
                    this.audioElement.play();
                    document.getElementById('playBtn').textContent = '⏸️';
                }
                this.isPlaying = !this.isPlaying;
            }

            playNext() {
                let nextTrack = this.currentTrack + 1;
                if (nextTrack >= this.playlist.length) {
                    nextTrack = 0;
                }
                this.loadTrack(nextTrack);
                if (this.isPlaying) {
                    this.audioElement.play();
                }
            }

            playPrevious() {
                let prevTrack = this.currentTrack - 1;
                if (prevTrack < 0) {
                    prevTrack = this.playlist.length - 1;
                }
                this.loadTrack(prevTrack);
                if (this.isPlaying) {
                    this.audioElement.play();
                }
            }

            toggleShuffle() {
                this.isShuffled = !this.isShuffled;
                document.getElementById('shuffleBtn').style.color = this.isShuffled ? '#1DB954' : '#ffffff';
            }

            toggleRepeat() {
                this.isRepeat = !this.isRepeat;
                document.getElementById('repeatBtn').style.color = this.isRepeat ? '#1DB954' : '#ffffff';
            }

            updateProgress() {
                const progressBar = document.getElementById('progressBar');
                const currentTime = document.getElementById('currentTime');
                const duration = document.getElementById('duration');

                const percent = (this.audioElement.currentTime / this.audioElement.duration) * 100;
                progressBar.style.width = `${percent}%`;

                currentTime.textContent = this.formatTime(this.audioElement.currentTime);
                duration.textContent = this.formatTime(this.audioElement.duration);
            }

            formatTime(seconds) {
                const minutes = Math.floor(seconds / 60);
                seconds = Math.floor(seconds % 60);
                return `${minutes}:${seconds.toString().padStart(2, '0')}`;
            }

            handleTrackEnd() {
                if (this.isRepeat) {
                    this.audioElement.play();
                } else if (this.isShuffled) {
                    const nextTrack = Math.floor(Math.random() * this.playlist.length);
                    this.loadTrack(nextTrack);
                    this.audioElement.play();
                } else {
                    this.playNext();
                }
            }

            setupVisualization() {
                const canvas = document.getElementById('visualizer');
                const ctx = canvas.getContext('2d');
                const bufferLength = this.analyser.frequencyBinCount;
                const dataArray = new Uint8Array(bufferLength);

                const draw = () => {
                    const WIDTH = canvas.width;
                    const HEIGHT = canvas.height;

                    requestAnimationFrame(draw);

                    this.analyser.getByteFrequencyData(dataArray);

                    ctx.fillStyle = 'rgb(18, 18, 18)';
                    ctx.fillRect(0, 0, WIDTH, HEIGHT);

                    const barWidth = (WIDTH / bufferLength) * 2.5;
                    let barHeight;
                    let x = 0;

                    for (let i = 0; i < bufferLength; i++) {
                        barHeight = dataArray[i] / 2;

                        const r = barHeight + 25;
                        const g = 250;
                        const b = 50;

                        ctx.fillStyle = `rgb(${r},${g},${b})`;
                        ctx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight);

                        x += barWidth + 1;
                    }
                };

                const resizeCanvas = () => {
                    canvas.width = canvas.offsetWidth;
                    canvas.height = canvas.offsetHeight;
                };

                window.addEventListener('resize', resizeCanvas);
                resizeCanvas();
                draw();
            }
        }

        // Initialize the music player when the page loads
        window.addEventListener('load', () => {
            const player = new MusicPlayer();
        });
    </script>
</body>
</html>
</antArtif
