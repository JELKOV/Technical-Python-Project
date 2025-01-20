import os
import requests
from pprint import pprint
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SHEETY_ID = os.getenv("SHEETY_USERNAME")

SHEETY_PRICES_ENDPOINT = f"https://api.sheety.co/{SHEETY_ID}/flightDeals/prices"

SHEETY_USERS_ENDPOINT = f"https://api.sheety.co/{SHEETY_ID}/flightDeals/users"


class DataManager:

    def __init__(self):
        self.headers = {"Authorization": f"Bearer {os.getenv('SHEETY_PASSWORD')}"}
        self.destination_data = {}

    def get_destination_data(self):
        # Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["prices"]
        # Try importing pretty print and printing the data out again using pprint() to see it formatted.
        pprint(data)
        return self.destination_data

    # In the DataManager Class make a PUT request and use the row id from sheet_data
    # to update the Google Sheet with the IATA codes. (Do this using code).
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=self.headers
            )
            response.raise_for_status()
            print(response.text)

    def get_customer_emails(self):
        response = requests.get(url=SHEETY_USERS_ENDPOINT, headers=self.headers)
        response.raise_for_status()
        return response.json()["users"]