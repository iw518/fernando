#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      xml
# date:         2016-07-19
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------
import os

ROOTDIR = os.path.abspath(os.path.dirname(__file__))
CONFDIR = os.path.abspath(os.path.join(ROOTDIR, 'app', 'xml'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    CSRF_ENABLED = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FERNANDO_MAIL_SUBJECT_PREFIX = '[fernando]'
    FERNANDO_MAIL_SENDER = 'fernando admin <iw518@163.com>'
    FERNANDO_ADMIN = os.environ.get('FERNANDO_ADMIN')
    UPLOAD_FOLDER = os.path.join(ROOTDIR, 'upload')
    TEMP_FOLDER = os.path.join(ROOTDIR, 'tmp')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(ROOTDIR, 'database', 'fernando-dev.db')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(ROOTDIR, 'database', 'fernando-test.db')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(ROOTDIR, 'database', 'fernando.db')


config = {
    'development_config': DevelopmentConfig,
    'testing_config': TestingConfig,
    'production_config': ProductionConfig,
    'default': DevelopmentConfig
}


def cleandir(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            file = os.path.join(root, filename)
            os.remove(file)
        for dir in dirs:
            cleandir(os.path.join(root, dir))
