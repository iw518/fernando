#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      views
# date:         2016-07-24
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------
from flask import render_template, redirect, url_for, request

from app import db
from app.model.models import Project, Job, Profile, TechFee
from . import order
from .forms import EmployeeForm, BuildInfForm, FundForm, FeeForm
from .forms import RegisterForm


@order.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        Project(nickname=form.nickname.data.upper(), fullname=form.fullname.data)
        return redirect(url_for('order.employee'))
    return render_template('order/register.html', form=form)


@order.route('/employee', methods=['POST', 'GET'])
def employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        project_nickname = form.nickname.data
        project = Project.query.filter_by(nickname=project_nickname).first()
        for job in Job.query.all():
            form_control = getattr(form, job.nickname)
            user_id = form_control.data
            project.insert_team(job_id=job.id, user_id=user_id)
        return render_template('/project.html', projectNo=project_nickname, project=project)
        # return redirect(url_for('services.index', projectNo=project_nickname, project=project, _external=True))
    return render_template('order/employee.html', form=form)


@order.route('/build_inf', methods=['POST', 'GET'])
def build_inf():
    project_nickname = request.args.get('projectNo')
    project = Project.query.filter_by(nickname=project_nickname).first()
    profile = project.profile
    form = BuildInfForm()
    if form.validate_on_submit():
        profile = Profile.query.filter_by(project_id=project.id).first()
        profile.phase = form.phase.data
        profile.client = form.client.data
        profile.design = form.design.data
        profile.size = form.size.data
        project.fullname = form.project_fullname.data
        return render_template('/project.html', projectNo=project_nickname, project=project)
    form.project_fullname.data = project.fullname
    form.phase.data = 2 if (profile.phase is None) or (profile.phase is '') else int(profile.phase)
    form.client.data = profile.client
    form.design.data = profile.design
    form.size.data = profile.size
    return render_template('order/build_inf.html', project=project, form=form)


@order.route('/fund', methods=['POST', 'GET'])
def fund():
    project_nickname = request.args.get('projectNo')
    project = Project.query.filter_by(nickname=project_nickname).first()
    profile = project.profile
    fund_form = FundForm()
    fee_form = FeeForm()
    if fund_form.validate_on_submit() and fund_form.fund_submit.data:
        profile = Profile.query.filter_by(project_id=project.id).first()
        profile.fund_contract_sum = fund_form.fund_contract_sum.data
        profile.fund_income_sum = fund_form.fund_income_sum.data
        return render_template('/project.html', projectNo=project_nickname, project=project)
    if fee_form.validate_on_submit() and fee_form.fee_submit.data:
        print("tech_form is submitted")
        fee_income = fee_form.fee_income.data
        income_date = fee_form.income_date.data
        notation = fee_form.notation.data
        techfee = TechFee(project_id=project.id, fee_income=fee_income, income_date=income_date, notation=notation)
        db.session.add(techfee)
        db.session.commit()
        return render_template('/project.html', projectNo=project_nickname, project=project)
    fund_form.fund_contract_sum.data = profile.fund_contract_sum
    fund_form.fund_income_sum.data = profile.fund_income_sum
    return render_template('order/fund.html', project=project, fund_form=fund_form, fee_form=fee_form)
