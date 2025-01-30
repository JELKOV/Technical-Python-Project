# Flask 및 필요한 모듈 임포트
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash  # 비밀번호 해싱 및 검증을 위한 라이브러리
from flask_sqlalchemy import SQLAlchemy  # 데이터베이스 ORM
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  # SQLAlchemy 모델을 위한 기본 설정
from sqlalchemy import Integer, String  # 데이터 타입 정의
import os  # 파일 경로를 다루기 위한 os 모듈
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# Flask-Login: 사용자 인증 및 세션 관리

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# 비밀 키 설정 (Flask에서 보안 관련 기능 사용 시 필요, 세션 및 쿠키 보호)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# 데이터베이스 파일 경로 설정 (프로젝트 디렉토리 내 'instance' 폴더에 위치)
base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 실행 중인 파일의 디렉토리 경로
users_db_path = os.path.join(base_dir, "instance", "users.db")  # 사용자 정보 저장 데이터베이스
posts_db_path = os.path.join(base_dir, "instance", "posts.db")  # 게시글 저장 데이터베이스

# Flask-Login 설정
login_manager = LoginManager()  # 로그인 관리자 인스턴스 생성
login_manager.init_app(app)  # Flask 애플리케이션에 로그인 관리자 추가
login_manager.login_view = "login"  # 인증이 필요한 페이지에 접근할 경우 리디렉트할 페이지 설정
login_manager.login_message = "⚠ 로그인 후 이용 가능합니다."
login_manager.login_message_category = "warning"

# SQLAlchemy 기본 설정 및 여러 데이터베이스 바인딩 설정
class Base(DeclarativeBase):
    """SQLAlchemy에서 사용할 기본 모델 클래스"""
    pass

# 여러 개의 데이터베이스 사용 설정 (users.db, posts.db)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{users_db_path}"  # 기본 데이터베이스 URI 설정
app.config['SQLALCHEMY_BINDS'] = {
    'users': f'sqlite:///{users_db_path}',   # 사용자 관련 데이터 저장
    'posts': f'sqlite:///{posts_db_path}'    # 게시글 관련 데이터 저장
}

# SQLAlchemy 데이터베이스 객체 생성 및 Flask 애플리케이션에 연결
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# 사용자(User) 모델 정의 (Flask-Login을 위한 UserMixin 상속)
class User(db.Model, UserMixin):
    """사용자 모델 (users.db에 저장됨)"""
    __bind_key__ = 'users'  # users.db를 사용하도록 설정
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # 사용자 ID (기본 키)
    email: Mapped[str] = mapped_column(String(100), unique=True)  # 이메일 (고유 값)
    password: Mapped[str] = mapped_column(String(100))  # 비밀번호 (해싱되어 저장)
    name: Mapped[str] = mapped_column(String(1000))  # 사용자 이름

# 게시글(Post) 모델 정의
class Post(db.Model):
    """게시글 모델 (posts.db에 저장됨)"""
    __bind_key__ = 'posts'  # posts.db를 사용하도록 설정
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # 게시글 ID (기본 키)
    title: Mapped[str] = mapped_column(String(255), nullable=False)  # 게시글 제목
    content: Mapped[str] = mapped_column(String(5000), nullable=False)  # 게시글 내용

# 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()  # 모든 테이블 생성

# Flask-Login에서 사용자 로드를 위한 함수 정의
@login_manager.user_loader
def load_user(user_id):
    """사용자 ID로 사용자를 로드하는 함수"""
    return User.query.get(int(user_id))

# 홈 페이지 라우트
@app.route('/')
def home():
    """메인 페이지"""
    return render_template("index.html", logged_in=current_user.is_authenticated)

# 회원가입 라우트
@app.route('/register', methods=['GET', 'POST'])
def register():
    """회원가입 기능"""
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        # 이미 등록된 이메일인지 확인
        if User.query.filter_by(email=email).first():
            flash('⚠ 이미 등록된 이메일입니다. 다시 회원가입하세요.', 'warning') # 경고 메세지 표기
            return redirect(url_for('register'))  # 회원가입 페이지로 리디렉트

        # 비밀번호 해싱 후 저장
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(email=email, name=name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # 회원가입 후 자동 로그인
        login_user(new_user)
        flash('✅ 회원가입이 완료되었습니다. 환영합니다!', 'success')
        return redirect(url_for('secrets'))  # 로그인 후 secrets 페이지로 이동

    return render_template("register.html")

# 로그인 라우트
@app.route('/login', methods=['GET', 'POST'])
def login():
    """사용자 로그인 기능"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()  # 사용자가 DB에 존재하는지 확인

        # 이메일이 존재하지 않는 경우
        if not user:
            flash('⚠ 이메일이 존재하지 않습니다. ID를 확인하세요.', 'warning')
            return redirect(url_for('login'))

        if user and check_password_hash(user.password, password):  # 비밀번호 확인
            login_user(user)  # 로그인 처리
            flash('🎉 로그인 성공! 환영합니다.', 'success')
            return redirect(url_for('secrets'))  # 로그인 성공 시 secrets 페이지로 이동
        else:
            flash('🚨 비밀번호가 틀렸습니다. 다시 시도하세요.', 'danger')
            return redirect(url_for('login'))

    return render_template("login.html", logged_in=current_user.is_authenticated)

# 로그아웃 라우트
@app.route('/logout')
@login_required  # 로그인한 사용자만 접근 가능
def logout():
    """사용자 로그아웃 기능"""
    logout_user()  # 현재 사용자 로그아웃
    flash("👋 로그아웃되었습니다.", 'info')  # 로그아웃 메시지 표시
    return redirect(url_for('home'))  # 홈 페이지로 이동

# 비밀 페이지 라우트 (로그인한 사용자만 접근 가능)
@app.route('/secrets')
@login_required  # 로그인한 사용자만 접근 가능
def secrets():
    """로그인한 사용자만 접근 가능한 페이지"""
    return render_template("secrets.html", name=current_user.name, logged_in=True)

# 파일 다운로드 라우트 (로그인한 사용자만 접근 가능)
@app.route('/download')
@login_required  # 로그인한 사용자만 접근 가능
def download():
    """로그인한 사용자만 파일 다운로드 가능"""
    return send_from_directory(
        'static/files',  # 파일이 위치한 디렉토리
        'cheat_sheet.pdf',  # 다운로드할 파일 이름
        as_attachment=True  # 브라우저에서 파일을 다운로드하도록 설정
    )

# 애플리케이션 실행
if __name__ == "__main__":
    app.run(debug=True)
