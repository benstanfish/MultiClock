__version__ = '1.1'

from PyQt6.QtWidgets import (QApplication,
                             QWidget,
                             QVBoxLayout,
                             QGridLayout,
                             QLabel)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
import sys, os
import pytz
from tzlocal import get_localzone
from datetime import datetime
from time import perf_counter, sleep
import config

basedir = os.path.dirname(__file__)

settings = config.load_settings()

clocks = settings['clock.defaults']['clocks']
zones = [key for key in clocks.keys()]
current_zone = str(get_localzone())

theme_name = settings['selected_theme']

def screen_size():
    screen = QApplication.primaryScreen()
    if screen:
        geom = screen.geometry()
    return (geom.width(), geom.height())

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

        self.setWindowTitle(settings['window.defaults']['title'])

        window_width = 325
        window_height = int(100 * len(clocks))
        screen_width, screen_height = screen_size()
        left = screen_width - window_width - 20
        #top = (screen_height - window_height) // 2
        top = 40

        self.setGeometry(left, top, window_width, window_height)
        self.setWindowIcon(QIcon(settings['window.defaults']['icon']))
        self.setStyleSheet(f'background: {settings['themes'][theme_name]['window.background']};')
        self.setWindowOpacity(settings['window.defaults']['opacity'])

        self.night = QPixmap('./assets/night.png')
        self.dawn = QPixmap('./assets/dawn.png')
        self.day = QPixmap('./assets/day.png')
        self.dusk = QPixmap('./assets/dusk.png')

        self.create_clocks()
        self.update_time()

        # The following function aligns the timer to the computer clock within milliseconds
        self.align_time()

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(settings['window.defaults']['timer'])

    def create_clocks(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(12, 6, 12, 6)

        self.tz_names = []
        self.tz_dates = []
        self.tz_imgs = []
        self.tz_clocks = []
        self.tz_grids = []

        # Initialize Qlabels for each Timezone in Clocks
        for key in clocks.keys():
            self.tz_names.append(QLabel())
            self.tz_dates.append(QLabel())
            self.tz_imgs.append(QLabel())
            self.tz_clocks.append(QLabel())
            self.tz_grids.append(QGridLayout())

        for grid in self.tz_grids:
            vbox.addLayout(grid)

        theme = settings['themes'][theme_name]
        align = settings['clock.align']

        # Set formats for labels
        for tz_name, tz_date, tz_img, tz_clock, tz_grid, zone in \
            zip(self.tz_names, self.tz_dates, self.tz_imgs, self.tz_clocks, self.tz_grids, zones):

            tz_name.setStyleSheet(f'background: {theme['zone']['background']}; color: {theme['zone']['font.color']};')
            tz_name.setFont(QFont(theme['zone']['font'], theme['zone']['font.size'], theme['zone']['font.weight']))
            tz_name.setAlignment(Qt.AlignmentFlag(align['zone']['horizontal']) | Qt.AlignmentFlag(align['zone']['vertical']))
            tz_name.setText(zone)

            tz_date.setStyleSheet(f'background: {theme['date']['background']}; color: {theme['date']['font.color']};')
            tz_date.setFont(QFont(theme['date']['font'], theme['date']['font.size'], theme['date']['font.weight']))
            tz_date.setAlignment(Qt.AlignmentFlag(align['date']['horizontal']) | Qt.AlignmentFlag(align['date']['vertical']))

            tz_img.setStyleSheet(f'background: {theme['date']['background']}; color: {theme['date']['font.color']}; height: 50; width: 50;')

            tz_clock.setStyleSheet(f'background: {theme['clock']['background']}; color: {theme['clock']['font.color']};')
            tz_clock.setFont(QFont(theme['clock']['font'], theme['clock']['font.size'], theme['clock']['font.weight']))
            tz_clock.setAlignment(Qt.AlignmentFlag(align['clock']['horizontal']) | Qt.AlignmentFlag(align['clock']['vertical']))

            tz_grid.addWidget(tz_name, 0, 0, 1, 1)
            tz_grid.addWidget(tz_date, 0, 1, 1, 2)
            tz_grid.addWidget(tz_img, 1, 0, 1, 1)
            tz_grid.addWidget(tz_clock, 1, 1, 1, 2)

        self.tz_imgs[-1].setStyleSheet('margin-bottom: 12px')

        static = QLabel()
        static.setMaximumHeight(15)
        static.setText(f'MultiClock v{__version__}, Copyright © 2025, Ben Fisher')
        static.setFont(QFont('Aptos Narrow', 9))
        static.setStyleSheet(f'color: {theme['zone']['font.color']};')
        static.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        vbox.addWidget(static)
        self.setLayout(vbox)



    def update_time(self):

        _test_chime = False

        for zone, tz_name, tz_date, tz_img, tz_clock, current_time in \
            zip(zones, self.tz_names, self.tz_dates, self.tz_imgs, self.tz_clocks, current_times(clocks)):
            tz_name.setText(zone + ' (UTC ' + utc_offsets[zone] + ')')
            tz_date.setText(current_time.strftime(settings['clock.defaults']['date.format']))
            if clocks[zone] == current_zone:
                tz_clock.setText(current_time.strftime('%H:%M') + f'<span style="font-size: 20px;">:{current_time.strftime('%S')}</span>')
            else:
                tz_clock.setText(current_time.strftime(settings['clock.defaults']['time.format']))
            self.set_image(tz_img, current_time)
        if _test_chime:
            if datetime.now().second == 59 + settings['clock.defaults']['chime.offset']:
                self.play_chime()
        if datetime.now().minute == 59 and \
            datetime.now().second == 59 + settings['clock.defaults']['chime.offset']:
                if datetime.now().hour > 7 and datetime.now().hour < 22:
                # The chime is overridden (silent mode) between 22:00 to 08:00 the next day
                    self.play_chime()

    def play_chime(self):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(full_path(settings['clock.defaults']['chime'])))
        self.audio_output.setVolume(settings['clock.defaults']['chime.volume'])
        self.player.play()

    def set_image(self, image_host: QLabel, current_time):
        if current_time.hour >= 5 and current_time.hour < 8:
            image_host.setPixmap(self.dawn)
        elif current_time.hour >= 8 and current_time.hour < 17:
            image_host.setPixmap(self.day)
        elif current_time.hour >= 17 and current_time.hour < 19:
            image_host.setPixmap(self.dusk)
        else:
            image_host.setPixmap(self.night)
        image_host.setScaledContents(False)

    def align_time(self):
        """This function aligns the application timer and the now() time."""
        sleep(1 - perf_counter() % 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir, settings['window.defaults']['icon'])))
    window = Window()
    window.show()
    sys.exit(app.exec())