# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        GLayer
# Purpose:
#
# Author:      Robot of Fernando
#
# Created:     17-06-2015
# Copyright:   (c) Administrator 2015
# Licence:     <GPLV3>
# -------------------------------------------------------------------------------
import math

from app.services.base.func import AcPoint
from .hole import Hole
from app.services.geometry.line import Line


class Paper:
    # unit mm
    marginX = 10 / 1000
    marginY = 15 / 1000

    def __init__(self, section, name='A3', width=420, height=297, orientation='H'):
        self.section = section
        self.name = name
        self.width = width / 1000
        self.height = height / 1000
        if orientation.capitalize() == 'V':
            self.width = height / 1000
            self.height = width / 1000
        self.orientation = orientation

    @property
    def lt(self):
        # unit m
        left = self.section.dss[0]
        top = max([hole.elevation for hole, accumulate_distance in self.section._items])
        return AcPoint(left, top)

    @property
    def rb(self):
        # unit m
        right = self.section.dss[-1]
        bottom = min([hole.elevation - hole.Dep for hole, accumulate_distance in self.section._items])
        return AcPoint(right, bottom)

    @property
    def scale(self):
        sect_width = self.rb.x - self.lt.y
        scale = sect_width / (self.width - self.marginX * 2)
        x = math.ceil(scale / 100) * 100

        sect_height = self.lt.y - self.rb.y
        scale = sect_height / (self.height - self.marginY * 2)
        y = math.ceil(scale / 100) * 100
        return AcPoint(x, y)

    @property
    def offset(self):
        # unit m
        sect_width = self.rb.x - self.lt.y
        sect_height = self.lt.y - self.rb.y
        x = self.width / 2 - sect_width / self.scale.x / 2
        y = self.lt.y / self.scale.y + (self.height / 2 - sect_height / self.scale.y / 2)
        return AcPoint(x, y)


