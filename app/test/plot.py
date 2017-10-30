#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      plot
# date:         2017-10-04
# copyright:    copyright  2017 Xu, Aiwu
# -------------------------------------------------------------------------------
from bezier import *
from matplotlib import pyplot as plt

from app.services.core import *


# 画图框函数
def frame_4corners(width, height, left_margin=10,
                   top_margin=10,
                   bottom_margin=10,
                   right_margin=10):
    # abbreviation of coordinate point:{lef_top:lt,left_bottom:lb,right_top:rt,right_bottom:rb}
    # left bottom corner is zero point
    lt_point = AcPoint(left_margin, height - top_margin)
    lb_point = AcPoint(left_margin, bottom_margin)
    rt_point = AcPoint(width - right_margin, height - top_margin)
    rb_point = AcPoint(width - right_margin, bottom_margin)
    return lt_point, rt_point, rb_point, lb_point


projectNo = 'K171-2017'
section = find_sections(projectNo)[5]
curves = section.draw_sectionLine()
for hLine in section.hLines:
    plt.plot([hLine[0].x, hLine[1].x], [hLine[0].y, hLine[1].y])

for line in curves:
    for segment in line:
        if len(segment) > 2:
            # points = createCurve(len(segment), *segment)
            points = segment
            for n in range(len(points) - 1):
                plt.plot([points[n].x, points[n + 1].x], [points[n].y, points[n + 1].y])
        else:
            for n in range(len(segment) - 1):
                left_pt = segment[n]
                right_pt = segment[n + 1]
                plt.plot([left_pt.x, right_pt.x], [left_pt.y, right_pt.y])
plt.show()
