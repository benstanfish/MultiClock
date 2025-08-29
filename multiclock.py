from PyQt6.QtWidgets import (QApplication, 
                             QWidget, 
                             QVBoxLayout,
                             QGridLayout, 
                             QLabel)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
import sys, os
import pytz
from datetime import datetime
import config

basedir = os.path.dirname(__file__)

defaults = config.defaults
clocks = defaults['clock.defaults']['clocks']
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

        self.setWindowTitle(defaults['window.defaults']['title'])
        left, top, width, height = defaults['window.defaults']['geometry']
        self.setGeometry(left, top, width, height)
        self.setWindowIcon(QIcon(defaults['window.defaults']['icon']))
        self.setStyleSheet(f'background: {defaults['window.defaults']['background']};')
        self.setWindowOpacity(defaults['window.defaults']['opacity'])

        self.create_clocks()
        self.update_clocks()

        timer = QTimer(self)
        timer.timeout.connect(self.update_clocks)
        timer.start(defaults['window.defaults']['timer'])


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
            grid.setContentsMargins(0, 0, 0, 0)
            vbox.addLayout(grid)
            vbox.addStretch()
        
        self.tz_grids[0].setContentsMargins(0, 24, 0, 0)
        self.tz_grids[-1].setContentsMargins(0, 0, 0, 24)

        theme = defaults['clock.themes']['plain']
        align = defaults['clock.align']

        # Set formats for labels
        for tz_name, tz_date, tz_clock, tz_grid, zone in zip(self.tz_names, 
                                                             self.tz_dates, 
                                                             self.tz_clocks, 
                                                             self.tz_grids,
                                                             zones):
            
            tz_name.setStyleSheet(f'background: {theme['zone']['background']}; color: {theme['zone']['font.color']};')
            tz_name.setFont(QFont(theme['zone']['font'], theme['zone']['font.size'], theme['zone']['font.weight']))
            tz_name.setAlignment(align['zone']['horizontal'] | align['zone']['vertical'])
            
            tz_name.setText(zone)
        
            tz_date.setStyleSheet(f'background: {theme['date']['background']}; color: {theme['date']['font.color']};')
            tz_date.setFont(QFont(theme['date']['font'], theme['date']['font.size'], theme['date']['font.weight']))
            tz_date.setAlignment(align['date']['horizontal'] | align['date']['vertical'])

            tz_clock.setStyleSheet(f'background: {theme['clock']['background']}; \
                                   color: {theme['clock']['font.color']}; border-top: {theme['clock']['border-top']};')
            tz_clock.setFont(QFont(theme['clock']['font'], theme['clock']['font.size'], theme['clock']['font.weight']))
            tz_clock.setAlignment(align['clock']['horizontal'] | align['clock']['vertical'])

            tz_grid.addWidget(tz_name, 0, 0, 1, 1)
            tz_grid.addWidget(tz_date, 0, 1, 1, 1)
            tz_grid.addWidget(tz_clock, 1, 0, 1, 2)

        self.setLayout(vbox)

    def update_clocks(self):
        for zone, tz_name, tz_date, tz_clock, current_time in \
            zip(zones, self.tz_names, self.tz_dates, self.tz_clocks, current_times(clocks)):
            tz_name.setText(zone + ' (GMT ' + utc_offsets[zone] + ')')
            tz_date.setText(current_time.strftime(defaults['clock.defaults']['date.format']))
            tz_clock.setText(current_time.strftime(defaults['clock.defaults']['time.format']))
        if datetime.now().minute == 59 and \
            datetime.now().second == 60 + defaults['clock.defaults']['chime.offset']:
            self.play_chime()
    
    def play_chime(self):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(full_path(defaults['clock.defaults']['chime'])))
        self.audio_output.setVolume(defaults['clock.defaults']['chime.volume'])
        self.player.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir, defaults['window.defaults']['icon'])))
    window = Window()
    window.show()
    sys.exit(app.exec())