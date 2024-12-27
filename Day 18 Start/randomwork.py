from turtle import Turtle, Screen
import random

jaeho_turtle = Turtle()
jaeho_turtle.shape("turtle")
jaeho_turtle.pensize(15) # 선 두께 설정
jaeho_turtle.speed("fastest")  # 속도

colors = ["DeepPink", "IndianRed", "HotPink", "Magenta", "SaddleBrown", "Indigo", "Yellow", "BlueViolet", "Gold","PowderBlue"]

directions= [0, 90, 180, 270] # 방향

# 반복 횟수를 랜덤으로 설정
random_steps = random.randint(100, 500)  # 100에서 500 사이의 무작위 반복

for i in range(random_steps):
    jaeho_turtle.color(random.choice(colors))
    jaeho_turtle.setheading(random.choice(directions))
    jaeho_turtle.fd(30)

# 화면을 클릭하면 종료
screen = Screen()  # 화면 객체 생성
screen.exitonclick()  # 사용자가 화면을 클릭할 때까지 대기