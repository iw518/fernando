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
from flask import request, render_template,redirect
from . import trans
from .forms import AccessForm
import pyodbc
from app.model.trans import CPT,Hole
from app import db
from app.models import Project


@trans.route('/mdb2cpt', methods=['POST','GET'])
def mdb2cpt():
    form=AccessForm()
    form.projectNo.choices=[]
    if request.method == "POST":
        if 'file' not in request.files:
            print('success!')
        else:
            f=request.files['file']
            cnxn = pyodbc.connect(
                r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+f.path+';UID=admin;PWD=;')
            cursor = cnxn.cursor()
            cursor.execute("select project_name,project_nameing from base")
            rows = cursor.fetchall()
            form.projectNo.choices = [(row.project_name, row.project_nameing) for row in rows]
            print('fuck!')
        return redirect(request.url)
    return render_template('trans/trans.html')

