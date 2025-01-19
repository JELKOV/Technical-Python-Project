import requests
from flight_data import FlightData
from config import AMADEUS_APP_KEY, AMADEUS_APP_SECRET

class FlightSearch:
    """
    Amadeus API와 통신하여 IATA 코드 검색 및 항공편 데이터를 가져오는 클래스
    """
    def __init__(self):
        self.token = None  # Amadeus API 토큰 초기화
        self.token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"  # 토큰 발급 URL
        self.city_search_url = "https://test.api.amadeus.com/v1/reference-data/locations"  # 도시 검색 URL
        self.flight_search_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"  # 항공편 검색 URL
        self.token = self.get_access_token()  # 토큰 발급 및 저장

    def get_access_token(self):
        """
        Amadeus API에 토큰 요청
        """
        response = requests.post(
            self.token_url,  # 토큰 요청 URL
            data={
                "grant_type": "client_credentials",  # 인증 방식: client_credentials
                "client_id": AMADEUS_APP_KEY,  # Amadeus API Key
                "client_secret": AMADEUS_APP_SECRET  # Amadeus API Secret
            }
        )
        response.raise_for_status()  # 요청 실패 시 예외 발생
        return response.json()["access_token"]  # JSON 응답에서 토큰 추출

    def get_iata_code(self, city_name):
        """
        도시 이름을 기반으로 IATA 코드를 검색
        """
        headers = {"Authorization": f"Bearer {self.token}"}  # 인증 헤더 설정
        params = {"keyword": city_name, "subType": "CITY"}  # 검색 매개변수 설정
        response = requests.get(self.city_search_url, headers=headers, params=params)  # IATA 코드 요청

        # 토큰 만료 시 새로운 토큰 발급 후 재시도
        if response.status_code == 401:
            self.token = self.get_access_token()
            headers["Authorization"] = f"Bearer {self.token}"
            response = requests.get(self.city_search_url, headers=headers, params=params)

        response.raise_for_status()  # 요청 실패 시 예외 발생
        data = response.json()  # JSON 응답 데이터를 파싱

        # 검색 결과가 없을 경우 None 반환
        if not data.get("data"):
            print(f"No IATA code found for city: {city_name}")
            return None

        # 첫 번째 결과의 IATA 코드 반환
        iata_code = data["data"][0]["iataCode"]
        print(f"Found IATA code for {city_name}: {iata_code}")
        return iata_code

    def search_flights(self, origin, destination, date_from, date_to):
        """
        주어진 출발지와 목적지 간의 항공권을 검색하고 동적으로 날짜를 설정.
        """
        url = self.flight_search_url
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": date_from,
            "returnDate": date_to,
            "adults": 1,
            "currencyCode": "KRW",
            "max": 10  # 최대 10개 항공편 검색
        }

        try:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 401:
                # 토큰 만료 처리
                print("Token expired. Fetching a new token...")
                self.token = self.get_access_token()
                headers["Authorization"] = f"Bearer {self.token}"
                response = requests.get(url, headers=headers, params=params)

            response.raise_for_status()
            data = response.json()

            # 검색 결과가 없을 경우 처리
            if not data.get("data"):
                print(f"No flights found from {origin} to {destination}.")
                return None

            # 첫 번째 검색 결과에서 동적으로 날짜 추출
            flight_info = data["data"][0]
            departure_date = flight_info["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight_info["itineraries"][0]["segments"][-1]["arrival"]["at"].split("T")[0]

            print(f"Dynamic Dates: Departure: {departure_date}, Return: {return_date}")

            return {
                "price": flight_info["price"]["total"],
                "departure_date": departure_date,
                "return_date": return_date
            }

        except requests.exceptions.HTTPError as e:
            print(f"Error details: {e.response.text}")
            return None

    def search_flights_for_date(self, origin, destination, departure_date, return_date):
        """
        특정 출발 날짜 및 귀환 날짜에 대해 항공편 검색
        """
        url = self.flight_search_url
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "returnDate": return_date,
            "adults": 1,
            "currencyCode": "KRW",
            "max": 5
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 401:
                self.token = self.get_access_token()
                headers["Authorization"] = f"Bearer {self.token}"
                response = requests.get(url, headers=headers, params=params)

            response.raise_for_status()
            data = response.json()
            return data

        except requests.exceptions.HTTPError as e:
            print(f"Error details: {e.response.text}")
            return None