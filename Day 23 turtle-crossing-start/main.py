import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

# 화면 설정
screen = Screen()
screen.setup(width=600, height=600)  # 화면 크기 설정 (600x600 픽셀)
screen.tracer(0)  # 애니메이션을 끄고 수동 업데이트 사용

# 플레이어(거북이) 객체 생성
player = Player()

# 자동차 관리자 객체 생성
car_manager = CarManager()

# 점수판 객체 생성
scoreboard = Scoreboard()

# 키보드 입력 설정
screen.listen()  # 키 입력 감지 활성화
screen.onkey(player.move, "Up")  # "위" 키를 누르면 플레이어가 위로 이동

# 게임 루프 시작
game_is_on = True
while game_is_on:
    time.sleep(0.1)  # 루프 딜레이 (0.1초마다 갱신)
    screen.update()  # 화면 업데이트

    # 1. 자동차 생성 및 이동
    car_manager.create_car()  # 랜덤한 확률로 새로운 자동차 생성
    car_manager.move_cars()  # 모든 자동차를 왼쪽으로 이동

    # 2. 충돌 감지
    for car in car_manager.all_cars:  # 모든 자동차를 순회하며 충돌 여부 확인
        if car.distance(player) < 20:  # 플레이어와 자동차 간의 거리 계산
            game_is_on = False  # 충돌 시 게임 종료
            scoreboard.game_over()  # "GAME OVER" 메시지 표시

    # 3. 플레이어가 화면 위쪽에 도달했는지 확인
    if player.has_crossed_finish_line():
        player.starting_position()  # 플레이어를 시작 위치로 리셋
        car_manager.increase_speed()  # 자동차 속도 증가
        scoreboard.increase_level()  # 점수판의 레벨 증가

# 클릭 시 프로그램 종료
screen.exitonclick()
