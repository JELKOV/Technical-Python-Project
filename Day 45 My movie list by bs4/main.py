from bs4 import BeautifulSoup
import requests

# 웹사이트에서 HTML 데이터를 가져옵니다.
response = requests.get("https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/")
response.raise_for_status()  # HTTP 요청 상태 확인 (문제가 있을 시 예외 발생)
soup = BeautifulSoup(response.text, 'html.parser')  # HTML 데이터를 BeautifulSoup 객체로 파싱

# 1. 영화 제목 가져오기
# - <h3> 태그 중 클래스가 "title"인 모든 요소를 찾아 리스트로 반환
movies_name = soup.find_all(name="h3", class_="title")

# 2. 영화 제목 텍스트 추출
# - 리스트 컴프리헨션을 사용해 각 <h3> 태그에서 텍스트만 추출
movies_text = [movie_name.get_text() for movie_name in movies_name]
print(movies_text)  # 영화 제목 리스트를 출력하여 확인

# 3. 영화 제목을 역순으로 출력
# 방법 1: 리스트 슬라이싱 활용
for movie in movies_text[::-1]:  # 리스트를 슬라이싱([::-1])하여 역순으로 순회
    print(movie)

# 4. 영화 제목을 파일에 저장
# 방법 1: 리스트 슬라이싱 활용
with open("movies.txt", "w", encoding="utf-8") as file:  # UTF-8 인코딩으로 파일을 쓰기 모드로 열기
    for movie in movies_text[::-1]:  # 영화 제목 리스트를 역순으로 순회
        file.write(f"{movie}\n")  # 각 영화 제목 뒤에 줄바꿈을 추가하여 파일에 기록

# 방법 2: for 루프와 range 활용 (주석 처리된 코드)
# - 리스트의 마지막 인덱스부터 0까지 역순으로 접근
# - `range(len(movies_text)-1, 0, -1)`:
#   - `len(movies_text)-1`: 리스트의 마지막 인덱스부터 시작
#   - `0`: 루프 종료 조건 (0까지 실행)
#   - `-1`: 인덱스를 감소시키는 스텝
# - movies_text[n]: n번째 영화 제목을 출력
# 주석 처리된 코드는 아래와 같이 동작:
# ```
# for n in range(len(movies_text)-1, 0, -1):
#     print(movies_text[n])
# ```

# 코드의 두 가지 구현 방법 비교:
# - **방법 1**(슬라이싱): 코드가 간결하며, 리스트를 역순으로 순회.
# - **방법 2**(range 활용): 리스트 인덱스를 명시적으로 제어하며, 특정 인덱스 범위를 설정 가능.