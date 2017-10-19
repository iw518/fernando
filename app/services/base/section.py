# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        GLayer
# Purpose:
#
# Author:      Robot of Fernando
#
# Created:     17-06-2015
# Copyright:   (c) Administrator 2015
# Licence:     <GPLV3>
# -------------------------------------------------------------------------------
from .hole import Hole


class Section:
    def __init__(self, name=''):
        self.name = name
        self._items = []

    @property
    def items(self):
        return self._items

    @property
    def holes(self):
        return [hole for hole, accumulate_distance in self._items]

    def to_json(self):
        mydict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
                mydict[key] = value
            elif isinstance(value, list):
                items = []
                for item in value:
                    if isinstance(item[0], Hole):
                        items.append({"hole": item[0].to_json(), "accumulate_distance": item[1]})
                mydict['items'] = items
        return mydict
