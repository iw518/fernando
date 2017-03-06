#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      forms
# date:         2016-12-15
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------

from flask_wtf import Form
from wtforms import StringField, SelectField,FieldList
from wtforms.validators import DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectField
from app.module.button import ButtonField
from app.models import Project, Job, User, Team, Profile


class UserForm(Form):

    def __init__(self, *args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
