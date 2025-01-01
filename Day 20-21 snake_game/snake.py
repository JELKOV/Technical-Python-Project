from turtle import Turtle

STARTING_POSITION = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
RIGHT = 0
LEFT = 180
UP = 90
DOWN = 270

class Snake:
    def __init__(self):
        """뱀의 초기 설정"""
        # 뱀의 세그먼트 리스트
        self.segments = []
        # # 초기 위치들
        # self.starting_positions = [(0, 0), (-20, 0), (-40, 0)]
        # 뱀 생성
        self.create_snake()
        # 뱀의 머리 설정
        self.head = self.segments[0]

    def create_snake(self):
        """뱀의 세그먼트를 생성하고 초기 위치에 배치"""
        for position in STARTING_POSITION:
            self.add_segment(position)

    def add_segment(self, position):
        """새로운 세그먼트를 특정 위치에 추가"""
        new_segment = Turtle("square")
        new_segment.color("white")
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)

    def extend(self):
        """점수를 먹었을때 새로운 새그먼트를 맨뒤 위치에 추가"""
        self.add_segment(self.segments[-1].position())

    def move(self):
        """뱀을 앞으로 이동"""
        for seg_num in range(len(self.segments) - 1, 0, -1):
            # 앞 세그먼트의 위치를 현재 세그먼트로 복사
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        # 뱀의 머리를 앞으로 이동
        self.head.forward(MOVE_DISTANCE)

    def turn_left(self):
        """뱀의 머리를 왼쪽으로 회전"""
        # 현재 오른쪽으로 움직이는 경우 제외 반대쪽은 제외
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def turn_right(self):
        """뱀의 머리를 오른쪽으로 회전"""
        # 현재 왼쪽으로 움직이는 경우 제외 반대쪽은 제외
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

    def turn_up(self):
        """뱀의 머리를 위쪽으로 회전"""
        # 현재 아래로 움직이는 경우 제외 반대쪽은 제외
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def turn_down(self):
        """뱀의 머리를 아래쪽으로 회전"""
        # 현재 위로 움직이는 경우 제외 반대쪽은 제외
        if self.head.heading() != UP:
            self.head.setheading(DOWN)