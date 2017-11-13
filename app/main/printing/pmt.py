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
import math

from flask import render_template, request

from app.services.base.func import AcPoint
from app.services.core import find_sections, find_layers
from app.services.geometry.line import Line
from . import printing


@printing.route("/pmt", methods=['POST', 'GET'])
def pmt():
    projectNo = request.args.get('projectNo')
    sectionNo = request.args.get('sectionNo')
    if request.method == 'POST':
        return None
    sections = find_sections(projectNo)
    section = sections[int(sectionNo)]
    paper = section.set_paper()
    layers = section.draw_sectionLine(find_layers(projectNo))
    lines = section.fill_layer()

    return render_template('printing/pmt.html', projectNo=projectNo, section=section, layers=layers,
                           hLines=section.hLines, paper=paper, lines=lines)
