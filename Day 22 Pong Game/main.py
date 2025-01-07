from turtle import Screen
from paddle import Paddle
from paddle_controller import PaddleController
from ball import Ball
from scoreboard import Scoreboard

# ------------------------ UI 설정 -----------------------------
# 화면(게임 창) 설정
screen = Screen()
screen.setup(width=800, height=600)  # 창 크기 설정 (너비: 800, 높이: 600).
screen.bgcolor("black")  # 배경색을 검정색으로 설정.
screen.title("Pong")  # 창 제목 설정.
screen.tracer(0)  # 화면 갱신 비활성화 (애니메이션 효과용).

# 각 플레이어를 위한 Paddle 객체 생성
paddle_1 = Paddle(position=(-350, 0))  # 왼쪽 Paddle 생성.
paddle_2 = Paddle(position=(350, 0))  # 오른쪽 Paddle 생성.

# 공 생성
ball = Ball(position=(0, 0))  # 공 초기 위치 (0, 0)에서 생성.

# 점수판 추가
scoreboard = Scoreboard()  # 점수판 초기화.

# PaddleController 생성: Paddle과 키 설정
paddle_1_controller = PaddleController(screen, paddle_1, "w", "s")  # W/S 키로 Paddle1 제어.
paddle_2_controller = PaddleController(screen, paddle_2, "Up", "Down")  # 방향키로 Paddle2 제어.

# ------------------------ 게임 루프 -----------------------------
game_is_on = True
while game_is_on:
    # PaddleController의 move 메서드 호출
    paddle_1_controller.move()  # 플레이어 1의 패들 이동.
    paddle_2_controller.move()  # 플레이어 2의 패들 이동.

    # 화면 갱신
    screen.update()

    # 공 움직임
    ball.move()

    # 공이 패들에 닿으면 반전
    if ball.distance(paddle_1) < 50 and ball.xcor() < -335:
        # 공과 왼쪽 패들 사이의 거리가 50 이내이고, 공이 패들 왼쪽 영역에 있을 경우
        ball.bounce_x()  # X축 방향 반전.

    if ball.distance(paddle_2) < 50 and ball.xcor() > 335:
        # 공과 오른쪽 패들 사이의 거리가 50 이내이고, 공이 패들 오른쪽 영역에 있을 경우
        ball.bounce_x()  # X축 방향 반전.

    # 공이 X축 경계에 닿으면 점수 증가 및 공 초기화
    if ball.xcor() > 390:
        scoreboard.update_score("left")
        ball.reset_position()

    if ball.xcor() < -390:
        scoreboard.update_score("right")
        ball.reset_position()
# 클릭으로 창 닫기
screen.exitonclick()