#!/usr/bin/python3
import sys
from typing import List, Tuple
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QPen, QColor, QBrush, QPolygonF, QPainter, QImage, QPalette
from PyQt5.QtCore import QPointF, pyqtSlot, QSize, QRectF

OBSTACLE_COLOR = (66, 134, 244)
BACKGROUND_COLOR = (25, 25, 25)
LINE = 0
POLYGON = 1
KEY_LINE = 76       # L
KEY_POLYGON = 80    # P

from polygon import Polygon
from point import Point


class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = "PolyTest"
        self.table_left = 0
        self.table_top = 0
        self.table_width = 1200
        self.table_height = 800
        self.polys = []             #type: List[Polygon]
        self.tmpPoly = None         #type: Polygon
        self.lines = []             #type: List[Tuple[Point]]
        self.line = None
        self.ptList = []            #type: List[Point]
        self.mode = POLYGON
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.table_left, self.table_top, self.table_width, self.table_height)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(*BACKGROUND_COLOR))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        self.pen = QPen(QColor(255,0,0))
        self.pen.setWidth(1)
        self.brush = QBrush(QColor(0,0,0))
        self.show()

    def paintEvent(self, event):
        self.table_width = min(self.geometry().width(), self.geometry().height() * 3/2)
        # The table will keep the 3/2 ratio whatever the window ratio
        self.table_height = min(self.geometry().height(), self.geometry().width() * 2/3)
        painter = QPainter(self)
        self.paint_background(painter, 0, 0, self.table_width - 1, self.table_height - 1)
        
        painter.setPen(QPen(QColor(255,0,0)))
        painter.drawLine(0, 0, 0, self.table_height-1)
        painter.drawLine(0, self.table_height-1, self.table_width-1, self.table_height-1)
        painter.drawLine(self.table_width-1, self.table_height-1, self.table_width-1, 0)
        painter.drawLine(self.table_width-1, 0,0, 0)
        
        painter.setPen(QPen(QColor(*OBSTACLE_COLOR)))
        painter.setBrush(QBrush(QColor(*OBSTACLE_COLOR)))

        if self.tmpPoly is not None:
            self.polys.append(self.tmpPoly)
        for poly in self.polys:
            qpo = self.convert_polygon(poly)
            painter.drawPolygon(qpo)
        if self.tmpPoly is not None:
            self.polys.remove(self.tmpPoly)
        painter.setPen(QPen(QColor(255,0,0)))
        for line in self.lines:
            painter.drawLine(line[0].x, line[0].y, line[1].x, line[1].y)
        if self.line is not None :
            painter.drawLine(self.line[0].x, self.line[0].y, self.line[1].x, self.line[1].y)
    
    def mousePressEvent(self, mouseEvent):
        mouseEvent.accept()
        x=mouseEvent.pos().x()
        y=mouseEvent.pos().y()

        self.ptList.append(Point(x,y))
        if self.mode == LINE and len(self.ptList) == 2:
            #self.lines.append(tuple(self.ptList))
            self.line = tuple(self.ptList)
            self.testLine(self.ptList)
            self.ptList = []

        if self.mode == POLYGON and len(self.ptList) > 2:
            if mouseEvent.button() == 2:
                self.polys.append(Polygon(self.ptList))
                self.ptList = []
            else:
                self.tmpPoly = Polygon(self.ptList)
        self.update()
    
    def keyPressEvent(self, keyEvent):
        if keyEvent.key() == KEY_LINE:
            self.mode = LINE
        elif keyEvent.key() == KEY_POLYGON:
            self.mode = POLYGON
        self.ptList = []


    @pyqtSlot()
    def on_quit(self):
        pass

    def paint_background(self, painter, x_offset, y_offset, width, height):
        pass
     
    def convert_polygon(self, poly):
        pol = QPolygonF()
        for p in poly.vertices:
            pol.append(QPointF(p.x, p.y))
        return pol
    
    def testLine(self, ptlist):
        count = 0
        for poly in self.polys:
            ret = poly.intersect(ptlist[0], ptlist[1])
            print(ret)
            if ret:
                print("plop")
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.aboutToQuit.connect(ex.on_quit)
    sys.exit(app.exec_())
