import smtplib

def sending_email(random_quotes):
    my_email = "jaehoahn425@gmail.com"
    password = "tgvevtiqglctiqyh"

    connection = smtplib.SMTP("smtp.gmail.com") # 이메일 회사마다 다르다
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs="ajh4234@yahoo.com",
        msg=f"Subject:Monday Quote\n\n{random_quotes}")
    connection.close()

### WITH AS

# import smtplib
#
# my_email = "jaehoahn425@gmail.com"  # 본인의 Gmail 주소
# password = "tgvevtiqglctiqyh"  # 앱 비밀번호
#
# # 이메일 전송
# with smtplib.SMTP("smtp.gmail.com", port=587) as connection:  # with 구문으로 SMTP 연결
#     connection.starttls()  # TLS 보안 시작
#     connection.login(user=my_email, password=password)  # 로그인
#     connection.sendmail(
#         from_addr=my_email,
#         to_addrs="ajh4234@yahoo.com",
#         msg="Subject:Hello\n\nThis is the body of my email"  # 이메일 제목과 본문
#     )

# Yahoo to Google

# import smtplib
#
# my_email = "ajh4234@yahoo.com"
# password = ""
#
# connection = smtplib.SMTP("smtp.mail.yahoo.com") # 이메일 회사마다 다르다
# connection.starttls()
# connection.login(user=my_email, password=password)
# connection.sendmail(
#     from_addr=my_email,
#     to_addrs="jaehoahn425@gmail.com",
#     msg="Subject:Hello\n\nThis is the body of my email")
# connection.close()

import datetime as dt  # datetime 모듈을 dt라는 별칭으로 가져옴

# 현재 날짜와 시간을 가져옴
now = dt.datetime.now()
# 날짜와 시간을 "YYYY-MM-DD HH:MM:SS" 형식으로 포맷팅
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
# print(formatted_date)  # 예: "2024-12-20 15:30:45"

# 연도, 월, 요일 추출
year = now.year  # 현재 연도 (예: 2024)
month = now.month  # 현재 월 (예: 12)


# 두 날짜 간 차이 계산
start_date = dt.date(2024, 12, 1)  # 시작 날짜: 2024년 12월 1일
end_date = dt.date(2024, 12, 20)  # 종료 날짜: 2024년 12월 20일
delta = end_date - start_date  # 두 날짜의 차이 계산
# print(delta.days)  # 차이를 일(days) 단위로 출력 (예: 19일)

# 현재 UTC 시간 가져오기
now = dt.datetime.now(dt.timezone.utc)  # 현재 UTC 시간
# UTC 시간을 한국 시간(KST, UTC+9)으로 변환
kst = now.astimezone(dt.timezone(dt.timedelta(hours=9)))
# print(kst)  # 한국 시간 출력 (예: "2024-12-20 15:30:45+09:00")

# 오늘 날짜와 요일 출력
today = dt.date.today()  # 오늘 날짜 객체 가져오기 (예: 2024-12-20)
# 요일 리스트 (월요일부터 시작)
weekdays = ["월", "화", "수", "목", "금", "토", "일"]
# 오늘 요일 출력 (숫자로 반환된 weekday 값을 이용하여 문자열로 변환)
# print(f"오늘은 {weekdays[today.weekday()]}요일입니다.")  # 예: "오늘은 금요일입니다."


date_of_birth = dt.datetime(year=1995, month=12, day=15, hour=4)
print(date_of_birth)

import random
# 파일에서 랜덤으로 한 줄을 읽어오는 함수
def get_random_quote(files_path):
    # 파일 열기: open 함수를 사용하여 파일을 읽기 모드("r")로 엶.
    # 인코딩: encoding="utf-8"로 설정하여 한글과 같은 다국어 텍스트를 깨지지 않게 처리함.
    # with 문: 파일을 열고 나서 자동으로 닫아주는 역할을 함. 코드 블록이 끝나면 파일이 안전하게 닫힘.
    # as file: 열어둔 파일 객체를 file이라는 변수에 저장함.
    with open(files_path, "r", encoding="utf-8") as file:
        # 파일의 모든 줄을 읽어서 리스트로 반환.
        # 각 줄은 리스트의 한 요소로 저장됨. 예: ["첫 번째 줄\n", "두 번째 줄\n"]
        lines = file.readlines()  # 모든 줄을 리스트로 읽기
    return random.choice(lines).strip()  # 랜덤으로 한 줄 선택 후 양쪽 공백 제거

# email sending the quote

day_of_week = now.weekday()  # 현재 요일 (월=0, 화=1, ..., 일=6)
# print(day_of_week)  # 예: 4 (금요일)
# print(now)  # 전체 현재 날짜와 시간 출력 (예: "2024-12-20 15:30:45.123456")
if day_of_week == 0:
    # 파일 경로 설정
    file_path = "quotes.txt"  # .txt 파일의 경로

    random_quote = get_random_quote(file_path)
    print(f"랜덤 명언: {random_quote}")
    sending_email(random_quote)
