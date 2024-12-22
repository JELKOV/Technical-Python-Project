from flask import Flask, render_template, request  # Flask, 템플릿 렌더링 및 HTTP 요청 데이터 처리를 위한 모듈 가져오기

# Flask 애플리케이션 생성
app = Flask(__name__)

# 루트 경로('/')에 대한 라우팅 설정
@app.route('/')
def home():
    # "index.html" 파일을 렌더링하여 반환
    return render_template("index.html")

# '/login' 경로에 POST 요청이 들어올 때 실행될 함수
@app.route('/login', methods=["POST"])
def receive_data():
    # 클라이언트가 보낸 폼 데이터에서 'username'과 'password' 값 가져오기
    name = request.form["username"]
    password = request.form["password"]
    # HTML로 사용자 이름과 비밀번호를 응답
    return f"<h1>Name: {name}, Password: {password}</h1>"

# 애플리케이션 실행
if __name__ == '__main__':
    # 디버그 모드를 활성화하고 로컬 서버 실행
    app.run(debug=True)
