#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      plot
# date:         2017-10-04
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------
from matplotlib import pyplot as plt

from app.services.core import *

projectNo = 'K043-2015-4'
layers = find_layers(projectNo)
section = find_sections(projectNo)[12]


def paired_points(base_points, pt1, pt2):
    # base_points必须是按照X从左至右排序，否则本函数必须先排序
    # pt1,pt2传入时可不按照X从左至右排序，本函数会将其排序
    left_pt = pt1
    right_pt = pt2
    if pt1[0] > pt2[0]:
        left_pt = pt2
        right_pt = pt1
    points = [left_pt, right_pt]
    for n in range(len(base_points)):
        if base_points[n][0] < left_pt[0]:
            points.insert(points.index(left_pt), base_points[n])
        elif base_points[n][0] > right_pt[0]:
            points.append(base_points[n])
    return points


# 画图框函数
def draw_frame(width, height, left_margin=10,
               top_margin=10,
               bottom_margin=10,
               right_margin=10):
    # abbreviation of coordinate point:{lef_top:lt,left_bottom:lb,right_top:rt,right_bottom:rb}
    # left bottom corner is zero point
    lt_point = (left_margin, height - top_margin)
    lb_point = (left_margin, bottom_margin)
    rt_point = (width - right_margin, height - top_margin)
    rb_point = (width - right_margin, bottom_margin)
    return lt_point, rt_point, rb_point, lb_point


def draw_hole():
    # draw hole line
    points = []
    for (hole, accumulate_distance) in section.items:
        top_x = accumulate_distance
        bottom_x = accumulate_distance
        top_y = hole.elevation
        bottom_y = top_y - hole.Dep
        top_point = (top_x, top_y)
        bottom_point = (bottom_x, bottom_y)
        points.extend([top_point, bottom_point])
    return points


