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
from flask import render_template, request, make_response
from flask_login import login_required

from app.main.decorators import admin_required
from app.model.models import Project
from . import main


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
        return render_template('project.html', projectNo=projectNo, project=project)
    else:
        return render_template('index.html')


@main.route("/index2", methods=['POST', 'GET'])
def index2():
    if request.method == 'POST':
        projectNo = request.form['projectNo']
        # return redirect(url_for('index',projectNo=request.form['projectNo']))
        return render_template('project_home_old.html', projectNo=projectNo)
    else:
        return render_template('index_old.html')


# make_response没搞懂，似乎不好用
@main.route("/index3")
def index3():
    edition = request.cookies.get('edition')
    if edition:
        print("YES COOKIES! EDITION:" + edition)
        return make_response('go page2')
    else:
        print("NO COOKIES!")
        edition = 'Enterprise'
        resp = make_response('SET COOKIES' + edition)
        return resp
