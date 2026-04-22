import sys
import time
import random
import pygame
import requests
from syncedlyrics import search
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
from io import BytesIO

# CONFIG
song_path = r"c:\Users\Ulfrán\Desktop\Python\P_1\TheWorldEnder.mp3.mp3"
query = "The World Ender Lord Huron"

# AUDIO
pygame.mixer.init()
pygame.mixer.music.load(song_path)

# LETRAS
lyrics = search(query)
lines = []

if lyrics:
    for line in lyrics.split("\n"):
        if "]" in line:
            try:
                t = line.split("]")[0][1:]
                text = line.split("]")[1]
                mins, secs = map(float, t.split(":")[:2])
                total = mins * 60 + secs
                lines.append((total, text))
            except:
                continue

if not lines:
    lines = [(0, "No hay letras")]

#  Portada (Spotify API)
def get_cover():
    try:
        url = f"https://api.deezer.com/search?q={query}"
        data = requests.get(url).json()
        img_url = data["data"][0]["album"]["cover_big"]
        img_data = requests.get(img_url).content
        return QPixmap.fromImage(QImage.fromData(img_data))
    except:
        return None

# APP
class Player(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SEVEN.FM")
        self.setGeometry(200, 100, 1100, 600)
        self.setStyleSheet("background-color: #0d0d1a; color: white;")

        main = QHBoxLayout()

        # IZQUIERDA
        left = QVBoxLayout()

        self.cover = QLabel()
        self.cover.setFixedSize(250, 250)
        pix = get_cover()
        if pix:
            self.cover.setPixmap(pix.scaled(250, 250))
        else:
            self.cover.setText("No cover")

        self.visual = QLabel()
        self.visual.setAlignment(Qt.AlignCenter)

        left.addWidget(self.cover)
        left.addWidget(self.visual)

        # DERECHA
        right = QVBoxLayout()

        self.lyrics = QLabel("Cargando...")
        self.lyrics.setAlignment(Qt.AlignCenter)
        self.lyrics.setStyleSheet("font-size: 24px;")

        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                background: #222;
                height: 10px;
            }
            QProgressBar::chunk {
                background: #9b5cff;
            }
        """)

        self.play = QPushButton("▶")
        self.play.clicked.connect(self.play_music)

        right.addWidget(self.lyrics)
        right.addWidget(self.progress)
        right.addWidget(self.play)

        main.addLayout(left, 1)
        main.addLayout(right, 2)

        container = QWidget()
        container.setLayout(main)
        self.setCentralWidget(container)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.start_time = None

    def play_music(self):
        pygame.mixer.music.play()
        self.start_time = time.time()
        self.timer.start(50)

    def update_ui(self):
        t = time.time() - self.start_time

        # LETRAS
        current = ""
        for time_l, text in lines:
            if t >= time_l:
                current = text

        self.lyrics.setText(current)

        # VISUALIZER ANIMADO
        bars = " ".join(["▇" * random.randint(1, 6) for _ in range(20)])
        self.visual.setText(bars)

        # PROGRESO
        prog = min(int((t / 180) * 100), 100)
        self.progress.setValue(prog)

# RUN
app = QApplication(sys.argv)
w = Player()
w.show()
sys.exit(app.exec_())

print ("¡Gracias por usar SEVEN.FM!")
print ("¡Hasta la próxima!")