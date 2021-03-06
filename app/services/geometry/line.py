#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      line
# date:         2017-10-31
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------
from app.services.base.func import iszero
from app.services.geometry.point import Point


class Line:
    def __init__(self, pt1, pt2):
        self.pt1 = pt1
        self.pt2 = pt2
        self.A = 0
        self.B = 0
        self.C = 0
        self.f = self.func()
        self.style = {}

    @property
    def attr(self, key):
        return self.style.get(key, None)

    @attr.setter
    def attr(self, key, value):
        self.style[key] = value


    def func(self):
        x1 = self.pt1.x
        y1 = self.pt1.y
        x2 = self.pt2.x
        y2 = self.pt2.y
        if x1 * y2 - x2 * y1 == 0:
            self.A = y1 - y2
            self.B = -(x1 - x2)
            self.C = 0
        else:
            self.A = (y1 - y2) / (x1 * y2 - x2 * y1)
            self.B = -(x1 - x2) / (x1 * y2 - x2 * y1)
            self.C = 1
        def wrapper(pt):
            return self.A * pt.x + self.B * pt.y + self.C
        return wrapper

    def x2y(self, x):
        if not iszero(self.B):
            y = -self.f(Point(x, 0)) / self.B
            pt = Point(x, y)
            if self.isexsit(pt):
                return pt
            else:
                return None
        return None

    def y2x(self, y):
        if not iszero(self.A):
            x = -self.f(Point(0, y)) / self.A
            pt = Point(x, y)
            if self.isexsit(pt):
                return pt
            else:
                return None
        return None

    def isexsit(self, pt):
        x = pt.x
        y = pt.y
        x1 = self.pt1.x
        y1 = self.pt1.y
        x2 = self.pt2.x
        y2 = self.pt2.y
        f = self.f(pt)
        if (round(x, 8) - round(x1, 8)) * (round(x, 8) - round(x2, 8)) <= 0 and (round(y, 8) - round(y1, 8)) * (
            round(y, 8) - round(y2, 8)) <= 0 and round(f, 8) == 0:
            return True
        else:
            return False

    def intersect(self, line):
        A1 = self.A
        B1 = self.B
        C1 = self.C
        A2 = line.A
        B2 = line.B
        C2 = line.C
        if A2 * B1 - A1 * B2 == 0:
            return None
        else:
            x = -(B1 * C2 - B2 * C1) / (A2 * B1 - A1 * B2)
            y = (A1 * C2 - A2 * C1) / (A2 * B1 - A1 * B2)
            pt = Point(x, y)
            if self.isexsit(pt) and line.isexsit(pt):
                return Point(x, y)
            else:
                return None

    def offset(self, ox=0, oy=0):
        line = Line(self.pt1.offset(ox, oy), self.pt2.offset(ox, oy))
        line.style = self.style
        return line

    def scale(self, sx=1, sy=1):
        line = Line(self.pt1.scale(sx, sy), self.pt2.scale(sx, sy))
        return line


class SiltLine(Line):
    def __init__(self):
        pass




def test():
    a = [Point(-32697.1588, -39666.0098),
         Point(-29394.9287, -40395.1101),
         Point(-30092.4929, -42249.8391),
         Point(-33170.7344, -42217.8610),
         Point(-34431.4695, -40740.4734), Point(-32697.1588, -39666.0098)]
    b = Line(Point(-34437.8692, -42160.3004), Point(-29465.3251, -39512.5149))

    for i in range(len(a) - 1):
        c = Line(a[i], a[i + 1])
        d = b.intersect(c)
        if a:
            print(d)


test()
