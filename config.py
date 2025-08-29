"""
Internal configurations and fall-back defaults for MultiClock.
User configuration is intended through the settings.json file.
"""

import json
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

clocks = {
    'Tokyo': 'Asia/Tokyo',
    'New York': 'US/Eastern',
    'Denver': 'US/Mountain',
    'Seattle': 'US/Pacific',
    'Honolulu': 'US/Hawaii'
}

defaults = {
    'window.defaults': {
        'title': 'MultiClock',
        'icon': 'icon.ico',
        'background': '#222',
        'opacity': 0.95,
        'timer': 1000
    },
    'clock.defaults': {
        'clocks': clocks,
        'date.format': '%a, %d %B %Y',
        'time.format': '%H:%M:%S',
        'chime': 'jihou-sine-3f.mp3',
        'chime.offset': -4,
        'chime.volume': 50
    },
    'clock.align': {
        'zone': {
            'horizontal': Qt.AlignmentFlag.AlignLeft,
            'vertical': Qt.AlignmentFlag.AlignBottom
        },
        'date': {
            'horizontal': Qt.AlignmentFlag.AlignRight,
            'vertical': Qt.AlignmentFlag.AlignBottom
        },
        'clock': {
            'horizontal': Qt.AlignmentFlag.AlignHCenter,
            'vertical': Qt.AlignmentFlag.AlignTop
        }
    },
    'themes': {
        'classic': {
            'window.background': '#031417',
            'zone': {
                'font': 'Consolas',
                'font.size': 10,
                'font.weight': QFont.Weight.Thin,
                'font.color': '#49e9a6',
                'background': 'transparent'
            },
            'date': {
                'font': 'Consolas',
                'font.size': 10,
                'font.weight': QFont.Weight.Thin,
                'font.color': '#49e9a6',
                'background': 'transparent'
            },
            'clock': {
                'font': 'Consolas',
                'font.size': 28,
                'font.weight': QFont.Weight.Normal,
                'font.color': '#49e9a6',
                'border-top': '1px solid #223b3f',
                'background': 'transparent'
            }
        }
    }

}

