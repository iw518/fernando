#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      pmt
# date:         2017-10-05
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------
from flask import render_template, request

from app.services.core import find_sections, find_layers
from . import printing
from app.services.geometry.line import Line
from app.services.base.func import AcPoint
import math

@printing.route("/pmt", methods=['POST', 'GET'])
def pmt():
    projectNo = request.args.get('projectNo')
    if request.method == 'POST':
        return None
    sections = find_sections(projectNo)
    section = sections[1]
    paper = section.set_paper()
    layers = section.draw_sectionLine(find_layers(projectNo))

    lines = []
    delta = (layers[0].top_curve.get_points()[1].x - layers[0].top_curve.get_points()[0].x) / 1.5
    left = -int(math.ceil(section.top / delta)) - 1
    right = int(math.ceil((section.dss[-1] - section.bottom) / delta)) + 3
    for layer in layers[0:-1]:
        for i in range(left, right):
            silt_clay = Line(AcPoint(-1000, -1000 - delta * i), AcPoint(5000, 5000 - delta * i))
            pt1 = layer.bottom_curve.intersect(silt_clay)
            pt2 = layer.top_curve.intersect(silt_clay)
            if pt1 and pt2:
                line = Line(pt1, pt2)
                lines.append(line)
            if (not pt1) and pt2:
                x = layer.top_curve.get_points()[0].x
                line = Line(silt_clay.x2y(x), pt2)
                lines.append(line)
            if pt1 and (not pt2):
                x = layer.top_curve.get_points()[-1].x
                line = Line(pt1, silt_clay.x2y(x))
                lines.append(line)

    return render_template('printing/pmt.html', projectNo=projectNo, section=section, layers=layers,
                           hLines=section.hLines, paper=paper, lines=lines)
