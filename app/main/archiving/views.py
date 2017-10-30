#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      views
# date:         2016-12-08
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------

import datetime

import collections
from flask import render_template, request, jsonify

from app.model.models import Project
from app.services.base.utility import read_xml
from . import archiving


@archiving.route('/record', methods=['POST', 'GET'])
def record():
    if request.method == "GET":
        catalog = importCatalog('doc_catalog')
        return render_template('archiving/record.html', catalog=catalog)
    print(request.form)
    project_nickname = request.form['project_nickname'].upper()
    project = Project.query.filter_by(nickname=project_nickname).first()

    if request.form["type"] == "query":
        print({"project_fullname": project.fullname, "project_assistant_fullname": project.find_user().fullname})
        return jsonify(
            {"project_fullname": project.fullname, "project_assistant_fullname": project.find_user().fullname})
    elif request.form["type"] == "submit":
        archiving_amount = int(request.form['archiving'])
        archiving_date = datetime.datetime.strptime(request.form['archiving_date'], '%Y-%m-%d')
        print(archiving_date)
        if archiving_amount > 0 and archiving_date != '':
            project.profile.archiving = archiving_amount
            project.profile.archiving_date = archiving_date
            return jsonify(result='successful!')
        else:
            return jsonify(result='false!')


def importCatalog(filename):
    nodes = read_xml(filename)
    catalog = collections.OrderedDict()
    for node in nodes:
        if node.nodeType == 1:
            items = []
            for item in node.childNodes:
                if item.nodeType == 1:
                    items.append(item.firstChild.nodeValue)
            catalog[node.getAttribute("name")] = items
    return catalog
