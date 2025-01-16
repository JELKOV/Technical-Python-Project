from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

# ChromeDriver 경로 설정
chrome_driver_path = "C:/resource/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# Chrome WebDriver 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-popup-blocking")
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option("useAutomationExtension", False)

# WebDriver 실행
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# 브라우저 감지 우회 설정
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
    """
})

def tinder_login(driver):
    try:
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="q7720314"]/div/div[1]/div/main/div[1]/div/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]/div'))
        )
        ActionChains(driver).move_to_element(login_button).click(login_button).perform()
        print("로그인 버튼 클릭 성공")
    except Exception as e:
        print("로그인 버튼 클릭 실패:", e)

def handle_google_login(driver):
    try:
        # iframe 전환
        google_iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//iframe[contains(@src, "https://accounts.google.com/gsi/button")]'))
        )
        driver.switch_to.frame(google_iframe)  # iframe으로 전환
        print("iframe 전환 성공")

        # Google 로그인 버튼 클릭
        google_login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Google 계정으로 계속하기")]'))
        )
        google_login_button.click()
        print("Google 로그인 버튼 클릭 성공")

        # iframe에서 기본 창으로 돌아오기
        driver.switch_to.default_content()
        print("기본 창으로 전환 성공")

        # 팝업 대기
        WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])  # 새 창으로 전환
        print("Google 로그인 창으로 전환 성공")

        # Google 로그인 페이지에서 이메일 입력
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys("구글 아이디")  # 이메일 입력
        email_input.send_keys(Keys.ENTER)
        print("이메일 입력 성공")

        # 비밀번호 입력
        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="password" and @name="Passwd"]'))
        )
        password_input.send_keys("구글 비밀번호")  # 비밀번호 입력
        password_input.send_keys(Keys.ENTER)
        print("비밀번호 입력 성공")

        print("인증 처리 후 Enter를 누르세요.")
        input()

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

def handle_tinder_permissions(driver):
    try:
        # 허용 버튼 클릭
        allow_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="q229060750"]/div/div[1]/div/div/div[3]/button[1]/div[2]/div[2]/div'))
        )
        allow_button.click()
        print("허용 버튼 클릭 성공")

        # 동의함 버튼 클릭
        agree_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="q229060750"]/div/div[2]/div/div/div[1]/div[1]/button/div[2]/div[2]/div'))
        )
        agree_button.click()
        print("동의함 버튼 클릭 성공")
        
        # 지금은 괜찮아요 버튼 클릭
        now_ok_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="q229060750"]/div/div/div/div/div[3]/button[2]/div[2]/div[2]/div'))
        )
        now_ok_button.click()
        print("지금 괜찮아요 버튼 클릭 성공")
    except Exception as e:
        print(f"허용 및 동의 버튼 처리 중 에러 발생: {e}")


def like_profiles(driver):
    while True:  # 무한 반복으로 여러 프로필에 좋아요를 누름
        try:
            # 팝업 닫기
            try:
                close_popup = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="틴더로 돌아가기"]'))
                )
                close_popup.click()
                print("팝업 닫기 성공")
            except:
                print("팝업 없음, 계속 진행")

            # '좋아요' 버튼을 기다림
            like_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "(//div[contains(@class, 'gamepad-button-wrapper')]//button)[4]"))
            )

            # 버튼 가려짐 문제 해결: JavaScript로 클릭
            driver.execute_script("arguments[0].scrollIntoView(true);", like_button)
            driver.execute_script("arguments[0].click();", like_button)
            print("좋아요 버튼 클릭 성공")

            # 1초 대기 (로봇 감지 방지)
            time.sleep(1)

        except Exception as e:
            print(f"좋아요 버튼 처리 중 에러 발생: {e}")

            # 로딩 중일 가능성 → 2초 대기 후 재시도
            time.sleep(2)

# 메인 실행
try:
    driver.get("https://tinder.com/")
    print("[메인] 틴더 페이지 열림")
    tinder_login(driver)
    print("[메인] 로그인 버튼 누름")
    handle_google_login(driver)
    print("[메인] 구글 로그인 완료")
    handle_tinder_permissions(driver)
    print("[메인] 틴더 동의 버튼 체크 완료")
    like_profiles(driver)
    print("[메인] 좋아요 선택 완료")
except Exception as e:
    print(f"에러 발생: {e}")
