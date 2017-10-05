#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      ztk
# date:         2017-10-05
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------
from flask import render_template, request

from app.services.core import *
from app.test.auth2 import *
from . import printing


@printing.route("/ztk", methods=['POST', 'GET'])
def ztk():
    projectNo = request.args.get('projectNo')
    hole_list = find_holes_with_layer(projectNo, 1)
    return render_template(
        'printing/ztk.html',
        projectNo=projectNo,
        hole_list=hole_list,
        manager=FindManager(projectNo)
    )
