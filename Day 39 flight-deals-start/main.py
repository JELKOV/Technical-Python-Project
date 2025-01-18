import requests
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta

# Datamanager 인스턴스 생성
# Google Sheet와 통신하기 위한 DataManager 클래스 초기화
data_manager = DataManager()

# Google Sheet 데이터를 가져옴
sheet_data = data_manager.get_data()

# FlightSearch 인스턴스 생성
# Amadeus API를 사용하여 IATA 코드를 검색하기 위한 클래스 초기화
flight_search = FlightSearch()

# 현재 날짜 및 6개월 후 날짜 계산
today = datetime.today()
six_months_from_now = today + timedelta(days=180)

# Google Sheet 데이터를 순회하며 각 도시의 IATA 코드 확인
for row in sheet_data["prices"]:
    if not row["iataCode"]:  # IATA 코드가 비어 있는 경우에만 처리
        city_name = row["city"]  # 도시 이름 가져오기
        print(f"Searching IATA code for city: {city_name}")

        # Amadeus API를 사용하여 IATA 코드 검색
        iata_code = flight_search.get_iata_code(city_name)

        # 검색된 IATA 코드를 sheet_data에 업데이트
        row["iataCode"] = iata_code

        # Google Sheet에 IATA 코드 업데이트
        data_manager.update_data(row["id"], iata_code)

    city_name = row["city"]
    iata_code = row["iataCode"]
    print(f"Searching flights for {city_name} ({iata_code})")

    # 항공권 검색
    try:
        flight_data = flight_search.search_flights(
            origin="LON",
            destination=iata_code,
            date_from=today.strftime("%Y-%m-%d"),
            date_to=six_months_from_now.strftime("%Y-%m-%d")
        )

        # 항공권 데이터 파싱
        if flight_data.get("data"):
            offer = flight_data["data"][0]["price"]["total"]
            print(f"Cheapest flight to {city_name}: £{offer}")
            # Google Sheet 업데이트
            data_manager.update_data(row["id"], offer)
        else:
            print(f"No flights found for {city_name}")
            data_manager.update_data(row["id"], "N/A")

    except Exception as e:
        print(f"Error searching flights for {city_name}: {e}")
        data_manager.update_data(row["id"], "N/A")