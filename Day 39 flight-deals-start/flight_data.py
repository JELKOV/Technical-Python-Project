class FlightData:
    """
    항공편 데이터를 구조화하는 클래스
    """
    def __init__(self, price, origin_city, origin_airport, destination_city, destination_airport, departure_date, return_date):
        self.price = price  # 항공권 가격
        self.origin_city = origin_city  # 출발 도시 이름
        self.origin_airport = origin_airport  # 출발 공항 코드
        self.destination_city = destination_city  # 도착 도시 이름
        self.destination_airport = destination_airport  # 도착 공항 코드
        self.departure_date = departure_date  # 출발 날짜
        self.return_date = return_date  # 귀환 날짜

    def __str__(self):
        """
        FlightData 객체의 정보를 문자열로 반환
        """
        return f"Price: {self.price}, From: {self.origin_city} ({self.origin_airport}) To: {self.destination_city} ({self.destination_airport}), Dates: {self.departure_date} - {self.return_date}"