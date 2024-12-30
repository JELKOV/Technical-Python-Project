# with open("weather_data.csv") as data_file:
#     data = data_file.readlines()
#     print(data)

# import csv
#
# with open("weather_data.csv") as data_file:
#     csv_reader = csv.reader(data_file)
#     print(csv_reader)
#     temperatures = []
#     for row in csv_reader:
#         print(row[1])
#         if row[1] != "temp":
#             temperatures.append(int(row[1]))
#     print(temperatures)

# import pandas  # Pandas 라이브러리 임포트
#
# # CSV 파일("weather_data.csv")을 읽어 DataFrame으로 로드
# data = pandas.read_csv("weather_data.csv")
# print(data)  # DataFrame 내용을 출력
#
# # DataFrame의 데이터 타입 확인
# print(type(data))  # 출력: <class 'pandas.core.frame.DataFrame'>
#
# # 'temp' 열 데이터를 가져와 데이터 타입 확인
# print(type(data["temp"]))  # 출력: <class 'pandas.core.series.Series'>
#
# # DataFrame을 딕셔너리로 변환
# data_dic = data.to_dict()
# print(data_dic)  # 딕셔너리 형태로 변환된 데이터 출력
#
# # 'temp' 열 데이터를 리스트로 변환
# temp_list = data["temp"].to_list()
# print(temp_list)  # 리스트 형태로 변환된 'temp' 열 데이터 출력
# print(len(temp_list))  # 리스트의 길이(데이터 개수) 출력
#
#
# # 평균 온도를 구하기
# avg_temp = sum(temp_list) / len(temp_list)
# print("평균값:", avg_temp)
#
# # 평균 온도를 구하기
# print(data["temp"].mean())
#
# # 최대 값 구하기
# print(data["temp"].max())
#
# # 컨디션 열 값 구하기
# print(data["condition"])
#
# print(data.condition)
#
# # 행의 값을 구하기
# ## 행안에 있는 값을 찾은 후 그행을 보여달라고 하면서 구함
# print(data[data.day == "Monday"])
#
# # 가장 높은 온도가 있는 데이터의 행을 검색해보자
# # 가장 높은 온도를 찾기
# max_temp = data["temp"].max()
# result = data[data["temp"] == max_temp]
# print(result)
#
# # 2번째 방법
# print(data[data.temp == data.temp.max()])
#
# # 변수로 설정해서 행값 뽑아내기
# monday = data[data.day == "Monday"]
# print(monday.condition)
# print(monday.temp)
# monday_temp = int(monday.temp.iloc[0])
# monday_temp_F = monday_temp * 9 / 5 + 32
# print(monday_temp_F)
#
# # 데이터 프레임을 만들어보자
# data_dict = {
#     "students": ["Amy", "James", "Angela"],
#     "scores": [ 76, 56, 65]
# }
#
# data = pandas.DataFrame(data_dict)
# print(data)
# # CSV 파일로 바꾸기
# data.to_csv("new_data.csv")

import pandas as pd
data = pd.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data_20241230.csv")

print(data["Primary Fur Color"])
data_color_counts = data["Primary Fur Color"].value_counts()
print(data_color_counts)
data_color_counts.to_csv("squrriel_data.csv")


##
grey_squirrels_count = len(data[data["Primary Fur Color"] == "Grey"])
red_squirrels_count = len(data[data["Primary Fur Color"] == "Red"])
black_squirrels_count = len(data[data["Primary Fur Color"] == "Black"])

data_dict = {
    "Fur Color": ["Grey", "Cinnamon", "Black"],
    "Count": [grey_squirrels_count, red_squirrels_count, black_squirrels_count]
}
df = pd.DataFrame(data_dict)
df.to_csv("squirrel2_data.csv")
