from turtle import Turtle
import random
"""
전체 코드 실행 순서 요약
food = Food()가 호출되면:

Food 클래스의 생성자(__init__) 실행.
터틀 객체 초기화 및 음식의 초기 설정 완료.
refresh()를 호출하여 랜덤 위치로 이동.
초기 화면이 갱신되면서 음식이 설정된 위치에 표시됩니다.

이후, 뱀이 음식을 먹을 때마다 food.refresh()가 호출되어 음식이 새 위치로 이동.

"""
class Food(Turtle):
    def __init__(self):
        super().__init__()  # 부모 클래스(Turtle)의 초기화 메서드 호출
        self.shape("circle")  # 모양을 원으로 설정
        self.penup()  # 이동 시 선을 그리지 않도록 설정
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)  # 크기 축소
        self.color("gold")  # 색상을 골드로 설정
        self.speed("fastest")  # 이동 속도를 가장 빠르게 설정
        self.refresh()  # 랜덤 위치 설정

    def refresh(self):
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)