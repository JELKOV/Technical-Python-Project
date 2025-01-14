from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time

# Chrome WebDriver 옵션 설정
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# WebDriver 실행
driver = webdriver.Chrome(options=options)

# WebDriver가 브라우저 감지를 우회하도록 설정
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
    """
})


def click_button_by_xpath(driver, xpath, button_description):
    """
    클릭 가능한 버튼을 XPath를 통해 찾고 클릭합니다.
    :param driver: Selenium WebDriver 객체
    :param xpath: 버튼의 XPath
    :param button_description: 버튼 설명 (로그 출력용)
    :return: 클릭 성공 여부 (True/False)
    """
    try:
        buttons = driver.find_elements(By.XPATH, xpath)
        if buttons:
            driver.execute_script("arguments[0].click();", buttons[0])
            print(f"'{button_description}' 버튼 클릭 성공")
            return True
        else:
            print(f"'{button_description}' 버튼이 존재하지 않음.")
    except Exception as e:
        print(f"'{button_description}' 버튼 클릭 중 에러 발생: {e}")
    return False

def handle_google_login(driver):
    try:
        # Google 로그인 버튼 클릭
        google_login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'LgbsSe')]"))
        )
        driver.execute_script("arguments[0].click();", google_login_button)
        print("Google 로그인 버튼 클릭 성공")

        # 창 핸들 확인 및 전환
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        windows = driver.window_handles
        print(f"창 핸들 목록: {windows}")
        driver.switch_to.window(windows[-1])
        print("새 창으로 전환 성공")

        # Google 로그인 페이지에서 이메일 입력
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys("ajh42341")
        email_input.send_keys(Keys.ENTER)
        print("이메일 입력 성공")

        # 비밀번호 입력
        password_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))
        )
        password_input.click()
        password_input.send_keys("tjsrur132!")
        password_input.send_keys(Keys.ENTER)
        print("비밀번호 입력 성공")

        # CAPTCHA 또는 추가 인증 확인
        print("CAPTCHA 확인 또는 추가 인증 대기 중...")
        input("CAPTCHA 또는 추가 인증을 완료한 후 Enter를 눌러주세요.")

        # 창 핸들 다시 확인
        time.sleep(2)  # 창 전환 대기
        windows = driver.window_handles
        print(f"현재 창 핸들 목록: {windows}")
        if len(windows) < 2:
            print("Google 로그인 창이 닫혔습니다. 메인 창으로 돌아갑니다.")
            driver.switch_to.window(windows[0])
        else:
            driver.switch_to.window(windows[-1])
            print("Google 로그인 창 활성화 중...")

    except Exception as e:
        print(f"Google 로그인 처리 중 에러 발생: {e}")
        raise

def handle_continue_as_jacob(driver):
    """
    Handles the 'Continue as Jacob' button click and Google account selection process.
    """
    try:
        # "Continue as Jacob" 버튼 클릭
        if click_button_by_xpath(driver, "//div[text()='Continue as Jacob']", "Continue as Jacob"):
            return True

        # Google 계정 선택 버튼 클릭
        if click_button_by_xpath(driver, "//div[@id='picker-item-label-0' and contains(text(),'Jacob ahn')]", "Google 계정 선택"):
            return True

    except Exception as e:
        print(f"handle_continue_as_jacob 함수 처리 중 에러 발생: {e}")

    return False  # 클릭 성공하지 못한 경우 False 반환


def handle_job_search(driver):
    try:
        # 채용공고 검색 URL 열기
        search_url = "https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=102257491&keywords=python%20developer&location=London%2C%20England%2C%20United%20Kingdom&redirect=false&position=1&pageNum=0"
        driver.get(search_url)
        print(f"채용공고 페이지 열림: {search_url}")

        # 페이지 로드 확인
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
        )
        print("채용공고 페이지 로드 완료")

        # 채용공고 크롤링
        job_cards = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card-container"))
        )
        print(f"채용공고 {len(job_cards)}건 발견")
        for idx, job in enumerate(job_cards[:5], start=1):  # 상위 5개만 크롤링
            title = job.find_element(By.CLASS_NAME, "job-card-list__title").text
            company = job.find_element(By.CLASS_NAME, "job-card-container__company-name").text
            location = job.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text
            print(f"{idx}. {title} at {company} - {location}")

    except TimeoutException:
        print("채용공고를 로드하지 못했습니다.")
        driver.quit()
        exit()

## 메인 로직
try:
    # LinkedIn 로그인 페이지로 이동
    driver.get("https://www.linkedin.com/login")
    print("LinkedIn 로그인 페이지 열림")
    # Google 로그인 처리
    handle_google_login(driver)
    # Google 로그인 예외 처리
    handle_continue_as_jacob(driver)

    # 채용공고 검색 및 크롤링 처리
    handle_job_search(driver)

except TimeoutException as e:
    print(f"타임아웃 발생: {e}")
except NoSuchElementException as e:
    print(f"요소를 찾을 수 없음: {e}")
except WebDriverException as e:
    print(f"브라우저 에러 발생: {e}")
except Exception as e:
    print(f"에러 발생: {e}")