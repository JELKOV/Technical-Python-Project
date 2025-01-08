from flask import Flask, render_template
import random
import datetime
import requests

app = Flask(__name__)

# 기본 페이지
@app.route('/')
def home():
    random_number = random.randint(1, 100)  # 1에서 100 사이의 랜덤 숫자 생성
    current_year = datetime.datetime.now().year  # 현재 연도 가져오기
    return render_template("index.html", num=random_number, CURRENT_YEAR=current_year)

# 이름으로 나이와 성별 예측
@app.route('/guess/<name>')
def guess_name(name):
    agify_response = requests.get(f"https://api.agify.io?name={name}").json()  # 이름으로 나이 예측
    genderize_response = requests.get(f"https://api.genderize.io?name={name}").json()  # 이름으로 성별 예측
    gender = genderize_response.get("gender", "unknown")  # 성별 가져오기
    age = agify_response.get("age", "unknown")  # 나이 가져오기
    return render_template("guess.html", name=name, gender=gender, age=age)

# 블로그 데이터 로드
@app.route('/blog/<num>')
def blog_load(num):
    print(num)  # URL의 숫자 파라미터 출력
    npoint_response = requests.get(f"https://api.npoint.io/2440b480cbe39e1b5c71").json()  # JSON 데이터 가져오기
    return render_template("blog.html", posts=npoint_response)

if __name__ == "__main__":
    app.run(debug=True)


