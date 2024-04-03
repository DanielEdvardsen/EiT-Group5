import os
import sys
import time

import pandas as pd
from PyQt5.QtCore import Qt, QUrl, QPoint
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QGroupBox,
    QPushButton,
    QSlider,
    QLabel,
    QOpenGLWidget,
)

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QSurfaceFormat, QOpenGLContext
import moderngl as mgl

from player import Player
from scene import Scene
from settings import *
from shader_program import ShaderProgram

MUSIC_DIR = "genres_original/"
MESH_DIR = "/3d_files/"


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.media_player = QMediaPlayer()
        # Song specifics
        self.current_song_index = 0
        self.genre = None
        self.song_files = []

        # Subject specifics
        self.cur_subject = 1

        self.init_ui()
        self.media_player.positionChanged.connect(self.update_progress_bar)
        self.media_player.durationChanged.connect(self.update_duration)

    def init_ui(self):
        # Create layout
        main_layout = QVBoxLayout()

        # Genre selection
        genre_group_box = QGroupBox("Genres")  # Changed the title to 'Genres'
        genre_layout = QVBoxLayout()

        genres = [genre for genre in os.listdir(MUSIC_DIR)]
        self.genre_radio_buttons = []
        for genre in genres:
            radio_button = QRadioButton(genre)
            self.genre_radio_buttons.append(radio_button)
            genre_layout.addWidget(radio_button)

        genre_group_box.setLayout(genre_layout)

        # Subject group box
        subject_group_box = QGroupBox("Subjects")
        subject_layout = QVBoxLayout()
        subjects = [i for i in range(1, 6)]
        self.subject_radio_buttons = []
        for subject in subjects:
            radio_button = QRadioButton(str(f"Subject: {subject}"))
            self.subject_radio_buttons.append(radio_button)
            subject_layout.addWidget(radio_button)
        subject_group_box.setLayout(subject_layout)

        self.subject_radio_buttons[0].setChecked(True)

        # 3D Animation
        animation_group_box = QGroupBox("3D Animation")
        animation_layout = QVBoxLayout()

        self.opengl_widget = QOpenGLWidget()
        animation_layout.addWidget(self.opengl_widget)

        animation_group_box.setLayout(animation_layout)
        group_boxes_layout = QHBoxLayout()

        main_layout.addLayout(group_boxes_layout)
        main_layout.addWidget(animation_group_box)

        # voxel engine
        voxel_widget = VoxelWidget()
        main_layout.addWidget(voxel_widget)

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
        self.volume_slider.setValue(100)
        self.volume_slider.setToolTip("Volume")
        self.volume_slider.valueChanged.connect(self.set_volume)

        # Playback Slider
        self.playback_slider = QSlider(Qt.Horizontal)

        # Now Playing Label
        now_playing_label = QLabel("Now playing:")

        # Genres and subjects

        group_boxes_layout.addWidget(genre_group_box)
        group_boxes_layout.addWidget(subject_group_box)

        # Add the horizontal layout to the main layout
        main_layout.addLayout(group_boxes_layout)
        # Music controls
        main_layout.addWidget(now_playing_label)
        main_layout.addWidget(self.playback_slider)
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.volume_slider)

        self.setLayout(main_layout)
        self.setWindowTitle("Music Player")

        # Logic
        self.play_button.clicked.connect(self.play_song)
        self.pause_button.clicked.connect(self.media_player.pause)
        self.stop_button.clicked.connect(self.media_player.stop)
        self.next_button.clicked.connect(self.play_next_song)
        self.previous_button.clicked.connect(self.play_previous_song)

        for radio_button in self.subject_radio_buttons:
            radio_button.clicked.connect(self.update_subject)
        for radio_button in self.genre_radio_buttons:
            radio_button.clicked.connect(self.update_genre)

        self.load_song_list()

    def update_genre(self):
        """
        Update the genre based on the selected radio button.
        """
        for radio_button in self.genre_radio_buttons:
            if radio_button.isChecked():
                self.genre = radio_button.text().lower()
                break

    def set_volume(self, value):
        """
        Set the volume of the media player.
        """
        self.media_player.setVolume(value)

    def update_subject(self):
        """
        Update the current subject based on the selected radio button, reload the song list.
        """
        for radio_button in self.subject_radio_buttons:
            if radio_button.isChecked():
                self.cur_subject = int(radio_button.text().split(": ")[1])
                break
        self.load_song_list()

    def load_song_list(self):
        """
        Load the songs related to the current subject session.
        """
        df = pd.read_csv(
            f"dataset/sub-00{self.cur_subject}/func/sub-00{self.cur_subject}_task-Test_run-01_events.tsv",
            sep="\t",
        )
        self.song_files = {}

        for index, row in df.iterrows():
            genre = row["genre"].strip("'")
            track = row["track"]
            start = row["start"]
            end = row["end"]

            if genre not in self.song_files:
                self.song_files[genre] = {}

            self.song_files[genre][track] = {"start": start, "end": end}

    def play_song(self):
        """
        Plays the first song the subject listened to in the selected genre.
        """

        if not self.genre:
            print("No genre selected.")
            return

        # Check if there are any songs in the list
        if not self.song_files:
            print("No songs available to play.")
            return

        # Get the first song in the selected genre
        cur_song = list(self.song_files[self.genre].keys())[0]
        # pad the string with zeros such that it adheres to the naming convention
        cur_song = str(cur_song).zfill(5)

        # Play the song
        song_url = QUrl.fromLocalFile(
            os.path.join(MUSIC_DIR, self.genre, f"{self.genre}.{cur_song}.wav")
        )
        print(f"song url: {song_url}")
        print(f"Playing {self.genre}.{cur_song}")
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
        song_url = QUrl.fromLocalFile(
            os.path.join(genre_dir, next_song_file)
        )  # Modify this line
        print(f"Playing {next_song_file}")
        self.media_player.setMedia(QMediaContent(song_url))
        self.media_player.play()

    def play_previous_song(self):
        # Check if there are any songs in the list
        if not self.song_files:
            print("No songs available to play.")
            return

        if self.current_song_index == 0:
            self.current_song_index = len(self.song_files) - 1
        else:
            self.current_song_index -= 1

        # Construct the new file name
        previous_song_file = f"{self.genre}.{str(self.current_song_index).zfill(5)}.wav"

        # Check if the new file name exists in the list of songs
        if previous_song_file not in self.song_files:
            print("No more songs available in this genre.")
            return

        # Update the current song index
        self.current_song_index = self.song_files.index(previous_song_file)

        # Play the previous song
        genre_dir = os.path.join(MUSIC_DIR, self.genre)
        song_url = QUrl.fromLocalFile(os.path.join(genre_dir, previous_song_file))
        print(f"Playing {previous_song_file}")
        self.media_player.setMedia(QMediaContent(song_url))
        self.media_player.play()

    def update_progress_bar(self, position):
        self.playback_slider.setValue(position)

    def update_duration(self, duration):
        """
        Update the duration of the song.
        """
        self.playback_slider.setRange(0, duration)


