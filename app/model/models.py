#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      models.py
# date:         2016-07-19
# copyright:    copyright  2016 Xu, Aiwu
# --
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), unique=True)
    fullname = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(11), unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, nickname, fullname, email, phone, password):
        self.nickname = nickname
        self.fullname = fullname
        self.email = email
        self.phone = phone
        self.password = password

    def find_projects(self, job_id=4):
        team = Team.query.filter_by(job_id=job_id, user_id=self.id).first()
        registrations = Registration.query.filter_by(team_id=team.id).all()
        projects = []
        for registration in registrations:
            project = Project.query.filter_by(id=registration.project_id).first()
            projects.append(project)
        return projects

    @property
    def __repr__(self):
        return '<User %r>' % self.fullname

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verifypassword(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique=True)
    fullname = db.Column(db.String(64))
    description = db.Column(db.String(64))
    duties = db.Column(db.Integer)
    users = db.relationship('User', secondary='teams', backref=db.backref('jobs', lazy='select'),
                            lazy='select')

    @staticmethod
    def insert_jobs():
        jobs = {
            'Worker': ('作业班组', '负责现场作业', Duty.WORK),
            'TestManager': ('试验负责人', '负责室内试验', Duty.TEST | Duty.MANAGE),
            'TestAuditor': ('试验审核人', '负责审核土工报告', Duty.TEST | Duty.AUDIT),
            'ProjectAssistant': ('项目助理', '辅助项目经理开展工作', Duty.WORK | Duty.TEST | Duty.ASSISTANT),
            'ProjectAuditor': ('项目审核人', '负责勘察报告审核', Duty.WORK | Duty.TEST | Duty.AUDIT),
            'AuthorizingPerson': ('项目审定人', '负责勘察报告审定', Duty.WORK | Duty.TEST | Duty.AUTHORIZE),
            'ProjectManager': ('项目经理', '全面管理项目', Duty.WORK | Duty.TEST | Duty.MANAGE)
        }
        for key in jobs:
            job = Job.query.filter_by(nickname=key).first()
            if job is None:
                job = Job(nickname=key)
            job.fullname = jobs[key][0]
            job.description = jobs[key][1]
            job.duties = jobs[key][2]
            db.session.add(job)
        db.session.commit()


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='team')

    def __init__(self, job_id, user_id):
        self.job_id = job_id
        self.user_id = user_id
        if Team.query.filter_by(job_id=job_id, user_id=user_id).first() is None:
            db.session.add(self)
            db.session.commit()


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique=True)
    fullname = db.Column(db.String(64))

    profile = db.relationship('Profile', uselist=False)

    opinions = db.relationship('Opinion', backref='project')
    holes = db.relationship('Hole', backref='project')
    registrations = db.relationship('Registration', backref='project')
    techfees = db.relationship('TechFee', backref='project')

    def __init__(self, nickname, fullname):
        self.nickname = nickname
        self.fullname = fullname
        db.session.add(self)
        db.session.commit()
        # commit之后才能生成id
        _profile_ = Profile(project_id=self.id)
        db.session.add(_profile_)
        db.session.commit()

    def find_user(self, job_id=4):
        for reginstration in self.registrations:
            team_id = reginstration.team_id
            team = Team.query.filter_by(id=team_id).first()
            if team.job_id == job_id:
                return User.query.filter_by(id=team.user_id).first()

    def insert_team(self, job_id, user_id):
        job = Job.query.filter_by(id=job_id).first()
        team = Team.query.filter_by(job_id=job.id, user_id=user_id).first()
        registration = Registration.query.filter_by(project_id=self.id, team_id=team.id).first()
        if (registration is None) or (self.find_user(job_id=job_id) is None):
            registration = Registration(project_id=self.id, team_id=team.id)
        registration.project_id = self.id
        registration.team_id = team.id
        db.session.add(registration)
        db.session.commit()


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    phase = db.Column(db.String(8))
    client = db.Column(db.String(32))
    design = db.Column(db.String(32))
    size = db.Column(db.String(100))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    archiving = db.Column(db.Integer, default=0)
    archiving_date = db.Column(db.Date)
    fund_contract_sum = db.Column(db.Integer)
    fund_income_sum = db.Column(db.Integer)
    notation = db.Column(db.String(100))

    # @staticmethod
    # def insert_profile():
    #     for project in Project.query.all():
    #         if project.profile is None:
    #             profile=Profile(project_id=project.id)
    #             db.session.add(profile)
    #     db.session.commit()


class Opinion(db.Model):
    __tablename__ = 'opinions'
    id = db.Column(db.Integer, primary_key=True)
    stage = db.Column(db.String(64))
    content = db.Column(db.Text())
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, project_id, stage, content):
        self.project_id = project_id
        self.stage = stage
        self.content = content


class Registration(db.Model):
    __tablename__ = 'registrations'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    # @classmethod
    # def insert_registration(cls, projectNo, job_name, user_nickname):
    #     project = Project.query.filter_by(nickname=projectNo).first()
    #     job = Job.query.filter_by(name=job_name).first()
    #     user=User.query.filter_by(name=user_nickname).first()
    #     team = Team.query.filter_by(job_id=job.id,user_id=user.id)
    #     registration = cls.query.filter_by(project_id=project.id, team_id=team.id).first()
    #     if registration is None:
    #         registration=cls(project.id,team.id)
    #     registration.project_id = project.id
    #     registration.team_id = team.id
    #     db.session.add(registration)
    #     db.session.commit()


    def findUser(self):
        team = Team.query.filter_by(id=self.team_id).first()
        user = User.query.filter_by(id=team.user_id).first()
        return user.fullname

    def findJob(self):
        team = Team.query.filter_by(id=self.team_id).first()
        job = Job.query.filter_by(id=team.job_id).first()
        return job.fullname


class Permission:
    View = 0x01
    EDIT = 0x08
    UPLOAD = 0x10
    MANAGE = 0x40
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Integer)
    label = db.Column(db.String(64))
    description = db.Column(db.String(64))
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'Guest': ('来宾', '默认账户，只能浏览一般数据', Permission.View, True),
            'CommonUser': ('一般用户', '网站浏览数据编辑', Permission.View | Permission.EDIT, False),
            'AdvancedUser': ('高级用户', '网站浏览数据编辑文件上传', Permission.View | Permission.EDIT | Permission.UPLOAD, False),
            'CommonManager': ('一般管理员', '对项目进行分配', Permission.MANAGE, False),
            'AdvancedManager': ('高级管理员', '对用户数据编辑', Permission.ADMINISTER, False),
            'Administrator': ('网站管理员', '网站管理员', 0xff, False)
        }
        for key in roles:
            role = Role.query.filter_by(name=key).first()
            if role is None:
                role = Role(name=key)
            role.default = roles[key][3]
            role.permissions = roles[key][2]
            role.description = roles[key][1]
            role.label = roles[key][0]
            db.session.add(role)
        db.session.commit()


class TechFee(db.Model):
    __tablename__ = 'techfees'
    id = db.Column(db.Integer, primary_key=True)
    notation = db.Column(db.String(100))
    fee_income = db.Column(db.Integer)
    income_date = db.Column(db.Date)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, project_id, fee_income, income_date, notation):
        self.project_id = project_id
        self.fee_income = fee_income
        self.income_date = income_date
        self.notation = notation


class Duty:
    WORK = 0x01
    TEST = 0x02
    ASSISTANT = 0x04
    MANAGE = 0x08
    AUDIT = 0x10
    AUTHORIZE = 0x10


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
