from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time

# ChromeDriver 경로 설정
chrome_driver_path = "C:/resource/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# Chrome WebDriver 옵션 설정
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# WebDriver 실행
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# WebDriver가 브라우저 감지를 우회하도록 설정
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
    """
})

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
        email_input.send_keys("구글 아이디")
        email_input.send_keys(Keys.ENTER)
        print("이메일 입력 성공")

        # 비밀번호 입력
        password_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))
        )
        password_input.click()
        password_input.send_keys("구글 비밀번호")
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


def handle_easy_apply_process(driver):
    """
    간편 지원 프로세스를 처리합니다.
    """
    try:
        # 전화번호 입력
        phone_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'phoneNumber')]"))
        )
        phone_input.clear()
        phone_input.send_keys("01062734585")
        print("전화번호 입력 완료")

        # "다음" 버튼 확인
        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, '다음 단계로')]"))
            )
            if next_button:
                print("다음 버튼 발견, 지원 창 닫기 시작")

                # X 버튼 클릭 (닫기)
                close_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, '닫기')]")
                close_button.click()
                print("닫기 버튼 클릭 완료")

                # 삭제 버튼 클릭
                delete_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(@data-control-name, 'discard_application_confirm_btn')]"))
                )
                delete_button.click()
                print("삭제 버튼 클릭 완료")
                return  # "다음 단계"가 있으면 해당 지원을 건너뜁니다.

        except TimeoutException:
            print("다음 버튼 없음, 지원 계속 진행")

        # 제출 버튼 클릭
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, '지원서 전송')]"))
        )
        submit_button.click()
        print("지원 완료")

        # "나중에 하기" 버튼 찾기
        later_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='나중에 하기']]"))
        )
        later_button.click()
        print("'나중에 하기' 버튼 클릭 완료")
    except Exception as e:
        print(f"간편 지원 처리 중 에러 발생: {e}")


# 공고 처리 로직
def process_visible_jobs(driver):
    try:
        # 공고 리스트 로드 대기
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'job-card-container')]"))
        )

        # 공고 리스트 가져오기
        job_list = driver.find_elements(By.XPATH, "//li[contains(@class, 'job-card-container')]")
        print(f"총 {len(job_list)}개의 공고를 찾았습니다.")

        # 공고를 순회하며 처리
        for idx, job in enumerate(job_list, start=1):
            try:
                print(f"{idx}번째 공고 클릭 시도")

                # 공고를 클릭
                driver.execute_script("arguments[0].scrollIntoView();", job)
                job.click()
                time.sleep(2)  # 상세 정보 로드 대기

                # 공고 제목 확인
                job_title = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, 't-24')]"))
                ).text
                print(f"{idx}번째 공고 제목: {job_title}")

                # 간편 지원 버튼 확인
                easy_apply_button = driver.find_elements(By.XPATH, "//button[contains(@class, 'jobs-apply-button')]")
                if easy_apply_button:
                    print(f"{idx}번째 공고: 간편 지원 시작")
                    easy_apply_button[0].click()
                    handle_easy_apply_process(driver)
                else:
                    print(f"{idx}번째 공고: 간편 지원 버튼이 없어 건너뜁니다.")

            except NoSuchElementException as e:
                print(f"{idx}번째 공고: 필수 요소를 찾을 수 없어 건너뜁니다: {e}")
            except TimeoutException:
                print(f"{idx}번째 공고: 요소 로드 대기 시간 초과")
            except Exception as e:
                print(f"{idx}번째 공고 처리 중 에러 발생: {e}")

    except Exception as e:
        print(f"공고 처리 중 에러 발생: {e}")


def handle_job_search_and_apply(driver):
    """
    화면에 보이는 공고에서 상위 3개만 처리.
    """
    search_url = "https://www.linkedin.com/jobs/search/?currentJobId=4108115414&f_AL=true&f_E=2&f_WT=1%2C3%2C2&geoId=90010114&keywords=python%20java%20react&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&spellCorrectionEnabled=true"

    # 채용공고 페이지 열기
    try:
        driver.get(search_url)
        print(f"채용공고 페이지 열림: {search_url}")
        process_visible_jobs(driver)
    except Exception as e:
        print(f"채용공고 처리 중 에러 발생: {e}")


## 메인 로직
try:
    # LinkedIn 로그인 페이지로 이동
    driver.get("https://www.linkedin.com/login")
    print("LinkedIn 로그인 페이지 열림")
    # Google 로그인 처리
    handle_google_login(driver)
    print("구글 로그인 완료")
    # 채용공고 검색 및 크롤링 처리
    handle_job_search_and_apply(driver)
    print("지원 완료")

except TimeoutException as e:
    print(f"타임아웃 발생: {e}")
except NoSuchElementException as e:
    print(f"요소를 찾을 수 없음: {e}")
except WebDriverException as e:
    print(f"브라우저 에러 발생: {e}")
except Exception as e:
    print(f"에러 발생: {e}")