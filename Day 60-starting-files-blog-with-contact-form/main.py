from flask import Flask, render_template, request
import requests
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# JSON API로부터 블로그 게시물 데이터를 가져옴
# npoint에서 데이터를 JSON 형식으로 제공
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)

# 홈 페이지
@app.route('/')
def get_all_posts():
    # index.html 템플릿에 게시물 데이터를 전달하여 렌더링
    return render_template("index.html", all_posts=posts)

# 'About' 페이지
@app.route("/about")
def about():
    # about.html 템플릿 렌더링
    return render_template("about.html")

# 'Contact' 페이지 (GET 및 POST 요청 처리)
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":  # 사용자가 폼 데이터를 제출했을 때
        # 폼 데이터를 받아옴
        data = request.form
        name = data["name"]  # 이름
        email = data["email"]  # 이메일
        phone = data["phone"]  # 전화번호
        message = data["message"]  # 메시지
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])

        # 이메일 전송 함수 호출
        send_email(name, email, phone, message)

        # 성공 상태를 전달하며 contact.html 렌더링
        return render_template("contact.html", success=True)

    # GET 요청일 경우 contact.html을 렌더링하고 success 상태는 False
    return render_template("contact.html", success=False)

# 이메일 전송 함수
def send_email(name, email, phone, message):
    my_email = "my-email@gmail.com"  # 본인의 이메일 주소
    password = "password"  # 본인의 이메일 계정 비밀번호

    # 이메일 메시지 생성
    msg = MIMEMultipart()
    msg["From"] = my_email  # 발신자
    msg["To"] = my_email  # 수신자 (본인의 이메일로 보냄)
    msg["Subject"] = "New Contact Form Submission"  # 이메일 제목

    # 이메일 본문 작성
    email_body = (
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
        f"Message:\n{message}"
    )

    # 본문을 UTF-8 인코딩으로 첨부
    msg.attach(MIMEText(email_body, "plain", "utf-8"))

    try:
        # SMTP 서버를 사용하여 이메일 전송
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()  # TLS 암호화 시작
            connection.login(user=my_email, password=password)  # 로그인
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=msg.as_string()  # 메시지를 문자열로 변환 후 전송
            )
        print("이메일 전송 성공")  # 성공 메시지 출력
    except Exception as e:
        # 오류 발생 시 메시지 출력
        print(f"이메일 전송 실패: {e}")

# 특정 게시물 페이지
@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None  # 요청된 게시물을 저장할 변수
    for blog_post in posts:  # 모든 게시물 탐색
        if blog_post["id"] == index:  # 게시물 ID가 일치하면
            requested_post = blog_post  # 해당 게시물 저장
    # post.html 템플릿에 해당 게시물 데이터를 전달하여 렌더링
    return render_template("post.html", post=requested_post)

# 애플리케이션 실행
if __name__ == "__main__":
    app.run(debug=True, port=5001)  # 디버그 모드 활성화 및 포트 설정
