import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from math import *


class Point:
    def __init__(self, x=0, y=0):
        if type(x) == str:
            self.x, self.y = map(int, x.split())
        else:
            self.x = x
            self.y = y

    def __str__(self):
        return str(self.x) + ' ' + str(self.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, n):
        return Point(self.x * n, self.y * n)

    def __rmul__(self, n):
        return Point(n * self.x, n * self.y)

    def __truediv__(self, a):
        return Point(self.x / a, self.y / a)

    def dist(self, other):
        return ((abs(self.x - other.x)) ** 2 + (abs(self.y - other.y)) ** 2) ** 0.5


X = 500
Y = 300


class MyWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.resize(X, Y)
        self.__num = 0
        self.__cur = 'The Koch curve'
        self.__cen = Point()
        self.__k = 1

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        if self.__cur == 'The Koch curve':
            if self.__num == 0:
                self.plot_koch(Point(0, self.size().height() / 2), Point(self.size().width(), self.size().height() / 2), self.__num, painter)
            else:
                r = min(self.size().width() / 3, self.size().height() * 2 / 3 ** 0.5) - 3
                self.plot_koch(Point(self.size().width() / 2 - 1.5 * r, self.size().height() / 2 + r * 3 ** 0.5 / 4), Point(self.size().width() / 2 + 1.5 * r, self.size().height() / 2 + r * 3 ** 0.5 / 4), self.__num, painter)
        elif self.__cur == 'Cross':
            if self.__num == 0:
                self.plot_koch(Point(0, self.size().height() / 2), Point(self.size().width(), self.size().height() / 2), self.__num, painter)
            else:
                r = min(self.size().width() / 2, self.size().height()) - 3
                self.plot_cross(Point(self.size().width() / 2 - r, self.size().height() / 2 + r / 2), Point(self.size().width() / 2 + r, self.size().height() / 2 + r / 2), self.__num, painter)
        elif self.__cur == 'Sierpinskis triangular carpet':
            r = min(self.size().width(), self.size().height() * 2 / 3 ** 0.5) - 3
            self.triangle_sierpinski_carpet(Point(self.size().width() / 2 - 0.5 * r, self.size().height() / 2 + r * 3 ** 0.5 / 4), Point(self.size().width() / 2 + 0.5 * r, self.size().height() / 2 + r * 3 ** 0.5 / 4), self.__num, painter)
        elif self.__cur == 'The Minkovski curve':
            if self.__num == 0:
                self.plot_koch(Point(0, self.size().height() / 2), Point(self.size().width(), self.size().height() / 2), self.__num, painter)
            else:
                r = min(self.size().width() / 2, self.size().height() / 2) - 3
                self.plot_minkovski(Point(self.size().width() / 2 - r, self.size().height() / 2), Point(self.size().width() / 2 + r, self.size().height() / 2), self.__num, painter)
        painter.end()

    def plot_koch(self, a, b, n, painter):
        self.__cen = (a + b) / 2
        if n == 0:
            painter.drawLine((self.__cen - (self.__cen - a) * self.__k).x, (self.__cen - (self.__cen - a) * self.__k).y, (self.__cen + (b - self.__cen) * self.__k).x, (self.__cen + (b - self.__cen) * self.__k).y)
        else:
            k = a + (b - a) / 3
            m = k + (b - a) / 3
            l = k + Point(cos(-pi / 3) * (m - k).x - sin(-pi / 3) * (m - k).y, sin(-pi / 3) * (m - k).x + cos(-pi / 3) * (m - k).y)
            self.plot_koch(a, k, n - 1, painter)
            self.plot_koch(k, l, n - 1, painter)
            self.plot_koch(l, m, n - 1, painter)
            self.plot_koch(m, b, n - 1, painter)

    def plot_cross(self, a, b, n, painter):
        if n == 0:
            painter.drawLine(a.x, a.y, b.x, b.y)
        else:
            c = a + (b - a) / 3
            f = c + (b - a) / 3
            d = c + Point((f - c).y, -(f - c).x)
            e = d + Point(-(d - c).y, (d - c).x)
            self.plot_cross(a, c, n - 1, painter)
            self.plot_cross(c, d, n - 1, painter)
            self.plot_cross(d, e, n - 1, painter)
            self.plot_cross(e, f, n - 1, painter)
            self.plot_cross(f, b, n - 1, painter)

    def triangle_sierpinski_carpet(self, a, b, n, painter):
        if n == 0:
            c = a + Point(cos(-pi / 3) * (b - a).x - sin(-pi / 3) * (b - a).y, sin(-pi / 3) * (b - a).x + cos(-pi / 3) * (b - a).y)
            painter.drawLine(a.x, a.y, c.x, c.y)
            painter.drawLine(a.x, a.y, b.x, b.y)
            painter.drawLine(c.x, c.y, b.x, b.y)
        else:
            c = a + Point(cos(-pi / 3) * (b - a).x - sin(-pi / 3) * (b - a).y, sin(-pi / 3) * (b - a).x + cos(-pi / 3) * (b - a).y)
            d = (b + a) / 2
            e = (c + a) / 2
            f = (c + b) / 2
            self.triangle_sierpinski_carpet(a, d, n - 1, painter)
            self.triangle_sierpinski_carpet(d, b, n - 1, painter)
            self.triangle_sierpinski_carpet(e, f, n - 1, painter)

    def plot_minkovski(self, a, b, n, painter):
        if n == 0:
            painter.drawLine(a.x, a.y, b.x, b.y)
        else:
            c = a + (b - a) / 4
            h = a + (b - a) * 3 / 4
            m = a + (b - a) / 2
            d = c + Point((m - c).y, -(m - c).x)
            e = d + Point(-(d - c).y, (d - c).x)
            i = d + 2 * Point(-(d - c).y, (d - c).x)
            f = e + Point(-(i - d).y, (i - d).x)
            j = e + 1.5 * Point(-(i - d).y, (i - d).x)
            g = f + Point((j - f).y, -(j - f).x)
            self.plot_minkovski(a, c, n - 1, painter)
            self.plot_minkovski(c, d, n - 1, painter)
            self.plot_minkovski(d, e, n - 1, painter)
            self.plot_minkovski(e, m, n - 1, painter)
            self.plot_minkovski(m, f, n - 1, painter)
            self.plot_minkovski(f, g, n - 1, painter)
            self.plot_minkovski(g, h, n - 1, painter)
            self.plot_minkovski(h, b, n - 1, painter)

    def setValue(self, val):
        self.__num = val
        self.repaint()

    def setText(self, cur):
        self.__cur = cur
        self.repaint()

    def wheelEvent(self, event):
        self.__k *= event.angleDelta().y() / 7 / 8
        self.repaint()

app = QApplication(sys.argv)

Window = QWidget()
Widget = MyWidget(Window)
SpinBox = QSpinBox(Window)
Combobox = QComboBox(Window)
SpinBox.setRange(0, 7)
Window.setWindowTitle("Painter demo")
Window.resize(X, Y)
layout = QVBoxLayout()
layout.addWidget(Combobox, 0)
layout.addWidget(SpinBox, 1)
layout.addWidget(Widget, 2)
Combobox.addItem('The Koch curve')
Combobox.addItem('Cross')
Combobox.addItem('Sierpinskis triangular carpet')
Combobox.addItem('The Minkovski curve')
Combobox.currentTextChanged.connect(Widget.setText)
SpinBox.valueChanged.connect(Widget.setValue)
Window.setLayout(layout)
Window.show()
app.exec_()