from turtle import Turtle


class Ball(Turtle):
    """Ball 클래스는 공의 형태를 정하고, 볼을 움직임을 제어합니다."""

    def __init__(self, position):
        """
        Ball 초기화 메서드
        """
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.penup()
        self.goto(position)
        self.x_move = 1  # X축 이동 거리
        self.y_move = 1  # Y축 이동 거리
        self.move_speed = 0.1  # 공의 초기 이동 속도
        self.speed_limit = 0.4  # 공의 최대 속도 제한

    def move(self):
        """공을 이동시키는 메서드"""
        new_x = self.xcor() + self.x_move * self.move_speed
        new_y = self.ycor() + self.y_move * self.move_speed

        # 상단 및 하단 경계에 닿으면 Y축 방향 반전
        if new_y >= 290 or new_y <= -290:  # 화면 높이 600px 기준
            self.bounce_y()

        # 새로운 위치로 이동
        self.goto(new_x, new_y)

    def bounce_y(self):
        """Y축에서 튕겨나갈 때 방향을 반전"""
        self.y_move *= -1

    def bounce_x(self):
        """X축에서 튕겨나갈 때 방향을 반전"""
        self.x_move *= -1
        print(self.move_speed)
        # 속도 증가, 최대치 제한
        if self.move_speed < self.speed_limit:
            self.move_speed *= 1.1

    def reset_position(self):
        """공이 중앙으로 리셋되며 방향 반전"""
        self.goto(0, 0)  # 중앙으로 이동
        self.x_move *= -1  # X축 방향 반전
        self.move_speed = 0.1  # 초기 이동 속도로 설정
