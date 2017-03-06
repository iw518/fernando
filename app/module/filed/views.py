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

from . import filed
from app.main.core import readXML

from flask import render_template,request,jsonify
from app.models import Project,Profile,Team,User
import collections,datetime
@filed.route('/record', methods=['POST', 'GET'])
def record():
    if request.method == "GET":
        catalog=importCatalog('doc_catalog')
        return render_template('filed/record.html', catalog=catalog)
    print(request.form)
    project_nickname = request.form['project_nickname'].upper()
    project = Project.query.filter_by(nickname=project_nickname).first()

    if request.form["type"]=="query":
        print({"project_fullname":project.fullname,"project_assistant_fullname":project.find_user().fullname})
        return jsonify({"project_fullname":project.fullname,"project_assistant_fullname":project.find_user().fullname})
    elif request.form["type"]=="submit":
        filed = int(request.form['filed'])
        filed_date = datetime.datetime.strptime(request.form['filed_date'], '%Y-%m-%d')
        print(filed_date)
        if filed>0 and filed_date !='':
            project.profile.filed=filed
            project.profile.filed_date=filed_date
            return jsonify(result='successful!')
        else:
            return jsonify(result='false!')

def importCatalog(filename):
    nodes=readXML(filename)
    catalog=collections.OrderedDict()
    for node in nodes:
        if node.nodeType==1:
            items=[]
            for item in node.childNodes:
                if item.nodeType==1:
                    items.append(item.firstChild.nodeValue)
            catalog[node.getAttribute("name")]=items
    return catalog
