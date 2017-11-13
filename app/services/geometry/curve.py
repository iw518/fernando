#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      curve
# date:         2017-10-31
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------
from .line import Line


class Curve:
    # 注意line和 point必须互动，否则增改删可能不会同时反映到另一个身上
    def __init__(self):
        self._points = []
        self._lines = []

    def get_lines(self):
        return self._lines

    def get_points(self):
        return self._points

    def x2y(self, x):
        points = []
        for line in self._lines:
            pt = line.x2y(x)
            if pt:
                points.append(pt)
        if len(points) >= 1:
            return points[0]
        else:
            return None

    def y2x(self, y):
        # self 注意此处有可能返回多个点
        points = []
        for line in self._lines:
            pt = line.y2x(y)
            if pt:
                points.append(pt)
        if len(points) >= 1:
            return points[0]
        else:
            return None

    def intersect(self, line):
        for myline in self._lines:
            pt = myline.intersect(line)
            if pt:
                return pt

    def slice(self, pt1, pt2):
        curve = Curve()
        for pt in self._points:
            if (pt.x - pt1.x) * (pt.x - pt2.x) < 0:
                curve.append_point(pt)
        return curve

    def concat(self, curve):
        for point in curve.get_points():
            self.append_point(point)

    def append_point(self, pt):
        self._points.append(pt)
        if len(self._points) > 1:
            pt1 = self._points[-2]
            pt2 = self._points[-1]
            line = Line(pt1, pt2)
            self._lines.append(line)

    def append_line(self, line):
        if len(self._points) == 0:
            self._points.append(line.pt1)
            self._points.append(line.pt2)
        elif line.pt1.x == self._points[-1].x:
            self._points.append(line.pt2)
        elif line.pt2.x == self._points[-1].x:
            self._points.append(line.pt1)
        else:
            self._points.append(line.pt1)
            self._points.append(line.pt2)
