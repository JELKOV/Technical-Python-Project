import requests
from datetime import datetime
import smtplib
import time

# 현재 위치 (서울, 대한민국)
MY_LAT = 126.977966
MY_LONG = 37.566536

# Gmail 계정 정보
MY_EMAIL = "secret"
APP_PASSWORD = "secret"  # 카카오톡 확인


# ISS(국제우주정거장)의 현재 위치를 가져오는 함수
def get_iss_position():
    # ISS 위치 API 호출
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    # 위도와 경도를 추출하여 반환
    iss_lat = float(data["iss_position"]["latitude"])
    iss_lon = float(data["iss_position"]["longitude"])
    return iss_lat, iss_lon


# ISS가 현재 위치에서 ±5도 이내에 있는지 확인하는 함수
def is_close_my_position(iss_latitude, iss_longitude):
    # 현재 위치와 ISS 위치를 비교하여 가까운지 여부 반환
    if MY_LAT - 5 < iss_latitude < MY_LAT + 5 and MY_LONG - 5 < iss_longitude < MY_LONG + 5:
        return True


# 현재 위치가 밤인지 확인하는 함수
def is_dark():
    # Sunrise-Sunset API 호출 파라미터 설정
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    # Sunrise-Sunset API 호출
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    # 일출 및 일몰 시간 (UTC 기준) 추출
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # 현재 시간 (로컬 기준) 가져오기
    time_now = datetime.now().hour

    # 현재 시간이 일출 이전 또는 일몰 이후인 경우 True 반환
    if time_now < sunrise or time_now > sunset:
        return True


# 이메일을 전송하는 함수
def send_email():

    # 이메일 서버 연결 및 전송
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()  # 보안 연결 활성화
        connection.login(user=MY_EMAIL, password=APP_PASSWORD)  # 로그인
        connection.sendmail(
            from_addr=MY_EMAIL,  # 발신자
            to_addrs=MY_EMAIL,  # 수신자 (자기 자신)
            msg="Subject:Look Up!\n\nThe ISS is above you in the sky!"  # 이메일 내용
        )
        print(f"이메일 전송 완료")  # 로그 출력


# 주기적으로 ISS 위치와 조건 확인
start = 0  # 실행 횟수 카운터
while True:
    # ISS의 현재 위치 가져오기
    iss_lat, iss_long = get_iss_position()
    start += 1
    print(f"TestTime: {start}")  # 실행 횟수 출력
    print(f"now lat: {iss_lat}")  # 현재 ISS 위도 출력
    print(f"now long: {iss_long}")  # 현재 ISS 경도 출력

    # ISS가 가까운 위치에 있고, 현재가 밤이라면 이메일 전송
    if is_close_my_position(iss_lat, iss_long) and is_dark():
        send_email()

    # 60초 대기 후 다시 실행
    time.sleep(60)

# 주석
# 1. 매 60초마다 ISS 위치와 일출/일몰 조건을 확인합니다.
# 2. ISS가 현재 위치에서 가까우며, 밤인 경우 이메일을 전송합니다.
# 3. 이메일 전송을 위해 Gmail 계정과 앱 비밀번호를 사용합니다.
