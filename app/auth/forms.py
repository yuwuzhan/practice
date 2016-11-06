from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                          Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住登陆状态')
    submit = SubmitField('登陆')


class RegistrationFrom(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                          Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1,64), Regexp('^[\u4e00-\u9fa5]{1,7}$|^[\dA-Za-z_]{1,14}$', 0,
                                                                                   '输入不符合标准！')])
    password = PasswordField('密码', validators=[
        DataRequired(), EqualTo('password2', message='密码必须一致.')])
    password2 = PasswordField('重新输入密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册！')

    def validate_username(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('用户已存在！')
