"""Vectorized version of analog clock."""

from PyQt6.QtWidgets import (QWidget,
                             QGraphicsScene,
                             QGraphicsView,
                             QGraphicsEllipseItem,
                             QGraphicsLineItem)
from PyQt6.QtGui import QPen, QColor, QPainter
from PyQt6.QtCore import Qt, QRectF, QPointF, QTimer
import math
from datetime import datetime
import config

settings = config.load_settings()
clocks = settings['clock.defaults']['clocks']
theme_name = settings['selected_theme']

size = 125
pad = 5
center = QPointF(size / 2, size / 2)
min_hand = (size - pad * 4) / 2
hour_hand = min_hand * 0.6

class QAClock(QWidget):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet('border: 0px solid transparent;')
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.draw_clock(datetime.now())
        
    def draw_clock(self, draw_time: datetime):

        self.scene.clear()
        bezel_pen = QPen()
        bezel_pen.setWidth(1)
        bezel_pen.setColor(QColor(settings['themes'][theme_name]['clock']['font.color']))

        bound_box = QRectF(pad, pad,
                           size - pad * 2,
                           size - pad * 2)
        bezel = QGraphicsEllipseItem(bound_box)
        bezel.setPen(bezel_pen)
        self.scene.addItem(bezel)

        tick_pen = QPen()
        tick_pen.setWidth(1)
        tick_pen.setColor(QColor('#777'))


        ticks = list(range(12))
        for tick in ticks:
            angle = 360 / 12 * tick
            angle_r = math.radians(angle - 90)
            tick_start = QPointF(center.x() + min_hand * 0.9 * math.cos(angle_r), 
                                 center.y() + min_hand * 0.9 * math.sin(angle_r))
            tick_tip = QPointF(center.x() + min_hand * math.cos(angle_r), 
                               center.y() + min_hand * math.sin(angle_r))
            tick_line = QGraphicsLineItem(tick_start.x(), tick_start.y(),
                                          tick_tip.x(), tick_tip.y())
            tick_line.setPen(tick_pen)
            self.scene.addItem(tick_line)

        sec_pen = QPen()
        sec_pen.setWidth(1)
        sec_pen.setColor(QColor('tomato'))
        
        angle = 360 / 60 * draw_time.second
        angle_r = math.radians(angle - 90)
        sec_tip = QPointF(center.x() + min_hand * 0.95 * math.cos(angle_r), 
                          center.y() + min_hand * 0.95 * math.sin(angle_r))
        sec_line = QGraphicsLineItem(center.x(), center.y(), sec_tip.x(), sec_tip.y())
        sec_line.setPen(sec_pen)
        self.scene.addItem(sec_line)

        min_pen = QPen()
        min_pen.setWidth(2)
        min_pen.setColor(QColor(settings['themes'][theme_name]['clock']['font.color']))
        
        angle = 360 / 60 * draw_time.minute
        angle_r = math.radians(angle - 90)
        min_tip = QPointF(center.x() + min_hand * math.cos(angle_r), 
                          center.y() + min_hand * math.sin(angle_r))

        min_line = QGraphicsLineItem(center.x(), center.y(), min_tip.x(), min_tip.y())
        min_line.setPen(min_pen)
        self.scene.addItem(min_line)

        hour_pen = QPen()
        hour_pen.setWidth(4)
        hour_pen.setColor(QColor(settings['themes'][theme_name]['clock']['font.color']))

        angle = 360 / 12 * (draw_time.hour + draw_time.minute / 60)
        angle_r = math.radians(angle - 90)
        hour_tip = QPointF(center.x() + hour_hand * math.cos(angle_r), 
                           center.y() + hour_hand * math.sin(angle_r))
        
        hour_line = QGraphicsLineItem(center.x(), center.y(), hour_tip.x(), hour_tip.y())
        hour_line.setPen(hour_pen)
        self.scene.addItem(hour_line)

        self.view.setScene(self.scene)
