#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      trans
# date:         2016-08-12
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------

from app import db
from app.models import Project

HOLETYPE={
    'Bore_Hole':(1,'取土孔'),
    'CPT_Hole':(2,'静探孔'),
    'SPT_Hole':(3,'标贯孔'),
    'Shear_Hole':(4,'十字板'),
    'Pump_Hole':(5,'抽水孔'),
    'Precipitation_Hole':(6,'降水孔'),
    'Affusion_Hole':(7,'注水孔'),
    'SidePressure_Hole':(8,'旁压孔'),
    'FlatDilatometer_Hole':(9,'扁铲孔'),
    'Small_Hole':(10,'小孔'),
    'Creek_Hole':(11,'明浜孔'),
    'LDP_Hole':(12,'轻便触探'),
    'WaveVelocity_Hole':(13,'波速孔'),
    'HDP_Hole':(14,'重力触探')
}

class Hole(db.Model):
    __tablename__ = 'holes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    kind = db.Column(db.Integer)
    order=db.Column(db.Integer)
    project_id=db.Column(db.Integer, db.ForeignKey('projects.id'))
    depth=db.Column(db.Float(2))
    elevation=db.Column(db.Float(2))
    water_level=db.Column(db.Float(2))
    x=db.Column(db.Float(4))
    y=db.Column(db.Float(4))

    def __init__(self, name, kind,project_id):
        self.name = name
        self.kind=kind
        self.project_id=project_id


class CPT(db.Model):
    __tablename__ = 'cpts'
    id = db.Column(db.Integer, primary_key=True)
    hole_id=db.Column(db.Integer, db.ForeignKey('holes.id'))
    qc_fs=db.Column(db.BLOB)
    probe_no=db.Column(db.String(64))
    probeHead_area=db.Column(db.Integer)
    probe_fixedRatio=db.Column(db.Float(4))
    test_date=db.Column(db.Date)
    attributes = db.relationship('Hole', uselist=False)

    def __init__(self, hole_id,qc_fs):
        self.hole_id=hole_id
        self.qc_fs = qc_fs

