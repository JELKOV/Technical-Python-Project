from flask import Flask, render_template
import requests

app = Flask(__name__)

# JSON 데이터 가져오기
API_URL = "https://api.npoint.io/55812ea376577b8994ed"
response = requests.get(API_URL)
blog_posts = response.json()


@app.route('/')
def get_all_posts():
    return render_template("index.html", posts=blog_posts)

# 소개 페이지
@app.route("/about")
def about():
    return render_template("about.html")

# 문의 페이지
@app.route("/contact")
def contact():
    return render_template("contact.html")

# 게시글 페이지
@app.route("/post/<int:post_id>")
def post(post_id):
    # 특정 ID와 일치하는 게시물 찾기
    selected_post = None
    for post in blog_posts:
        if post['id'] == post_id:
            selected_post = post
            break
    return render_template("post.html", post=selected_post)

if __name__ == "__main__":
    app.run(debug=True)