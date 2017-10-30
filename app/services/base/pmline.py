#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      pmline
# date:         2017-10-08
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------


class Pmline:
    def __init__(self, *args):
        self.points = []
        for arg in args:
            self.points.append(arg)

    @property
    def line_func(self):
        def func(x):
            num = len(self.points)
            for n in range(num - 1):
                if self.points[n].x <= x <= self.points[n + 1].x:
                    k = (self.points[n + 1].y - self.points[n].y) / (self.points[n + 1].x - self.points[n].x)
                    return (x - self.points[n].x) * k + self.points[n].y

        return func

    @property
    def reverse_line_func(self):
        def func(y):
            num = len(self.points)
            for n in range(num - 1):
                if (y - self.points[n].y) * (y - self.points[n + 1].y) < 0:
                    k = (self.points[n + 1].y - self.points[n].y) / (self.points[n + 1].x - self.points[n].x)
                    return (y - self.points[n].y) / k + self.points[n].x
                elif y == self.points[n].y:
                    return self.points[n].x

        return func
