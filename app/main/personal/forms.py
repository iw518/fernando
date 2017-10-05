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


class UserForm(Form):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
