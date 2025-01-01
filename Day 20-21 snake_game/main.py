from turtle import Screen
from snake import Snake
import time

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
# 화면 갱신을 수동으로 설정
screen.tracer(0)

snake = Snake()

screen.listen()
screen.onkey(snake.turn_up, "Up")
screen.onkey(snake.turn_down, "Down")
screen.onkey(snake.turn_left, "Left")
screen.onkey(snake.turn_right, "Right")

game_is_on = True  # 게임 루프를 제어하는 플래그 (True일 동안 게임이 계속 실행됨)

while game_is_on:
    screen.update()  # 화면을 갱신하여 모든 변경 사항을 즉시 반영
    time.sleep(0.1)  # 루프마다 0.1초 대기하여 게임 속도를 조절

    snake.move()

screen.exitonclick()