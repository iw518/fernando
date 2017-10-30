# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        GPoint
# Purpose:
#
# Author:      Robot of Fernando
#
# Created:     17-06-2015
# Copyright:   (c) Administrator 2015
# Licence:     <GPLV3>
# -------------------------------------------------------------------------------
import math


class AbstractPoint:
    def __init__(self):
        self.pointID = 0
        self.testDep = 0.0
        self.testValue = 0.0
        self.holeName = ""
        self.soilType = ""
        self.clayContent = -1.0


class SamplingPoint(AbstractPoint):
    def __init__(self, start_dep, end_dep):
        super(SamplingPoint, self).__init__()
        start_dep = start_dep
        end_dep = end_dep


class PsPoint(AbstractPoint):
    def __init__(self):
        super(PsPoint, self).__init__()


class NPoint(AbstractPoint):
    # 注意类变量和对象变量的区别

    def __init__(self):
        super(NPoint, self).__init__()
        # startDep=0
        # endDep=0
        # midDep=(startDep+endDep)/2
        self.N = -1.0
        self.testValue = self.N
        self.Wi = -1.0
        self.Di = -1.0
        self.inf = ''

    @property
    def Ncr(self):
        N0 = 7
        # 2016局部修订版
        beta = 0.95
        DW = 0.50
        _Ncr = -1.0
        ds = self.testDep
        cc = self.clayContent
        if cc >= 10:
            return '-'
        elif cc <= 3:
            _Ncr = N0 * beta * (math.log(0.6 * ds + 1.5) - 0.1 * DW)
            return round(_Ncr, 2)
        else:
            _Ncr = N0 * beta * (math.log(0.6 * ds + 1.5) - 0.1 * DW) * math.sqrt(3 / cc)
            return round(_Ncr, 2)

    @property
    def FLei(self):
        if self.Ncr == '-':
            return '-'
        elif self.Ncr <= self.N:
            return '-'
        elif self.Ncr > self.N:
            return round(self.N / self.Ncr, 2)

    @property
    def ILei(self):
        if self.FLei == '-':
            return '-'
        else:
            return round((1 - self.FLei) * self.Di * self.Wi, 2)

    @property
    def lique_flag(self):
        if self.Ncr == '-':
            return '否'
        elif self.Ncr <= self.N:
            return '否'
        elif self.Ncr > self.N:
            return '是'


class Points(list):
    def __init__(self):
        super(Points, self).__init__()

    def append(self, item):
        if isinstance(item, AbstractPoint):
            list.append(self, item)

    def filter(self, pointType):
        xList = []
        for xPoint in self:
            if isinstance(xPoint, pointType):
                xList.append(xPoint)
        return xList
