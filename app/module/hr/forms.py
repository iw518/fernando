#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      forms
# date:         2016-12-14
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------

from flask_wtf import Form
from wtforms import StringField, SelectField,FieldList
from wtforms.validators import DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectField
from app.module.button import ButtonField
from app.models import Project, Job, User, Team, Profile


class RegisterForm(Form):
    job_selections=SelectField('职责', coerce=int)
    user_selections=SelectField('人员', coerce=int)
    submit = ButtonField('确定')

    def __init__(self, *args,**kwargs):
        super(RegisterForm,self).__init__(*args,**kwargs)
        self.job_selections.choices=[(job.id,job.fullname) for job in Job.query.order_by(Job.duties).all() ]
        self.user_selections.choices=[(user.id,user.fullname) for user in User.query.order_by(User.fullname).all()]
