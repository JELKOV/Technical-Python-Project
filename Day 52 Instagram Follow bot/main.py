from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# ChromeDriver 경로 설정
chrome_driver_path = "C:/resource/chromedriver-win64/chromedriver-win64/chromedriver.exe"

SIMILAR_ACCOUNT = "다른 사람 계정 닉네임"
INSTAGRAM_ACCOUNT = "인스타그램 ID"
INSTAGRAM_PASSWORD = "비밀번호"

class InstaFollowers:
    def __init__(self):
        # Chrome WebDriver 옵션 설정
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_experimental_option("detach", True)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        self.options.add_experimental_option("useAutomationExtension", False)

        # WebDriver 실행
        self.service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

        # 브라우저 감지 우회 설정
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            """
        })

    def login(self):

        self.driver.get("https://www.instagram.com/accounts/login/")

        # 창 크기 설정
        self.driver.set_window_size(400, 800)  # 너비 800px, 높이 600px
        print("Browser window resized to 800x600")

        print("Logging Page in...")
        login_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div[1]/div[1]/div/label/input'))
        )
        print("Logged In")
        login_input.send_keys(INSTAGRAM_ACCOUNT)
        print("Logged Input ID Complete")

        print("Password Page in...")
        password_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div[1]/div[2]/div/label/input'))
        )
        print("Password In")
        password_input.send_keys(INSTAGRAM_PASSWORD)
        password_input.send_keys(Keys.ENTER)
        print("Password Complete")

        # 나중에 하기 버튼 클릭
        try:
            print("Find the later do Button...")
            pass_button = WebDriverWait(self.driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'x1yc6y37') and @role='button']"))
            )
            print("Found the later do Button")
            pass_button.click()
            print("Success Click Pass the button")
        except Exception as e:
            print("Fail Click Pass the button:", str(e))


    def find_follower(self):

        ## 상대방 계정 검색하기
        print("Finding another account...")
        search_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='입력 검색']"))
        )
        print("input another account name")
        search_input.send_keys(SIMILAR_ACCOUNT)
        search_input.send_keys(Keys.ENTER)
        print("Success Click Search button")

        ## 상대방 계정 들어가기
        print("Into another account...")
        click_another_account = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='nakedbibi님의 프로필 사진']"))
        )
        print("Found another account name")
        click_another_account.click()

        ## 상대방 계정 팔로우 버튼 눌르기
        print("Find another account followers...")
        click_another_account_followers = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/nakedbibi/followers/']"))
        )
        print("Found another account followers")
        click_another_account_followers.click()

    def follow(self):
        print("Starting to follow all followers...")

        try:
            # 모달 로드 확인
            modal = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']"))
            )
            print("Modal loaded successfully.")

            previous_height = 0
            current_index = 1  # 클릭 시작 인덱스

            while True:
                try:
                    # 동적으로 div[{i}]의 버튼 찾기
                    dynamic_xpath = f"/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div[{current_index}]/div/div/div/div[3]/div/button"
                    print(f"Processing div[{current_index}]")

                    try:
                        # 현재 div[{i}]의 팔로우 버튼 가져오기
                        follow_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, dynamic_xpath))
                        )
                        print(f"Found follow button for div[{current_index}]. Attempting to click...")

                        # 클릭 시도
                        follow_button.click()
                        time.sleep(random.uniform(2, 5))  # 클릭 후 대기

                        # 클릭 후 팝업 감지
                        try:
                            popup_xpath = "//button[contains(@class, '_a9--') and contains(@class, '_a9_1')]"
                            popup_button = WebDriverWait(self.driver, 2).until(
                                EC.presence_of_element_located((By.XPATH, popup_xpath))
                            )
                            print("Popup detected after clicking follow button.")

                            # 팝업 처리 (취소 또는 확인 버튼 클릭)
                            button_options = [
                                ("취소",
                                 "//button[contains(@class, '_a9--') and contains(@class, '_a9_1') and text()='취소']"),
                                ("확인",
                                 "//button[contains(@class, '_a9--') and contains(@class, '_a9_1') and text()='확인']")
                            ]

                            popup_handled = False  # 팝업이 처리되었는지 확인

                            for label, xpath in button_options:
                                try:
                                    button = WebDriverWait(self.driver, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, xpath))
                                    )
                                    button.click()
                                    print(f"Handled '{label}' popup for div[{current_index}].")
                                    time.sleep(2)
                                    popup_handled = True
                                    break  # 성공 시 반복 종료
                                except Exception as button_error:
                                    print(f"Failed to handle '{label}' popup for div[{current_index}]: {button_error}")

                            if not popup_handled:
                                print(f"No popup handled for div[{current_index}]. Moving to the next follower.")

                        except Exception:
                            print("No popup detected after clicking. Continuing to next follower.")

                    except Exception as click_error:
                        print(f"Error clicking follow button for div[{current_index}]: {click_error}")

                    # div[{current_index}] 작업 완료
                    print(f"Finished processing div[{current_index}]. Moving to the next div...")
                    current_index += 1  # 다음 div로 이동
                    time.sleep(2)

                except Exception:
                    # XPath가 유효하지 않으면 스크롤
                    print(f"Unable to find button for div[{current_index}]. Scrolling down...")
                    self.driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;", modal
                    )
                    time.sleep(2)

                    # DOM 갱신
                    modal = WebDriverWait(self.driver, 20).until(
                        EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']"))
                    )
                    print("DOM updated successfully after scrolling.")

                    # 스크롤 종료 조건 확인
                    current_height = self.driver.execute_script("return arguments[0].scrollHeight;", modal)
                    print("Current height of modal is:", current_height)
                    if current_height == previous_height:
                        print("Reached the end of the list. Exiting loop...")
                        break
                    previous_height = current_height

        except Exception as e:
            print(f"Error during following process: {e}")


insta_followers = InstaFollowers()
try:
    insta_followers.login()
    insta_followers.find_follower()
    insta_followers.follow()
except Exception as e:
    print(e)