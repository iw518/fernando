#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      views
# date:         2017-08-05
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------
import os
from flask import request, render_template, jsonify, session

from app.services.core import import_xml
from app.services.dataset import MSSQL
from config import ROOTDIR
from . import setting


@setting.route("/layer_template", methods=['POST', 'GET'])
def layer_template():
    layerConfigDict = import_xml()
    if request.method == 'POST':
        return jsonify(result=layerConfigDict)
    else:
        return render_template(
            "setting/layer_template.html",
            layerConfigDict=layerConfigDict
        )


# 不同POST在一个函数中的写法，如果分开在两个函数中，要更简单
@setting.route('/data_source', methods=['POST', 'GET'])
def data_source():
    if request.method == 'POST':
        print(request.form)
        if "name" in request.form:
            file = request.files['file']
            if file:
                file.save(os.path.join(ROOTDIR, 'upload', 'database', "Tran_shgeodb.mdb"))
        if "edition" in request.form:
            edition = request.form["edition"]
            session['edition'] = edition
    return render_template('setting/data_source.html', edition=MSSQL.edition)
