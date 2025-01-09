from turtle import Turtle, Screen

# 초기 설정 상수
STARTING_POSITION = (0, -280)  # 플레이어의 시작 위치 (화면 아래쪽 중앙)
MOVE_DISTANCE = 10  # 한 번 이동 시 거북이가 전진하는 거리
FINISH_LINE_Y = 280  # 화면 위쪽의 목표선 Y좌표

class Player(Turtle):
    def __init__(self):
        """플레이어(거북이) 객체 초기화"""
        super().__init__()  # 부모 클래스(Turtle)의 초기화 메서드 호출
        self.shape("turtle")  # 거북이 모양 설정
        self.penup()  # 선을 그리지 않도록 설정
        self.starting_position()  # 초기 위치로 이동
        self.setheading(90)  # 거북이 방향을 위쪽(90도)으로 설정

    def starting_position(self):
        """플레이어를 시작 위치로 이동"""
        self.goto(STARTING_POSITION)  # 지정된 시작 위치로 이동

    def move(self):
        """플레이어를 위로 이동"""
        self.forward(MOVE_DISTANCE)  # 지정된 거리만큼 위로 이동

    def has_crossed_finish_line(self):
        """
        플레이어가 화면 위쪽 목표선에 도달했는지 확인
        :return: 목표선(FINISH_LINE_Y)을 넘어섰으면 True, 아니면 False
        """
        return self.ycor() > FINISH_LINE_Y  # 현재 Y좌표가 목표선보다 큰지 확인
