#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      point
# date:         2017-11-14
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------


class Point:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.style = {"belongHole": True, "type": "normal", "bottom": False}

    def attr(self, key, value=None):
        if value is None:
            return self.style.get(key)
        self.style[key] = value
        return self.style

    def offset(self, ox=0, oy=0, oz=0):
        return Point(self.x + ox, self.y + oy, self.z + oz)

    def scale(self, sx=1, sy=1, sz=1):
        return Point(self.x * sx, self.y * sy, self.z * sz)

    def __str__(self):
        return "%.4f,%.4f" % (self.x, self.y)

    __repr__ = __str__
