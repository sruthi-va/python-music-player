import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel
import pygame

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Music Player")
        self.setGeometry(100, 100, 300, 150)

        self.init_ui()

        pygame.mixer.init()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("No file selected")
        layout.addWidget(self.label)

        self.btn_browse = QPushButton("Browse MP3")
        self.btn_browse.clicked.connect(self.load_file)
        layout.addWidget(self.btn_browse)

        self.btn_play = QPushButton("Play")
        self.btn_play.clicked.connect(self.play_music)
        layout.addWidget(self.btn_play)

        self.btn_pause = QPushButton("Pause")
        self.btn_pause.clicked.connect(self.pause_music)
        layout.addWidget(self.btn_pause)

        self.setLayout(layout)
        self.music_file = None
        self.is_paused = False

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open MP3 File", "", "Audio Files (*.mp3)")
        if file_name:
            self.music_file = file_name
            self.label.setText(f"Loaded: {file_name.split('/')[-1]}")
            pygame.mixer.music.load(self.music_file)

    def play_music(self):
        if self.music_file:
            pygame.mixer.music.play()
            self.is_paused = False

    def pause_music(self):
        if self.music_file:
            if self.is_paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
            self.is_paused = not self.is_paused

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())
