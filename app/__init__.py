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

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    from app.model.models import User, Job
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    # attach routes and custom error pages here
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .main import analysis_blueprint, archiving_blueprint, audit_blueprint, auth_blueprint, calc_blueprint, \
        hr_blueprint, importation_blueprint, logginData_blueprint, \
        order_blueprint, personal_blueprint, printing_blueprint, \
        setting_blueprint, stats_blueprint, situ_blueprint, trans_blueprint

    app.register_blueprint(analysis_blueprint, url_prefix="/analysis")
    app.register_blueprint(archiving_blueprint, url_prefix="/archiving")
    app.register_blueprint(audit_blueprint, url_prefix='/audit')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(calc_blueprint, url_prefix="/calc")

    app.register_blueprint(hr_blueprint, url_prefix="/hr")
    app.register_blueprint(importation_blueprint, url_prefix='/importation')
    app.register_blueprint(logginData_blueprint, url_prefix="/logginData")

    app.register_blueprint(order_blueprint, url_prefix="/order")
    app.register_blueprint(personal_blueprint, url_prefix="/personal")
    app.register_blueprint(printing_blueprint, url_prefix='/printing')

    app.register_blueprint(setting_blueprint, url_prefix="/setting")
    app.register_blueprint(situ_blueprint, url_prefix="/situ")
    app.register_blueprint(stats_blueprint, url_prefix="/stats")
    app.register_blueprint(trans_blueprint, url_prefix="/trans")

    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()
        from app.model.models import Role, Job, Profile
        Role.insert_roles()
        Job.insert_jobs()
    return app
