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
        response.raise_for_status()  # 오류 발생 시 예외 처리
        sheet_data = response.json()  # JSON 응답 데이터를 딕셔너리로 변환
        pprint(sheet_data)  # 데이터 출력
        return sheet_data

    def update_data(self, row_id, iata_code):
        """
        특정 행(row)의 IATA 코드를 업데이트하는 메서드
        """
        body = {
            "price": {
                "iataCode": iata_code  # 업데이트할 IATA 코드 값 설정
            }
        }

        # PUT 요청으로 특정 행(row)의 데이터를 업데이트
        response = requests.put(
            f"{self.url}/{row_id}",  # 행 ID를 URL에 포함
            json=body,  # 요청 본문에 JSON 데이터 포함
            headers=self.headers  # 인증 헤더 포함
        )
        response.raise_for_status()  # 오류 발생 시 예외 처리
        print(response.text)  # 응답 본문 출력
        print(f"Updated row {row_id} with IATA code: {iata_code}")
