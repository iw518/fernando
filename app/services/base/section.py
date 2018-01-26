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

from app.services.base.hole import Hole
from app.services.geometry.line import Line
from app.services.geometry.point import Point


class Paper:
    # unit mm
    marginX = 20
    marginY = 15

    def __init__(self, section, name='A3', width=420, height=297, orientation='H'):
        self.section = section
        self.name = name
        self.width = width
        self.height = height
        if orientation.capitalize() == 'V':
            self.width = height
            self.height = width
        self.orientation = orientation
        self.sx = 1
        self.sy = 1

    @property
    def lt(self):
        # unit m
        left = self.section.dss[0]
        top = self.section.top
        return Point(left, top)

    @property
    def rb(self):
        # unit m
        right = self.section.dss[-1]
        bottom = self.section.bottom
        return Point(right, bottom)

    @property
    def scale(self):
        sect_width = (self.rb.x - self.lt.x) * 1000
        scale = sect_width / (self.width - self.marginX * 2)
        x = math.ceil(scale / 100) * 100

        sect_height = (self.lt.y - self.rb.y) * 1000
        scale = sect_height / (self.height - self.marginY * 2)
        y = math.ceil(scale / 100) * 100

        self.sx = 1000 / x
        self.sy = 1000 / y

        return Point(x, y)

    @property
    def scale2(self):
        sect_width = (self.rb.x - self.lt.x) * 1000
        scale = sect_width / (self.width - self.marginX * 2)
        x = math.ceil(scale / 100) * 100

        sect_height = (self.lt.y - self.rb.y) * 1000
        scale = sect_height / (self.height - self.marginY * 2)
        y = math.ceil(scale / 100) * 100

        self.sx = 1000 / x
        self.sy = 1000 / y

        return Point(x, y)


    @property
    def offset(self):
        # unit mm
        # 中点坐标重合
        # 剖面原始中心坐标x1,图纸中心坐标x0
        x0 = self.width / 2
        x1 = (self.lt.x + self.rb.x) * self.sx / 2

        # 剖面原始中心y1,图纸中心坐标y0
        y1 = ((-1) * self.lt.y * self.sy + (-1) * self.rb.y * self.sy) / 2
        y0 = self.height / 2

        x = x0 - x1
        y = y0 - y1
        return Point(x, y)


