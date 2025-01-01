import turtle
from turtle import Turtle, Screen
import random

# 게임 종료 조건
is_race_on = False  # 레이스가 시작되었는지 여부를 확인하는 플래그

# 화면 설정
screen = Screen()
screen.setup(500, 600)  # 화면 크기 설정 (가로: 500, 세로: 600)

# 사용자로부터 터틀 색상에 베팅 입력받기
user_bet = screen.textinput(title="Betting", prompt="Which turtle will win the race?: Enter a Color: red, blue, green, yellow, purple, cyan, pink")

# 터틀의 색상을 정의
colors = ["red", "blue", "green", "yellow", "purple", "cyan", "pink"]

# 생성된 터틀 객체를 저장할 리스트
turtles = []

# 출발선 좌표 설정
start_x = -230  # 모든 터틀의 x축 시작 위치
start_y = -100  # 첫 번째 터틀의 y축 시작 위치
y_offset = 30   # 각 터틀 간 y축 간격

# 터틀 생성 및 배치
for index, color in enumerate(colors):
    new_turtle = Turtle(shape="turtle")  # 터틀 생성
    new_turtle.color(color)  # 터틀 색상 설정
    new_turtle.penup()  # 선을 그리지 않도록 설정
    new_turtle.goto(x=start_x, y=start_y + index * y_offset)  # 출발선에 터틀 배치
    turtles.append(new_turtle)  # 생성된 터틀을 리스트에 추가

# 사용자 입력이 있다면 게임 시작
if user_bet:
    is_race_on = True  # 레이스 시작

# 레이스가 진행 중인 동안 반복
while is_race_on:
    for turtle in turtles:
        # 터틀이 결승선(x > 230)에 도달하면 종료 조건 만족
        if turtle.xcor() > 230:  # x 좌표가 230을 넘으면 레이스 종료
            is_race_on = False  # 레이스 종료
            winning_color = turtle.pencolor()  # 우승한 터틀의 색상 가져오기
            # 우승한 터틀이 사용자의 베팅과 일치하면 승리 메시지 출력
            if winning_color == user_bet:
                print(f"You Win! The {winning_color} turtle is at {turtle.xcor()}.")
            else:
                # 베팅 실패 시 메시지 출력
                print(f"You Lost! The {winning_color} turtle is at {turtle.xcor()}.")
        # 터틀의 움직임을 랜덤으로 설정 (0 ~ 10 픽셀 이동)
        rand_instance = random.randint(0, 10)
        turtle.forward(rand_instance)

# 화면 종료 조건 (클릭 시 종료)
screen.exitonclick()
