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

from app.services.core import *
from . import printing


@printing.route("/pmt", methods=['POST', 'GET'])
def pmt():
    projectNo = request.args.get('projectNo')
    if request.method == 'POST':
        return None
    sections = find_sections(projectNo)
    layers = [item.to_json() for item in find_layers(projectNo)]
    return render_template('pmt.html', projectNo=projectNo, sections=sections, layers=layers)
