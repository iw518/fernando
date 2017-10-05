#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      __init__
# date:         2016-08-13
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------
from flask import Blueprint
trans = Blueprint('trans', __name__)
from . import views
