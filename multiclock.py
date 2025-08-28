from PyQt6.QtWidgets import (QApplication, 
                             QWidget, 
                             QVBoxLayout,
                             QGridLayout, 
                             QLabel)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
import sys, os, json
import pytz
from datetime import datetime

clocks = {
    'Tokyo': 'Asia/Tokyo',
    'New York': 'US/Eastern',
    'GTNP': 'US/Mountain',
    'Seattle': 'US/Pacific',
    'Honolulu': 'US/Hawaii'
}

zones = [key for key in clocks.keys()]


def current_times(clocks=clocks):
    times = []
    for key in clocks.keys():
        times.append(datetime.now(pytz.timezone(clocks[key])))
    return times

def utc_offset(timezone_name, dt_obj=None):
    try:
        tz = pytz.timezone(timezone_name)
    except pytz.UnknownTimeZoneError:
        return '?'
    dt_obj = datetime.now(tz) if not None else tz.localize(dt_obj)
    offset_timedelta = dt_obj.utcoffset()
    if offset_timedelta is None:
        return '?'
    return int(offset_timedelta.total_seconds() / 3600)

def get_utc_offsets(clocks=clocks):
    offsets = {}
    for key in clocks.keys():
        offsets[key] = str(utc_offset(clocks[key]))
    return offsets

utc_offsets = get_utc_offsets(clocks)

def full_path(rel_path):
    return os.path.abspath(rel_path)

class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('MultiClock')
        self.setGeometry(200, 200, 350, 1)
        self.setWindowIcon(QIcon(full_path('./img/yagura_starfield.png')))
        self.setStyleSheet('background: #333;')
        self.setWindowOpacity(0.95)

        self.create_clocks()
        self.update_clocks()

        timer = QTimer(self)
        timer.timeout.connect(self.update_clocks)
        timer.start(1000)


    def create_clocks(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(12, 0, 12, 0)

        self.tz_names = []
        self.tz_dates = []
        self.tz_clocks = []
        self.tz_grids = []

        # Initialize Qlabels for each Timezone in Clocks
        for key in clocks.keys():
            self.tz_names.append(QLabel())
            self.tz_dates.append(QLabel())
            self.tz_clocks.append(QLabel())
            self.tz_grids.append(QGridLayout())

        for grid in self.tz_grids:
            grid.setContentsMargins(0, 6, 0, 6)
            vbox.addLayout(grid)
            vbox.addStretch()
        
        self.tz_grids[0].setContentsMargins(0, 24, 0, 0)
        self.tz_grids[-1].setContentsMargins(0, 0, 0, 24)

        # Set formats for labels
        for tz_name, tz_date, tz_clock, tz_grid, zone in zip(self.tz_names, 
                                                             self.tz_dates, 
                                                             self.tz_clocks, 
                                                             self.tz_grids,
                                                             zones):
            tz_name.setStyleSheet('background: transparent; color: #FFD700;')
            tz_name.setFont(QFont('Aptos Narrow', 11, QFont.Weight.Normal))
            tz_name.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
            tz_name.setText(zone)
        
            tz_date.setStyleSheet('background: transparent; color: #FF6347;')
            tz_date.setFont(QFont('Aptos Narrow', 11))
            tz_date.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

            tz_clock.setStyleSheet('color: #1E90FF; border-top: 1px solid #555;')
            tz_clock.setFont(QFont('Aptos', 36))
            tz_clock.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

            tz_grid.addWidget(tz_name, 0, 0, 1, 1)
            tz_grid.addWidget(tz_date, 0, 1, 1, 1)
            tz_grid.addWidget(tz_clock, 1, 0, 1, 2)

        self.setLayout(vbox)

    def update_clocks(self):
        for zone, tz_name, tz_date, tz_clock, current_time in zip(zones, self.tz_names, self.tz_dates, self.tz_clocks, current_times(clocks)):
            tz_name.setText(zone + ' (GMT ' + utc_offsets[zone] + ')')
            tz_date.setText(current_time.strftime('%a, %d %B %Y'))
            tz_clock.setText(current_time.strftime('%H:%M:%S'))
        if datetime.now().minute == 59 and datetime.now().second == 56:
            self.play_chime()
    
    def play_chime(self):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(full_path('jihou-sine-3f.mp3')))
        self.audio_output.setVolume(50)
        self.player.play()

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())