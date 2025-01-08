from flask import Flask, render_template
import requests

app = Flask(__name__)

NPOINT_URL = "https://api.npoint.io/2440b480cbe39e1b5c71"

@app.route('/')
def home():
    npoint_response = requests.get(NPOINT_URL).json()
    return render_template("index.html", posts = npoint_response)

@app.route('/post/<int:blog_id>')
def post(blog_id):
    npoint_response = requests.get(NPOINT_URL).json()

    # blog_id에 해당하는 포스트 찾기
    post = None
    for p in npoint_response:
        if p["id"] == blog_id:
            post = p
            break  # 조건을 만족하는 첫 번째 포스트를 찾으면 루프 종료

    # 포스트가 없으면 404 에러 반환
    if not post:
        return "<h1>Post Not Found</h1>", 404

    # 포스트 데이터를 템플릿에 전달
    return render_template("post.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)
