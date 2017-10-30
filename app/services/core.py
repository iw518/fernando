# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        services
# Purpose:     gen result txt
#
# Author:      Robot of Fernando
#
# Created:     17-06-2015
# Copyright:   (c) Robot of Fernando 2015
# Licence:     The MIT License
# -------------------------------------------------------------------------------

import sys

import copy
import struct

from .base.hole import *
from .base.layer import *
from .base.point import *
from .base.section import *
from .base.utility import read_xml
from .dataset import *

# SILTYS=['砂质粉土','粉砂','细砂','粉细砂','中砂','粗砂','中粗砂','砾砂']
paths = []
dirs = ["勘探数据/单孔数据/",
        "勘探数据/静力触探数据/",
        "勘探数据/水位表/",
        "勘探数据/统计/",
        "勘探数据/计算书/",
        "勘探数据/其他/",
        "勘探数据/register/"
        ]

#  若用os.path.dirname(x)来查找上级目录，并创建父目录，有时候查找不到，具体原因不明
#  os.mkdir(x)用来创建一层目录，os.makedirs(x)用来创建多层目录
for dirname in dirs:
    path = os.path.join(ROOTDIR, 'tmp', dirname)
    if not os.path.exists(path):
        os.makedirs(path)
    if path not in paths:
        paths.append(path)


def find_sections(projectNo):
    func_name = sys._getframe().f_code.co_name
    res = read_sql(func_name, projectNo)
    holes = find_holes_with_layer(projectNo)
    sections = []
    section = Section()
    accumulate_distance = 0
    last_distance = 0
    for name, holeName, distance in res:
        if section.name != name:
            section = Section(name)
            sections.append(section)
            hole = extract_element(holes, "holeName", holeName)
            section.items.append((hole, 0))
            accumulate_distance = 0
            last_distance = distance
        else:
            hole = extract_element(holes, "holeName", holeName)
            accumulate_distance = accumulate_distance + last_distance
            section.items.append((hole, accumulate_distance))
            last_distance = distance
    return sections


def find_holes_with_BG(projectNo):
    func_name = sys._getframe().f_code.co_name
    res = read_sql(func_name, projectNo)
    '将采集的bgpoint加入到hole中'
    hole_list = find_holes_with_layer(projectNo, 1)
    for (holeName, bgPoint, testDep, N635, k_0005, k025_0074) in res:
        xPoint = NPoint()
        try:
            xPoint.name = bgPoint.encode('latin-1').decode('gbk')
        except UnicodeEncodeError:
            xPoint.name = bgPoint
        try:
            xPoint.holeName = holeName.encode('latin-1').decode('gbk')
        except UnicodeEncodeError:
            xPoint.holeName = holeName
        xPoint.testDep = testDep
        soilType = '粉质粘土'

        # 部分土样可能没有颗粒分析数据
        k025_0074 = k025_0074 if k025_0074 else 0
        k_0005 = k_0005 if k_0005 else 0

        if k025_0074 > 50:
            soilType = '粉砂'
        elif k_0005 < 10:
            soilType = '砂质粉土'
        elif k_0005 < 15:
            soilType = '粘质粉土'
        xPoint.soilType = soilType
        xPoint.clayContent = k_0005
        xPoint.N = N635
        holeName = xPoint.holeName
        hole = extract_element(hole_list, "holeName", holeName)
        hole.points.append(xPoint)
    return hole_list


