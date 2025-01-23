from flask import Flask, render_template  # Flask와 템플릿 렌더링을 위한 모듈 임포트
from flask_wtf import FlaskForm  # Flask-WTF 폼 클래스
from wtforms import StringField, PasswordField, SubmitField  # WTForms의 입력 필드
from wtforms.validators import DataRequired, Email, Length  # 입력 필드 유효성 검사를 위한 검증기

# Flask 애플리케이션 설정
app = Flask(__name__)
app.secret_key = "some secret string"  # CSRF 보호를 위한 비밀키 설정

# 로그인 폼 클래스 정의
class LoginForm(FlaskForm):
    # 이메일 입력 필드 (필수 입력 및 이메일 형식 검증)
    email = StringField(label='Email', validators=[
        DataRequired(message="이메일은 필수 입력 사항입니다."),
        Email(message="유효한 이메일을 입력해주세요")
    ])
    # 비밀번호 입력 필드 (필수 입력 및 최소 길이 검증)
    password = PasswordField(label='Password', validators=[
        DataRequired(message="비밀번호는 필수로 입력해야 합니다."),
        Length(min=8, message="비밀번호는 최소 8자리 이상")
    ])
    # 제출 버튼
    submit = SubmitField('Login')

# Flask 애플리케이션 라우트 정의

# 메인 페이지 경로
@app.route("/")
def home():
    # index.html 템플릿 렌더링
    return render_template('index.html')

# 로그인 페이지 경로
@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()  # 로그인 폼 인스턴스 생성
    # 폼 유효성 검사 후 제출 처리
    if login_form.validate_on_submit():
        # 이메일과 비밀번호가 올바른 경우 성공 페이지 렌더링 시작
        if login_form.email.data == "admin@email.com" and login_form.password.data == "12345678":
            return render_template("success.html")
        else:
            # 잘못된 경우 접근 거부 페이지 렌더링
            return render_template("denied.html")
    # 로그인 폼 페이지 렌더링
    return render_template("login.html", form=login_form)

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)  # 디버그 모드로 Flask 앱 실행
