from flask import Flask, render_template, request
import requests
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # 폼 데이터를 받아 처리
        data = request.form
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        message = data["message"]
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])

        # SMTP를 사용하여 이메일 전송
        send_email(name, email, phone, message)

        # POST 요청에서는 "성공적으로 메시지가 전송됨" 상태 전달
        return render_template("contact.html", success=True)
    # GET 요청에서는 기본 페이지 렌더링
    return render_template("contact.html", success=False)

def send_email(name, email, phone, message):
    my_email = "my-email@gmail.com"
    password = "password"

    # 이메일 메시지 생성
    msg = MIMEMultipart()
    msg["From"] = my_email
    msg["To"] = my_email
    msg["Subject"] = "New Contact Form Submission"

    # 이메일 본문 작성
    email_body = (
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
        f"Message:\n{message}"
    )

    # 본문에 UTF-8 인코딩 설정
    msg.attach(MIMEText(email_body, "plain", "utf-8"))

    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=msg.as_string()  # 메시지를 문자열로 변환 후 전송
            )
        print("이메일 전송 성공")
    except Exception as e:
        print(f"이메일 전송 실패: {e}")

# @app.route("/form-entry", methods=["POST"])
# def receive_data():
#     name = request.form["name"]
#     print(name)
#     email = request.form["email"]
#     print(email)
#     phone = request.form["phone"]
#     print(phone)
#     message = request.form["message"]
#     print(message)
#     return f"<h1>Successfully sent your message</h1>"

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
