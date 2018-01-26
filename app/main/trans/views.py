#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      views
# date:         2016-08-13
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------
import pypyodbc

from flask import request, render_template, redirect

from . import trans
from .forms import AccessForm


@trans.route('/mdb2cpt', methods=['POST', 'GET'])
def mdb2cpt():
    form = AccessForm()
    form.projectNo.choices = []
    if request.method == "POST":
        if 'file' not in request.files:
            print('success!')
        else:
            f = request.files['file']
            cnxn = pypyodbc.connect(
                r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + f.path + ';UID=admin;PWD=;')
            cursor = cnxn.cursor()
            cursor.execute("SELECT project_name,project_nameing FROM base")
            rows = cursor.fetchall()
            form.projectNo.choices = [(row.project_name, row.project_nameing) for row in rows]
        return redirect(request.url)
    return render_template('trans/trans.html')