def res_lique(projectNo):
    siltLayers = FindSiltLayers(projectNo)
    holeList = find_liqueholes(projectNo)
    caculatedHoleCount = len(holeList)
    caculatedPointCount = 0
    erroCount = 0
    liqueList = []
    for hole in holeList:
        for xLayer in hole.layers:
            '查找该土层是否是砂土或砂质粉土层，若是，则进行判别，否则跳过判别，继续下一个点的计算'
            if extract_element(siltLayers, "layerName", xLayer.layerName):
                for i in range(len(xLayer.points)):
                    xPoint = xLayer.points[i]
                    caculatedPointCount += 1
                    # 如果该点是判别层中的第一个点，则代表厚度的上半部分(delta1)的起始位置取判别层的层顶深度
                    if i == 0:
                        priorTestDep = xLayer.startDep
                        delta1 = xPoint.testDep - priorTestDep
                    # 如果该点不是判别层中的第一个点，则代表厚度的上半部分(delta1)的起始位置取其上一点的试验深度
                    else:
                        priorTestDep = xLayer.points[i - 1].testDep
                        delta1 = (xPoint.testDep - priorTestDep) / 2
                    # 如果该点是判别层中的最后一个点，则代表厚度的下半部分(delta2)的结束位置取判别层的层底深度与20m的最小值
                    if i == len(xLayer.points) - 1:
                        nextTestDep = min(xLayer.endDep, 20)
                        delta2 = (nextTestDep - xPoint.testDep)
                    # 如果该点不是判别层中的最后一个点，则代表厚度的下半部分(delta2)的结束位置取其下一点的试验深度
                    else:
                        nextTestDep = xLayer.points[i + 1].testDep
                        delta2 = (nextTestDep - xPoint.testDep) / 2
                    # midH为代表厚度的中点
                    # print('%s\t%s\t%.2f\t%.2f'%(xHole.holeName,xPoint.name,priorTestDep,nextTestDep))
                    midH = (nextTestDep + priorTestDep) / 2
                    xPoint.Di = delta1 + delta2
                    xPoint.Wi = calc_Wi(midH)
                    '注意python中float小数精度的问题,即使是1.50,float可能显示的也是1.5000062'
                    if round(xPoint.Di, 4) > 1.5:
                        xPoint.inf = '%s%.2f' % ('erro', xPoint.Di)
                        erroCount += 1
                    else:
                        xPoint.inf = ''
                    if xPoint.clayContent is None:
                        result = (hole.holeName,
                                  xLayer.layerNo,
                                  '%.2f' % xPoint.testDep,
                                  xPoint.N,
                                  '',
                                  '否',
                                  '-',
                                  '-',
                                  '%.2f' % xPoint.Di,
                                  '',
                                  '',
                                  xPoint.inf)
                        liqueList.append(result)
                    else:
                        result = (hole.holeName,
                                  xLayer.layerNo,
                                  '%.2f' % xPoint.testDep,
                                  '%.2f' % xPoint.clayContent,
                                  xPoint.N,
                                  FilterZero(xPoint.Ncr, True),
                                  # ('%.2f' % (xPoint.Ncr) if type(xPoint.Ncr) is float else xPoint.Ncr),
                                  xPoint.lique_flag,
                                  xPoint.FLei,
                                  '%.2f' % xPoint.Di,
                                  '%.2f' % xPoint.Wi,
                                  xPoint.ILei,
                                  xPoint.inf)
                        liqueList.append(result)
    return liqueList, caculatedHoleCount, caculatedPointCount, erroCount


def find_holes_with_layer(projectNo, holeType=-1):
    low = 0
    high = 50
    if holeType > -1:
        high = holeType + 1
        low = holeType - 1
    func_name = sys._getframe().f_code.co_name
    res = read_sql(func_name, projectNo, low, high)
    layers = find_layers(projectNo)
    hole_list = find_holes_with_info(projectNo, holeType)
    L1 = len(res)
    for i in range(0, L1):
        try:
            holeName = res[i][0].encode('latin-1').decode('gbk')
        except UnicodeEncodeError:
            holeName = res[i][0]
        hole = extract_element(hole_list, "holeName", holeName)
        layer_order = res[i][2]
        layer = copy.deepcopy(layers[layer_order - 1])
        layer.endDep = res[i][1]
        if layer_order == 1:
            layer.startDep = 0.0
            layer.endDep = res[i][1]
        elif layer.endDep == 0.0:
            layer.startDep = hole.layers[-1].endDep
            layer.endDep = hole.layers[-1].endDep
        else:
            layer.startDep = hole.layers[-1].endDep
            layer.endDep = res[i][1]
        hole.layers.append(layer)
    for hole in hole_list:
        if len(hole.layers) > 1:
            layer = copy.deepcopy(layers[len(hole.layers)])
            layer.startDep = hole.layers[-1].endDep
            layer.endDep = hole.Dep
            hole.layers.append(layer)
            # (xLayer.layerNo,xLayer.layerName,xLayer.startDep,xLayer.endDep)
    return hole_list


def find_holes_with_info(projectNo, holeType=-1):
    low = 0
    high = 50
    if holeType > -1:
        high = holeType + 1
        low = holeType - 1
    func_name = sys._getframe().f_code.co_name
    res = read_sql(func_name, projectNo, low, high)
    hole_list = []
    for (holeName, elevation, holeDepth, waterLevel, holeType) in res:
        hole = Hole()
        try:
            hole.holeName = holeName.encode('latin-1').decode('gbk')
        except UnicodeEncodeError:
            hole.holeName = holeName
        hole.projectNo = projectNo
        hole.elevation = elevation
        hole.Dep = holeDepth
        hole.waterLevel = waterLevel
        hole.holeType = holeType
        hole_list.append(hole)
    return hole_list


