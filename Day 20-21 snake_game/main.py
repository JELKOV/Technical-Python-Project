from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
# 화면 갱신을 수동으로 설정
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

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

    # 먹이 감지 (distance)
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()
        print("꿀꺽")

    # 벽꿍 (game over)
    if snake.head.xcor() > 290 or snake.head.xcor() < -290 or snake.head.ycor() > 290 or snake.head.ycor() < -290:
        game_is_on = False
        scoreboard.game_over()

    # 꼬리 붇히기 (game over)
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            game_is_on = False
            scoreboard.game_over()


screen.exitonclick()