from turtle import Turtle, Screen  # Turtle과 Screen 클래스를 가져옴
import turtle as t  # turtle 모듈을 t로 축약하여 가져옴

import random

# 거북이 객체 생성 및 초기 설정
jaeho_turtle = Turtle()  # Turtle 객체 생성
jaeho_turtle.shape("turtle")  # 거북이 모양 설정
# jaeho_turtle.color("gold")  # 거북이 색상 설정

colors = ["DeepPink", "IndianRed", "HotPink", "Magenta", "SaddleBrown", "Indigo", "Yellow", "BlueViolet", "Gold","PowderBlue"]

# 100만큼 전진 후 90도 오른쪽으로 회전하는 함수 정의
def forward100_right90():
    """
    거북이를 100픽셀 앞으로 이동시키고 90도 오른쪽으로 회전시킵니다.
    """
    jaeho_turtle.forward(100)  # 100픽셀 전진
    jaeho_turtle.right(90)  # 90도 오른쪽 회전

#  10 색 10 무색
def forward10_teleport10():
    jaeho_turtle.forward(10)
    jaeho_turtle.penup()
    jaeho_turtle.forward(10)
    jaeho_turtle.pendown()

# 삼각형 그리기
def triangle():
    jaeho_turtle.forward(100)
    jaeho_turtle.right(120)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(120)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(120)
# 사각형 그리기
def square():
    jaeho_turtle.forward(100)
    jaeho_turtle.right(90)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(90)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(90)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(90)
# 오각형 그리기
def pentagon():
    jaeho_turtle.forward(100)
    jaeho_turtle.right(72)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(72)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(72)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(72)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(72)
# 육각형 그리기
def hexagon():
    jaeho_turtle.forward(100)
    jaeho_turtle.right(60)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(60)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(60)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(60)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(60)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(60)
# 칠각형 그리기
def heptagon():
    jaeho_turtle.forward(100)
    jaeho_turtle.right(51)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(51)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(51)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(51)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(51)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(51)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(51)
# 팔각형 그리기
def octagon():
    jaeho_turtle.forward(100)
    jaeho_turtle.right(45)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(45)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(45)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(45)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(45)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(45)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(45)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(45)
# 구각형 그리기
def nonagon():
    jaeho_turtle.forward(100)
    jaeho_turtle.right(40)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(40)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(40)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(40)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(40)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(40)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(40)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(40)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(40)

# 십각형 그리기
def decagon():
    jaeho_turtle.forward(100)
    jaeho_turtle.right(36)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(36)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(36)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(36)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(36)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(36)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(36)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(36)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(36)
    jaeho_turtle.forward(100)
    jaeho_turtle.right(36)


# N각형 그리기 함수화
def draw_shape(num_sides):
    angle = 360 / num_sides
    for i in range(num_sides):
        jaeho_turtle.forward(100)
        jaeho_turtle.right(angle)

for shape_side_n in range(3,11):
    jaeho_turtle.color(random.choice(colors))
    draw_shape(shape_side_n)
# 실행문
# for i in range(1):


# 화면을 클릭하면 종료
screen = Screen()  # 화면 객체 생성
screen.exitonclick()  # 사용자가 화면을 클릭할 때까지 대기
