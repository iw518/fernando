# -*-coding:utf-8-*-
# -------------------------------------------------------------------------
# Name:        statisticsxapp
# Purpose:     start web
#
# Author:      Robot of Fernando
#
# Created:     29-05-2016
# Copyright:   (c) Robot of Fernando 2015
# Licence:     The MIT License
# -------------------------------------------------------------------------

from flask import Blueprint, render_template, request

from app.main.test.auth2 import *
from ..main.core import *

statistics = Blueprint('statistics', __name__)


@statistics.route('/workloads')
def workloads():
    projectNo = request.args.get('projectNo')
    hole_list = find_holes_with_info(projectNo)
    dict_workloads = {}
    dict_soilloads = lab_workloads(projectNo)
    for key in DICT_HoleType.keys():
        sumN = 0
        sumDep = 0
        for hole in hole_list:
            if hole.holeType == DICT_HoleType[key][0]:
                sumDep += hole.Dep
                sumN += 1
        dict_workloads[key] = (DICT_HoleType[key][1], sumN, sumDep)
    list1=[]
    list2=[]
    hole_list=find_holes_with_info(projectNo, 1)
    for hole in hole_list:
        list1.append(hole)
    hole_list=find_holes_with_dep(projectNo)
    for hole in hole_list:
        list2.append(hole)

    return render_template('statistics/workloads.html', projectNo=projectNo, dict_workloads=dict_workloads, dict_soilloads=dict_soilloads, manager=FindManager(projectNo), list1=list1, list2=list2)


@statistics.route('/excavation')
def excavation():
    projectNo = request.args.get('projectNo')
    layers = ExportLayers_Stat(projectNo, 2)
    return render_template('statistics/excavation.html', projectNo=projectNo, manager=FindManager(projectNo), layers=layers)
