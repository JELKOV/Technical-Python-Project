import requests
import json
from twilio.rest import Client
from datetime import datetime, timedelta

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# alphavantage API KEY
ALPHA_API_KEY = "secrets"

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

url = f'{STOCK_ENDPOINT}?function=TIME_SERIES_DAILY&symbol={STOCK_NAME}&apikey={ALPHA_API_KEY}'
r = requests.get(url)
data = r.json()

print(data)

# JSON 데이터를 보기 좋게 파일로 저장
with open("meta_data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("JSON 데이터가 'meta_data.json' 파일에 저장되었습니다.")

# JSON 데이터 로드
time_series = data["Time Series (Daily)"]

# 날짜 정렬
sorted_dates = sorted(time_series.keys(), reverse=True)
# (1) 어제 폐장가 계산
yesterday_close = float(time_series[sorted_dates[0]]["4. close"])
print(yesterday_close)

# (2) 그저꼐 폐장가 계산
day_before_yesterday_close = float(time_series[sorted_dates[1]]["4. close"])
print(day_before_yesterday_close)

# (3) 차이 비교
price_difference = yesterday_close - day_before_yesterday_close
print(price_difference)

# (4) 변동률 계산하기
percentage_difference = (price_difference / day_before_yesterday_close) * 100
print(percentage_difference)

## STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if abs(percentage_difference) >= 5:
    print("Get News")

    # 현재 날짜 가져오기
    today = datetime.now()

    # 30일 전 날짜 계산
    thirty_days_ago = today - timedelta(days=30)

    # 날짜를 ISO 8601 형식(YYYY-MM-DD)으로 변환
    from_date = thirty_days_ago.strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")

    NEWS_API_KEY = "secrets"
    news_params = {
        "q": COMPANY_NAME,
        "from": from_date,
        "to": to_date,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_data = news_response.json()

    # JSON 데이터를 보기 좋게 파일로 저장
    with open("news_data.json", "w", encoding="utf-8") as file:
        json.dump(news_data, file, indent=4, ensure_ascii=False)

    print("JSON 데이터가 'news_data.json' 파일에 저장되었습니다.")

    # 상위 3개의 뉴스 기사 가져오기
    articles = news_data["articles"][:3]
    print(articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.

    ## 메세지 생성
    # 상승/하락 기호
    symbol = "🔺" if percentage_difference > 0 else "🔻"
    formatted_percentage = f"{symbol}{abs(percentage_difference):.2f}%"

    # 뉴스 메시지 구성
    news_messages = [
        f"""
        TSLA: {formatted_percentage}
        Headline: {article['title']}
        Brief: {article['description']}
        """
        for article in articles
    ]

    # TWILIO
    TWILIO_SID = "secrets"
    TWILIO_AUTH_TOKEN = "secrets"
    FROM_WHATSAPP_NUMBER = 'secrets'
    TO_WHATSAPP_NUMBER = 'secrets'

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    # 메시지 전송
    for message in news_messages:
        try:
            message_whatsapp = client.messages.create(
                from_=FROM_WHATSAPP_NUMBER,
                body=message.strip(),
                to=TO_WHATSAPP_NUMBER,
            )
            print(f"Message sent with SID: {message_whatsapp.sid}")
        except Exception as e:
            print(f"Failed to send message: {e}")
else:
    print("No significant change in stock price.")


