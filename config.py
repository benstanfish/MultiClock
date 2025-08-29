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
        'geometry': (200, 200, 325, 1),
        'background': '#333',
        'opacity': 1,
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
    'clock.themes': {
        'plain': {
            'zone': {
                'font': 'Aptos Narrow',
                'font.size': 11,
                'font.weight': QFont.Weight.Normal,
                'font.color': "#ffffff",
                'background': 'transparent'
            },
            'date': {
                'font': 'Aptos Narrow',
                'font.size': 11,
                'font.weight': QFont.Weight.Normal,
                'font.color': "#ffffff",
                'background': 'transparent'
            },
            'clock': {
                'font': 'Aptos',
                'font.size': 36,
                'font.weight': QFont.Weight.Normal,
                'font.color': "#ffffff",
                'border-top': '1px solid #555',
                'background': 'transparent'
            }
        }
    }

}

