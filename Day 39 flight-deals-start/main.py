from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta


# 주요 변수 초기화
today = datetime.today()
print(today)
six_months_from_now = today + timedelta(days=180)
print(six_months_from_now)

# 클래스 인스턴스 초기화
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

def update_iata_codes(sheet_data):
    """
    Google Sheet에서 도시 이름을 기반으로 IATA 코드를 검색하고 업데이트합니다.
    """
    for row in sheet_data["prices"]:
        if not row["iataCode"]:  # IATA 코드가 비어 있는 경우 처리
            city_name = row["city"]
            print(f"Searching IATA code for city: {city_name}")

            try:
                iata_code = flight_search.get_iata_code(city_name)

                if not iata_code or iata_code == "N/A":
                    print(f"Invalid IATA code for {city_name}. Skipping update.")
                    data_manager.update_data(row["id"], "iataCode", "N/A")
                    continue

                row["iataCode"] = iata_code
                data_manager.update_data(row["id"], "iataCode", iata_code)
            except Exception as e:
                print(f"Error fetching IATA code for {city_name}: {e}")
                data_manager.update_data(row["id"], "iataCode", "N/A")


def search_and_update_flight_prices(sheet_data):
    """
    출발 및 귀환 날짜를 순회하며 항공권 최저가 검색 및 업데이트
    """
    for row in sheet_data["prices"]:
        city_name = row["city"]
        iata_code = row["iataCode"]
        current_lowest_price = float(row["lowestPrice"]) if row["lowestPrice"] != "N/A" else float("inf")

        if not iata_code or iata_code == "N/A":
            print(f"Skipping flight search for {city_name} due to missing IATA code.")
            continue

        print(f"Searching flights for {city_name} ({iata_code})")

        cheapest_price = None
        best_departure_date = None
        best_return_date = None

        # 출발 및 귀환 날짜 순회
        for days_offset in range(0, 180, 7):  # 6개월 동안 주 단위로 탐색
            departure_date = (today + timedelta(days=days_offset)).strftime("%Y-%m-%d")
            return_date = (today + timedelta(days=days_offset + 7)).strftime("%Y-%m-%d")

            flight_data = flight_search.search_flights_for_date(
                origin="ICN",
                destination=iata_code,
                departure_date=departure_date,
                return_date=return_date
            )

            if flight_data and "data" in flight_data and flight_data["data"]:
                price = float(flight_data["data"][0]["price"]["total"])
                print(f"Found flight price for {city_name}: {price}")
                if cheapest_price is None or price < cheapest_price:
                    cheapest_price = price
                    best_departure_date = departure_date
                    best_return_date = return_date
                    print(f"cheapest Price: {cheapest_price} best_departure_date: {best_departure_date} best_return_date: {best_return_date}")

            # 최저가와 기존 Google Sheet 가격 비교
        if cheapest_price and cheapest_price < current_lowest_price:
            print(f"New cheapest flight for {city_name}: ₩{cheapest_price}")
            print(f"Best dates: Departure - {best_departure_date}, Return - {best_return_date}")
            data_manager.update_data(row["id"], "lowestPrice", cheapest_price)
            data_manager.update_data(row["id"], "departureDate", best_departure_date)
            data_manager.update_data(row["id"], "returnDate", best_return_date)
        else:
            print(f"No cheaper flights found for {city_name}. Keeping existing price: ₩{current_lowest_price}")



def notify_cheaper_flights(sheet_data):
    """
    Google Sheet에 저장된 데이터를 기반으로 WhatsApp 알림을 전송합니다.
    """
    for row in sheet_data["prices"]:
        city_name = row["city"]
        iata_code = row["iataCode"]
        lowest_price = row["lowestPrice"]
        departure_date = row["departureDate"]  # Google Sheet에서 출발 날짜 가져오기
        return_date = row["returnDate"]  # Google Sheet에서 귀환 날짜 가져오기

        # IATA 코드와 최저가 정보가 없는 경우 건너뜀
        if not iata_code or iata_code == "N/A" or not lowest_price or lowest_price == "N/A":
            print(f"Skipping notification for {city_name} due to missing data.")
            continue

        # 알림 메시지 생성
        message = (
            f"Deal Alert! 🎉\n"
            f"Price: ₩{lowest_price}\n"
            f"From: ICN\n"
            f"To: {iata_code} ({city_name})\n"
            f"Departure: {departure_date}\n"
            f"Return: {return_date}\n"
            f"Book now to grab the deal!"
        )

        # WhatsApp 메시지 전송
        notification_manager.send_whatsapp(message)
        print(f"Notification sent for {city_name}!")



# 실행 흐름
if __name__ == "__main__":
    sheet_data = data_manager.get_data()
    update_iata_codes(sheet_data)
    search_and_update_flight_prices(sheet_data)
    notify_cheaper_flights(sheet_data)
