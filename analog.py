from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMainWindow
from PyQt6.QtGui import QPixmap, QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        canvas = QPixmap(201, 201)
        canvas.fill(Qt.GlobalColor.transparent)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw_something()

    def draw_something(self):
        canvas = self.label.pixmap()
        
        painter = QPainter(canvas)
        pen = QPen()
        pen.setWidth(1)
        pen.setColor(QColor(0,255,255))

        
        painter.setPen(pen)
        painter.drawEllipse(1, 1, 198, 198)

        
        min_pen = QPen()
        min_pen.setWidth(2)
        min_pen.setColor(QColor(255,0,0))
        painter.setPen(min_pen)
        
        painter.drawLine(100, 100, 0, 0)
        
        painter.end()
        self.label.setPixmap(canvas)







if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())