def draw_sectionLine(extra_dist=10):
    section_lines = []
    for layer_index in range(len(layers) - 1):
        layer = layers[layer_index]
        layer_line = []
        hole_index = 0
        while hole_index < len(section.items) - 1:

            aHole = section.items[hole_index][0]
            aLayer = aHole.layers.find(layer.layerNo)
            ax = section.items[hole_index][1]
            ay = aHole.elevation - aLayer.endDep
            # 第1步：A和B为相邻孔，A在左，B在右；
            # 判断当前A孔是否已到层底，若到层底，将右侧相邻孔设为A孔，否则进入第2步
            if layer_index >= len(section.items[hole_index][0].layers) - 1:
                hole_index = hole_index + 1
                continue

            # 第2步：画左延伸线，必须考虑深部地层，左延伸线可能不是第一个孔
            leftEdge_flag = 0
            rightEdge_index = 0
            if aLayer.thickness > 0:
                leftEdge_flag = leftEdge_flag + 1
                rightEdge_index = hole_index
                if leftEdge_flag == 1:
                    left_pt = (ax - extra_dist, ay)
                    right_pt = (ax, ay)
                    layer_line.extend([left_pt, right_pt])
                    plt.plot([ax - extra_dist, ax], [ay, ay])

            # 第3步：画地形线及中间层底线
            while hole_index <= len(section.items) - 2:
                hole_index = hole_index + 1
                if layer_index >= len(section.items[hole_index][0].layers) - 1:
                    print('A孔：{0}，B孔:{1}该孔已经到层底{2}--'.format(aHole.holeName, section.items[hole_index][0].holeName,
                                                             layer.layerNo))

                    if hole_index == len(section.items) - 1:
                        rightEdge_hole = section.items[rightEdge_index][0]
                        rightEdge_currentLayer = rightEdge_hole.layers.find(layer.layerNo)
                        rightEdge__x = section.items[rightEdge_index][1]
                        rightEdge__y = rightEdge_hole.elevation - rightEdge_currentLayer.endDep
                        plt.plot([rightEdge__x, rightEdge__x + 10], [rightEdge__y, rightEdge__y])
                    else:
                        continue
                else:
                    bHole = section.items[hole_index][0]
                    bl = bHole.layers.find(layer.layerNo)
                    bx = section.items[hole_index][1]
                    by = bHole.elevation - bl.endDep
                    print('A孔：{0}，B孔:{1}该孔未到层底{2}---'.format(aHole.holeName, section.items[hole_index][0].holeName,
                                                             layer.layerNo))

                    if layer_index == 0:
                        if hole_index - 1 == 0:
                            plt.plot([-10, ax], [aHole.elevation, aHole.elevation])
                        if aLayer.thickness > 0 and bl.thickness > 0:
                            aLayer.gen_pmline((ax, ay), (bx, by))
                            plt.plot([ax, bx], [aHole.elevation, bHole.elevation])
                            plt.plot([ax, bx], [ay, by])

                            rightEdge_index = hole_index
                            if hole_index == len(section.items) - 1:
                                rightEdge_hole = section.items[rightEdge_index][0]
                                rightEdge_currentLayer = rightEdge_hole.layers.find(layer.layerNo)
                                rightEdge__x = section.items[rightEdge_index][1]
                                rightEdge__y = rightEdge_hole.elevation - rightEdge_currentLayer.endDep
                                plt.plot([rightEdge__x, rightEdge__x + 10], [rightEdge__y, rightEdge__y])

                        elif aLayer.thickness > 0 and bl.thickness == 0:
                            x = (ax + 2 * bx) / 3
                            y = aHole.elevation
                            points = [(ax, ay), (x, y), (bx, by)]
                            aLayer.gen_pmline(*points)
                            plt.plot([ax, x, bx], [aHole.elevation, y, bHole.elevation])
                            plt.plot([ax, x], [ay, y])
                        elif aLayer.thickness == 0 and bl.thickness > 0:

                            x = (2 * ax + bx) / 3
                            y = bHole.elevation
                            points = [(ax, ay), (x, y), (bx, by)]
                            aLayer.gen_pmline(*points)
                            plt.plot([ax, x, bx], [aHole.elevation, y, bHole.elevation])
                            plt.plot([x, bx], [y, by])

                            rightEdge_index = hole_index
                            if hole_index == len(section.items) - 1:
                                rightEdge_hole = section.items[rightEdge_index][0]
                                rightEdge_currentLayer = rightEdge_hole.layers.find(layer.layerNo)
                                rightEdge__x = section.items[rightEdge_index][1]
                                rightEdge__y = rightEdge_hole.elevation - rightEdge_currentLayer.endDep
                                plt.plot([rightEdge__x, rightEdge__x + 10], [rightEdge__y, rightEdge__y])

                        elif aLayer.thickness == 0 and bl.thickness == 0:
                            aLayer.gen_pmline((ax, ay), (bx, by))
                            plt.plot([ax, bx], [aHole.elevation, bHole.elevation])

                        if hole_index == len(section.items) - 1:
                            plt.plot([bx, bx + 10], [bHole.elevation, bHole.elevation])


                    else:
                        # al0 = aHole.layers.find(layers[layer_index - 1].layerNo)
                        # 想一想，为什么这里面要重新赋值
                        al0 = section.items[hole_index - 1][0].layers.find(layers[layer_index - 1].layerNo)

                        if aLayer.thickness > 0 and bl.thickness > 0:
                            aLayer.gen_pmline((ax, ay), (bx, by))
                            plt.plot([ax, bx], [ay, by])

                            rightEdge_index = hole_index
                            if hole_index == len(section.items) - 1:
                                rightEdge_hole = section.items[rightEdge_index][0]
                                rightEdge_currentLayer = rightEdge_hole.layers.find(layer.layerNo)
                                rightEdge__x = section.items[rightEdge_index][1]
                                rightEdge__y = rightEdge_hole.elevation - rightEdge_currentLayer.endDep
                                plt.plot([rightEdge__x, rightEdge__x + 10], [rightEdge__y, rightEdge__y])

                        elif aLayer.thickness > 0 and bl.thickness == 0:

                            ymax = al0.pmline.points[-1][1]
                            ymin = al0.pmline.points[0][1]
                            if (ay - ymax) * (ay - ymin) < 0:
                                y = ay
                                x = al0.pmline.reverse_line_func(y)
                            else:
                                x = (ax + 2 * bx) / 3
                                y = al0.pmline.line_func(x)
                            points = paired_points(al0.pmline.points, (ax, ay), (x, y))

                            # #TEST BEGIN
                            # if layer_index==7 and bHole.holeName=='ZFG17':
                            #     print(y)
                            #     print(al0.pmline.points)
                            #     print(points)
                            # # TEST END
                            aLayer.gen_pmline(*points)
                            plt.plot([ax, x], [ay, y])
                        elif aLayer.thickness == 0 and bl.thickness > 0:

                            ymax = al0.pmline.points[-1][1]
                            ymin = al0.pmline.points[0][1]
                            if (by - ymax) * (by - ymin) < 0:
                                y = by
                                x = al0.pmline.reverse_line_func(y)
                            else:
                                x = (2 * ax + bx) / 3
                                y = al0.pmline.line_func(x)
                            points = paired_points(al0.pmline.points, (x, y), (bx, by))
                            aLayer.gen_pmline(*points)
                            plt.plot([x, bx], [y, by])

                            rightEdge_index = hole_index
                            if hole_index == len(section.items) - 1:
                                rightEdge_hole = section.items[rightEdge_index][0]
                                rightEdge_currentLayer = rightEdge_hole.layers.find(layer.layerNo)
                                rightEdge__x = section.items[rightEdge_index][1]
                                rightEdge__y = rightEdge_hole.elevation - rightEdge_currentLayer.endDep
                                plt.plot([rightEdge__x, rightEdge__x + 10], [rightEdge__y, rightEdge__y])

                        elif aLayer.thickness == 0 and bl.thickness == 0:
                            aLayer.gen_pmline(*al0.pmline.points)

                    hole_index = hole_index - 1
                    break
            hole_index = hole_index + 1


plt.show()
