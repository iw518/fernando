#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      views
# date:         2016-07-19
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------
from flask import render_template, request, jsonify
from flask_login import login_required

from app.decorators import admin_required
from app.models import Project
from . import main
from .core import *

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrator!"


@main.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        projectNo = request.form['projectNo']
        project = Project.query.filter_by(nickname=projectNo).first()
        return render_template('project.html', projectNo=projectNo,project =project)
    else:
        return render_template('index.html')


@main.route("/layer_config", methods=['POST', 'GET'])
def layer_config():
    layerConfigDict = import_XML()
    if request.method == 'POST':
        return jsonify(result=layerConfigDict)
    else:
        return render_template(
            "layer_config.html",
            layerConfigDict=layerConfigDict
        )


@main.route("/index2", methods=['POST', 'GET'])
def index2():
    if request.method == 'POST':
        projectNo = request.form['projectNo']
        # return redirect(url_for('index',projectNo=request.form['projectNo']))
        return render_template('project_home_old.html', projectNo=projectNo)
    else:
        return render_template('index_old.html')