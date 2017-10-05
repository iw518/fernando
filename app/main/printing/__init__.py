#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      __init__
# date:         2017-08-12
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------
from flask import Blueprint

printing = Blueprint('printing', __name__)
from . import prtcptdata
from . import ztk
from . import pmt
