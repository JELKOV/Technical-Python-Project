from selenium import webdriver
from selenium.webdriver.common.by import By

# Chrome WebDriver 초기화 및 옵션 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # 브라우저를 자동으로 닫지 않음
driver = webdriver.Chrome(options=chrome_options)

# Python.org URL
url = "https://www.python.org/"
driver.get(url)

# 이벤트 데이터 수집
try:
    # CSS 선택자를 사용해 이벤트 시간과 이름 요소 가져오기
    event_times = driver.find_elements(By.CSS_SELECTOR, ".event-widget time")  # 시간 요소
    event_names = driver.find_elements(By.CSS_SELECTOR, ".event-widget li a")  # 이벤트 이름 요소

    # 딕셔너리 생성
    events = {}
    for i in range(len(event_times)):  # 시간과 이름의 인덱스는 동일
        events[i] = {
            "time": event_times[i].get_attribute("datetime"),  # 시간 추출
            "title": event_names[i].text  # 이름 추출
        }

    # 결과 출력
    print(events)

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    driver.quit()  # WebDriver 닫기