class Section:
    def __init__(self, name=''):
        self.name = name
        self._items = []
        self._hlines = []
        self._paper = Paper(self)

    @property
    def items(self):
        return self._items

    @property
    def holes(self):
        return [hole for hole, accumulate_distance in self._items]

    @property
    def dss(self):
        return [accumulate_distance for hole, accumulate_distance in self._items]

    @property
    def bottom(self):
        # unit m
        bottom = min([hole.elevation - hole.Dep for hole, accumulate_distance in self._items])
        return bottom

    @property
    def top(self):
        # unit m
        top = max([hole.elevation for hole, accumulate_distance in self._items])
        return top

    def to_json(self):
        mydict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
                mydict[key] = value
            elif isinstance(value, list):
                items = []
                for item in value:
                    if isinstance(item[0], Hole):
                        items.append({"hole": item[0].to_json(), "accumulate_distance": item[1]})
                mydict['items'] = items
        return mydict

    @property
    def hLines(self):
        self._hlines = []
        for (hole, accumulate_distance) in self.items:
            top = AcPoint()
            bottom = AcPoint()
            top.x = accumulate_distance
            top.y = hole.elevation
            bottom.x = accumulate_distance
            bottom.y = top.y - hole.Dep
            hLine = (top, bottom)
            self._hlines.append(hLine)
        return self._hlines

    def set_paper(self, name='A3', width=420, height=297, orientation='H'):
        self._paper = Paper(self, name, width, height, orientation)
        return self._paper

    def draw_sectionLine(self, layers):
        HNUM = len(self.holes)
        LCOUNT = max(len(hole.layers) for hole in self.holes)
        layers = layers[0:LCOUNT]
        extra_dist = 0.015 * self._paper.scale.x

        # 第一部分：画地形线，即0层的层顶线
        hole_index = 0
        layer = layers[0]
        while hole_index <= HNUM - 1:
            # 1-1定义A孔
            aHole = self.holes[hole_index]
            ax = self.dss[hole_index]
            al = aHole.layers[0]
            pt = AcPoint(ax, aHole.elevation)
            if hole_index == 0:
                layer.top_curve.append_point(pt.offset_x(- extra_dist))
            # 1-2添加A点
            layer.top_curve.append_point(pt)
            if hole_index == HNUM - 1:
                layer.top_curve.append_point(pt.offset_x(extra_dist))
                break
            hole_index = hole_index + 1

            # 1-3：对局部缺失情况进行添加特征点处理
            bHole = self.holes[hole_index]
            bl = bHole.layers[0]
            bx = self.dss[hole_index]
            if al.thickness > 0 and bl.thickness == 0:
                x = (ax + 2 * bx) / 3
                y = aHole.elevation
                pt = AcPoint(x, y)
                layer.top_curve.append_point(pt)
            if al.thickness == 0 and bl.thickness > 0:
                x = (2 * ax + bx) / 3
                y = bHole.elevation
                pt = AcPoint(x, y)
                layer.top_curve.append_point(pt)

        # 第二部分：画各层的层底线
        for layer_index in range(LCOUNT - 1):
            # 初始化
            hole_index = 0
            layer = layers[layer_index]
            # 将上层层底信息传递至下层层顶
            if layer_index >= 1:
                layer.top_curve = layers[layer_index - 1].bottom_curve
            while hole_index <= HNUM - 1:
                # 2-1定义A孔
                aHole = self.holes[hole_index]
                ax = self.dss[hole_index]
                # (1)若A孔已到层底，直接跳到下一次循环，此处未考虑A孔与右侧孔存在层位相交错情况，日后可优化！！！
                if layer_index >= len(aHole.layers) - 1:
                    hole_index = hole_index + 1
                    continue
                # (2)若A孔未到层底,：画A孔层底线
                aLayer = aHole.layers[layer_index]
                ay = aHole.elevation - aLayer.endDep
                ptA = AcPoint(ax, ay)
                # 处理当前层层底左延伸线
                if hole_index == 0:
                    layer.bottom_curve.append_point(ptA.offset_x(-extra_dist))
                layer.bottom_curve.append_point(ptA)
                if hole_index == HNUM - 1:
                    layer.bottom_curve.append_point(ptA.offset_x(extra_dist))
                    break

                hole_index = hole_index + 1
                while hole_index <= HNUM - 1:
                    bHole = self.holes[hole_index]
                    bx = self.dss[hole_index]
                    # 判断当前B孔是否已到层底，若未到层底，连线，否则自增长
                    if layer_index >= len(bHole.layers) - 1:
                        hole_index = hole_index + 1
                        # 增加类似美化功能，例如K043-2015-4中的D剖面
                        continue
                    else:
                        bl = bHole.layers[layer_index]
                        by = bHole.elevation - bl.endDep
                        ptB = AcPoint(bx, by)
                        if aLayer.thickness > 0 and bl.thickness == 0:
                            virtual_line = Line(ptA, AcPoint(bx, ay))
                            pt = layer.top_curve.intersect(virtual_line)
                            if not pt:
                                x = (ax + 2 * bx) / 3
                                pt = layer.top_curve.x2y(x)
                            layer.bottom_curve.append_point(pt)
                            layer.bottom_curve.concat(layer.top_curve.slice(pt, ptB))
                        if aLayer.thickness == 0 and bl.thickness > 0:
                            virtual_line = Line(AcPoint(ax, by), ptB)
                            pt = layer.top_curve.intersect(virtual_line)
                            if not pt:
                                x = (2 * ax + bx) / 3
                                pt = layer.top_curve.x2y(x)
                            layer.bottom_curve.append_point(pt)
                            layer.bottom_curve.concat(layer.top_curve.slice(ptA, pt))
                        if aLayer.thickness == 0 and bl.thickness == 0:
                            layer.bottom_curve.concat(layer.top_curve.slice(ptA, ptB))
                        break
        return layers
