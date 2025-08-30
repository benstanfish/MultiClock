"""
Internal configurations and fall-back defaults for MultiClock.
User configuration is intended through the settings.json file.
"""

import json
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

clocks = {
    'Tokyo': 'Asia/Tokyo',
    'UTC': 'UTC',
    'New York': 'US/Eastern',
    'Mountain': 'US/Mountain',
    'Seattle': 'US/Pacific',
    'Hawaii': 'US/Hawaii'
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
        'chime.volume': 100
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
            'horizontal': Qt.AlignmentFlag.AlignRight,
            'vertical': Qt.AlignmentFlag.AlignCenter
        }
    },
    'selected_theme': 'classic',
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
                'background': "transparent"
            }
        },
        'artic': {
            'window.background': "#00064A",
            'zone': {
                'font': 'Consolas',
                'font.size': 10,
                'font.weight': QFont.Weight.Thin,
                'font.color': "#51ceff",
                'background': 'transparent'
            },
            'date': {
                'font': 'Consolas',
                'font.size': 10,
                'font.weight': QFont.Weight.Thin,
                'font.color': "#51ceff",
                'background': 'transparent'
            },
            'clock': {
                'font': 'Consolas',
                'font.size': 28,
                'font.weight': QFont.Weight.Normal,
                'font.color': "#51ceff",
                'border-top': '1px solid #223b3f',
                'background': 'transparent'
            }
        }
    }

}

