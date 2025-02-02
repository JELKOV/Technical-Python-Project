from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, URL, Email, Length
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# TODO: Create a RegisterForm to register new users
class RegisterForm(FlaskForm):
    email = StringField("이메일", validators=[
        DataRequired(message="이메일을 입력해주세요"),
        Email(message="올바른 이메일 형식이 아닙니다.")
    ])
    password = PasswordField("비밀번호", validators=[
        DataRequired(message="비밀번호를 입력해주세요"),
        Length(min=6, message="비밀번호는 최소 6자 이상이어야 합니다.")
    ])
    name = StringField("이름", validators=[
        DataRequired(message="사용자 명을 입력해주세요"),
        Length(min=3, max=20, message="사용자명은 3자에서 20자 사이여야 합니다.")
    ])
    submit =SubmitField("회원가입")


# TODO: Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    email = StringField("이메일", validators=[
        DataRequired(message="이메일을 입력해주세요"),
        Email(message="올바른 형식이 아닙니다.")
    ])
    password = PasswordField("비밀번호", validators=[
        DataRequired(message="비밀번호를 입력해주세요"),
    ])
    submit = SubmitField("로그인")


# TODO: Create a CommentForm so users can leave comments below posts
class CommentForm(FlaskForm):
    text = CKEditorField("댓글", validators=[
        DataRequired(message="댓글을 입력해주세요"),
    ])
    submit = SubmitField("댓글 입력")