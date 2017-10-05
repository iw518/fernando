#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      __init__.py
# date:         2016-07-19
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------

from flask import Blueprint

from .analysis import analysis as analysis_blueprint
from .archiving import archiving as archiving_blueprint
from .audit import audit as audit_blueprint
from .auth import auth as auth_blueprint
from .calc import calc as calc_blueprint
from .hr import hr as hr_blueprint
from .importation import importation as importation_blueprint
from .logginData import logginData as logginData_blueprint
from .order import order as order_blueprint
from .personal import personal as personal_blueprint
from .printing import printing as printing_blueprint
from .setting import setting as setting_blueprint
from .situ import situ as situ_blueprint
from .stats import stats as stats_blueprint
from .trans import trans as trans_blueprint

main = Blueprint('main', __name__)
from . import views