def find_liqueholes(projectNo):
    hole_list = find_holes_with_BG(projectNo)
    for hole in hole_list:
        pointL = len(hole.points.filter(NPoint))
        if pointL == 0:
            continue
        for i in range(0, pointL):
            xPoint = hole.points[i]
            # 查找标贯点对应的土层
            if xPoint.testDep - 0.15 < 20:
                layer = findlayer_existpoint(xPoint, hole)
                layer.points.append(xPoint)
    LiqueHoleList = []
    siltLayers = FindSiltLayers(projectNo)
    for hole in hole_list:
        for layer in hole.layers:
            if (layer.layerNo in [item.layerNo for item in siltLayers]) and len(layer.points) > 0:
                LiqueHoleList.append(hole)
                break
    return LiqueHoleList


def find_holes_with_dep(projectNo):
    """查找每个项目所含钻孔及其孔深,
    hole主要组成为hole.holeName,hole.Dep,
    返回list[xhole,....]"""
    func_name = sys._getframe().f_code.co_name
    res = read_sql(func_name, projectNo)
    hole_list = []
    for (holeName, holeDepth) in res:
        hole = Hole()
        try:
            hole.holeName = holeName.encode('latin-1').decode('gbk')
        except UnicodeEncodeError:
            hole.holeName = holeName
        hole.projectNo = projectNo
        hole.Dep = holeDepth
        hole_list.append(hole)
    return hole_list


def findlayer_existpoint(xPoint, xHole):
    for xLayer in xHole.layers:
        if xLayer.thickness > 0:
            if (xPoint.testDep - xLayer.startDep) * (xPoint.testDep - xLayer.endDep) < 0:
                return xLayer


def find_layers(projectNo):
    func_name = sys._getframe().f_code.co_name
    res = read_sql(func_name, projectNo)
    layers = []
    count = 0
    for (layerNo, layerName, layerAge) in res:
        count += 1
        xLayer = Layer()
        xLayer.layerOrder = count
        try:
            xLayer.layerNo = layerNo.encode('latin-1').decode('gbk')
        except UnicodeEncodeError:
            xLayer.layerNo = layerNo
        try:
            xLayer.layerName = layerName.encode('latin-1').decode('gbk')
        except UnicodeEncodeError:
            xLayer.layerName = layerName
        xLayer.layerAge = layerAge
        layers.append(xLayer)
    # print("本工程地基土可划分为%d个工程地质层。"%(count))
    return layers


# 统计时需要考虑分期号
def ExportLayers_Stat(projectNo, mode=1):
    keytuple = (["PS1", "比贯入阻力", "Ps", "MPa", 1, 2],
                ["DENSITY", "重度", "&gamma;", "kN/m<sup>3</sup>", 1, 1],
                ["CON_C", "固结快剪", "C", "kPa", 2, 0],
                ["CON_F", "固结快剪", "&phi;", "&deg;", 0, 1],
                ["QUICK_C", "快剪", "C<sub>q</sub>", "kPa", 2, 0],
                ["QUICK_F", "快剪", "&phi;<sub>q</sub>", "&deg;", 0, 1],
                ["SLOW_C", "慢剪", "C", "kPa", 2, 0],
                ["SLOW_F", "慢剪", "&phi;", "&deg;", 0, 1],
                ["CCU", "CU", "C<sub>cu</sub>", "kPa", 2, 0],
                ["FCU", "CU", "&phi;<sub>cu</sub>", "&deg;", 0, 1],
                ["CU", "UU", "C<sub>uu</sub>", "kPa", 2, 0],
                ["FU", "UU", "&phi;<sub>uu</sub>", "&deg;", 0, 1],
                ["KH", "渗透系数", "K<sub>H</sub>", "cm/s&times;10<sup>-6</sup>", 2, 2],
                ["KV", "渗透系数", "K<sub>V</sub>", "cm/s&times;10<sup>-6</sup>", 0, 2],
                ["K0", "静止侧压力", "K0", "-", 1, 2]
                )
    try:
        res = read_sql("retrieve_indexes.enterprise", projectNo)
    except pypyodbc.ProgrammingError:
        res = read_sql("retrieve_indexes.personal", projectNo)
    layers = []
    for item in res:
        xLayer = LayerStats()
        try:
            xLayer.layerNo = item[0].encode('latin-1').decode('gbk')
        except UnicodeEncodeError:
            xLayer.layerNo = item[0]
        try:
            xLayer.layerName = item[1].encode('latin-1').decode('gbk')
        except UnicodeEncodeError:
            xLayer.layerName = item[1]
        myrange = []
        if mode == 1:
            myrange = range(0, 4)
        elif mode == 2:
            myrange = range(1, len(keytuple))
        for i in myrange:
            key = keytuple[i][0]
            if key == "DENSITY":
                value = round(item[2 + i] * 9.8, keytuple[i][5])
            elif key == "KH" or key == "KV":
                value = round(item[2 + i] * 1000000, keytuple[i][5])
            else:
                value = round(item[2 + i], keytuple[i][5])
            setattr(xLayer, key, value)
        layers.append(xLayer)
    return layers


