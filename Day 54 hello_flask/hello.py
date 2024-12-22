from flask import Flask

# 1. Flask 애플리케이션 생성
app = Flask(__name__)

# 2. 현재 모듈의 이름 출력
print(__name__)

# 3. 루트 URL("/") 라우트 설정
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/bye")
def say_bye():
    return "<p>Say Good bye!</p>"


# 4. 현재 파일이 직접 실행되었을 때 Flask 애플리케이션 실행
if __name__ == "__main__":
    app.run()