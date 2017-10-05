# -*-coding:utf-8-*-
# -------------------------------------------------------------------------
# Name:        situ
# Purpose:     start web
#
# Author:      Robot of Fernando
#
# Created:     29-05-2016
# Copyright:   (c) Robot of Fernando 2015
# Licence:     The MIT License
# -------------------------------------------------------------------------

from flask import render_template, request

from app.services.core import *
from app.test.auth2 import *
from . import situ


@situ.route("/sitePhoto", methods=['POST', 'GET'])
def sitePhoto():
    if request.method == "GET":
        projectNo = request.args.get('projectNo')
        return render_template(
            'situ/sitePhoto.html',
            projectNo=projectNo,
            manager=FindManager(projectNo)
        )
    else:
        files = request.files.getlist('file[]')
        # 多个同名name的input提交采用getlist
        notes = request.form.getlist("note")
        # 此处需重复
        basedir = os.path.abspath(os.path.dirname(__file__))
        basedir = os.path.abspath(os.path.dirname(basedir))
        archivingir = os.path.join(basedir, 'upload')
        responseTxt = "%d files have been uploaded!" % len(files)
        print(responseTxt)
        for i in range(0, len(files)):
            note = notes[i]
            f = files[i]
            filename = f.filename
            f.save(os.path.join(archivingir, filename))
            print("%s note:%s" % (filename, note))
        return responseTxt


@situ.route("/siteMap")
def siteMap():
    projectNo = request.args.get('projectNo')
    return render_template(
        'situ/siteMap.html',
        projectNo=projectNo,
        manager=FindManager(projectNo)
    )
