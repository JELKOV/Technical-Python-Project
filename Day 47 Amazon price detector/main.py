from bs4 import BeautifulSoup
import smtplib
import requests

#amazon 상품 URL
AMAZON_URL="https://www.amazon.com/CyberPowerPC-i5-13400F-GeForce-Windows-GXiVR8060A24/dp/B0DCMPRRFD/ref=sr_1_1?_encoding=UTF8&content-id=amzn1.sym.860dbf94-9f09-4ada-8615-32eb5ada253a&dib=eyJ2IjoiMSJ9.d9IPnRE6tAt-jLfAjOennMt4nMKb0llUb3kh95nLJxj30Uc-x3Cr64xLi13PkNOlyy_LWncqNFs7k0UqRKkG5Is1kWaAd0pal4sLPng0qvwUCgOurQLxSEdsNRhj6CiULTxqpTdSKUXjNcISHj2zAcOfsDmKUnp_K_tPLxjTNU48x-ILMPB8aV_YEfC_NABQhTMBqmlZ4rR2vB0aNNmthnM5-CPAPL61Hd5gU7pxRa8LnarSUTTKamSltFyo676toRaCseIIOLWz_89zRSL7dyFNfKjpS6lL-FPZL4Wxb2115xQBYYy3XN7a22yF0lNyoSNx5VrC-Lt4KsNMlEgHBdDbjnjT_JTAfgQJI51tHKQuhgSF25YZLUy3ncpl7cnZ9VP9ayyOcGDvp9UFWQULQ4JDTZAsbOLdB599nK1QcWgfRuU7q_lAQyyR_mgPn8MA.gMIZbyWBnFfIVs4k0H_iFOVlJDSkrNekm_yCZ-iFkWg&dib_tag=se&keywords=gaming&pd_rd_r=85903a4b-9f15-4613-ae62-4843145456a6&pd_rd_w=HDASl&pd_rd_wg=ccwjB&pf_rd_p=860dbf94-9f09-4ada-8615-32eb5ada253a&pf_rd_r=RPD7TMFAA4Z1K0ZZ53B4&qid=1736614219&sr=8-1&th=1"

# Gmail 계정 정보
MY_EMAIL = "secret"
APP_PASSWORD = "secret"  # 카카오톡 확인

# 목표 가격
TARGET_PRICE = 900

#아마존 스크랩핑을 위한 헤더 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
}

# 응답 받기
response = requests.get(url=AMAZON_URL, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# 상품명 추출
product_title = soup.find(id="productTitle").get_text(strip=True)

# 가격 정보 추출
price_whole = soup.find("span", class_="a-price-whole").get_text(strip=True)
price_fraction = soup.find("span", class_="a-price-fraction").get_text(strip=True)
price = float(price_whole + price_fraction)  # 가격을 float로 변환

print(price)

# 2. 가격 확인 및 이메일 전송
if price < TARGET_PRICE:
    message = f"Subject: Amazon Price Alert!\n\n{product_title} is now ${price}!\n\nBuy it here: {AMAZON_URL}"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, APP_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=message
        )
    print("Email sent successfully!")
else:
    print(f"The price is still ${price}, which is above the target price of ${TARGET_PRICE}.")