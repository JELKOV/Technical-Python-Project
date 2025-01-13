from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 사용자 지정 헤더를 위한 Chrome 옵션 설정
chrome_options = webdriver.ChromeOptions()

# 브라우저가 종료되지 않도록 설정
chrome_options.add_experimental_option("detach", True)

# User-Agent 설정: 브라우저가 자동화 도구가 아닌 일반 사용자처럼 보이도록 설정
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

# 브라우저 언어 설정: 요청이 한국어 사용자처럼 보이도록 설정
chrome_options.add_argument("accept-language=ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7")

# Selenium 자동화 탐지를 줄이기 위해 Blink 엔진의 자동화 관련 기능 비활성화
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# WebDriver 초기화
driver = webdriver.Chrome(options=chrome_options)

# Amazon 페이지 URL
url = "https://www.amazon.com/CyberPowerPC-i5-13400F-GeForce-Windows-GXiVR8060A24/dp/B0DCMPRRFD"
driver.get(url)  # Amazon 페이지로 이동

# CAPTCHA가 발생했을 경우 사용자 입력 대기
if "Type the characters" in driver.page_source:  # CAPTCHA 페이지 감지
    print("CAPTCHA가 발생했습니다. 수동으로 CAPTCHA를 해결하고 Enter를 누르세요...")
    input("CAPTCHA를 완료했습니까? Enter를 누르세요.")  # 사용자가 CAPTCHA를 해결하고 계속 진행

# 페이지 로딩 후 대기 시간 추가
time.sleep(5)  # 페이지 로딩이 완료될 때까지 대기

# 상품 가격 추출
try:
    # 상품 가격의 정수 부분 추출 (예: $999.99의 '999')
    price_dollar = driver.find_element(By.CLASS_NAME, "a-price-whole").text

    # 상품 가격의 소수 부분 추출 (예: $999.99의 '.99')
    price_cent = driver.find_element(By.CLASS_NAME, "a-price-fraction").text

    # 상품 가격 출력
    print(f"The price is {price_dollar}.{price_cent}")
except Exception as e:
    # 가격 정보를 찾지 못했을 경우 예외 처리
    print("가격 정보를 찾을 수 없습니다. 오류:", e)


# 브라우저 닫기
driver.quit()  # 사용 후 브라우저를 종료하여 리소스 해제
