#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      views
# date:         2017-10-05
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------

import os
from flask import request, render_template, current_app

from config import cleandir
from . import importation


@importation.route('/cpt_txt', methods=['POST', 'GET'])
def cpt_txt():
    upload_path = current_app.config.get('UPLOAD_FOLDER')
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(upload_path, 'cpt', 'txt', file.filename))
    cleandir(upload_path)
    return render_template('importation/cpt_txt.html')
