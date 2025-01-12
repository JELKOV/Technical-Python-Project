import json
import requests
from twilio.rest import Client
import os

# Twilio API
ACCOUNT_SID = os.environ.get("TWILLIO_SID")
AUTH_TOKEN = os.environ.get("TWILLIO_TOKEN")

# API URL 및 키 설정
BASE_URL = "https://api.openweathermap.org/data/2.8/onecall"
API_KEY = os.environ.get("OWM_API_KEY")

# 내 위치 설정
LAT = 37.566536  # 위도
LON = 126.977966  # 경도

# 요청 파라미터
parameters = {
    "lat": LAT,
    "lon": LON,
    "exclude": "current,minutely,daily",
    "appid": API_KEY  # API 키
}

# API 요청
response = requests.get(BASE_URL, params=parameters)
response.raise_for_status()

# 데이터 출력
data = response.json()

# JSON 데이터를 보기 좋게 파일로 저장
with open("weather_data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("JSON 데이터가 'weather_data.json' 파일에 저장되었습니다.")

# 슬라이스를 사용해 특정 시간대의 데이터를 반복 처리
hourly_data_slice = data["hourly"][7:19]  # 7시부터 18시까지 데이터 슬라이스

# 우산이 필요한지 확인
will_rain = False
for hourly in hourly_data_slice:
    if hourly["weather"][0]["id"] < 700:  # 바로 비교
        will_rain = True
        break  # 조건이 만족되면 반복문 종료

# 결과 출력
if will_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='☔ 비가 올 예정입니다. 우산을 꼭 챙기세요! 오늘도 좋은 하루 되세요! 😊',
        to='whatsapp:+821062734585'
    )
    print(message.sid)
else:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='☀️ 오늘은 비 소식이 없습니다! 마음 편히 외출하세요. 멋진 하루 보내세요! 😄',
        to='whatsapp:+821062734585'
    )
    print(message.sid)
