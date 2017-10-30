#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      utility
# date:         2017-10-05
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------
import xml

import os

from config import XMLDIR


def read_xml(filename, dirname=XMLDIR):
    file = os.path.join(dirname, filename + '.xml')
    dom = xml.dom.minidom.parse(file)
    root = dom.documentElement
    nodes = root.childNodes
    return nodes
