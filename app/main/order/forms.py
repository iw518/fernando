#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      forms
# date:         2016-07-24
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------
from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Length

from app.model.models import Team


class RegisterForm(Form):
    nickname = StringField('项目编号', validators=[
        DataRequired('请输入项目编号'),
        Length(min=4, max=25, message='length must between 4 and 25')
    ])
    fullname = StringField('项目名称', validators=[
        DataRequired('请输入项目名称'),
        Length(min=4, max=50, message='length must between 4 and 25')
    ])
    submit = SubmitField('注册')


# class EmployeeEntries(Form):
#     # for key,value in EMPLOYEE:
#     #     vars()[key]=SelectField(value, coerce=int)
#     def __init__(self, *args, **kwargs):
#         super(EmployeeEntries, self).__init__(*args, **kwargs)
# employee_list=FormField(EmployeeEntries,'')


class EmployeeForm(Form):
    nickname = StringField('项目编号', validators=[
        DataRequired('请输入项目编号'),
        Length(min=4, max=25, message='length must between 4 and 25')
    ])
    Worker = SelectField('作业班组', coerce=int)
    TestManager = SelectField('试验负责人', coerce=int)
    TestAuditor = SelectField('试验审核人', coerce=int)
    ProjectAssistant = SelectField('项目助理', coerce=int)
    ProjectAuditor = SelectField('项目审核人', coerce=int)
    AuthorizingPerson = SelectField('项目审定人', coerce=int)
    ProjectManager = SelectField('项目经理', coerce=int)
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        users = []
        for team in Team.query.filter_by(job_id=1).all():
            users.append(team.user)
        self.Worker.choices = [(user.id, user.fullname) for user in users]

        users = []
        for team in Team.query.filter_by(job_id=2).all():
            users.append(team.user)
        self.TestManager.choices = [(user.id, user.fullname) for user in users]

        users = []
        for team in Team.query.filter_by(job_id=3).all():
            users.append(team.user)
        self.TestAuditor.choices = [(user.id, user.fullname) for user in users]

        users = []
        for team in Team.query.filter_by(job_id=4).all():
            users.append(team.user)
        self.ProjectAssistant.choices = [(user.id, user.fullname) for user in users]

        users = []
        for team in Team.query.filter_by(job_id=5).all():
            users.append(team.user)
        self.ProjectAuditor.choices = [(user.id, user.fullname) for user in users]

        users = []
        for team in Team.query.filter_by(job_id=6).all():
            users.append(team.user)
        self.AuthorizingPerson.choices = [(user.id, user.fullname) for user in users]

        users = []
        for team in Team.query.filter_by(job_id=7).all():
            users.append(team.user)
        self.ProjectManager.choices = [(user.id, user.fullname) for user in users]


class BuildInfForm(Form):
    project_fullname=StringField('项目名称：')
    phase = SelectField('勘察阶段', coerce=int, choices=[(1, '初步勘察'), (2, '详细勘察'), (3, '补充勘察'), (4, '施工勘察'), (5, '其他')])
    client = StringField('建设单位')
    design = StringField('设计单位')
    size = StringField('项目规模')
    submit = SubmitField('提交')


class FundForm(Form):
    fund_contract_sum = StringField('合同额(万元)：')
    fund_income_sum = StringField('进款额(万元)：')
    fund_submit = SubmitField('提交')


class FeeForm(Form):
    fee_income = StringField('本次进款技术费(元)：', validators=[DataRequired('金额不能为空')])
    income_date = DateField('本次进款日期:', validators=[DataRequired('日期不能为空')])
    notation = StringField('备注：')
    fee_submit = SubmitField('提交')
