#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      views
# date:         2017-10-05
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------

from flask import render_template, request, url_for, jsonify

from app.services.core import *
from app.test.auth2 import *
from . import analysis


@analysis.route('/cptAnalysis', methods=['POST', 'GET'])
def cptAnalysis():
    projectNo = request.args.get('projectNo')
    cpt_list = find_CPT(projectNo)
    hole_list = find_holes_with_layer(projectNo, 2)
    for hole in hole_list:
        cpt = extract_element(cpt_list, "holeName", hole.holeName)
        hole.testPoints = cpt.points
    if request.method == 'GET':
        layer_hole_ps_list = []
        for i in range(0, len(find_layers(projectNo))):
            hole_ps_list = []
            for hole in hole_list:
                SumPs = 0
                if i >= len(hole.layers):
                    hole_ps_list.append((hole.holeName, 0))
                else:
                    xLayer = hole.layers[i]
                    for testPoint in hole.points:
                        # 注意小数位数不等也可能导致不相等，情况允许时，应该调整layer函数的位数
                        if round(xLayer.startDep, 2) < testPoint.testDep <= round(xLayer.endDep, 2):
                            SumPs = SumPs + testPoint.testValue
                    if xLayer.endDep - xLayer.startDep == 0:
                        hole_ps_list.append([hole.holeName, 0])
                    else:
                        hole_ps_list.append([hole.holeName,
                                             round(SumPs / (xLayer.endDep - xLayer.startDep) / 10, 2)
                                             ]
                                            )
            layer_hole_ps_list.append([find_layers(projectNo)[i].layerNo,
                                       hole_ps_list])
        return render_template('analysis/cptAnalysis.html',
                               projectNo=projectNo,
                               layer_hole_ps_list=layer_hole_ps_list
                               )

    if request.method == 'POST':
        str0 = "%s\t" % ''
        for hole in hole_list:
            str0 = str0 + "%s\t" % hole.holeName
        str0 = str0 + "\n"
        for i in range(0, len(find_layers(projectNo))):
            str0 = str0 + find_layers(projectNo)[i].layerNo + "\t"

            for hole in hole_list:
                SumPs = 0
                # print("%s\t"%(xHole.holeName))
                if i >= len(hole.layers):
                    str0 = str0 + "%s\t" % ''
                else:
                    xLayer = hole.layers[i]
                    for testPoint in hole.points:
                        # 注意小数位数不等也可能导致不相等，情况允许时，应该调整layer函数的位数
                        if round(xLayer.startDep, 2) < testPoint.testDep <= round(xLayer.endDep, 2):
                            SumPs = SumPs + testPoint.testValue
                    if xLayer.endDep - xLayer.startDep == 0:
                        str0 = str0 + "%s\t" % ''
                    else:
                        str0 = str0 + "%.2f\t" % (SumPs / (xLayer.endDep - xLayer.startDep) / 10)
            str0 = str0 + "\n"
        basedir = os.path.abspath(os.path.dirname(__file__))
        filename = os.path.join(
            basedir,
            'static',
            'download',
            "1.txt"
        )
        f = open(filename, 'w', encoding="UTF-8")
        print(str0, f)
        f.close()
        myurl = url_for(
            "static",
            filename="download/1.txt"
        )
        print(myurl)
        return jsonify(result=myurl)


@analysis.route('/layerAnalysis')
def layerAnalysis():
    projectNo = request.args.get('projectNo')
    hole_list = find_holes_with_layer(projectNo)
    layerDict = OrderedDict()
    for xLayer in find_layers(projectNo):
        layerNo = xLayer.layerNo
        layerName = xLayer.layerName
        maxThickness = 0
        minThickness = 1000
        maxTopElevation = -1000
        minTopElevation = 1000
        maxBottomElevation = -1000
        minBottomElevation = 1000
        dict1 = {}
        for hole in hole_list:
            if hole.layers.find(layerNo):
                dict1["layerName"] = layerName
                top = hole.elevation - hole.layers.find(layerNo).startDep
                bottom = hole.elevation - hole.layers.find(layerNo).endDep
                thickness = hole.layers.find(layerNo).thickness
                if thickness > 0:
                    if top > maxTopElevation:
                        maxTopElevation = top
                    if top < minTopElevation:
                        minTopElevation = top
                    dict1["maxTopElevation"] = "%.2f" % maxTopElevation
                    dict1["minTopElevation"] = "%.2f" % minTopElevation
                    if layerNo != hole.layers[-1].layerNo:
                        # 部分钻孔层位未钻穿，不应统计进去
                        if thickness > maxThickness:
                            maxThickness = thickness
                        if thickness < minThickness and thickness != 0:
                            minThickness = thickness
                        if bottom > maxBottomElevation:
                            maxBottomElevation = bottom
                        if bottom < minBottomElevation:
                            minBottomElevation = bottom
                        dict1["maxThickness"] = "%.2f" % maxThickness
                        dict1["minThickness"] = "%.2f" % minThickness
                        dict1["maxBottomElevation"] = "%.2f" % maxBottomElevation
                        dict1["minBottomElevation"] = "%.2f" % minBottomElevation
        layerDict[layerNo] = dict1
        layer_hole_elevation_list = []
        for xLayer in find_layers(projectNo):
            layerNo = xLayer.layerNo
            list1 = []
            for hole in hole_list:
                if hole.layers.find(layerNo):
                    if layerNo != hole.layers[-1].layerNo:
                        top = hole.elevation - hole.layers.find(layerNo).startDep
                        bottom = hole.elevation - hole.layers.find(layerNo).endDep
                        thickness = hole.layers.find(layerNo).thickness
                        list1.append([hole.holeName, thickness])
            layer_hole_elevation_list.append([layerNo, list1])
        '''

        layerDict = {"layerNo":{
                                "layerName":layerName,
                                "maxThickness":maxThickness,
                                "minThickness":minThickness,
                                "maxTopElevation":maxTopElevation,
                                "minTopElevation":minTopElevation,
                                "maxBottomElevation":maxBottomElevation,
                                "minBottomElevation":minBottomElevation
                                }
                    }
        '''

    return render_template('analysis/layerAnalysis.html',
                           projectNo=projectNo,
                           layerDict=layerDict,
                           layer_hole_elevation_list=layer_hole_elevation_list,
                           manager=FindManager(projectNo)
                           )
