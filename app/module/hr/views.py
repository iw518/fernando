#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      views
# date:         2016-12-14
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------

from . import hr
from flask import redirect,url_for,render_template
from .forms import RegisterForm
from app.models import Project, Job, User, Team, Profile


@hr.route('/team_manage',methods=['POST','GET'])
def team_manage():
    form = RegisterForm()
    if form.validate_on_submit():
        Team(job_id=form.job_selections.data,user_id=form.user_selections.data)
        return redirect(url_for('order.employee'))
    return render_template('hr/team_manage.html', form=form)