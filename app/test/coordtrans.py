#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      coordtrans
# date:         2017-10-02
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------


from numpy import *

A2R = pi / 180


class Point2D:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y


class Point3D(Point2D):
    def __init__(self, X, Y, Z):
        super(Point3D, self).__init__(X, Y)
        self.Z = Z


# 第一步转换，大地坐标系转换成空间直角坐标系
def BL2XYZ(B, L, a, b):
    B = B * A2R
    L = L * A2R

    f = (a - b) / a
    e = sqrt(a * a - b * b) / a
    W = sqrt(1 - e * e * sin(B) * sin(B))
    N = a / W

    X = N * cos(B) * cos(L)
    Y = N * cos(B) * sin(L)
    Z = N * (1 - e * e) * sin(B)
    return Point3D(X, Y, Z)


# 第二步转换，空间直角坐标系里七参数转换
def transXYZ(pt3d, para7):
    Ex = para7.ex * A2R
    Ey = para7.ey * A2R
    Ez = para7.ez * A2R
    R0 = array([[1, Ez, -Ey], [-Ez, 1, Ex], [Ey, -Ex, 1]])

    A1 = array([pt3d.X, pt3d.Y, pt3d.Z])
    m = para7.m
    A2 = (1 + m) * R0 + A1
    return Point3D(A2[0], A2[1], A2[2])


# 第三步转换，空间直角坐标系转换成大地坐标系
def XYZ2BL(pt3d, a, b):
    f = (a - b) / a
    e = math.sqrt(a * a - b * b) / a

    X = pt3d.X
    Y = pt3d.Y
    Z = pt3d.Z
    S = sqrt(X * X + Y * Y)

    tanB1 = Z / S
    B1 = math.atan(tanB1)
    B = 0
    while fabs(B - B1) > 0.0000000001:
        B1 = B
        W = sqrt(1 - e * e * sin(B1) * sin(B1))
        N = a / W
        tanB = (Z + N * e * e * sin(B1)) / S
        B = math.atan(tanB)

    cosL = X / S
    L = arccos(cosL)
    L = fabs(L)

    return B / A2R, L / A2R


# 第四部转换，高斯变换，大地坐标系转平面坐标系，84转80

def gaussBL2XY(B, L, daihao):
    a = 6378137
    b = 6356752.3142

    e = math.sqrt(a * a - b * b) / a
    W = sqrt(1 - e * e * sin(B) * sin(B))
    N = a / W
    MidLongitude = daihao * 6 - 3
    x_offset = 500000
    y_offset = 0.0
    B = B * A2R
    l = (L - MidLongitude) * A2R

    m0 = a * (1 - e * e)
    m2 = 3 / 2 * e * e * m0
    m4 = 5 / 4 * e * e * m2
    m6 = 7 / 6 * e * e * m4
    m8 = 9 / 8 * e * e * m6

    a0 = m0 + 1 / 2 * m2 + 3 / 8 * m4 + 5 / 16 * m6 + 35 / 128 * m8
    a2 = 1 / 2 * m2 + 1 / 2 * m4 + 15 / 32 * m6 + 7 / 16 * m8
    a4 = 1 / 8 * m4 + 3 / 16 * m6 + 7 / 32 * m8
    a6 = 1 / 32 * m6 + 1 / 16 * m8
    a8 = 1 / 128 * m8

    X = a0 * B - 1 / 2 * a2 * sin(2 * B) + 1 / 4 * a4 * sin(4 * B) - 1 / 6 * a6 * sin(6 * B) + 1 / 8 * a8 * sin(8 * B)

    t = tan(B)
    h = e * a / b * cos(B)
    m = cos(B) * l

    Ax = 1 / 24 * (5 - pow(t, 2) + 9 * pow(h, 2) + 4 * pow(h, 4))
    Bx = 1 / 720 * (61 - 58 * pow(t, 2) + pow(t, 4)) * pow(m, 2)
    x = X + N * t * (1 / 2 + (Ax + Bx) * pow(m, 2)) * pow(m, 2)

    Ay = 1 / 6 * (1 - pow(t, 2) + pow(h, 2))
    By = 1 / 120 * (5 - 18 * pow(t, 2) + pow(t, 4) + 14 * pow(h, 2) - 58 * pow(h, 2) * pow(t, 2)) * pow(m, 2)
    y = N * (1 + (Ay + By) * pow(m, 2)) * m

    x = x + x_offset
    y = y + y_offset
    print(x)
    print(y)
    return x, y


if __name__ == '__main__':
    B = 22.26638
    L = 111.4811539
    daihao = 3
    gaussBL2XY(B, L, daihao)
