# ###This code will not work in repl.it as there is no access to the colorgram package here.###
# ##We talk about this in the video tutorials##
# import colorgram
#
# rgb_colors = []
# colors = colorgram.extract('image.jpg', 30)
# for color in colors:
#     # rgb_colors.append(color.rgb)
#     r = color.rgb.r
#     g = color.rgb.g
#     b = color.rgb.b
#
#     new_rgb = (r, g, b)
#     rgb_colors.append(new_rgb)
#
# print(rgb_colors)

from turtle import Turtle, Screen  # Turtle과 Screen 클래스 가져오기
import turtle  # turtle 모듈 가져오기
import random  # random 모듈 가져오기

# Turtle 모듈의 색상 모드를 255로 설정 (RGB 값으로 색상 표현 가능)
turtle.colormode(255)

# 터틀 객체 생성 및 초기 설정
jaeho_turtle = Turtle()  # 터틀 객체 생성
jaeho_turtle.shape("turtle")  # 거북이 모양 설정
jaeho_turtle.speed("fastest")  # 터틀 속도 최대로 설정
jaeho_turtle.penup()  # 선을 그리지 않도록 설정 (점만 찍기 위해 사용)
jaeho_turtle.hideturtle()  # 터틀을 숨겨 화면에 표시하지 않음

# 색상 리스트 정의 (이미지에서 추출한 색상 데이터)
color_list = [
    (202, 164, 110), (240, 245, 241), (236, 239, 243), (149, 75, 50),
    (222, 201, 136), (53, 93, 123), (170, 154, 41), (138, 31, 20),
    (134, 163, 184), (197, 92, 73), (47, 121, 86), (73, 43, 35),
    (145, 178, 149), (14, 98, 70), (232, 176, 165), (160, 142, 158),
    (54, 45, 50), (101, 75, 77), (183, 205, 171), (36, 60, 74),
    (19, 86, 89), (82, 148, 129), (147, 17, 19), (27, 68, 102),
    (12, 70, 64), (107, 127, 153), (176, 192, 208), (168, 99, 102)
]

# 시작 위치 설정
jaeho_turtle.setheading(225)  # 터틀 방향을 왼쪽 아래(225도)로 설정
jaeho_turtle.forward(300)  # 터틀을 왼쪽 아래로 300 이동 (그리기 시작 위치로 이동)
jaeho_turtle.setheading(0)  # 터틀 방향을 오른쪽(0도)으로 설정

color_index = 0  # 색상 리스트의 현재 색상 인덱스를 초기화

# 10x10 점 배열 생성
for row in range(10):  # 10개의 행을 반복
    for col in range(10):  # 각 행에 10개의 점을 생성
        # 색상 리스트에서 순서대로 색상 선택
        if color_index < len(color_list):
            current_color = color_list[color_index]  # 현재 색상 설정
            color_index += 1  # 다음 색상으로 이동
        else:
            # 색상 리스트의 색상이 소진되면 랜덤 색상 선택
            current_color = random.choice(color_list)

        # 터틀이 점을 찍음
        jaeho_turtle.dot(20, current_color)  # 점 크기: 20, 색상: current_color
        jaeho_turtle.forward(50)  # 점 사이 간격: 50 (오른쪽으로 이동)

    # 한 행이 끝나면 다음 행으로 이동
    jaeho_turtle.setheading(90)  # 터틀 방향을 위쪽(90도)으로 설정
    jaeho_turtle.forward(50)  # 세로 간격: 50
    jaeho_turtle.setheading(180)  # 터틀 방향을 왼쪽(180도)으로 설정
    jaeho_turtle.forward(500)  # 한 줄의 폭만큼 왼쪽으로 이동
    jaeho_turtle.setheading(0)  # 터틀 방향을 다시 오른쪽(0도)으로 설정

# 화면 종료 조건 설정
screen = Screen()  # 화면 객체 생성
screen.exitonclick()  # 사용자가 화면을 클릭하면 프로그램 종료
