from bs4 import BeautifulSoup
## 사용하면 데이터를 가져올수 있다.
import requests

# 1. 데이터 가져오기
response = requests.get("https://news.ycombinator.com/news")
response.raise_for_status()  # 요청 오류 발생 시 예외 발생
soup = BeautifulSoup(response.text, "html.parser")  # HTML 파싱
# print(response.text)
# print(response.content)
# print(soup.prettify())

# 2. 웹사이트 제목 가져오기
# <title> 태그의 내용 출력
print("Website Title:")
print(soup.title.get_text())  # .get_text()로 텍스트만 추출


# 3. 첫 번째 기사 정보 가져오기
print("\nFirst Article:")
first_title = soup.select_one("span.titleline > a")  # 첫 번째 기사 제목 선택
print("Title:", first_title.get_text())  # 기사 제목
article_link = first_title.get("href")  # 기사 링크
print("Link:", article_link)


# 4. 첫 번째 기사 투표수 가져오기
article_upvotes = soup.find('span', class_="score")  # 첫 번째 기사 투표수 선택

# 5. 모든 기사 투표수 가져오기
print("\nAll Article Upvotes:")
article_upvotes_all = soup.find_all('span', class_="score")  # 모든 투표수 선택
upvotes = [int(article.get_text().split()[0]) for article in article_upvotes_all]  # 리스트 컴프리헨션으로 텍스트 추출
print(upvotes)


# 6. 모든 기사 제목 가져오기
print("\nAll Article Titles and Links:")
titles_list = soup.select("span.titleline > a")  # 모든 기사 제목 선택
titles_texts = [title.get_text() for title in titles_list]  # 제목 텍스트만 추출
print(titles_texts)
links = [title.get("href") for title in titles_list]  # 링크만 추출
print(links)


# 7. 조회수 높은거 구하기
max_upvote = max(upvotes)
max_index = upvotes.index(max_upvote)

print(upvotes[max_index])
print(titles_texts[max_index])
print(links[max_index])