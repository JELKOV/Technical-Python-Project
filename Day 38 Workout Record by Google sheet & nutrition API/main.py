import requests
from datetime import datetime
import json
import os

QUERY = input(f"Tell me which exersice you did?")

NUTRITION_APP_ID = os.getenv("ENV_NUTRITION_APP_ID")
NUTRITION_API_KEY = os.getenv("ENV_NUTRITION_APP_KEY")

url = "https://trackapi.nutritionix.com/v2/natural/exercise"
headers = {
    "x-app-id": NUTRITION_APP_ID,
    "x-app-key": NUTRITION_API_KEY,
    "Content-Type": "application/json"
}
data = {
    "query": QUERY
}

response = requests.post(url, json=data, headers=headers)
print(response.json())


# 모든 운동 정보를 출력하는 함수
def process_exercise_data(data):
    exercises = data.get('exercises', [])

    SHEETY_ID = os.getenv("ENV_SHEETY_ID")

    SHEETY_URL = f'https://api.sheety.co/{SHEETY_ID}/workOutTracking/workouts'
    BEARER_TOKEN = os.getenv("ENV_SHEETY_TOKEN")

    today = datetime.today()
    print(today)

    year_month_day = today.strftime("%Y/%m/%d")
    print(year_month_day)
    time = today.strftime("%H:%M")
    print(time)

    # 운동 정보가 있을 경우 반복 처리
    for exercise in exercises:
        duration = exercise.get('duration_min')
        calories = exercise.get('nf_calories')
        exercise_name = exercise.get('name')

        # 헤더에 Bearer 토큰 추가
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}"
        }

        body = {
            "workout": {
                "date": year_month_day,
                "time": time,
                "exercise": exercise_name,
                "duration": duration,
                "calories": calories
            }
        }

        try:
            response = requests.post(SHEETY_URL, headers=headers, json=body)
            response.raise_for_status()  # HTTP 에러가 발생하면 예외를 발생시킴
            print("Request successful!")
            print(response.json())
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")



# 함수 호출
process_exercise_data(response.json())



