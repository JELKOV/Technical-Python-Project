from selenium import webdriver
from selenium.webdriver.common.by import By

# 사용자 지정 헤더를 위한 Chrome 옵션 설정
chrome_options = webdriver.ChromeOptions()
# 브라우저가 종료되지 않도록 설정
chrome_options.add_experimental_option("detach", True)

# WebDriver 초기화
driver = webdriver.Chrome(options=chrome_options)

url = "https://www.python.org/"
driver.get(url)  # Amazon 페이지로 이동

# Q로된 NAME 값 찾아보기
search_bar = driver.find_element(By.NAME, "q")
print(search_bar.tag_name)
print(search_bar.get_attribute("type"))
print(search_bar.get_attribute("placeholder"))

# submit Button 값 찾아보기
button = driver.find_element(By.ID, "submit")
print(button.tag_name)
print(button.size)

# CSS Selector 이용하기
documentation_link = driver.find_element(By.CSS_SELECTOR, ".documentation-widget a")
print(documentation_link.text)

# X Path 이용하기
bug_link = driver.find_element(By.XPATH, '//*[@id="dive-into-python"]/ul[2]/li[1]/div[1]/pre/code')
print(bug_link.text)

#브라우저 닫기
driver.quit()