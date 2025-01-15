import requests
from datetime import datetime

TOKEN = "secret"
USERNAME = "secret"
GRAPH_ID = "secret"

##################### 계정 생성 #######################

PIXELA_ENDPOINT = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,  # 내 스스로 생성
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}
# 계정 생성 한번만
# ## POST 요청
# response = requests.post(url=PIXELA_ENDPOINT, json=user_params) ## JSON 형식으로 보내야 한다.
# print(response.json())



#################### 그래프 정의 #######################

PIXELA_GRAPH_ENDPOINT = f"{PIXELA_ENDPOINT}/{user_params['username']}/graphs/"

graph_definition_params = {
    "id": GRAPH_ID,
    "name": "coding-process",
    "unit": "time",
    "type": "int",
    "color": "kuro",
}

######################### 토큰 헤더#############################################
headers = {
    "X-USER-TOKEN": user_params['token']
}
######################### 토큰 헤더#############################################

## POST 요청 # 한번만
# response = requests.post(url=PIXELA_GRAPH_ENDPOINT, json=graph_definition_params, headers=headers)
# print(response.json())


#################### 픽셀 추가하기 ######################

PIXELA_PIXEL_ENDPOINT = f"{PIXELA_ENDPOINT}/{user_params['username']}/graphs/{graph_definition_params['id']}"

today = datetime.now() ## 현재 시간
# today = datetime(year=2025, month=1, day=13)  ## 수동 입력

to_date = today.strftime("%Y%m%d")
print(to_date)

post_pixel_params = {
    "date": to_date,
    "quantity": input("Enter the quantity you would like to add: ")
}

# ## POST 요청
response = requests.post(url=PIXELA_PIXEL_ENDPOINT, json=post_pixel_params, headers=headers)
print(response.json())


################## 픽셀 업데이트 #########################

# PUT 요청
update_date = datetime(year=2025, month=1, day=13)
fix_date = update_date.strftime("%Y%m%d")

PIXELA_PIXEL_UPDATE_ENDPOINT = f"{PIXELA_ENDPOINT}/{user_params['username']}/graphs/{graph_definition_params['id']}/{fix_date}"

update_pixel_params = {
    "quantity": "80"
}

# response = requests.put(url=PIXELA_PIXEL_UPDATE_ENDPOINT, json=update_pixel_params, headers=headers)
# print(response.json())



################ 픽셀 삭제 #############################

# DELETE 요청
delete_date = datetime(year=2025, month=1, day=13)
delete_date = delete_date.strftime("%Y%m%d")

PIXELA_PIXEL_DELETE_ENDPOINT = f"{PIXELA_ENDPOINT}/{user_params['username']}/graphs/{graph_definition_params['id']}/{delete_date}"

# response = requests.delete(url=PIXELA_PIXEL_DELETE_ENDPOINT, headers=headers)
# print(response.text)