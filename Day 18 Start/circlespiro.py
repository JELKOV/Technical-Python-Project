from turtle import Turtle, Screen
import turtle  # turtle 모듈 가져오기
import random
# RGB 색상 모드를 255 범위로 설정
turtle.colormode(255)

# 터틀 객체 생성 및 초기 설정
jaeho_turtle = Turtle()  # 터틀 객체 생성
jaeho_turtle.shape("turtle")  # 거북이 모양 설정
jaeho_turtle.speed("fastest")  # 속도


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
"""
사용된 기능:
    단순히 left(i)로 각도를 점진적으로 증가시키며 원을 그립니다.
    각 반복에서 증가하는 i 값이 회전 각도에 반영되므로, 각도가 계속 변화합니다.
결과 패턴:
    원의 회전 각도가 점진적으로 커지는 비대칭적인 패턴이 생성됩니다.
    점진적 변화로 인해 중심이 이동하며, 원들이 겹치거나 비대칭적으로 배치됩니다

"""
for i in range(1, 360):
    this_color = random_color()  # 랜덤 색상 생성
    jaeho_turtle.pencolor(this_color)  # 펜 색상 변경
    jaeho_turtle.circle(50)
    jaeho_turtle.left(i)

"""
사용된 기능:
    draw_spirograph(size_of_gap) 함수는 지정된 간격(size_of_gap)만큼 회전하며 원을 그립니다.
    각 원의 크기(circle(100))는 고정되어 있으며, size_of_gap에 따라 각도만 변화합니다.
결과 패턴:
    중심에서 시작하여 회전 간격이 일정한 대칭적이고 정렬된 스피로그래프(기하학적 무늬)가 생성됩니다.
"""
def draw_spirograph(size_of_gap):
    for i in range(int(360/ size_of_gap)):
        jaeho_turtle.color(random_color())
        jaeho_turtle.circle(100)
        jaeho_turtle.setheading((jaeho_turtle.heading() + size_of_gap))

draw_spirograph(5)
# 화면을 클릭하면 종료
screen = Screen()  # 화면 객체 생성
screen.exitonclick()  # 사용자가 화면을 클릭할 때까지 대기
