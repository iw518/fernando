from flask_wtf import Form
from sqlalchemy_utils import PhoneNumber
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp,ValidationError
import flask_sqlalchemy as sa
from app.models import User
from app.module.button import ButtonField


class LoginForm(Form):
    nickname = StringField('用户名', validators=[
        DataRequired('Please enter IDs'),
        Length(min=2, max=25, message='length must between 4 and 25')
    ])
    password = PasswordField('密码', validators=[
        DataRequired()
    ])
    remember_me = BooleanField('记住我')
    submit =ButtonField('登陆')


class RegisterForm(Form):
    email = StringField('电子邮箱', validators=[DataRequired('Please enter email'), Length(3, 64), Email()])
    nickname=StringField('用户名', validators=[DataRequired(), Length(2, 25), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                                                                       'UserName must have only letters,'
                                                                                       'Numbers,dots or underscores'
                                                                                       )])
    phone = StringField('手机号码', validators=[DataRequired(), Length(11), Regexp('^1[0-9]{10}$',0,
                                                                                       '手机号码必须是11位数字'
                                                                                       )])
    fullname = StringField('姓名', validators=[DataRequired(), Length(2, 25)])
    password=PasswordField('密码',validators=[DataRequired(),EqualTo('password2',message='Password must match.')])
    password2 = PasswordField('再次确认密码',
                             validators=[DataRequired()])


    submit= SubmitField('注册')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered!')

    def validata_nickname(self,field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('username already in use!')
