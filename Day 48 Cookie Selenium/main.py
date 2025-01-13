from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

# Chrome 옵션 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # 브라우저가 코드 종료 후에도 닫히지 않도록 설정

# Selenium WebDriver 초기화
driver = webdriver.Chrome(options=chrome_options)

# 게임 URL 접속
url = "https://orteil.dashnet.org/cookieclicker/"
driver.get(url)

# (1) 언어 선택
# 페이지 로드 후 한국어 버튼을 클릭하여 언어를 설정
korean_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="langSelect-KO"]'))
)
korean_button.click()

# (2) 큰 쿠키 버튼 로드 확인
# 클릭 가능한 쿠키 버튼(bigCookie)을 기다린 뒤 로드
button_cookie = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "bigCookie"))
)

# (3) 가격 변환 함수
def parse_price(price_text):
    """
    가격 텍스트를 숫자로 변환합니다.
    - 예: "19.777 Million" → 19777000
    - "Million", "Billion" 등의 단위를 숫자로 변환합니다.
    """
    try:
        # 숫자와 단위를 추출
        match = re.search(r"([\d,\.]+)\s*(\w+)?", price_text)
        if match:
            number_part = match.group(1).replace(",", "")  # 쉼표 제거
            unit_part = match.group(2)  # 단위 확인

            # 숫자를 float으로 변환
            price = float(number_part)
            # 단위에 따라 변환
            if unit_part == "Million":
                price *= 10 ** 6
            elif unit_part == "Billion":
                price *= 10 ** 9
            elif unit_part == "Trillion":
                price *= 10 ** 12

            return int(price)  # 정수로 변환 후 반환
    except Exception as e:
        print(f"[ERROR] 가격 변환 중 오류 발생: {e}")
    return 0  # 오류 발생 시 0 반환

# (4) 현재 쿠키 수 가져오기
def get_cookie_count():
    """
    현재 쿠키 수를 가져옵니다. 단위를 포함한 값도 처리합니다.
    - 쿠키 텍스트는 "2,398 쿠키" 또는 "2.5 Million 쿠키" 형식입니다.
    """
    try:
        # "cookies" ID를 가진 요소에서 텍스트를 가져옴
        cookie_count_element = driver.find_element(By.ID, "cookies")
        cookie_count_text = cookie_count_element.text.strip()
        # 텍스트에서 숫자와 단위 추출 후 변환
        match = re.search(r"([\d,\.]+)\s*(\w+)?", cookie_count_text)
        if match:
            return parse_price(match.group(0))
    except Exception as e:
        print(f"[ERROR] 쿠키 수 가져오기 중 오류 발생: {e}")
    return 0  # 오류 발생 시 0 반환

# (5) 상점 업그레이드 구매
def buy_store_upgrades(cookie_count):
    """
    상점 업그레이드 중 구매 가능한 가장 싼 상품을 구매합니다.
    """
    try:
        # 구매 가능한 상점 상품을 찾음
        available_products = driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")
        affordable_products = {}

        for product in available_products:
            try:
                # 상품 가격 가져오기
                price_element = product.find_element(By.CSS_SELECTOR, ".price")
                price_text = price_element.get_attribute("textContent").strip()
                product_price = parse_price(price_text)

                # 구매 가능한 상품 필터링
                if product_price <= cookie_count:
                    affordable_products[product] = product_price
            except Exception as e:
                print(f"[ERROR] 상점 업그레이드 가격 처리 중 오류: {e}")
                continue

        # 가장 싼 상품 구매
        if affordable_products:
            cheapest_product = min(affordable_products, key=affordable_products.get)
            print(f"[INFO] 상점 업그레이드 구매: {cheapest_product}")
            cheapest_product.click()
    except Exception as e:
        print(f"[ERROR] 상점 업그레이드 처리 중 오류 발생: {e}")

# (6) 특수 업그레이드 구매
def buy_special_upgrades(cookie_count):
    """
    특수 업그레이드 중 구매 가능한 가장 싼 업그레이드를 구매합니다.
    """
    try:
        # 활성화된 특수 업그레이드 찾기
        available_upgrades = driver.find_elements(By.CSS_SELECTOR, ".crate.upgrade.enabled")
        affordable_upgrades = {}

        for upgrade in available_upgrades:
            try:
                # 마우스를 업그레이드 위로 이동하여 툴팁 활성화
                ActionChains(driver).move_to_element(upgrade).perform()

                # 툴팁에서 가격 정보 가져오기
                tooltip_element = driver.find_element(By.ID, "tooltip")
                tooltip_text = tooltip_element.text
                upgrade_price = parse_price(tooltip_text)

                # 구매 가능한 업그레이드 필터링
                if upgrade_price <= cookie_count:
                    affordable_upgrades[upgrade] = upgrade_price
            except Exception as e:
                print(f"[ERROR] 특수 업그레이드 처리 중 오류: {e}")
                continue

        # 가장 싼 업그레이드 구매
        if affordable_upgrades:
            cheapest_upgrade = min(affordable_upgrades, key=affordable_upgrades.get)
            print(f"[INFO] 특수 업그레이드 구매: {cheapest_upgrade}")
            cheapest_upgrade.click()
    except Exception as e:
        print(f"[ERROR] 특수 업그레이드 처리 중 오류 발생: {e}")

# (7) 업그레이드 구매 통합 로직
def buy_best_upgrade():
    """
    특수 업그레이드와 상점 업그레이드를 확인하고 구매 가능한 항목을 구매합니다.
    """
    cookie_count = get_cookie_count()
    print(f"[DEBUG] 현재 쿠키 수: {cookie_count}")

    # 특수 업그레이드 구매
    buy_special_upgrades(cookie_count)

    # 상점 업그레이드 구매
    buy_store_upgrades(cookie_count)

# (8) 메인 실행 루프
timeout = time.time() + 100000 * 5  # 6일 정도 실행 테스트
check_interval = time.time() + 5  # 5초마다 업그레이드 확인

while time.time() < timeout:
    try:
        # (1) 황금 쿠키 탐지 및 클릭
        golden_cookies = driver.find_elements(By.CSS_SELECTOR, ".shimmer")
        if golden_cookies:
            print("[INFO] 황금 쿠키 발견! 클릭 시도 중...")
            for golden_cookie in golden_cookies:
                try:
                    # 클릭 가능 대기
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(golden_cookie)
                    )
                    golden_cookie.click()
                    print("[INFO] 황금 쿠키 클릭 성공!")
                except Exception as e:
                    print(f"[ERROR] 황금 쿠키 클릭 실패: {e}")

        # (2) 큰 쿠키 클릭
        button_cookie.click()

    except StaleElementReferenceException:
        # 큰 쿠키 버튼 재참조
        button_cookie = driver.find_element(By.ID, "bigCookie")
        button_cookie.click()

    # (3) 업그레이드 확인 및 구매
    if time.time() > check_interval:
        buy_best_upgrade()
        check_interval = time.time() + 5

# (9) 1초당 쿠키 개수 출력
cps_element = driver.find_element(By.ID, "cookiesPerSecond")
cps = cps_element.text
print(f"1초당 쿠키: {cps}")

# 드라이버 종료
driver.quit()