def FindSiltLayers(projectNo):
    siltLayers = []
    layers = find_layers(projectNo)
    for xLayer in layers:
        if xLayer.layerAge is None:
            print('地质时代未输入，请补齐')
        elif xLayer.layerAge.startswith('Q4') and ('砂' in xLayer.layerName.split('夹')[0]):
            siltLayers.append(xLayer)
            # print('本工程的砂土层或砂质粉土层为：%s\t%s\t'%(xLayer.layerNo,xLayer.layerName))
    return siltLayers


def calc_Wi(midDep):
    if midDep <= 5:
        return 10
    elif midDep == 20:
        return 0
    else:
        return -2 / 3 * midDep + 40 / 3


def find_CPT(projectNo, genfile=False):
    func_name = sys._getframe().f_code.co_name
    res = read_sql(func_name, projectNo)
    hole_list = []
    # cur.fetchone()是tuple格式
    # print(type(cur.fetchone()))
    # buff=cur.fetchone()[1]
    for item in res:
        hole = CPTHole()
        try:
            hole.holeName = item[0].encode('latin-1').decode('gbk')
        except UnicodeEncodeError:
            hole.holeName = item[0]
        hole.projectNo = projectNo
        buff = item[1]
        buff_len = len(buff)
        for x in range(0, buff_len, 2):
            ps = (struct.unpack('H', buff[x:(x + 2)])[0]) / 100
            xPoint = PsPoint()
            xPoint.testDep = round(x / 2 * 0.1 + 0.1, 2)
            xPoint.testValue = round(ps, 2)
            hole.points.append(xPoint)
        hole_list.append(hole)

    if genfile is True:
        # 生成静力触探文件
        for hole in hole_list:
            str1 = ""
            for point in hole.points:
                str1 += "%.2f\n" % point.testValue
            filename = os.path.join(paths[1], projectNo + '__' + hole.holeName + ".txt")
            f = open(filename, 'w')
            f.close()
    return hole_list


def lab_workloads(projectNo):
    mydict = {}
    res = read_sql("retrieve_common_index", projectNo)
    mydict["含水量、密度"] = (501, res[0][0])
    mydict["液、塑限"] = (502, res[0][1])
    mydict["固结快剪"] = (503, res[0][2])
    mydict["固结压缩"] = (504, res[0][3])

    res = read_sql("retrieve_grain_index", projectNo)
    mydict["颗粒分析"] = (505, res[0][0])

    res = read_sql("retrieve_penetration_index", projectNo)
    mydict["渗透系数"] = (601, res[0][0])

    res = read_sql("retrieve_special_index", projectNo)
    mydict["UU"] = (602, res[0][0])
    mydict["CU"] = (603, res[0][1])
    mydict["qu"] = (604, res[0][2])
    mydict["K0"] = (605, res[0][3])
    mydict["灼热减量"] = (606, res[0][4])

    res = read_sql("retrieve_slow_shearing_index", projectNo)
    mydict["慢剪"] = (607, res[0][0])

    res = read_sql("retrieve_quick_shearing_index", projectNo)
    mydict["快剪"] = (608, res[0][0])

    res = read_sql("retrieve_spt_index", projectNo)
    mydict["标贯试验"] = (801, res[0][0])
    return mydict


def GroupTotal(total, factor=8):
    """
    转置分列
    默认每张水位表最大可容纳8列'
      1,2,3,.......................1factor
      .............................2factor
      ....................................
      ....................................
      (rank-1)factor+1,..........rank*factor
    """

    rank = math.floor(total / factor)
    remainder = total % factor
    if remainder == 0:
        rank = rank
    else:
        rank = rank + 1
        factor = math.ceil(total / rank)
    return factor, rank


def import_xml():
    configDict = {}
    nodes = read_xml('template')
    for node in nodes:
        # 默认xml中换行符及空格也属于节点,即COMMENT_NODE
        # 此外还有ATTRIBUTE_NODE以及ELEMENT_NODE
        if node.nodeType == 1:
            print(node.nodeName)
            print(node.nodeType)
            keylist = []
            for item in node.childNodes:
                if item.nodeType == 1:
                    keylist.append(item.firstChild.nodeValue)
                    # print(item.firstChild.data)
                    # print(item.firstChild.nodeValue)
            configDict[node.getAttribute("name")] = keylist
    return configDict


def import_motto(filename):
    nodes = read_xml(filename)
    mottos = []
    for node in nodes:
        # 默认xml中换行符及空格也属于节点,即COMMENT_NODE
        # 此外还有ATTRIBUTE_NODE以及ELEMENT_NODE
        if node.nodeType == 1:
            motto = node.firstChild.nodeValue
            mottos.append(motto)
    return mottos
