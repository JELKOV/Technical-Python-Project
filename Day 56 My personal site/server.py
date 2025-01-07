from flask import Flask, render_template

# Flask app 생성
app = Flask(__name__)

# 홈 경로 설정
@app.route('/')
def home():
    return render_template("index.html")

# Flask app 실행
if __name__ == '__main__':
    app.run(debug=True)