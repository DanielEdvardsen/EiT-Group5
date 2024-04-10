import os
import sys
import time

import moderngl as mgl
import pandas as pd
from player import Player
from PyQt5.QtCore import QPoint, Qt, QTimer, QUrl
from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QOpenGLWidget,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)
from scene import Scene
from shader_program import ShaderProgram

MUSIC_DIR = "genres_original/"
DATASET_DIR = "dataset/"


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.media_player = QMediaPlayer()
        # Song specifics
        self.current_song_index = 0
        self.genre = None
        self.song_files = {}

        # Subject specifics
        self.cur_subject = 1

        self.init_ui()
        self.media_player.positionChanged.connect(self.update_progress_bar)
        self.media_player.durationChanged.connect(self.update_duration)

    def init_ui(self):
        # Create layout
        main_layout = QVBoxLayout()

        # Genre selection
        self.genre_combo_box = QComboBox()
        genres = [genre for genre in os.listdir(MUSIC_DIR)]
        self.genre_combo_box.addItems(genres)
        self.genre_combo_box.currentIndexChanged.connect(self.update_genre)

        genre_group_box = QGroupBox("Genres")
        genre_layout = QVBoxLayout()
        genre_layout.addWidget(self.genre_combo_box)
        genre_group_box.setLayout(genre_layout)
        self.genre = genres[0].lower()

        # Subject selection
        self.subject_combo_box = QComboBox()
        subjects = [str(i) for i in range(1, 6)]
        self.subject_combo_box.addItems(subjects)
        self.subject_combo_box.currentIndexChanged.connect(self.update_subject)

        subject_group_box = QGroupBox("Subjects")
        subject_layout = QVBoxLayout()
        subject_layout.addWidget(self.subject_combo_box)
        subject_group_box.setLayout(subject_layout)

        # 3D Animation
        animation_group_box = QGroupBox("3D Animation")
        animation_layout = QVBoxLayout()

        # self.opengl_widget = QOpenGLWidget()
        # self.opengl_widget.setMinimumSize(800, 600)
        # animation_layout.addWidget(self.opengl_widget)

        animation_group_box.setLayout(animation_layout)
        group_boxes_layout = QHBoxLayout()

        main_layout.addLayout(group_boxes_layout)
        main_layout.addWidget(animation_group_box)

        # voxel engine
        self.voxel_widget = VoxelWidget()
        self.voxel_widget.setMinimumSize(700, 700)
        main_layout.addWidget(self.voxel_widget)

        # Media Player Controls
        controls_layout = QHBoxLayout()
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        self.next_button = QPushButton("Next")
        self.previous_button = QPushButton("Previous")

        # controls_layout.addWidget(self.previous_button)
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.stop_button)
        # controls_layout.addWidget(self.next_button)

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
        self.pause_button.clicked.connect(self.pause_song)
        self.stop_button.clicked.connect(self.stop_song)
        self.next_button.clicked.connect(self.play_next_song)
        self.previous_button.clicked.connect(lambda: self.play_next_song(forward=False))
        self.load_song_list()

    def update_genre(self):
        """
        Update the genre based on the selected radio button.
        """
        self.genre = (
            self.genre_combo_box.currentText().lower()
        )  # CHANGE: Get the current text from the QComboBox
        self.load_song_list()  # CHANGE: Load songs for the selected genre
        self.play_song()

    def set_volume(self, value):
        """
        Set the volume of the media player.
        """
        self.media_player.setVolume(value)

    def update_subject(self):
        """
        Update the current subject based on the selected radio button, reload the song list.
        """
        self.cur_subject = int(self.subject_combo_box.currentText())
        self.load_song_list()

        self.voxel_widget.updateBrain(self.cur_subject)

    def load_song_list(self):
        """
        Load the songs related to the current subjects' session.
        """
        # check if path exist before attempting to read
        if not os.path.exists(
            f"{DATASET_DIR}/sub-00{self.cur_subject}/func/sub-001_task-Test_run-01_events.tsv"
        ):
            print("No songs available for this subject.")
            return

        df = pd.read_csv(
            f"{DATASET_DIR}/sub-00{self.cur_subject}/func/sub-001_task-Test_run-01_events.tsv",
            sep="\t",
        )
        self.song_files = {}

        for index, row in df.iterrows():
            genre = row["genre"].strip("'")
            track = row["track"]
            start = row["start"]
            end = row["end"]

            if genre in self.song_files:
                continue

            self.song_files[genre] = {"track": track, "start": start, "end": end}

    def play_song(self):
        """
        Plays the first song the subject listened to in the selected genre.
        """
        # If the player is paused, continue playing the current song
        if self.media_player.state() == QMediaPlayer.PausedState:
            self.media_player.play()
            return

        if not self.genre:
            print("No genre selected.")
            return

        # Check if there are any songs in the list
        if not self.song_files:
            print("No songs available to play.")
            return

        # Get the first song and pad the string with zeros such that it adheres to the naming convention
        cur_track = self.song_files[self.genre]["track"]
        cur_track = str(cur_track).zfill(5)
        start_time = int(self.song_files[self.genre]["start"] * 1000)

        # Play the song
        song_url = QUrl.fromLocalFile(
            os.path.join(MUSIC_DIR, self.genre, f"{self.genre}.{cur_track}.wav")
        )
        self.media_player.setMedia(QMediaContent(song_url))
        self.media_player.setPosition(start_time)
        self.media_player.play()
        self.media_player.positionChanged.connect(self.check_song_end)

        # Start animation
        self.voxel_widget.scene.toggle_anim(self.voxel_widget.current_time)

    def check_song_end(self, position):
        """
        Check if the current playback position has reached the end time of the current song and stop playback if so.
        """
        end_time_ms = int(self.song_files[self.genre]["end"] * 1000)
        if position >= end_time_ms:
            self.media_player.stop()
            self.media_player.positionChanged.disconnect(self.check_song_end)

    def pause_song(self):
        self.media_player.pause()
        self.voxel_widget.scene.toggle_anim(self.voxel_widget.current_time)

    def stop_song(self):
        self.media_player.stop()
        self.voxel_widget.scene.reset()

        # Start animation
        self.voxel_widget.scene.toggle_anim(self.voxel_widget.current_time)

    def play_next_song(self, forward=True):
        # Check if there are any songs in the list
        if not self.song_files or not self.genre or not self.song_files[self.genre]:
            print("No songs available to play.")
            return

        # Get the list of tracks for the current genre
        tracks = list(self.song_files[self.genre].keys())

        # Find the current track index
        current_track_index = (
            self.current_song_index if self.current_song_index < len(tracks) else -1
        )

        if forward:
            next_track_index = (current_track_index + 1) % len(tracks)
        else:
            next_track_index = (current_track_index - 1) % len(tracks)

        # Get the next track
        next_track = tracks[next_track_index]

        # Construct the new file name
        next_song_file = f"{self.genre}.{str(next_track).zfill(5)}.wav"

        # Update the current song index
        self.current_song_index = next_track_index

        # Play the next song
        genre_dir = os.path.join(MUSIC_DIR, self.genre)  # Add this line
        song_url = QUrl.fromLocalFile(
            os.path.join(genre_dir, next_song_file)
        )  # Modify this line
        self.media_player.setMedia(QMediaContent(song_url))
        self.media_player.play()

    def update_progress_bar(self, position):
        self.playback_slider.setValue(position)

    def update_duration(self, duration):
        self.playback_slider.setRange(0, duration)


