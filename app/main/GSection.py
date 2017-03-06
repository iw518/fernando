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
from .GHole import *

class Section:
    def __init__(self,name=''):
        self.name = name
        self._items=[]

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self,value):
        self._items.append(value)

    @property
    def holes(self):
        return [hole for hole, distance in self._items]

    def to_json(self):
        dict={}
        for key,value in self.__dict__.items():
            if isinstance(value,str) or isinstance(value,int) or isinstance(value,float):
                dict[key]=value
            elif isinstance(value,list):
                items=[]
                for item in value:
                    if isinstance(item[0],Hole):
                        items.append({"hole":item[0].to_json(),"distance":item[1]})
                dict['items'] =items
        return dict