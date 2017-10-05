#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      prtcptdata
# date:         2017-08-12
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------


import os
from flask import render_template, request, current_app, session, send_file

from app.services.base import func
from app.services.core import find_CPT
from app.services.cptpdf import export2pdf
from config import ROOTDIR
from . import printing


@printing.route('/export')
def export():
    pdf = session.get('pdf')
    return send_file(pdf, attachment_filename=os.path.basename(pdf))


@printing.route('/prtcptdata', methods=['POST', 'GET'])
def prtcptdata():
    projectNo = request.args.get('projectNo')
    holes_inf = scan_holes(projectNo)
    if request.method == 'POST':
        req = request.get_json()
        probe = req["probe"]
        holes = req["holes"]
        for hole in holes.values():
            holeName = hole["holeName"]
            data = read_data(holeName, projectNo)
            hole["data"] = data
        # 注意此处必须用req中获取
        pdf = export2pdf(holes, probe, req["projectNo"])
        if os.path.isfile(pdf):
            session['pdf'] = pdf
            return 'successful'
        return 'failure'
    else:
        return render_template(
            'printing/prtcptdata.html', holes=holes_inf,
            projectNo=projectNo
        )


def scan_holes(projectNo):
    holes = []
    if projectNo:
        for hole in find_CPT(projectNo):
            dep = len(hole.points) / 10
            holeName = hole.holeName
            holes.append({"holeName": holeName, "dep": dep})
        return holes
    TXT_DIR = os.path.join(ROOTDIR, 'upload', 'cpt', 'txt')
    for root, dirs, files in os.walk(TXT_DIR):
        for filename in files:
            f = open(os.path.join(root, filename))
            lines = f.readlines()
            dep = len(lines) / 10
            holeName = filename.split('.txt')[0]
            holes.append({"holeName": holeName, "dep": dep})
    return holes


def read_data(holeName, projectNo):
    TXT_DIR = os.path.join(current_app.config.get('UPLOAD_FOLDER'), 'cpt', 'txt')

    data = []
    if projectNo:
        cpt_list = find_CPT(projectNo)
        cpt = func.extract_element(cpt_list, "holeName", holeName)
        for point in cpt.points:
            data.append(point.testValue)
    else:
        file_path = os.path.join(TXT_DIR, holeName + '.txt')
        f = open(file_path)
        lines = f.readlines()
        for line in lines:
            data.append(line.split('\n')[0])
        f.close()
        # txt文件使用完毕后，删除其文件
        os.remove(file_path)
    return data
