import turtle  # turtle 모듈 가져오기
from turtle import Turtle, Screen  # Turtle 및 Screen 클래스 가져오기
import random  # random 모듈 가져오기

# RGB 색상 모드를 255 범위로 설정
turtle.colormode(255)

# 터틀 객체 생성 및 초기 설정
jaeho_turtle = Turtle()  # 터틀 객체 생성
jaeho_turtle.shape("turtle")  # 거북이 모양 설정
jaeho_turtle.pensize(15)  # 선 두께 설정
jaeho_turtle.speed("fastest")  # 터틀 속도를 가장 빠르게 설정

# 무작위 색상 생성 함수
def random_color():
    """
    0~255 사이의 RGB 값을 랜덤으로 생성하여 색상 반환
    """
    r = random.randint(0, 255)  # 빨강 값 생성
    g = random.randint(0, 255)  # 초록 값 생성
    b = random.randint(0, 255)  # 파랑 값 생성
    color = (r, g, b)  # RGB 색상 튜플 생성
    return color

# 터틀의 이동 방향 리스트
directions = [0, 90, 180, 270]  # 동쪽, 북쪽, 서쪽, 남쪽 방향

# 반복 횟수를 랜덤으로 설정
random_steps = random.randint(100, 500)  # 100에서 500 사이의 랜덤 반복 횟수

# 무작위 행보 구현
for i in range(random_steps):  # 랜덤 반복 횟수 동안 실행
    this_color = random_color()  # 랜덤 색상 생성
    jaeho_turtle.pencolor(this_color)  # 펜 색상 변경
    jaeho_turtle.setheading(random.choice(directions))  # 랜덤 방향 설정
    jaeho_turtle.fd(30)  # 30 픽셀 앞으로 이동

# 화면을 클릭하면 종료
screen = Screen()  # 화면 객체 생성
screen.exitonclick()  # 사용자가 화면을 클릭할 때까지 대기
