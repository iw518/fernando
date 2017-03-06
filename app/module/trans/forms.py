#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      forms
# date:         2016-08-13
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------
from flask_wtf import Form
from wtforms import StringField, SelectField
from app.module.button import ButtonField

class AccessForm(Form):
    projectNo= SelectField('选择工程')
    submit = ButtonField('导入静力触探')