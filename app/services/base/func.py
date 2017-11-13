# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        GFunction
# Purpose:     general function
#
# Author:      Robot of Fernando
#
# Created:     17-06-2015
# Copyright:   (c) Administrator 2015
# Licence:     <GPLV3>
# -------------------------------------------------------------------------------
import math


class AcPoint:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def offset(self, ox=0, oy=0, oz=0):
        return AcPoint(self.x + ox, self.y + oy, self.z + oz)

    def scale(self, sx=1, sy=1, sz=1):
        return AcPoint(self.x * sx, self.y * sy, self.z * sz)

    def __str__(self):
        return "(x=%.4f,y=%.4f)" % (self.x, self.y)

    __repr__ = __str__


class SuperList(list):
    def __init__(self, obj):
        super(SuperList, self).__init__()
        if isinstance(obj, list):
            self.extend(obj)

    def filter(self, my_attr, my_attr_value):
        # 此处只能用 for i range(),不能用for item in obj模式，不知道是不是迭代器在作怪
        L = len(self)
        for i in range(L):
            item = self[i]
            if getattr(item, my_attr) == my_attr_value:
                return item


def extract_element(objs, my_attr, my_attr_value):
    for obj in objs:
        if getattr(obj, my_attr) == my_attr_value:
            return obj
    return None


def iszero(num):
    # import sys
    # sys.float_info.epsilon
    # 有时候并不一定是epsilon
    MINIMUM = math.pow(10, -10)
    if (num - MINIMUM) * (num + MINIMUM) <= 0:
        return True
    return False


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


def AddDate(xDate, num=1):
    newDate = xDate.replace('.', '-').replace('/', '-')
    xlist = newDate.split('-')
    if len(xlist) < 3:
        return newDate
    else:
        year = int(xlist[0])
        month = int(xlist[1])
        day = int(xlist[2]) + num
        if month == 2:
            if day > 28:
                day = 1
                month += 1
        elif month in [4, 6, 9, 11]:
            if day > 30:
                day = 1
                month += 1
        elif month in [1, 3, 5, 7, 8, 12]:
            if day > 31:
                day = 1
                month += 1
            if month > 12:
                month = 1
                year += 1
        return '{year}-{month}-{day}'.format(year=year, month=month, day=day)


def convert2dict(objs):
    # 把对象列表转换为字典列表

    obj_arr = []
    for o in objs:
        mydict = {}
        '''
        for item in dir(o):
            dict[item] = o.item  #错误o没有‘item’
            dict.update(o.__dict__)
        '''
        for item in dir(o):
            mydict[item] = getattr(o, item, 0)
        # print(dir(o))
        print(mydict)
        obj_arr.append(mydict)
    return obj_arr


def Convert2json(obj):
    mydict = {}
    for (key, value) in obj.__dict__.items():
        if isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
            mydict[key] = value
    return mydict


def FilterZero(x, convert=False):
    try:
        print(float(x))
    except:
        return '-'
    else:
        if x > 0:
            if convert is True:
                return "%.2f" % x
            else:
                return x
        else:
            return '-'


def Matchlist(x, xlist):
    mylist = []
    if x <= xlist[0][0]:
        return xlist[0][1]
    elif x >= xlist[-1][0]:
        return xlist[-1][1]
    else:
        for i in range(len(xlist)):
            if x == xlist[i][0]:
                return xlist[i][1]
            elif x <= xlist[i + 1][0]:
                for j in range(len(xlist[i][1])):
                    x0 = xlist[i][0]
                    x1 = xlist[i + 1][0]
                    y0 = xlist[i][1][j]
                    y1 = xlist[i + 1][1][j]
                    y = (y1 - y0) / (x1 - x0) * (x - x0) + y0
                    mylist.append(y)
                return mylist
