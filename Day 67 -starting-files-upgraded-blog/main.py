from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import os

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['CKEDITOR_PKG_TYPE'] = 'standard'
ckeditor = CKEditor(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance", "posts.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

## 필요시 주석제거후 실행
# with app.app_context():
#     db.create_all()

## CreatePostForm WTF
class CreatePostForm(FlaskForm):
    title = StringField('Blog Title', validators=[DataRequired()])
    subtitle = StringField('Blog Subtitle', validators=[DataRequired()])
    img_url = StringField('Blog Image URL', validators=[DataRequired(), URL()])
    body = CKEditorField('Blog Content', validators=[DataRequired()])
    author = StringField('Blog Author', validators=[DataRequired()])
    submit = SubmitField('Submit')

# 게시글 전체 검색
@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    print(posts)
    return render_template("index.html", all_posts=posts)

# 게시글 하나 검색
@app.route('/post/<int:post_id>')
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post)

# 새로운 게시물을 추가하는 경로
@app.route('/new-post', methods=['GET', 'POST'])
def add_new_post():
    # CreatePostForm 인스턴스를 생성
    form = CreatePostForm()

    # 폼이 제출되었고 유효한 경우
    if form.validate_on_submit():
        print("Form submitted successfully!")  # 디버깅용 출력

        # 새로운 BlogPost 객체 생성
        new_post = BlogPost(
            title=form.title.data,  # 제목
            subtitle=form.subtitle.data,  # 부제목
            date=date.today().strftime("%B %d, %Y"),  # 오늘 날짜를 "월 일, 연도" 형식으로 저장
            img_url=form.img_url.data,  # 이미지 URL
            body=form.body.data,  # 본문 (HTML 형식으로 저장)
            author=form.author.data  # 작성자
        )

        # 데이터베이스에 저장
        with app.app_context():  # Flask 애플리케이션 컨텍스트 사용 (필요 없는 경우 삭제 가능)
            db.session.add(new_post)  # 새로운 게시물 추가
            db.session.commit()  # 변경 사항 저장
        return redirect('/')  # 홈페이지로 리다이렉트

    # 폼 렌더링 (GET 요청 또는 폼 검증 실패 시)
    return render_template("make-post.html", form=form)


# 기존 게시물을 수정하는 경로
@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    # 데이터베이스에서 post_id에 해당하는 게시물 가져오기
    requested_post = BlogPost.query.get(post_id)
    if not requested_post:
        return "Post not found", 404  # 게시물이 없는 경우 404 반환

    # 기존 데이터로 CreatePostForm 인스턴스 초기화
    form = CreatePostForm(
        title=requested_post.title,  # 제목
        subtitle=requested_post.subtitle,  # 부제목
        img_url=requested_post.img_url,  # 이미지 URL
        body=requested_post.body,  # 본문
        author=requested_post.author  # 작성자
    )

    # 폼이 제출되었고 유효한 경우
    if form.validate_on_submit():
        # 기존 게시물 객체의 필드 업데이트
        requested_post.title = form.title.data
        requested_post.subtitle = form.subtitle.data
        requested_post.img_url = form.img_url.data
        requested_post.body = form.body.data
        requested_post.author = form.author.data

        # 데이터베이스에 변경 사항 저장
        db.session.commit()
        # 수정된 게시물의 상세 페이지로 리다이렉트
        return redirect(url_for('show_post', post_id=post_id))

    # 폼 렌더링 (GET 요청 또는 폼 검증 실패 시)
    return render_template("make-post.html", form=form, is_edit=True)

@app.route('/delete-post/<int:post_id>', methods=['POST'])  # DELETE 대신 POST
def delete_post(post_id):
    requested_post = BlogPost.query.get(post_id)

    if not requested_post:
        return "Post not found", 404

    db.session.delete(requested_post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))
# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
