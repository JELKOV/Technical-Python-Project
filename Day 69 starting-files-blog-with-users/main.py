import os
from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_ckeditor import CKEditor
import hashlib
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
# Import your forms from the forms.py
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm

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
app.config['CKEDITOR_PKG_TYPE'] = 'full'
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

# TODO: Configure Flask-Login
# 로그인 매니저 초기화
login_manager = LoginManager()
# 로그인 매니저 초기화
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#  관리자 접근 가능 한 데코레이터
def admin_only(f):
    @wraps(f)  # ✅ 원래 함수의 이름과 문서화 문자열(docstring)을 유지
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            abort(403)  # ✅ 권한이 없으면 403 Forbidden 오류 발생
        return f(*args, **kwargs)  # ✅ 관리자면 원래 함수 실행
    return decorated_function

def generate_gravatar_url(email, size=50):
    """사용자의 이메일을 기반으로 Gravatar URL을 생성"""
    email_hash = hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=retro"

# ✅ BlogPost, User, Comment 모델을 정의하는 코드입니다.

# BlogPost(게시글) 모델
class BlogPost(db.Model):
    """
    BlogPost 모델 (게시글 정보 저장)
    - 각 게시글은 User(작성자)와 연결됨 (1명의 작성자가 여러 개의 게시글을 작성 가능)
    - 각 게시글에는 여러 개의 댓글(Comment)이 달릴 수 있음 (1개의 게시글이 여러 개의 댓글을 가질 수 있음)
    """
    __tablename__ = "blog_posts"

    # ✅ 게시글 ID (기본 키)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # ✅ 게시글 제목
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    # ✅ 게시글 부제목
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    # ✅ 게시글 작성 날짜 (문자열 형식으로 저장)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    # ✅ 게시글 본문 (HTML 저장 가능)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    # ✅ 게시글 이미지 URL
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    ## 외래키
    # ✅ 게시글 작성자의 ID (외래 키) - User 테이블과 연결 USER 1:N POST
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)

    ## 관계설정
    # ✅ 게시글과 작성자의 관계 (1명의 User가 여러 개의 게시글을 작성 가능)
    author = relationship("User", back_populates="posts")
    # ✅ 게시글과 댓글의 관계 (1개의 게시글에 여러 개의 댓글이 달릴 수 있음)
    comments = relationship("Comment", back_populates="post")

# User(사용자) 모델
class User(UserMixin, db.Model):
    """
    User 모델 (사용자 정보 저장)
    - 각 사용자는 여러 개의 게시글(BlogPost)을 작성할 수 있음 (1:N 관계)
    - 각 사용자는 여러 개의 댓글(Comment)을 작성할 수 있음 (1:N 관계)
    """
    __tablename__ = "users"

    # ✅ 사용자 ID (기본 키)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # ✅ 사용자 이메일 (고유 값, 중복 불가)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    # ✅ 비밀번호 해시 (보안 목적)
    password_hash: Mapped[str] = mapped_column(String(250), nullable=False)
    # ✅ 사용자 이름
    name: Mapped[str] = mapped_column(String(250), nullable=False)

    ## 관계 설정
    # ✅ 사용자가 작성한 게시글 목록 (1:N 관계)
    posts = relationship("BlogPost", back_populates="author")
    # ✅ 사용자가 작성한 댓글 목록 (1:N 관계)
    comments = relationship("Comment", back_populates="author")

# Comment(댓글) 모델
class Comment(db.Model):
    """
    Comment 모델 (댓글 정보 저장)
    - 각 댓글은 하나의 게시글(BlogPost)에 속함 (N:1 관계)
    - 각 댓글은 하나의 사용자(User)가 작성 (N:1 관계)
    """
    __tablename__ = "comments"

    # ✅ 댓글 ID (기본 키)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # ✅ 댓글 본문 (HTML 저장 가능)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    
    # 외래키
    # ✅ 댓글 작성자의 ID (외래 키) - User 테이블과 연결  USER 1:N COMMENT
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    # ✅ 댓글이 속한 게시글 ID (외래 키) - BlogPost 테이블과 연결 POST 1:N COMMENT
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('blog_posts.id'), nullable=False)
    
    ## 관계 설정
    # ✅ 댓글 작성자 (User와의 관계, 1명의 User가 여러 개의 댓글 작성 가능)
    author = relationship("User", back_populates="comments")
    # ✅ 댓글이 속한 게시글 (BlogPost와의 관계, 1개의 게시글에 여러 개의 댓글이 달릴 수 있음)
    post = relationship("BlogPost", back_populates="comments")

with app.app_context():
    # db.drop_all()  # 기존 테이블 삭제
    db.create_all()  # 새로운 테이블 생성


# TODO: Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('이미 존재하는 이메일 입니다.', 'danger')
            return redirect(url_for('login')) # 기존 회원이면 로그인 페이지로 리다이렉트
        
        hashed_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            password_hash=hashed_salted_password,
            name=form.name.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user) # 자동 로그인 회원가입후
        flash('회원가입 성공! 로그인해주세요.', 'success')
        return redirect(url_for('get_all_posts'))

    return render_template("register.html", form=form)


# TODO: Retrieve a user from the database based on their email. 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user is None:
            flash('해당 이메일이 존재하지 않습니다. 회원가입을 진행해주세요.', 'danger')
            return redirect(url_for('register'))  # ✅ 존재하지 않는 이메일이면 회원가입으로 리디렉션

        if not check_password_hash(user.password_hash, password):
            flash('비밀번호가 올바르지 않습니다. 다시 시도해주세요.', 'danger')
            return redirect(url_for('login'))  # ✅ 비밀번호 불일치 시 로그인 페이지로 리디렉트
       # 로그인 성공시 세션 유지
        login_user(user)
        flash('로그인 성공!', 'success')
        return redirect(url_for('get_all_posts'))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user() # 사용자 세션 해제
    flash("로그아웃 되었습니다.", "info")
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


# TODO: Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    form = CommentForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("로그인 후 댓글을 작성할 수 있습니다.", "danger")
            return redirect(url_for('login'))
        new_comment = Comment(
            text=form.text.data,
            author=current_user,
            post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))
    return render_template("post.html", post=requested_post, form=form)


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@login_required
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author_id=current_user.id,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
@login_required
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

# ✅ Jinja 템플릿에서 사용할 수 있도록 등록
@app.context_processor
def inject_gravatar():
    return dict(generate_gravatar_url=generate_gravatar_url)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
