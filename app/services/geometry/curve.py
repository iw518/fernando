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

    def get_points(self):
        return self._points

    @property
    def get_lines(self):
        lines = []
        points = self.get_points()
        for i in range(len(points) - 1):
            pt1 = points[i]
            pt2 = points[i + 1]
            lines.append(Line(pt1, pt2))
        return lines

    def x2y(self, x):
        points = []
        for line in self.get_lines:
            pt = line.x2y(x)
            if pt:
                points.append(pt)
        if 0 < len(points) < 3:
            return points[0]
        else:
            return None

    def y2x(self, y):
        # self 注意此处有可能返回多个点
        points = []
        for line in self.get_lines:
            pt = line.y2x(y)
            if pt:
                points.append(pt)
        if 0 < len(points) < 3:
            return points[0]
        else:
            return None

    def intersect(self, line):
        for myline in self.get_lines:
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

    def insert_point(self, index, pt):
        self._points.insert(index, pt)


    def append_line(self, line):
        if len(self._points) == 0:
            self.append_point(line.pt1)
            self.append_point(line.pt2)
        elif line.pt1.x == self._points[-1].x:
            self.append_point(line.pt2)
        elif line.pt2.x == self._points[-1].x:
            self.append_point(line.pt1)
        else:
            self.append_point(line.pt1)
            self.append_point(line.pt2)

    def scale(self, sx=1, sy=1):
        curve = Curve()
        for point in self.get_points():
            curve.append_point(point.scale(sx, sy))
        return curve

    def offset(self, ox=0, oy=0):
        curve = Curve()
        for pt in self.get_points():
            curve.append_point(pt.offset(ox, oy))
        return curve