class Section:
    def __init__(self, name=''):
        self.name = name
        self._items = []
        self._hlines = []
        self.paper = Paper(self)
        self.__layers = None
        self.curves = []

    @property
    def layers(self):
        return self.__layers

    @layers.setter
    def layers(self, value):
        self.__layers = value

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

    def set_paper(self, name='A3', width=420, height=297, orientation='H'):
        self.paper = Paper(self, name, width, height, orientation)

    def plot_hole(self):
        lines = []
        for (hole, accumulate_distance) in self.items:
            pt1 = Point(accumulate_distance, hole.elevation)
            pt2 = pt1.offset(0, - hole.Dep)
            lines.append(Line(pt1, pt2).scale(self.paper.sx, self.paper.sy))
        return lines

    def plot_scale(self):
        lines = []
        start_num = math.ceil(self.top)
        self.paper.sy / 100
        for (hole, accumulate_distance) in self.items:
            pt1 = Point(accumulate_distance, hole.elevation)
            pt2 = pt1.offset(0, - hole.Dep)
            lines.append(Line(pt1, pt2).scale(self.paper.sx, self.paper.sy))
        return lines

    def __draw_sectionLine(self):
        HNUM = len(self.holes)
        LCOUNT = len(self.layers)

        # 第一部分：画地形线，即0层的层顶线
        hole_index = 0
        layer = self.layers[0]
        while hole_index <= HNUM - 1:
            # 1-1定义A孔
            aHole = self.holes[hole_index]
            ax = self.dss[hole_index]
            al = aHole.layers[0]
            pt = Point(ax, aHole.elevation)
            # 1-2添加A点
            layer.top_curve.append_point(pt)
            if hole_index == HNUM - 1:
                break
            hole_index = hole_index + 1

            # 1-3：对局部缺失情况进行添加特征点处理
            bHole = self.holes[hole_index]
            bl = bHole.layers[0]
            bx = self.dss[hole_index]
            if al.thickness > 0 and bl.thickness == 0:
                x = (ax + 2 * bx) / 3
                y = aHole.elevation
                pt = Point(x, y)
                layer.top_curve.append_point(pt)
            if al.thickness == 0 and bl.thickness > 0:
                x = (2 * ax + bx) / 3
                y = bHole.elevation
                pt = Point(x, y)
                layer.top_curve.append_point(pt)

        # 第二部分：画各层的层底线
        for layer_index in range(LCOUNT):
            # 初始化
            hole_index = 0
            layer = self.layers[layer_index]
            # 将上层层底信息传递至下层层顶
            if layer_index >= 1:
                layer.top_curve = self.layers[layer_index - 1].bottom_curve
            while hole_index <= HNUM - 1:
                # 2-1定义A孔
                aHole = self.holes[hole_index]
                ax = self.dss[hole_index]
                # (1)若A孔已到层底，直接跳到下一次循环，此处未考虑A孔与右侧孔存在层位相交错情况，日后可优化！！！

                if layer_index > len(aHole.layers) - 1:
                    hole_index = hole_index + 1
                    continue
                # (2)若A孔未到层底,：画A孔层底线
                aLayer = aHole.layers[layer_index]
                ay = aHole.elevation - aLayer.endDep
                ptA = Point(ax, ay)
                if layer_index == len(aHole.layers) - 1:
                    ptA.attr("bottom", True)
                    print(ptA.attr("bottom"))
                layer.bottom_curve.append_point(ptA)
                if hole_index == HNUM - 1:
                    break

                hole_index = hole_index + 1
                while hole_index <= HNUM - 1:
                    bHole = self.holes[hole_index]
                    bx = self.dss[hole_index]
                    # 判断当前B孔是否已到层底，若未到层底，连线，否则自增长
                    if layer_index > len(bHole.layers) - 1:
                        hole_index = hole_index + 1
                        # 增加类似美化功能，例如K043-2015-4中的D剖面
                        continue
                    else:
                        bl = bHole.layers[layer_index]
                        by = bHole.elevation - bl.endDep
                        ptB = Point(bx, by)
                        if aLayer.thickness > 0 and bl.thickness == 0:
                            virtual_line = Line(ptA, Point(bx, ay))
                            pt = layer.top_curve.intersect(virtual_line)
                            if not pt:
                                x = (ax + 2 * bx) / 3
                                pt = layer.top_curve.x2y(x)
                            layer.bottom_curve.append_point(pt)
                            layer.bottom_curve.concat(layer.top_curve.slice(pt, ptB))
                        if aLayer.thickness == 0 and bl.thickness > 0:
                            virtual_line = Line(Point(ax, by), ptB)
                            pt = layer.top_curve.intersect(virtual_line)
                            if not pt:
                                x = (2 * ax + bx) / 3
                                pt = layer.top_curve.x2y(x)
                            layer.bottom_curve.append_point(pt)
                            layer.bottom_curve.concat(layer.top_curve.slice(ptA, pt))
                        if aLayer.thickness == 0 and bl.thickness == 0:
                            layer.bottom_curve.concat(layer.top_curve.slice(ptA, ptB))
                        break

    def stroke(self):
        DELTA = 15
        self.__draw_sectionLine()
        sx = 1000 / self.paper.scale.x
        sy = 1000 / self.paper.scale.y
        self.curves = []
        for layer in self.layers:
            # 按照比例尺缩放到纸质图中，单位mm
            curve = layer.top_curve.scale(sx, sy)
            # 插入左右延长线
            pt1 = curve.get_points()[0]
            pt2 = curve.get_points()[-1]
            if pt1.attr('bottom'):
                continue
            else:
                curve.insert_point(0, pt1.offset(-DELTA, 0))
            if pt2.attr('bottom'):
                continue
            else:
                curve.append_point(pt2.offset(DELTA, 0))
            self.curves.append(curve)

        self.curves.append(self.layers[-1].bottom_curve.scale(sx, sy))

    def fill(self):
        fills = []
        delta = 10
        sx = 1000 / self.paper.scale.x
        sy = 1000 / self.paper.scale.y
        left = -int(self.top * sy / delta) - 2
        right = int((self.dss[-1] * sx - self.bottom * sy) / delta) + 2
        for i in range(len(self.curves) - 1):
            top_curve = self.curves[i]
            bottom_curve = self.curves[i + 1]
            fill = []
            for i in range(left, right):
                silt_clay = Line(Point(-1000, -1000 - delta * i), Point(1000, 1000 - delta * i))
                pt1 = bottom_curve.intersect(silt_clay)
                pt2 = top_curve.intersect(silt_clay)
                if (not pt1) and pt2:
                    x = top_curve.get_points()[0].x
                    pt1 = silt_clay.x2y(x)
                elif pt1 and (not pt2):
                    x = top_curve.get_points()[-1].x
                    pt2 = silt_clay.x2y(x)
                if pt1 and pt2:
                    line = Line(pt1, pt2)
                    fill.append(line)
            fills.append(fill)
        return fills
