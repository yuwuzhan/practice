from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp
from ..models import Role, User
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
    name = StringField('你的名字?', validators=[DataRequired()])
    submit = SubmitField('提交')


class EditProfileForm(FlaskForm):
    name = StringField('真实姓名', validators=[Length(0,64)])
    location = StringField('地址', validators=[Length(0,64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1,64),
                                          Email()])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1,64), Regexp('^[\u4e00-\u9fa5]{1,7}$|^[\dA-Za-z_]{1,14}$', 0,
                                             '输入不符合标准')])
    confirmed = BooleanField('授权')
    role = SelectField('用户', coerce=int)
    name = StringField('真实姓名', validators=[Length(0,64)])
    location = StringField('地址',validators=[Length(0,64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise  ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被注册')


class PostForm(FlaskForm):
    body = PageDownField("想写点什么？", validators=[DataRequired()])
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    body = StringField('填写你的评论', validators=[DataRequired()])
    submit = SubmitField('提交')
