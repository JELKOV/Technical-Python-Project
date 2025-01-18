import requests
from flight_data import FlightData
from config import AMADEUS_APP_KEY, AMADEUS_APP_SECRET

class FlightSearch:
    """
    Amadeus API와의 통신을 담당하는 클래스
    """
    def __init__(self):
        self.token = None  # 초기 토큰 설정
        self.token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"  # 토큰 발급 URL
        self.city_search_url = "https://test.api.amadeus.com/v1/reference-data/locations"  # 도시 검색 URL
        self.flight_search_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"  # 항공권 검색 URL
        self.token = self.get_access_token()  # 토큰 발급 및 저장

    def get_access_token(self):
        """
        Amadeus API에 토큰을 요청하는 메서드
        """
        response = requests.post(
            self.token_url,  # 토큰 요청 URL
            data={
                "grant_type": "client_credentials",  # 인증 방식
                "client_id": AMADEUS_APP_KEY,  # Amadeus API Key
                "client_secret": AMADEUS_APP_SECRET  # Amadeus API Secret
            }
        )
        response.raise_for_status()  # 오류 발생 시 예외 처리
        return response.json()["access_token"]  # 액세스 토큰 반환

    def get_iata_code(self, city_name):
        """
        도시 이름을 기반으로 IATA 코드를 반환하는 메서드
        """
        headers = {"Authorization": f"Bearer {self.token}"}  # 인증 헤더 설정
        params = {"keyword": city_name, "subType": "CITY"}  # 요청 매개변수 설정
        response = requests.get(self.city_search_url, headers=headers, params=params)  # GET 요청

        # 토큰 만료 시 새로 발급
        if response.status_code == 401:
            self.token = self.get_access_token()
            headers["Authorization"] = f"Bearer {self.token}"
            response = requests.get(self.city_search_url, headers=headers, params=params)

        response.raise_for_status()  # 오류 발생 시 예외 처리
        data = response.json()  # JSON 응답 데이터를 딕셔너리로 변환

        # 결과가 없을 경우 처리
        if not data.get("data"):
            print(f"No IATA code found for city: {city_name}")
            return None

        # 첫 번째 결과의 IATA 코드 반환
        iata_code = data["data"][0]["iataCode"]
        print(f"Found IATA code for {city_name}: {iata_code}")
        return iata_code

    def search_flights(self, origin, destination, date_from, date_to):
        """
        주어진 기간 내에서 가장 저렴한 항공권을 검색합니다.
        """
        url = self.flight_search_url
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": date_from,
            "returnDate": date_to,
            "adults": 1,
            "nonStop": True,
            "currencyCode": "GBP",
            "max": 1,
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 401:
            # 토큰 만료 시 갱신
            self.token = self.get_access_token()
            headers["Authorization"] = f"Bearer {self.token}"
            response = requests.get(url, headers=headers, params=params)

        response.raise_for_status()
        data = response.json()

        # 결과가 없을 경우 처리
        if not data.get("data"):
            print(f"No flights found from {origin} to {destination}.")
            return None

        # JSON 데이터에서 필요한 정보를 추출
        flight_info = data["data"][0]
        price = flight_info["price"]["total"]
        origin_city = flight_info["itineraries"][0]["segments"][0]["departure"]["iataCode"]
        destination_city = flight_info["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
        departure_date = flight_info["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
        return_date = flight_info["itineraries"][0]["segments"][-1]["arrival"]["at"].split("T")[0]

        return FlightData(price, origin, origin_city, destination, destination_city, departure_date, return_date)