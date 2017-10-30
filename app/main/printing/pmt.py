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

from app.services.core import find_sections
from . import printing


@printing.route("/pmt", methods=['POST', 'GET'])
def pmt():
    projectNo = request.args.get('projectNo')
    if request.method == 'POST':
        return None
    sections = find_sections(projectNo)
    section = sections[0]

    curves = section.draw_sectionLine()
    return render_template('printing/pmt.html', projectNo=projectNo, section=section, curves=curves,
                           hLines=section.hLines, paper=section.paper)
