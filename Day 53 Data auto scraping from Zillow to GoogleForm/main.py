import requests

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import time
import pprint



Google_Form_Url = 'https://docs.google.com/forms/d/e/1FAIpQLSezigZseq6ezKYhu6xy76QCHLXZZ9gpLLunGSK9ZyxFxxO6vA/viewform?usp=header'
Zillow_Url = 'https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Afalse%2C%22mapBounds%22%3A%7B%22west%22%3A-122.59760893774414%2C%22east%22%3A-122.26904906225586%2C%22south%22%3A37.67169174960122%2C%22north%22%3A37.87874618631953%7D%2C%22mapZoom%22%3A12%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22price%22%3A%7B%22min%22%3Anull%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3Anull%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%2C%22max%22%3Anull%7D%7D%2C%22isListVisible%22%3Atrue%7D'
chrome_driver_path = "C:/resource/chromedriver-win64/chromedriver-win64/chromedriver.exe"
Google_ID = '구글아이디'
Google_Pass = '구글비밀번호'

# --------------------
# 1. Zillow 웹 스크래핑
# --------------------
def scrape_zillow_data(url):
    # HTTP Session 생성
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Host": "www.zillow.com",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.google.com/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
        "TE": "trailers"
    }

    # Session 생성 및 헤더 업데이트
    session = requests.Session()
    session.headers.update(headers)

    # 요청 보내기
    response = session.get(url)
    if response.status_code != 200:
        print(f"페이지 조회 실패, 응답코드: {response.status_code}")
        return []


    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.prettify())

    # 데이터 저장 리스트
    properties = []

    count = 0

    # 부동산 항목 스크래핑
    listings = soup.select("li.ListItem-c11n-8-107-0__sc-13rwu5a-0")
    if not listings:
        print("부동산 항목을 조회 하지 못했습니다.")

    for listing in listings:
        # 디버깅용 카운트
        count = count + 1
        print(f"반복문 시작{count}")
        try:
            # 광고 요소 필터링
            if listing.select_one("p:-soup-contains('Loading...')"):
                print("광고요소")
                continue

            # 주소
            address = listing.select_one('address[data-test="property-card-addr"]')
            print(f"Address Element: {address}")
            address_text = address.get_text(strip=True) if address else "N/A"

            # 가격
            price = listing.select_one('span[data-test="property-card-price"]')
            print(f"Price Element: {price}")  # 가격 확인
            price_text = price.get_text(strip=True) if price else "N/A"

            # 링크
            link = listing.select_one('a[data-test="property-card-link"]')
            print(f"Link Element: {link}")  # 링크 확인
            link_href = link['href'] if link else "N/A"

            # 유효성 검사
            if address_text != "N/A" and price_text != "N/A" and link_href != "N/A":
                properties.append({
                    "Address": address_text,
                    "Price": price_text,
                    "Link": link_href,
                })
            else:
                # 누락 데이터 디버깅 출력
                print(f"누락 데이터 출력: 주소={address_text}, 가격={price_text}, 링크={link_href}")

        except Exception as e:
            print(f"파싱 에러 리스트: {e}")

    # 유효한 데이터만 반환
    return properties


