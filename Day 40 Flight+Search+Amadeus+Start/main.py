import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

# ==================== Set up the Flight Search ====================

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Set your origin airport
ORIGIN_CITY_IATA = "ICN"

# ==================== Update the Airport Codes in Google Sheet ====================

for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        # slowing down requests to avoid rate limit
        time.sleep(2)
print(f"sheet_data:\n {sheet_data}")

data_manager.get_destination_data = sheet_data
data_manager.update_destination_codes()

## 시트 유저정보 가져오기
customer_emails = data_manager.get_customer_emails()
print(f"customer_emails:\n {customer_emails}")
## 이메일 뽑아서 넣기
emails = [customer["3. 이메일을 입력하세요"] for customer in customer_emails]
print(f"emails:\n {emails}")

# ==================== Search for Flights and Send Notifications ====================

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

# 검색 종료일: 2주 뒤
two_weeks_from_today = datetime.now() + timedelta(days=14)

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=two_weeks_from_today,
        is_direct = True
    )

    if not flights or not flights.get("data"):
        print(f"No direct flights found for {destination['city']}. Searching for indirect flights...")
        flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=two_weeks_from_today,
            is_direct=False
        )

    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: {cheapest_flight.price}WON")
    print(cheapest_flight)
    # Slowing down requests to avoid rate limit
    time.sleep(5)

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        print(f"Lower price flight found to {destination['city']}!")

        # Construct email message
        if cheapest_flight.stops == 0:
            message = (f"Low price alert! Only {cheapest_flight.price} KRW to fly from "
                       f"{cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                       f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}.")
        else:
            message = (f"Low price alert! Only {cheapest_flight.price} KRW to fly from "
                       f"{cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                       f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}.\n"
                       f"Flight has {cheapest_flight.stops} stop(s) via {cheapest_flight.stopover_city}.")

        # Send emails to all customers
        notification_manager.send_email(emails, message)

        # notification_manager.send_sms(
        #     message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
        #                  f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
        #                  f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        # )
        # SMS not working? Try whatsapp instead.
        # notification_manager.send_whatsapp(
        #     message_body=f"Low price alert! Only {cheapest_flight.price}WON to fly "
        #                  f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
        #                  f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        # )


