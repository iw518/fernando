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

from flask import render_template, request

from app.services.core import *
from app.test.auth2 import *
from . import stats


@stats.route('/workloads')
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

    engHole_list = find_holes_with_info(projectNo, 1)
    engHoleName_set = {hole.holeName for hole in engHole_list}
    soilHole_list = find_holes_with_dep(projectNo)
    soilHoleName_set = {hole.holeName for hole in soilHole_list}
    allHoleName_set = soilHoleName_set | engHoleName_set
    checkDep_list = []
    for holeName in allHoleName_set:
        engHole = extract_element(engHole_list, "holeName", holeName)
        soilHole = extract_element(soilHole_list, "holeName", holeName)
        engHole_dep = engHole.Dep if engHole  else 0
        soilHole_dep = soilHole.Dep if soilHole  else 0
        checkDep_list.append((holeName, engHole_dep, soilHole_dep))

    return render_template('stats/workloads.html', projectNo=projectNo, dict_workloads=dict_workloads,
                           dict_soilloads=dict_soilloads, manager=FindManager(projectNo), checkDep_list=checkDep_list)


@stats.route('/excavation')
def excavation():
    projectNo = request.args.get('projectNo')
    layers = ExportLayers_Stat(projectNo, 2)
    return render_template('stats/excavation.html', projectNo=projectNo, manager=FindManager(projectNo), layers=layers)