# --------------------
# 2. 구글 폼 자동 입력
# --------------------
def fill_google_form(data, form_url):
    # Chrome WebDriver 옵션 설정
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-blocking")
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)

    # WebDriver 실행
    service = Service(chrome_driver_path)  # ChromeDriver 경로 지정
    driver = webdriver.Chrome(service=service, options=options)

    # 브라우저 감지 우회 설정
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        """
    })

    driver.get(form_url)

    ## 로그인 a태그 누르기
    login_a_tag = driver.find_element(By.XPATH, '//*[@id="SMMuxb"]/a[1]')
    print("로그인 테그 확인")
    login_a_tag.click()
    print("로그인 테그 누르기 종료")
    time.sleep(2)

    ## 창 전환
    print("구글 로그인 창 열림 대기")
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    all_windows = driver.window_handles
    driver.switch_to.window(all_windows[-1])
    print("구글 로그인 창 전환 완료")
    time.sleep(2)

    # 로그인 필드 채우기
    login_field = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
    print("로그인 input 필드 확인")
    login_field.send_keys(Google_ID)
    login_field.send_keys(Keys.ENTER)
    print("이메일 입력 완료")
    time.sleep(2)

    # 비밀 번호 필드 채우기
    password_field = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    print("패스워드 input 필드 확인")
    password_field.send_keys(Google_Pass)
    password_field.send_keys(Keys.ENTER)
    print("패스워드 입력 완료")
    time.sleep(2)

    # 추가 인증 대기 (예: CAPTCHA)
    print("추가 인증 대기 중...")
    input("추가 인증을 완료한 후 Enter를 누르세요...")

    # 추가 인증후 돌아가기
    print("구글 시트 창으로 복귀 중...")
    driver.switch_to.window(all_windows[0])
    print("구글 시트 창으로 복귀 완료")
    time.sleep(2)

    try:
        for entry in data:
            driver.get(form_url)
            time.sleep(2)  # 페이지 로드 대기

            # 필드 채우기
            address_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

            address_field.send_keys(entry["Address"])
            price_field.send_keys(entry["Price"])
            link_field.send_keys(entry["Link"])

            # 제출 버튼 클릭
            print("제출 버튼 찾기")
            submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
            submit_button.click()

            time.sleep(2)  # 폼 제출 대기

    finally:
        driver.get(form_url)
        # 구글 시트로 전환
        print("구글 시트 관리 페이지 전환중 ...")
        google_form_manage_button = driver.find_element(By.XPATH, '/html/body/div/div[1]/div')
        print("구글 시트 관리 페이지 확인")
        google_form_manage_button.click()
        print("구글 시트 매니지 버튼 클릭")
        time.sleep(2)

        # 응답 버튼 누르기
        print("응답 버튼 찾기 ...")
        response_button = driver.find_element(By.XPATH, '//*[@id="tJHJj"]/div[3]/div[1]/div/div[2]')
        print("응답 버튼 확인")
        response_button.click()
        print("응답 버튼 클릭")
        time.sleep(2)

        try:
            # 이미 Google Sheet와 연결된 경우
            connected_sheet_button = driver.find_element(By.XPATH, '//*[text()="Sheets에서 보기"]')
            print("Google Sheet와 이미 연결된 상태입니다.")
            connected_sheet_button.click()
            print("Google Sheet로 바로 이동합니다.")
            time.sleep(2)
            return
        except NoSuchElementException:
            print("Google Sheet와 연결되지 않은 상태입니다. 새로 연결을 시작합니다.")

            # # 구글 시트 버튼 누르기
            print("구글 시트 전환 버튼 찾기...")
            to_google_sheet_button = driver.find_element(By.XPATH, '//*[@id="ResponsesView"]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div')
            print("구글 시트 전환 버튼 찾기 완료")
            to_google_sheet_button.click()
            print("구글 시트 전환 버튼 클릭")
            time.sleep(4)

            # 새 Google Sheet 생성
            print("구글 시트 새로 만들기...")
            new_google_sheet_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and @class="uArJ5e UQuaGc kCyAyd l3F1ye ARrCac HvOprf M9Bg4d"]'))
            )
            new_google_sheet_button.click()
            print("Google Sheet 생성 완료")
            time.sleep(2)
        finally:
            pass
            # # 창 끄기
            # time.sleep(2)
            # driver.quit()


# --------------------
# 3. 메인 실행 코드
# --------------------
if __name__ == "__main__":

    # 1. Zillow 데이터 스크래핑
    print("Scraping Zillow data...")
    zillow_data = scrape_zillow_data(Zillow_Url)
    print("*****BS4 최종 데이터*****")
    pprint.pprint(zillow_data)

    # 2. 구글 폼에 데이터 입력
    print("Filling Google Form...")
    fill_google_form(zillow_data, Google_Form_Url)
    print("구글폼 작성 제출 완료")

