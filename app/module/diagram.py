# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        logginData
# Purpose:     input data of layer and hole
#
# Author:      Robot of Fernando
#
# Created:     28-06-2016
# Copyright:   (c) Robot of Fernando 2015
# Licence:     The MIT License
# -------------------------------------------------------------------------------

from flask import render_template, request, Blueprint, url_for

from app.main.test.auth2 import *
from ..main.core import *
from ..main.genpdf import *

diagram = Blueprint('diagram', __name__)


@diagram.route('/cpt', methods=['POST', 'GET'])
def cpt():
    projectNo = request.args.get('projectNo')
    cpt_list = find_CPT(projectNo)
    hole_list = find_holes_with_layer(projectNo, 2)
    for hole in hole_list:
        # 防止静力触探孔中无测试数据
        try:
            cpt = SuperList(cpt_list).filter("holeName", hole.holeName)
            hole.testPoints = cpt.points
        except:
            continue
    index = None
    if request.method == 'POST':
        probeNo = request.form['probeNo']
        probeArea = request.form['probeArea']
        fixedRatio = request.form['fixedRatio']
        testDate = request.form['testDate']
        probeInf = {'probeNo': probeNo,
                    'probeArea': probeArea,
                    'fixedRatio': fixedRatio,
                    'testDate': testDate}

        if request.form['print_btn'] == '打印所有静力触探':
            MaxNofHole = 4          # 一天最多施工4只勘探孔
            MaxTotalDep = 160       # 一天总进尺最多160m
            autoDate(testDate, MaxNofHole, MaxTotalDep, hole_list)
            index = None
        elif request.form['print_btn'] == '打印单个静力触探':
            index = int(request.form['holeName'])
            hole_list[index].testDate = testDate

        filename = PrintPdf(projectNo, probeInf, hole_list, index)
        filename = 'download/' + os.path.basename(filename)
        pdfUrl = url_for('static', filename=filename)
        print(pdfUrl)
        return render_template('pdf.html', url=pdfUrl)
    return render_template(
        'diagram/cpt.html',
        projectNo=projectNo,
        hole_list=hole_list,
        manager=FindManager(projectNo),
    )


@diagram.route('/zzt')
def zzt():
    projectNo = request.args.get('projectNo')
    hole_list = find_holes_with_layer(projectNo, 1)
    return render_template(
        'diagram/zzt.html',
        projectNo=projectNo,
        hole_list=hole_list,
        manager=FindManager(projectNo)
    )

@diagram.route("/section_draw", methods=['POST', 'GET'])
def section_draw():
    projectNo = request.args.get('projectNo')
    if request.method == 'POST':
        return None
    sections=find_sections(projectNo)
    layers = [item.to_json() for item in find_layers(projectNo)]
    return render_template('section_draw.html',projectNo=projectNo,sections=sections,layers=layers)