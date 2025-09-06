from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMainWindow
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QRectF, QPointF, QTimer
import sys, math
from datetime import datetime, timedelta
import config

settings = config.load_settings()
clocks = settings['clock.defaults']['clocks']
theme_name = settings['selected_theme']

size = 150
pad = 5
center = QPointF(size / 2, size / 2)
min_hand = (size - pad * 4) / 2
hour_hand = min_hand * 0.6

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        canvas = QPixmap(size, size)
        canvas.fill(Qt.GlobalColor.transparent)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw_clock(datetime.now())

        timer = QTimer(self)
        timer.timeout.connect(lambda: self.draw_clock(datetime.now()))
        timer.start(1000)

    def draw_clock(self, draw_time: datetime):
        canvas = self.label.pixmap()
        canvas.fill(Qt.GlobalColor.transparent)
        painter = QPainter(canvas)
        bezel_pen = QPen()
        bezel_pen.setWidth(1)
        bezel_pen.setColor(QColor(settings['themes'][theme_name]['clock']['font.color']))

        painter.setPen(bezel_pen)

        bound_box = QRectF(pad, pad,
                           size - pad * 2,
                           size - pad * 2)
        painter.drawEllipse(bound_box)

        tick_pen = QPen()
        tick_pen.setWidth(2)
        tick_pen.setColor(QColor('#777'))
        painter.setPen(tick_pen)

        ticks = list(range(12))
        for tick in ticks:
            angle = 360 / 12 * tick
            angle_r = math.radians(angle - 90)
            tick_start = QPointF(center.x() + min_hand * 0.9 * math.cos(angle_r), 
                                 center.y() + min_hand * 0.9 * math.sin(angle_r))
            tick_tip = QPointF(center.x() + min_hand * math.cos(angle_r), 
                               center.y() + min_hand * math.sin(angle_r))
            painter.drawLine(tick_start, tick_tip)

        sec_pen = QPen()
        sec_pen.setWidth(1)
        sec_pen.setColor(QColor('tomato'))
        painter.setPen(sec_pen)
        
        angle = 360 / 60 * draw_time.second
        angle_r = math.radians(angle - 90)
        sec_tip = QPointF(center.x() + min_hand * 0.95 * math.cos(angle_r), 
                          center.y() + min_hand * 0.95 * math.sin(angle_r))

        painter.drawLine(center, sec_tip)

        min_pen = QPen()
        min_pen.setWidth(2)
        min_pen.setColor(QColor(settings['themes'][theme_name]['clock']['font.color']))
        painter.setPen(min_pen)
        
        angle = 360 / 60 * draw_time.minute
        angle_r = math.radians(angle - 90)
        min_tip = QPointF(center.x() + min_hand * math.cos(angle_r), 
                          center.y() + min_hand * math.sin(angle_r))

        painter.drawLine(center, min_tip)

        hour_pen = QPen()
        hour_pen.setWidth(4)
        hour_pen.setColor(QColor(settings['themes'][theme_name]['clock']['font.color']))
        painter.setPen(hour_pen)

        angle = 360 / 12 * (draw_time.hour + draw_time.minute / 60)
        angle_r = math.radians(angle - 90)
        hour_tip = QPointF(center.x() + hour_hand * math.cos(angle_r), 
                           center.y() + hour_hand * math.sin(angle_r))
        
        painter.drawLine(center, hour_tip)

        painter.end()
        self.label.setPixmap(canvas)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())