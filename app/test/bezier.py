#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      bezier
# date:         2017-10-20
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------
from app.services.base.func import AcPoint


def createCurve(originCount, *originPoint):
    # 控制点收缩系数 ，经调试0.6较好，AcPoint是opencv的，可自行定义结构体(x, y)
    curvePoint = []
    scale = 0.6
    midpoints = [AcPoint() for i in range(originCount)]
    # 生成中点
    for i in range(originCount):
        nexti = (i + 1) % originCount
        midpoints[i].x = (originPoint[i].x + originPoint[nexti].x) / 2.0
        midpoints[i].y = (originPoint[i].y + originPoint[nexti].y) / 2.0

        # 平移中点
    extrapoints = [AcPoint() for i in range(2 * originCount)]
    for i in range(originCount):
        nexti = (i + 1) % originCount
        backi = (i + originCount - 1) % originCount
        midinmid = AcPoint()
        midinmid.x = (midpoints[i].x + midpoints[backi].x) / 2.0
        midinmid.y = (midpoints[i].y + midpoints[backi].y) / 2.0
        offsetx = originPoint[i].x - midinmid.x
        offsety = originPoint[i].y - midinmid.y
        extraindex = 2 * i
        extrapoints[extraindex].x = midpoints[backi].x + offsetx
        extrapoints[extraindex].y = midpoints[backi].y + offsety
        # 朝 originPoint[i]方向收缩
        addx = (extrapoints[extraindex].x - originPoint[i].x) * scale
        addy = (extrapoints[extraindex].y - originPoint[i].y) * scale
        extrapoints[extraindex].x = originPoint[i].x + addx
        extrapoints[extraindex].y = originPoint[i].y + addy
        extranexti = (extraindex + 1) % (2 * originCount)
        extrapoints[extranexti].x = midpoints[i].x + offsetx
        extrapoints[extranexti].y = midpoints[i].y + offsety
        # 朝 originPoint[i]方向收缩
        addx = (extrapoints[extranexti].x - originPoint[i].x) * scale
        addy = (extrapoints[extranexti].y - originPoint[i].y) * scale
        extrapoints[extranexti].x = originPoint[i].x + addx
        extrapoints[extranexti].y = originPoint[i].y + addy

    controlPoint = [AcPoint() for i in range(4)]
    # 生成4控制点，产生贝塞尔曲线
    for i in range(originCount - 1):
        controlPoint[0] = originPoint[i]
        extraindex = 2 * i
        controlPoint[1] = extrapoints[extraindex + 1]
        extranexti = (extraindex + 2) % (2 * originCount)
        controlPoint[2] = extrapoints[extranexti]
        nexti = (i + 1) % originCount
        controlPoint[3] = originPoint[nexti]
        u = 1
        while (u >= 0):
            px = bezier3funcX(u, controlPoint)
            py = bezier3funcY(u, controlPoint)
            # u的步长决定曲线的疏密
            u -= 0.005
            tempP = AcPoint(px, py)
            # 存入曲线点
            curvePoint.append(tempP)
    return curvePoint


# 三次贝塞尔曲线
def bezier3funcX(uu, controlP):
    part0 = controlP[0].x * uu * uu * uu
    part1 = 3 * controlP[1].x * uu * uu * (1 - uu)
    part2 = 3 * controlP[2].x * uu * (1 - uu) * (1 - uu)
    part3 = controlP[3].x * (1 - uu) * (1 - uu) * (1 - uu)
    return part0 + part1 + part2 + part3


def bezier3funcY(uu, controlP):
    part0 = controlP[0].y * uu * uu * uu
    part1 = 3 * controlP[1].y * uu * uu * (1 - uu)
    part2 = 3 * controlP[2].y * uu * (1 - uu) * (1 - uu)
    part3 = controlP[3].y * (1 - uu) * (1 - uu) * (1 - uu)
    return part0 + part1 + part2 + part3
