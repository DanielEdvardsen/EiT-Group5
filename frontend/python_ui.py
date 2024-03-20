import os
import random
import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QRadioButton, QGroupBox, QPushButton, QSlider, QLabel, QOpenGLWidget)

MUSIC_DIR = '../genres_original/'


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.media_player = QMediaPlayer()
        self.current_song_index = 0
        self.genre = None
        self.song_files = []
        self.init_ui()

        self.media_player.positionChanged.connect(self.update_progress_bar)
        self.media_player.durationChanged.connect(self.update_duration)

    def init_ui(self):
        # Create layout
        main_layout = QVBoxLayout()

        # Genre selection
        genre_group_box = QGroupBox("Genres")  # Changed the title to 'Genres'
        genre_layout = QVBoxLayout()

        genres = ["Blues", "Jazz", "Classical", "Country", "Disco", "Hiphop",
                  "Metal", "Pop", "Reggae", "Rock"]
        self.genre_radio_buttons = []
        for genre in genres:
            radio_button = QRadioButton(genre)
            self.genre_radio_buttons.append(radio_button)
            genre_layout.addWidget(radio_button)

        genre_group_box.setLayout(genre_layout)

        # 3D Animation
        animation_group_box = QGroupBox("3D Animation")
        animation_layout = QVBoxLayout()

        self.opengl_widget = QOpenGLWidget()
        animation_layout.addWidget(self.opengl_widget)

        animation_group_box.setLayout(animation_layout)
        # Add widgets to main layout
        main_layout.addWidget(genre_group_box)
        main_layout.addWidget(animation_group_box)

        # Media Player Controls
        controls_layout = QHBoxLayout()
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        self.next_button = QPushButton("Next")
        self.previous_button = QPushButton("Previous")

        controls_layout.addWidget(self.previous_button)
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addWidget(self.next_button)

        # Volume Slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setToolTip("Volume")

        # Playback Slider
        self.playback_slider = QSlider(Qt.Horizontal)

        # Now Playing Label
        now_playing_label = QLabel("Now playing:")

        # Add widgets to main layout
        main_layout.addWidget(genre_group_box)
        main_layout.addWidget(now_playing_label)
        main_layout.addWidget(self.playback_slider)
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.volume_slider)

        self.setLayout(main_layout)
        self.setWindowTitle('Music Player')

        self.play_button.clicked.connect(self.play_random_song)
        self.pause_button.clicked.connect(self.media_player.pause)
        self.stop_button.clicked.connect(self.media_player.stop)
        self.next_button.clicked.connect(self.play_next_song)

    def play_random_song(self):
        # Determine selected genre
        for radio_button in self.genre_radio_buttons:
            if radio_button.isChecked():
                self.genre = radio_button.text().lower()
                print(self.genre)
                break

        if not self.genre:
            print("No genre selected.")
            return

        # Get list of all songs in selected genre's directory
        genre_dir = os.path.join(MUSIC_DIR, self.genre)

        self.song_files = [f for f in os.listdir(genre_dir) if os.path.isfile(os.path.join(genre_dir, f))]

        # Choose a random song
        random_song_file = random.choice(self.song_files)
        self.current_song_index = self.song_files.index(random_song_file)

        # Play the song
        song_url = QUrl.fromLocalFile(os.path.join(genre_dir, random_song_file))
        print(f"Playing {random_song_file}")
        self.media_player.setMedia(QMediaContent(song_url))
        self.media_player.play()

    def play_next_song(self):
        # Check if there are any songs in the list
        if not self.song_files:
            print(self.song_files)
            print("No songs available to play.")
            return

        if self.current_song_index == len(self.song_files) - 1:
            self.current_song_index = 0
        else:
            self.current_song_index += 1

        # Construct the new file name
        next_song_file = f"{self.genre}.{str(self.current_song_index).zfill(5)}.wav"

        # Check if the new file name exists in the list of songs
        if next_song_file not in self.song_files:
            print("No more songs available in this genre.")
            return

        # Update the current song index
        self.current_song_index = self.song_files.index(next_song_file)

        # Play the next song
        genre_dir = os.path.join(MUSIC_DIR, self.genre)  # Add this line
        song_url = QUrl.fromLocalFile(os.path.join(genre_dir, next_song_file))  # Modify this line
        print(f"Playing {next_song_file}")
        self.media_player.setMedia(QMediaContent(song_url))
        self.media_player.play()

    def update_progress_bar(self, position):
        self.playback_slider.setValue(position)

    def update_duration(self, duration):
        self.playback_slider.setRange(0, duration)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())
