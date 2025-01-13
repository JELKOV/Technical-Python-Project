from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Chrome 옵션 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# WebDriver 초기화
driver = webdriver.Chrome(options=chrome_options)

# URL 이동
url = "https://en.wikipedia.org/wiki/Main_Page"
driver.get(url)

# (1) find_elements()로 다수의 요소 가져오기
# search_articles_numbers = driver.find_elements(By.CSS_SELECTOR, "#articlecount a")
#
# # 필요 없는 마지막 요소 제외하고 텍스트 출력
# for element in search_articles_numbers[1:-1]:  # 마지막 요소 제외
#     print(element.text)  # 각 요소의 텍스트 출력
#     element.click()

# # (2) Link TEXT 가져오기
# all_portals = driver.find_element(By.LINK_TEXT, "Talk")
# all_portals.click()

# (3) 검색 버튼 클릭
# 'Special:Search' 링크를 가진 버튼 요소를 찾아 클릭
search_button = driver.find_element(By.CSS_SELECTOR, "a[href='/wiki/Special:Search']")
search_button.click()

# (3) 검색 입력 필드에 글자 입력
# 검색 입력 필드를 찾은 후 'Python' 키워드 입력
search = driver.find_element(By.NAME, "search")  # name 속성으로 검색 필드 찾기
search.send_keys("Python")  # 키워드 입력
search.send_keys(Keys.ENTER)

# # 브라우저 종료 (필요에 따라 주석 처리)
# driver.quit()
