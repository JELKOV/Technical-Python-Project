from bs4 import BeautifulSoup

# HTML 파일 읽어오기
with open("website.html", encoding="utf-8") as file:
    contents = file.read()  # 파일 내용을 문자열로 읽기

# BeautifulSoup 객체 생성 (HTML 파싱)
soup = BeautifulSoup(contents, 'html.parser')  # 'html.parser'는 HTML 데이터를 파싱하기 위한 파서

# ** HTML 파싱된 데이터 확인 **
# DOM 구조로 정리된 HTML을 보기 좋게 출력
# print(soup.prettify())

# ** Title 태그 정보 가져오기 **
# <title> 태그 전체 출력
print(soup.title)

# <title> 태그 이름 가져오기
print(soup.title.name)

# <title> 태그의 텍스트 내용 가져오기
print(soup.title.string)

# ** Anchor 태그 정보 가져오기 **
# <a> 태그를 모두 찾고 리스트로 반환
all_anchor_tags = soup.find_all('a')
print(all_anchor_tags)  # 모든 <a> 태그 출력

# <a> 태그의 총 개수 확인
print(len(all_anchor_tags))  # len() 함수로 리스트 길이 반환

# ** Anchor 태그의 속성과 텍스트 추출 **
for tag in all_anchor_tags:
    print(tag.getText())  # 각 <a> 태그의 텍스트 출력
    print(tag.get("href"))  # 각 <a> 태그의 href 속성 값 출력

# ** 특정 태그와 속성 기반 검색 **
# id="name"을 가진 <h1> 태그 검색
heading = soup.find(name='h1', id='name')
print(heading)

# class="heading"을 가진 <h3> 태그 검색
class_h3 = soup.find(name="h3", class_="heading")
print(class_h3)
print(class_h3.getText())

# ** CSS 선택자 사용 예제 **
# <p> 태그 안의 첫 번째 <a> 태그 선택
company_url = soup.select_one("p a")
print(company_url)

# id="name"을 가진 태그 선택
name = soup.select_one("#name")
print(name)

# class="heading"을 가진 모든 태그 선택
heading_s = soup.select(".heading")
print(heading_s)

# ** Input 태그 정보 가져오기 **
# <input> 태그 선택
input_a = soup.find("input")
print(input_a)

# <input> 태그의 maxlength 속성 값 가져오기
print(input_a.get("maxlength"))