# QtOpenGL.QGLWidget
class VoxelWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(VoxelWidget, self).__init__(parent)
        # self.setFixedSize(round(1600 / 3), round(900 / 3))
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

    def updateBrain(self, subject_id):
        self.scene.update_subject(subject_id)

    def updateGL(self):
        # Handle game logic updates here
        self.player.update()
        self.shader_program.update()
        self.scene.update()

        # Calculate delta_time and update time
        self.current_time = time.time()  # You need to import time
        self.delta_time = self.current_time - self.last_time
        self.last_time = self.current_time

    def resizeGL(self, w, h):
        # Adjust the viewport and projection matrix on resize
        pass

    def paintGL(self):
        # Call to update the game logic
        self.updateGL()
        # Perform rendering here
        # self.ctx.clear(color=BG_COLOR)
        self.scene.render(self.ctx, self.current_time)

    def keyPressEvent(self, event):
        # Handle keyboard input
        pass

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        # PyQt provides the current position via event.pos()
        # Calculate the difference between the last position and the current position
        mouse_dx = event.x() - self.lastPos.x()
        mouse_dy = event.y() - self.lastPos.y()

        print(f"Mouse dx: {mouse_dx}, Mouse dy: {mouse_dy}")

        MOUSE_SENSITIVITY = 0.01  # Adjust as necessary

        if mouse_dx:
            # self.player.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
            self.player.rotate_x(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            # self.player.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)
            self.player.rotate_y(delta_y=mouse_dy * MOUSE_SENSITIVITY)

        print(f"Yaw: {self.player.yaw}, Pitch: {self.player.pitch}")

        # Update the last position for the next call
        self.lastPos = event.pos()

    def wheelEvent(self, event):
        # Get the angle delta of the scroll wheel (in eighths of a degree)
        angle_delta = event.angleDelta().y()

        # Check if the angle delta is positive (scrolling up) or negative (scrolling down)
        if angle_delta < 0:
            self.player.move_forward(10)
        else:
            self.player.move_back(10)

        print(f"Position: {self.player.position}")


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
