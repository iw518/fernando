#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      line_func
# date:         2017-10-31
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------
from app.services.base.func import AcPoint, iszero


class Line:
    def __init__(self, pt1, pt2):
        self.pt1 = pt1
        self.pt2 = pt2
        self.A = 0
        self.B = 0
        self.C = 0
        self.f = self.func()

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

    def isexsit(self, pt):
        x = pt.x
        y = pt.y
        x1 = self.pt1.x
        y1 = self.pt1.y
        x2 = self.pt2.x
        y2 = self.pt2.y
        f = self.f(pt)
        if (x - x1) * (x - x2) <= 0 and (y - y1) * (y - y2) <= 0 and iszero(f):
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
            pt = AcPoint(x, y)
            if self.isexsit(pt) and line.isexsit(pt):
                return AcPoint(x, y)
            else:
                return None


M = [AcPoint(-32697.1588, -39666.0098),
     AcPoint(-29394.9287, -40395.1101),
     AcPoint(-30092.4929, -42249.8391),
     AcPoint(-33170.7344, -42217.8610),
     AcPoint(-34431.4695, -40740.4734), AcPoint(-32697.1588, -39666.0098)]
line = Line(AcPoint(-34437.8692, -42160.3004), AcPoint(-29465.3251, -39512.5149))

for i in range(len(M) - 1):
    line1 = Line(M[i], M[i + 1])
    a = line.intersect(line1)
    if a:
        print("x={},y={}".format(a.x, a.y))