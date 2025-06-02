import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel
from PyQt5.QtCore import QTimer
import pygame

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.setGeometry(100, 100, 300, 150)

        self.init_ui()

        pygame.mixer.init()
        self.playlist = self.load_songs_from_folder("songs")
        self.current_index = 0
        self.is_paused = False

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.check_song_finished)
        self.timer.start()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Ready")
        layout.addWidget(self.label)

        self.btn_play = QPushButton("Play")
        self.btn_play.clicked.connect(self.play_music)
        layout.addWidget(self.btn_play)

        self.btn_pause = QPushButton("Pause/Unpause")
        self.btn_pause.clicked.connect(self.pause_music)
        layout.addWidget(self.btn_pause)

        self.btn_next = QPushButton("Next Song")
        self.btn_next.clicked.connect(self.next_song)
        layout.addWidget(self.btn_next)

        self.setLayout(layout)

    def load_songs_from_folder(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
        files = [f for f in os.listdir(folder) if f.lower().endswith('.mp3')]
        full_paths = [os.path.join(folder, f) for f in sorted(files)]
        return full_paths

    def play_music(self):
        if not self.playlist:
            self.label.setText("No songs in folder.")
            return

        song = self.playlist[self.current_index]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.is_paused = False
        self.label.setText(f"Now Playing: {os.path.basename(song)}")

    def pause_music(self):
        if not self.playlist:
            return

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.label.setText(f"Resumed: {os.path.basename(self.playlist[self.current_index])}")
            self.is_paused = False
        else:
            pygame.mixer.music.pause()
            self.label.setText("Paused")
            self.is_paused = True


    def next_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play_music()

    def check_song_finished(self):
        if not pygame.mixer.music.get_busy() and not self.is_paused:
            self.next_song()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())
