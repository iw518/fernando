# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        calcultaion
# Purpose:     calculating water, liquefaction and pile
#
# Author:      Robot of Fernando
#
# Created:     03-07-2015
# Copyright:   (c) Robot of Fernando 2015
# Licence:     The MIT License
# -------------------------------------------------------------------------------

from flask import render_template, request, jsonify, json

from app.services.core import *
from app.test.auth2 import *
from . import calc


@calc.route('/water')
def water():
    projectNo = request.args.get('projectNo')
    old_holes = find_holes_with_info(projectNo, 1)
    # holelist=list(filter(lambda xHole: type(xHole.waterLevel) is float, holelist))
    # lambda example:    lambda x: boolfun(x), sequen
    # oldway:   filter(lambda xHole: type(xHole.waterLevel) is float, holelist)
    # newway:    list(filter(...))

    holes = []
    # 不应在列表循环中动态修改该列表元素个数
    for hole in old_holes:
        if FilterZero(hole.waterLevel) != '-':
            holes.append(hole)
    cnt = len(holes)
    factor = GroupTotal(cnt)[0]
    rank = GroupTotal(cnt)[1]
    return render_template('calc/water.html',
                           projectNo=projectNo,
                           holes=holes,
                           cnt=cnt,
                           rank=rank,
                           factor=factor,
                           manager=FindManager(projectNo)
                           )


@calc.route('/natural_foundation', methods=['POST', 'GET'])
def natural_foundation():
    projectNo = request.args.get('projectNo')
    if request.method == "GET":
        layers = ExportLayers_Stat(projectNo)
        return render_template('calc/naturalfoundation.html',
                               projectNo=projectNo,
                               layers=layers,
                               manager=FindManager(projectNo)
                               )
    else:
        depth = float(request.form['depth'])
        water_depth = float(request.form['water_depth'])
        layers = ExportLayers_Stat(projectNo)
        xlist = []
        for layer in layers:
            xlist.append((layer.Ps_Fak(depth, water_depth),
                          layer.Soil_Fak(depth, water_depth),
                          layer.Fak(depth, water_depth)
                          ))
        return jsonify(result=xlist)
        # return make_response(dumps(xlist))与jsonify(data=xlist)等效，
        # 前者在前端中可直接用data访问，但是后者在前端中需用字典访问，即data.data形式
        # erro jsonify(data=layers)由于layers中的元素为layer对象，
        # flask由于ES5的安全原因，不允许序列化,需转换为字符串、或与字符串相关的数组，元组，字典等


@calc.route('/pile', methods=['POST', 'GET'])
def pile():
    print(request.args)
    projectNo = request.args.get('projectNo')
    hole_list = find_holes_with_layer(projectNo, 1)
    hole_list.extend(find_holes_with_layer(projectNo, 2))

    if request.method == 'GET':
        layers = ExportLayers_Stat(projectNo)
        repeat_layerNolist = []
        for hole in hole_list:
            for layer in hole.layers:
                if not (layer.layerNo in repeat_layerNolist):
                    if layer.startDep < 6 and layer.endDep > 6:
                        repeat_layerNolist.append(layer.layerNo)
                        break
        return render_template('calc/pile.html',
                               projectNo=projectNo,
                               holes=[hole.holeName for hole in hole_list],
                               manager=FindManager(projectNo),
                               layers=layers,
                               repeat_layerNolist=repeat_layerNolist
                               )
    hole = extract_element(hole_list, 'holeName', request.form['hole_selected'])
    return json.dumps(hole.to_json())


# @calc.route('/pile_calculate')
# def pile_calculate():
#     req=request.args.to_dict()  #{"{G1:{1:[],2:[],3:[]}}":""}
#     dict2list=[]
#     for req_dict in req.keys(): #req_dict "{G1:{1:[],2:[],3:[]}}"
#         req_dict=eval(req_dict) #eval(req_dict) {G1:{1:[],2:[],3:[]}}
#         for value_dict in req_dict.values():
#             dict2list=sorted(value_dict.items(),key=lambda item:int(item[0]))
#             https://docs.python.org/3/howto/sorting.html#sortinghowto
#             print(dict2list) #value_dict {1:[],2:[],3:[]}
#     Rsk=0
#     for i in range(len(dict2list)):
#         try:
#             dict2list[i][1][0]=float(dict2list[i][1][0])
#         except ValueError:
#             dict2list[i][1][0]=0
#         try:
#             dict2list[i][1][1]=float(dict2list[i][1][1])
#         except ValueError:
#             dict2list[i][1][1]=0
#         if i==0:
#             Rsk=dict2list[0][1][0]+dict2list[0][1][1]
#         else:
#             Rsk=Rsk+(dict2list[i][1][0]-dict2list[i-1][1][0])*dict2list[i][1][1]
#     print(Rsk)
#     return jsonify(result=Rsk)


@calc.route('/liquefaction')
@before_req
def liquefaction():
    projectNo = request.args.get('projectNo')
    siltLayers = FindSiltLayers(find_layers(projectNo))
    siltLayersStr = '、'.join('%s：%s' % (item.layerNo, item.layerName) for item in siltLayers)
    liqueHolesStr = '、'.join(xHole.holeName for xHole in find_liqueholes(projectNo))
    res = res_lique(projectNo)
    return render_template('calc/liquefaction.html',
                           projectNo=projectNo,
                           siltLayersStr=siltLayersStr,
                           liqueHolesStr=liqueHolesStr,
                           liqueList=res[0],
                           caculatedHoleCount=res[1],
                           caculatedPointCount=res[2],
                           erroCount=res[3],
                           manager=FindManager(projectNo)
                           )
