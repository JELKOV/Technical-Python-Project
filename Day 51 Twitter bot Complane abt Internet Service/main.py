from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PROMISED_DOWN = 150
PROMISED_UP = 10
chrome_driver_path = "C:/resource/chromedriver-win64/chromedriver-win64/chromedriver.exe"
X_EMAIL= "구글로그인 아이디"
X_PASSWORD= "구글로그인 비밀번호"


class InternetSpeedXBot:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-popup-blocking")
        options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(service = Service(chrome_driver_path), options=options)

        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            """
        })

        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        print("Speedtest 페이지 로드 중...")
        self.driver.get("https://www.speedtest.net/")

        print("시작 버튼 찾는 중...")
        start_button = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[1]/a'))
        )
        print("시작 버튼 클릭...")
        start_button.click()

        # 강제로 대기 (측정 시간이 충분히 지났다고 가정)
        print("테스트가 진행 중입니다. 75초 대기...")
        time.sleep(75)

        print("속도 결과 가져오는 중...")
        # 다운로드 속도 가져오기
        self.down = self.driver.find_element(By.XPATH,
                                             '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text
        print(f"다운로드 속도: {self.down} Mbps")

        # 업로드 속도 가져오기
        self.up = self.driver.find_element(By.XPATH,
                                           '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text
        print(f"업로드 속도: {self.up} Mbps")

    def x_at_provider(self):
        print("X 페이지 로딩중")

        print("x button 찾는중")
        x_button = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[1]/div/div/div[1]/div[2]/div/div/div[1]/a[2]')
            )
        )
        print("x 버튼 클릭")
        x_button.click()

        # 창 전환 대기
        print("새 창 열림 대기")
        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
        all_windows = self.driver.window_handles
        self.driver.switch_to.window(all_windows[-1])  # 새 창으로 전환
        print("새 창으로 전환 완료")

        # 모달 로드 확인
        print("모달 로드 대기 중...")
        modal = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]'))
        )
        print("모달 로드 완료")

        # 로그인 버튼 찾기 및 클릭
        try:
            print("로그인 버튼 찾는 중...")
            login_button = WebDriverWait(modal, 50).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/button[2]'))
            )
            print("로그인 버튼 찾기 성공")
            self.driver.execute_script("arguments[0].click();", login_button)
        except Exception as e:
            print(f"로그인 버튼 처리 중 오류 발생: {e}")
            print("현재 창 핸들:", self.driver.current_window_handle)
            print("모든 창 핸들:", self.driver.window_handles)
            raise

        # Google 버튼 처리
        print("Google Login Button 찾는중")
        try:
            google_button = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "LgbsSe")]'))
            )
            self.driver.execute_script("arguments[0].click();", google_button)
            print("Google 버튼 클릭 성공")
        except Exception as e:
            print(f"Google 버튼 처리 중 오류 발생: {e}")
            print("현재 창 핸들:", self.driver.current_window_handle)
            print("모든 창 핸들:", self.driver.window_handles)
            raise

        # 두 번째 창 전환 대기
        print("Google 로그인 창 열림 대기")
        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(3))
        all_windows = self.driver.window_handles
        self.driver.switch_to.window(all_windows[-1])  # Google 로그인 창으로 전환
        print("Google 로그인 창으로 전환 완료")

        # Google 로그인 페이지에서 이메일 입력
        email_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys(X_EMAIL)
        email_input.send_keys(Keys.ENTER)
        print("이메일 입력 성공")

        # 비밀번호 입력
        password_input = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))
        )
        password_input.click()
        password_input.send_keys(X_PASSWORD)
        password_input.send_keys(Keys.ENTER)
        print("비밀번호 입력 성공")

        # 추가 인증 대기 (예: CAPTCHA)
        print("추가 인증 대기 중...")
        input("추가 인증을 완료한 후 Enter를 누르세요...")

        # 추가 인증후 돌아가기
        print("x 창으로 복귀 중...")
        self.driver.switch_to.window(all_windows[1])
        print("x 창으로 복귀 완료")

    def x_complaint(self):

        # 트윗 작성
        print("x 내용 작성 중...")
        x_input = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div'))
        )
        x_text = f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
        x_input.send_keys(x_text)
        print(f"x 내용 입력 완료: {x_text}")

        # 트윗 전송
        print("x 전송 중...")
        x_submit = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button'))
        )
        x_submit.click()
        print("X POST 완료")

internet_bot = InternetSpeedXBot()
try:
    internet_bot.get_internet_speed()
    internet_bot.x_at_provider()
    internet_bot.x_complaint()
except Exception as e:
    print(e)