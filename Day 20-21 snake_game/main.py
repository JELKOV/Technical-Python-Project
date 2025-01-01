from turtle import Turtle, Screen
import time

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
# 화면 갱신을 수동으로 설정
screen.tracer(0)

# 튜플로 반복문 돌리기
starting_position = [(0,0), (-20,0), (-40,0)]

# 튜플을 만드는 이유가 무엇일까 ?
turtle_list = []

for position in starting_position:
    new_turtle = Turtle("square")
    new_turtle.color("white")
    new_turtle.penup()
    new_turtle.goto(position)
    turtle_list.append(new_turtle)



game_is_on = True  # 게임 루프를 제어하는 플래그 (True일 동안 게임이 계속 실행됨)

while game_is_on:
    screen.update()  # 화면을 갱신하여 모든 변경 사항을 즉시 반영
    time.sleep(0.1)  # 루프마다 0.1초 대기하여 게임 속도를 조절

    # 터틀 리스트를 역순으로 반복 (뱀의 몸체를 뒤에서부터 처리)
    for turtle in range(len(turtle_list) - 1, 0, -1):
        # 앞 세그먼트(turtle_list[turtle - 1])의 x, y 좌표 가져오기
        new_x = turtle_list[turtle - 1].xcor()
        new_y = turtle_list[turtle - 1].ycor()

        # 현재 세그먼트(turtle_list[turtle])를 앞 세그먼트 위치로 이동
        turtle_list[turtle].goto(new_x, new_y)

    turtle_list[0].forward(20)
    turtle_list[0].left(90)

screen.exitonclick()