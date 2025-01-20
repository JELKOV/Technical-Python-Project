
class FlightData:

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops, stopover_city):
        """
        Constructor for initializing a new flight data instance with specific travel details.

         Parameters:
        - price: The cost of the flight.
        - origin_airport: The IATA code for the flight's origin airport.
        - destination_airport: The IATA code for the flight's destination airport.
        - out_date: The departure date for the flight.
        - return_date: The return date for the flight.
        - stops: The number of stopovers for the flight (default is 0 for direct flights).
        - stopover_city: The city name of the stopover location (if applicable).
        """
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops
        self.stopover_city = stopover_city

    def __repr__(self):
        return (f"FlightData(price={self.price}, origin={self.origin_airport}, destination={self.destination_airport}, "
                f"out_date={self.out_date}, return_date={self.return_date}, stops={self.stops}, stopover_city={self.stopover_city})")

def find_cheapest_flight(data):
    """
    Parses flight data received from the Amadeus API to identify the cheapest flight option among
    multiple entries.

    Args:
        data (dict): The JSON data containing flight information returned by the API.

    Returns:
        FlightData: An instance of the FlightData class representing the cheapest flight found,
        or a FlightData instance where all fields are 'NA' if no valid flight data is available.

    This function initially checks if the data contains valid flight entries. If no valid data is found,
    it returns a FlightData object containing "N/A" for all fields. Otherwise, it starts by assuming the first
    flight in the list is the cheapest. It then iterates through all available flights in the data, updating
     the cheapest flight details whenever a lower-priced flight is encountered. The result is a populated
     FlightData object with the details of the most affordable flight.
    """

    # Handle empty data if no flight or Amadeus rate limit exceeded
    if data is None or not data['data']:
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A",0,None)

    # Data from the first flight in the json
    first_flight = data['data'][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = first_flight["itineraries"][-1]["segments"][-1]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][-1]["segments"][-1]["arrival"]["at"].split("T")[0]
    stops = len(first_flight["itineraries"][0]["segments"]) - 1  # Number of stops is segments - 1
    stopover_city = None

    if stops > 0:
        stopover_city = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]  # First stopover city

    # Initialize FlightData with first flight
    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, stops, stopover_city)

    for flight in data["data"]:
        price = float(flight["price"]["grandTotal"])
        segments = flight["itineraries"][0]["segments"]
        current_stops = len(segments) - 1
        current_stopover_city = None
        if current_stops > 0:
            current_stopover_city = segments[0]["arrival"]["iataCode"]

        if price < lowest_price:
            lowest_price = price
            origin = segments[0]["departure"]["iataCode"]
            destination = segments[-1]["arrival"]["iataCode"]
            out_date = segments[0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][-1]["segments"][-1]["departure"]["at"].split("T")[0]
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, current_stops, current_stopover_city)

    return cheapest_flight

