__version__ = '1.1'

from PyQt6.QtWidgets import (QApplication,
                             QWidget,
                             QHBoxLayout,
                             QVBoxLayout,
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
from aclockv import QAClock

basedir = os.path.dirname(__file__)

settings = config.load_settings()

clocks = settings['clock.defaults.horizontal']['clocks']
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

        self.setWindowTitle("MultiClock Analog")

        window_height = 325
        window_width = int(175 * len(clocks))
        screen_width, screen_height = screen_size()
        left = screen_width - window_width - 20
        #top = (screen_height - window_height) // 2
        top = 40

        self.setGeometry(left, top, window_width, window_height)
        self.setWindowIcon(QIcon(settings['window.defaults']['icon_alt']))
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
        timer.timeout.connect(lambda: self.update_time())
        timer.start(settings['window.defaults']['timer'])

    def create_clocks(self):
        global_vbox = QVBoxLayout()


        hbox = QHBoxLayout()
        # hbox.setContentsMargins(0, 12, 0, 12)

        main_label = QLabel()
        main_label.setText(f'MultiClock Analog <span style="font-size: 12px;">(version {__version__})</span>')
        main_label.setMaximumHeight(60)
        main_label.setFont(QFont('Aptos Narrow', 16))
        main_label.setStyleSheet(f'color: {settings['themes'][theme_name]['zone']['font.color']}; border-bottom: 1px solid {settings['themes'][theme_name]['zone']['font.color']}; padding-bottom: 3px; margin-bottom: 6px;')
        main_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        global_vbox.addWidget(main_label)

        global_vbox.addLayout(hbox)

        self.tz_names = []
        self.tz_dates = []
        self.tz_aclocks = []
        self.tz_clocks = []
        self.tz_vboxes = []

        # Initialize Qlabels for each Timezone in Clocks
        for key in clocks.keys():
            self.tz_names.append(QLabel())
            self.tz_dates.append(QLabel())
            self.tz_aclocks.append(QAClock())
            self.tz_clocks.append(QLabel())
            self.tz_vboxes.append(QVBoxLayout())

        for tz_vbox in self.tz_vboxes:
            hbox.addLayout(tz_vbox)

        theme = settings['themes'][theme_name]
        align = settings['clock.align.horizontal']

        # Set formats for labels
        for tz_name, tz_date, tz_aclock, tz_clock, tz_vbox, zone in \
            zip(self.tz_names, self.tz_dates, self.tz_aclocks, self.tz_clocks, self.tz_vboxes, zones):

            tz_name.setStyleSheet(f'background: {theme['zone']['background']}; color: {theme['zone']['font.color']};')
            tz_name.setFont(QFont(theme['zone']['font'], theme['zone']['font.size'], theme['zone']['font.weight']))
            tz_name.setAlignment(Qt.AlignmentFlag(align['zone']['horizontal']) | Qt.AlignmentFlag(align['zone']['vertical']))
            tz_name.setText(zone)

            tz_date.setStyleSheet(f'background: {theme['date']['background']}; color: {theme['date']['font.color']};')
            tz_date.setFont(QFont(theme['date']['font'], theme['date']['font.size'], theme['date']['font.weight']))
            tz_date.setAlignment(Qt.AlignmentFlag(align['date']['horizontal']) | Qt.AlignmentFlag(align['date']['vertical']))

            tz_clock.setStyleSheet(f'background: {theme['clock']['background']}; color: {theme['clock']['font.color']};')
            tz_clock.setFont(QFont(theme['clock']['font'], theme['clock']['font.size'], theme['clock']['font.weight']))
            tz_clock.setAlignment(Qt.AlignmentFlag(align['clock']['horizontal']) | Qt.AlignmentFlag(align['clock']['vertical']))

            tz_vbox.addWidget(tz_name)
            tz_vbox.addWidget(tz_date)
            tz_vbox.addWidget(tz_aclock.view)
            tz_vbox.addWidget(tz_clock)


        theme_label = QLabel()
        theme_label.setMaximumHeight(20)
        theme_label.setText(f'The current theme is <span style="font-weight: bold;">{settings['selected_theme'].title()}</span>')
        theme_label.setFont(QFont('Aptos Narrow', 9))
        theme_label.setStyleSheet(f'color: {theme['zone']['font.color']}; border-bottom: 1px solid {theme['zone']['font.color']}; padding-bottom: 3px;')
        theme_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        global_vbox.addWidget(theme_label)



        static = QLabel()
        static.setMaximumHeight(15)
        static.setText(f'MultiClock Analog, Copyright © 2025, Ben Fisher')
        static.setFont(QFont('Aptos Narrow', 9))
        static.setStyleSheet(f'color: {theme['zone']['font.color']};')
        static.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        global_vbox.addWidget(static)


        self.setLayout(global_vbox)

    def update_time(self):

        _test_chime = False

        for zone, tz_name, tz_date, tz_aclock, tz_clock, current_time in \
            zip(zones, self.tz_names, self.tz_dates, self.tz_aclocks, self.tz_clocks, current_times(clocks)):
            tz_name.setText(zone + ' (UTC ' + utc_offsets[zone] + ')')
            tz_date.setText(current_time.strftime(settings['clock.defaults']['date.format']))
            if clocks[zone] == current_zone:
                tz_clock.setText(current_time.strftime('%H:%M') + f'<span style="font-size: 20px;">:{current_time.strftime('%S')}</span>')
            else:
                tz_clock.setText(current_time.strftime(settings['clock.defaults']['time.format']))
            tz_aclock.draw_clock(current_time)
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

    def align_time(self):
        """This function aligns the application timer and the now() time."""
        sleep(1 - perf_counter() % 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir, settings['window.defaults']['icon_alt'])))
    window = Window()
    window.show()
    sys.exit(app.exec())