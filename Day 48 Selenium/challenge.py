from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Chrome 옵션 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # 브라우저 종료 방지

driver = webdriver.Chrome(options=chrome_options)
url = "http://secure-retreat-92358.herokuapp.com/"
driver.get(url)

input_firstname = driver.find_element(By.NAME, "fName")
input_firstname.send_keys("AHN")

input_lastname = driver.find_element(By.NAME, "lName")
input_lastname.send_keys("JAEHO")

input_email = driver.find_element(By.NAME, "email")
input_email.send_keys("ajh4234@gmail.com")

# # 버튼 클릭 (CLASS NAME)
# signup_button = driver.find_element(By.CLASS_NAME, "btn-primary")
# signup_button.click()

# # 버튼 클릭 (CSS_SELECTOR)
# signup_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-lg.btn-primary.btn-block")
# signup_button.click()

# 버튼 클릭 (CSS_SELECTOR)
signup_button = driver.find_element(By.CSS_SELECTOR, "form button")
signup_button.click()