# QtOpenGL.QGLWidget
class VoxelWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(VoxelWidget, self).__init__(parent)
        self.setFixedSize(round(1600 / 3), round(900 / 3))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # Approximately 60 FPS

        self.player = None
        self.shader_program = None
        self.scene = None
        self.time = 0
        self.last_time = 0
        self.delta_time = 0

        self.lastPos = QPoint()

    def initializeGL(self):
        format = QSurfaceFormat()
        format.setVersion(3, 3)
        format.setProfile(QSurfaceFormat.CoreProfile)
        format.setDepthBufferSize(24)
        QSurfaceFormat.setDefaultFormat(format)

        self.ctx = mgl.create_context()

        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.blend_func = (mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA)
        self.ctx.gc_mode = "auto"

        self.delta_time = 0
        self.time = 0

        self.on_init()

    def on_init(self):
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)

    def updateGL(self):
        # Handle game logic updates here
        self.player.update()
        self.shader_program.update()
        self.scene.update()

        # Calculate delta_time and update time
        current_time = time.time()  # You need to import time
        self.delta_time = current_time - self.last_time
        self.last_time = current_time

    def resizeGL(self, w, h):
        # Adjust the viewport and projection matrix on resize
        pass

    def paintGL(self):
        # Call updateGL() to update the game logic
        self.updateGL()
        # Perform rendering here
        # self.ctx.clear(color=BG_COLOR)
        self.scene.render(self.ctx)

        # Optionally, update the window title with FPS
        self.setWindowTitle(f"{1.0 / (self.delta_time + 1e-4):.0f} FPS")

    def keyPressEvent(self, event):
        # Handle keyboard input
        pass

    def mouseMoveEvent(self, event):
        # PyQt provides the current position via event.pos()
        # Calculate the difference between the last position and the current position
        mouse_dx = event.x() - self.lastPos.x()
        mouse_dy = event.y() - self.lastPos.y()

        print(f"Mouse dx: {mouse_dx}, Mouse dy: {mouse_dy}")

        MOUSE_SENSITIVITY = 0.02  # Adjust as necessary

        if mouse_dx:
            self.player.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.player.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

        # Update the last position for the next call
        self.lastPos = event.pos()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setCentralWidget(VoxelWidget())
        self.setWindowTitle("Voxel Engine")
        # self.resize(*WIN_RES)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
