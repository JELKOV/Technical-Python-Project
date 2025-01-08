import requests

BASE_URL = "http://api.open-notify.org/iss-now.json"

response = requests.get(BASE_URL)
## 너무 많다 !!!
# if response.status_code == 404:
#     raise Exception("No Iss Found")
# elif response.status_code == 401:
#     raise Exception("You are not authorized to access the API")

# requests 응답 메서드로 처리한다.
response.raise_for_status()

data = response.json()
#.get('')  // ['']  두형식으로 데이터의 세부항목을 가져올수 있다.
longitude = data['iss_position']['longitude']
latitude = data['iss_position']['latitude']

iss_position = (longitude, latitude)

print(iss_position)
