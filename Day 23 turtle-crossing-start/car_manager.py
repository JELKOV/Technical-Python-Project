from turtle import Turtle, Screen
import random
import time

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:
    def __init__(self):
        self.all_cars = []  # 모든 자동차를 관리하는 리스트
        self.car_speed = STARTING_MOVE_DISTANCE  # 초기 자동차 이동 속도

    def create_car(self):
        """랜덤하게 새로운 자동차를 생성"""
        # 낮은 확률로 자동차 생성 (게임 루프에서 과도한 생성 방지)
        if random.randint(1, 6) == 1:  # 1~6 중 1일 때만 생성
            new_car = Turtle("square")
            new_car.shapesize(stretch_wid=1, stretch_len=2)  # 자동차 크기 설정 (높이 20, 너비 40)
            new_car.penup()
            new_car.color(random.choice(COLORS))  # 랜덤 색상 선택
            new_car.goto(300, random.randint(-250, 250))  # 화면 오른쪽에서 랜덤 y좌표 생성
            self.all_cars.append(new_car)  # 생성된 자동차를 리스트에 추가

    def move_cars(self):
        """모든 자동차를 왼쪽으로 이동"""
        for car in self.all_cars:
            car.backward(self.car_speed)  # 자동차를 왼쪽으로 이동

    def increase_speed(self):
        """자동차 속도를 증가 (레벨 업 시 호출)"""
        self.car_speed += MOVE_INCREMENT