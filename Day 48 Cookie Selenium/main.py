from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
# Cloudflare 보안 우회 실패 -> undetected-chromedriver로 교체
import undetected_chromedriver as uc

"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# ChromeDriver 경로 설정
chrome_driver_path = "C:/resource/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# ChromeDriver 서비스 초기화
service = Service(chrome_driver_path)

# Chrome 옵션 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # 브라우저가 코드 종료 후에도 닫히지 않도록 설정

# Selenium WebDriver 초기화
driver = webdriver.Chrome(service=service, options=chrome_options)
"""

options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)

# 게임 URL 접속
url = "https://orteil.dashnet.org/cookieclicker/"
driver.get(url)

print("\n==================================================================")
print("[INFO:01] 게임 접속 완료: Cookie Clicker")
print("==================================================================")

# (1) 언어 선택
korean_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="langSelect-KO"]'))
)
korean_button.click()
print("[INFO:15] 언어 선택 완료.")

# (2) 큰 쿠키 버튼 로드 확인
button_cookie = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "bigCookie"))
)
print("[INFO:21] 큰 쿠키 버튼 로드 완료.")

# (3) 가격 변환 함수
def parse_price(price_text):
    """
    가격 텍스트를 정수형 숫자로 변환합니다.
    - "1.3 million" → 1300000
    - 쉼표 제거, 단위 변환 포함
    """
    try:
        # 숫자와 단위를 추출
        match = re.search(r"([\d,\.]+)\s*(\w+)?", price_text)
        if match:
            number_part = match.group(1).replace(",", "")  # 쉼표 제거
            unit_part = match.group(2)  # 단위 추출 (optional)

            # 기본 숫자 변환
            price = float(number_part)

            # 단위에 따라 변환
            if unit_part:
                unit_part = unit_part.lower()  # 소문자로 변환
                if unit_part == "million":
                    price *= 10**6
                elif unit_part == "billion":
                    price *= 10**9
                elif unit_part == "trillion":
                    price *= 10**12

            print(f"[DEBUG:38] 변환 중...: Original='{price_text}', Converted={int(price)}")
            return int(price)  # 정수로 변환 후 반환
        else:
            return int(float(price_text.replace(",", "")))  # 단위가 없을 경우 숫자로 변환
    except Exception as e:
        print(f"[ERROR:44] 가격 변환 중 오류 발생: {e}")
        return 0

# (4) 현재 쿠키 수 가져오기
def get_cookie_count():
    """
    현재 쿠키 수를 가져옵니다. 단위를 포함한 값도 처리합니다.
    """
    try:
        cookie_count_element = driver.find_element(By.ID, "cookies")
        cookie_count_text = cookie_count_element.text.strip()
        match = re.search(r"([\d,\.]+)\s*(\w+)?", cookie_count_text)
        if match:
            cookie_count = parse_price(match.group(0))
            print(f"[DEBUG:54] Cookie count: Original='{cookie_count_text}', Parsed={cookie_count}")
            return cookie_count
    except Exception as e:
        print(f"[ERROR:58] 쿠키 수 가져오기 중 오류 발생: {e}")
    return 0

# (5) 상점 업그레이드 구매
def buy_store_upgrades(cookie_count):
    """
    상점 업그레이드 중 구매 가능한 가장 싼 상품을 구매합니다.
    """
    try:
        available_products = driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")
        affordable_products = {}

        for product in available_products:
            try:
                price_element = product.find_element(By.CSS_SELECTOR, ".price")
                price_text = price_element.get_attribute("textContent").strip()
                product_price = parse_price(price_text)
                print(f"[DEBUG:69] 일반 상품: Original='{price_text}', Parsed={product_price}")

                if product_price <= cookie_count:
                    affordable_products[product] = product_price
            except Exception as e:
                print(f"[ERROR:74] 상점 업그레이드 가격 처리 중 오류: {e}")
                continue

        if affordable_products:
            cheapest_product = min(affordable_products, key=affordable_products.get)
            print(f"[INFO:79] 상점 업그레이드 구매: {cheapest_product}, Price={affordable_products[cheapest_product]}")
            cheapest_product.click()
    except Exception as e:
        print(f"[ERROR:82] 상점 업그레이드 처리 중 오류 발생: {e}")

# (6) 특수 업그레이드 구매
def buy_special_upgrades(cookie_count):
    """
    특수 업그레이드 중 구매 가능한 항목을 확인하고 구매합니다.
    """
    try:
        available_upgrades = driver.find_elements(By.CSS_SELECTOR, ".crate.upgrade.enabled")
        if not available_upgrades:
            print("[DEBUG] 구매 가능한 업그레이드가 없음")
            return

        affordable_upgrades = {}
        for upgrade in available_upgrades:
            try:
                # 마우스를 업그레이드 위로 이동
                ActionChains(driver).move_to_element(upgrade).perform()
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.ID, "tooltip"))
                )
                tooltip_element = driver.find_element(By.ID, "tooltip")
                tooltip_text = tooltip_element.text.strip()
                if not tooltip_text:
                    print("[DEBUG] 툴팁 텍스트가 비어 있음")
                    continue

                # 가격만 추출
                upgrade_price = parse_price(tooltip_text.split("\n")[0])
                print(f"[DEBUG:94] 업그레이드 가격: {upgrade_price}")

                if upgrade_price <= cookie_count:
                    affordable_upgrades[upgrade] = upgrade_price
            except Exception as e:
                print(f"[ERROR] 특수 업그레이드 처리 중 오류: {e}")
                continue

        if affordable_upgrades:
            cheapest_upgrade = min(affordable_upgrades, key=affordable_upgrades.get)
            print(f"[INFO] 특수 업그레이드 구매: Price={affordable_upgrades[cheapest_upgrade]}")
            cheapest_upgrade.click()
    except Exception as e:
        print(f"[ERROR] 특수 업그레이드 처리 중 오류 발생: {e}")

# (7) 업그레이드 구매 통합 로직
def buy_best_upgrade():
    """
    특수 업그레이드와 상점 업그레이드를 확인하고 구매 가능한 항목을 구매합니다.
    """
    cookie_count = get_cookie_count()
    print(f"[DEBUG:114] 현재 쿠키 수: {cookie_count}")

    buy_special_upgrades(cookie_count)
    buy_store_upgrades(cookie_count)

# (8) 메인 실행 루프
timeout = time.time() + 100000 * 5  # 6일 정도 실행 테스트
check_interval = time.time() + 5  # 5초마다 업그레이드 확인

while time.time() < timeout:
    try:
        golden_cookies = driver.find_elements(By.CSS_SELECTOR, ".shimmer")
        if golden_cookies:
            print("[INFO:124] 황금 쿠키 발견! 클릭 시도 중...")
            for golden_cookie in golden_cookies:
                try:
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(golden_cookie)
                    )
                    golden_cookie.click()
                    print("[INFO:130] 황금 쿠키 클릭 성공!")
                except Exception as e:
                    print(f"[ERROR:132] 황금 쿠키 클릭 실패: {e}")

        button_cookie.click()

    except StaleElementReferenceException:
        button_cookie = driver.find_element(By.ID, "bigCookie")
        button_cookie.click()

    if time.time() > check_interval:
        print(f"\n------------------------------------------------------------------")
        print(f"[INFO:138] 업그레이드 확인 및 구매 실행")
        buy_best_upgrade()
        check_interval = time.time() + 5

cps_element = driver.find_element(By.ID, "cookiesPerSecond")
cps = cps_element.text
print(f"\n==================================================================")
print(f"[INFO:145] 1초당 쿠키: {cps}")
print("==================================================================")

# 드라이버 종료
driver.quit()
