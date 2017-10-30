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
        self.paper = Paper(self)


    @property
    def items(self):
        return self._items

    @property
    def holes(self):
        return [hole for hole, accumulate_distance in self._items]

    @property
    def dss(self):
        return [accumulate_distance for hole, accumulate_distance in self._items]

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

    def draw_sectionLine(self, name='A3', width=420, height=297, orientation='H'):
        self.paper = Paper(self, name, width, height, orientation)
        extra_dist = 0.015 * self.paper.scale.x
        HNUM = len(self.items)
        LCOUNT = max(len(hole.layers) for hole in self.holes)
        curves = []
        curve0 = []
        for layer_index in range(LCOUNT - 1):
            hole_index = 0
            leftEdge_flag = 0
            rightEdge_index = 0
            leftExt_line = []
            rightExt_line = []

            while hole_index < HNUM - 1:
                # 第1步：定义A孔
                aHole = self.items[hole_index][0]
                ax = self.items[hole_index][1]

                # 第2步：若当前A孔是第一个孔，层位处于第一层时，画地形左延伸线，否则进入第3步
                if layer_index == 0 and hole_index == 0:
                    left_pt = AcPoint(ax - extra_dist, aHole.elevation)
                    right_pt = AcPoint(ax, aHole.elevation)
                    curve0.extend([left_pt, right_pt])

                # 第3步：若A孔已到层底，将下一个孔设为A孔，否则进入第4步
                # 此处未考虑A孔与右侧孔存在层位相交错情况，日后可优化！！！
                if layer_index >= len(aHole.layers) - 1:
                    hole_index = hole_index + 1
                    continue

                # 第4步：若A孔未到层底，处理当前层层底左延伸线
                aLayer = aHole.layers[layer_index]
                ay = aHole.elevation - aLayer.endDep

                if hole_index == 0:
                    leftExt_line = line_extend(self, layer_index, -extra_dist, hole_index)
                # 若当前层厚度及其当前层下左侧是否还有孔
                else:
                    # 防止其下部还有层时左孔下部层和右孔下部层相连
                    n1 = len(aHole.layers)
                    n2 = len(self.items[hole_index - 1][0].layers)
                    n = min(n1, n2)
                    t = 0
                    for m in range(layer_index, n):
                        t1 = aHole.layers[m].thickness
                        t2 = self.items[hole_index - 1][0].layers[m].thickness
                        t = t + t1 * t2
                    if t == 0:
                        leftExt_line = line_extend(self, layer_index, -extra_dist, hole_index)
                        # A孔也可能存在右延伸线，故此处必须记录，此处需要日后优化！！！！
                        # rightEdge_index = hole_index

                # 第5步：定义B孔及AB孔相对关系，A和B相邻，A在左，B在右；
                # 用循环判断B孔当前层是否为或者已经超越层底，没有的话画地形线及中间孔的层位层底线定义
                hole_index = hole_index + 1
                while hole_index <= HNUM - 1:
                    bHole = self.items[hole_index][0]
                    bx = self.items[hole_index][1]

                    # 第5-1步：判断当前B孔是否已到层底，若未到层底，连线，否则跳到5-2步
                    if layer_index < len(bHole.layers) - 1:
                        print('A孔：{0}，B孔:{1}该孔未到层底{2}---'.format(aHole.holeName, self.items[hole_index][0].holeName,
                                                                 bHole.layers[layer_index]))
                        bl = bHole.layers[layer_index]
                        by = bHole.elevation - bl.endDep
                        # 第5-1-1步：若当前层为第一层时,画地形线及层底线
                        if layer_index == 0:
                            # 先行仅画出第一层层厚>0的地形线，当其小于0时，其对应层底线即是其地形线。
                            if aLayer.thickness > 0 and bl.thickness > 0:
                                left_pt = AcPoint(ax, aHole.elevation)
                                right_pt = AcPoint(bx, bHole.elevation)
                                curve0.extend([left_pt, right_pt])
                                aLayer.gen_pmline(AcPoint(ax, ay), AcPoint(bx, by))
                                rightEdge_index = hole_index
                            elif aLayer.thickness > 0 and bl.thickness == 0:
                                x = (ax + 2 * bx) / 3
                                y = aHole.elevation
                                curve0.extend(
                                    [AcPoint(ax, aHole.elevation), AcPoint(x, y), AcPoint(bx, bHole.elevation)])
                                points = [AcPoint(ax, ay), AcPoint(x, y), AcPoint(bx, by)]
                                aLayer.gen_pmline(*points)
                            elif aLayer.thickness == 0 and bl.thickness > 0:
                                x = (2 * ax + bx) / 3
                                y = bHole.elevation
                                curve0.extend(
                                    [AcPoint(ax, aHole.elevation), AcPoint(x, y), AcPoint(bx, bHole.elevation)])
                                points = [AcPoint(ax, ay), AcPoint(x, y), AcPoint(bx, by)]
                                aLayer.gen_pmline(*points)
                                rightEdge_index = hole_index
                            elif aLayer.thickness == 0 and bl.thickness == 0:
                                curve0.extend([AcPoint(ax, ay), AcPoint(bx, by)])
                                aLayer.gen_pmline(AcPoint(ax, ay), AcPoint(bx, by))
                            # 若当前B孔为最后一个孔，画右地形延伸线,但是当B孔只有一层是，此处会发生错误！！！
                            if hole_index == HNUM - 1:
                                left_pt = AcPoint(bx, bHole.elevation)
                                right_pt = AcPoint(bx + extra_dist, bHole.elevation)
                                curve0.extend([left_pt, right_pt])
                        # 第5-1-2步：当前层不为第一层，考虑到B孔可能比A孔浅，此时，只有当前B孔已到层底，且为最后一个孔时，才具备画右延伸线条件
                        else:
                            # al0 = aHole.layers.find(layers[layer_index - 1].layerNo)
                            # 想一想，为什么这里面要重新赋值
                            # 注意，当前层到了AB中间孔的层底时且存在层位错位时，无论其AB中间相隔多少孔，只计算B前一个孔
                            # 不是太合理，需优化，另外，若当前层超越AB中间孔的层底时，且存在层位错位时，仍选B前一个孔，计算会出错！！！！
                            al0 = self.holes[hole_index - 1].layers[layer_index - 1]

                            if aLayer.thickness > 0 and bl.thickness > 0:
                                left_pt = AcPoint(ax, ay)
                                right_pt = AcPoint(bx, by)
                                aLayer.gen_pmline(left_pt, right_pt)
                                rightEdge_index = hole_index

                            elif aLayer.thickness > 0 and bl.thickness == 0:
                                ymin = al0.pmline.points[0].y
                                ymax = al0.pmline.points[-1].y
                                if (ay - ymax) * (ay - ymin) < 0:
                                    y = ay
                                    x = al0.pmline.reverse_line_func(y)
                                else:
                                    x = (ax + 2 * bx) / 3
                                    y = al0.pmline.line_func(x)
                                points = paired_points(al0.pmline.points, AcPoint(ax, ay), AcPoint(x, y))
                                aLayer.gen_pmline(*points)

                            elif aLayer.thickness == 0 and bl.thickness > 0:
                                ymax = al0.pmline.points[-1].y
                                ymin = al0.pmline.points[0].y
                                if (by - ymax) * (by - ymin) < 0:
                                    y = by
                                    x = al0.pmline.reverse_line_func(y)
                                else:
                                    x = (2 * ax + bx) / 3
                                    y = al0.pmline.line_func(x)
                                points = paired_points(al0.pmline.points, AcPoint(x, y), AcPoint(bx, by))
                                aLayer.gen_pmline(*points)
                                rightEdge_index = hole_index

                            elif aLayer.thickness == 0 and bl.thickness == 0:
                                aLayer.gen_pmline(*al0.pmline.points)
                        if hole_index == HNUM - 1:
                            rightExt_line = line_extend(self, layer_index, extra_dist)
                        break
                    # 第5-2步：判断当前B孔已到或超越层底，将下一个孔设为B孔，同时跳出之前 考虑能否画右延伸线。
                    else:
                        print('A孔：{0}，B孔:{1}该孔已经到层底{2}--'.format(aHole.holeName, self.holes[hole_index].holeName,
                                                                 aHole.layers[layer_index]))
                        # 第5-2-1步：考虑到B孔可能比A孔浅，此时，只有当前B孔已到层底，且为最后一个孔时，才具备画右延伸线条件
                        if hole_index == HNUM - 1:
                            rightExt_line = line_extend(self, layer_index, extra_dist, rightEdge_index)
                            # break
                            # 此时内外层while循环同时结束结束
                        hole_index = hole_index + 1

            if layer_index == 0:
                curves.append(curve0)
            curve = []
            curve.extend(leftExt_line)
            for num in range(HNUM):
                hole = self.holes[num]
                if layer_index <= len(hole.layers) - 1 and hole.layers[layer_index].pmline:
                    points = self.holes[num].layers[layer_index].pmline.points
                    curve.extend(points)
            curve.extend(rightExt_line)
            curves.append(curve)
        return curves


def line_extend(_section, layer_index, extra_dist, hole_index=-1):
    # 默认是右延长线，若需要计算左延伸线，只要传入-extra_dist
    # 默认hole_index不传值，则使用最后一个孔
    hole = _section.holes[hole_index]
    current_layer = hole.layers[layer_index]
    x = _section.dss[hole_index]
    y = hole.elevation - current_layer.endDep
    pt0 = AcPoint(x, y)
    pt1 = AcPoint(x + extra_dist, y)
    # 注意先后顺序
    if extra_dist < 0:
        return pt1, pt0
    return pt0, pt1


def paired_points(base_points, pt1, pt2):
    # base_points必须是按照X从左至右排序，否则本函数必须先排序
    # pt1,pt2传入时可不按照X从左至右排序，本函数会将其排序
    left_pt = pt1
    right_pt = pt2
    if pt1.x > pt2.x:
        left_pt = pt2
        right_pt = pt1
    points = [left_pt, right_pt]
    for n in range(len(base_points)):
        if base_points[n].x < left_pt.x:
            points.insert(points.index(left_pt), base_points[n])
        elif base_points[n].x > right_pt.x:
            points.append(base_points[n])
    return points
