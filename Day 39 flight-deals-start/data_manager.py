import requests
from pprint import pprint
from config import SHEETY_ID_URL, SHEETY_TOKEN

class DataManager:
    """
    Google Sheet와의 통신을 담당하는 클래스
    """
    def __init__(self):
        # Sheety API 엔드포인트 및 인증 헤더 설정
        self.url = f"https://api.sheety.co/{SHEETY_ID_URL}/flightDeals/prices"
        self.headers = {"Authorization": f"Bearer {SHEETY_TOKEN}"}

    def get_data(self):
        """
        Google Sheet에서 데이터를 가져오는 메서드
        """
        response = requests.get(self.url, headers=self.headers)  # GET 요청
        response.raise_for_status()  # 요청 실패 시 예외 발생
        sheet_data = response.json()  # JSON 응답 데이터를 딕셔너리로 변환
        pprint(sheet_data)  # 디버깅용 데이터 출력
        return sheet_data

    def update_data(self, row_id, field_name, value):
        """
        특정 행(row)의 데이터를 업데이트하는 메서드
        """
        body = {
            "price": {
                field_name: value
            }
        }

        try:
            # URL 생성 및 디버깅용 출력
            url = f"{self.url}/{row_id}"
            print(f"Updating URL: {url}")
            print(f"Request body: {body}")

            # PUT 요청
            response = requests.put(
                url,
                json=body,
                headers=self.headers
            )
            response.raise_for_status()  # 요청 실패 시 예외 발생
            print(f"Updated row {row_id} - {field_name}: {value}")
        except requests.exceptions.HTTPError as e:
            print(f"HTTPError: {e.response.text}")  # 오류 내용 출력
            raise
