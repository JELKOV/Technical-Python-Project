from turtle import Turtle

class Paddle(Turtle):
    """Paddle 클래스는 공의 움직임을 방어하기 위한 Paddle을 나타냅니다."""

    def __init__(self, position):
        """
        Paddle 초기화 메서드.

        Args:
            position (tuple): Paddle의 초기 위치 (x, y 좌표).
        """
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(position)

    def go_up(self):
        """Paddle을 위로 이동하되, 화면 경계를 벗어나지 않도록 제한."""
        if self.ycor() < 250:  # 화면 위쪽 경계(250) 내에서만 이동.
            self.goto(self.xcor(), self.ycor() + 0.2)

    def go_down(self):
        """Paddle을 아래로 이동하되, 화면 경계를 벗어나지 않도록 제한."""
        if self.ycor() > -250:  # 화면 아래쪽 경계(-250) 내에서만 이동.
            self.goto(self.xcor(), self.ycor() - 0.2)



# 내부 사용
# from turtle import Turtle
#
# class Paddle:
#     def __init__(self, position):
#         """Paddle 초기화 및 위치 설정"""
#         self.paddle = Turtle()
#         self.paddle.shape("square")
#         self.paddle.color("white")
#         self.paddle.shapesize(stretch_wid=5, stretch_len=1)
#         self.paddle.penup()
#         self.paddle.goto(position)
#
#     def go_up(self):
#         """Paddle을 위로 이동"""
#         y = self.paddle.ycor() + 20
#         self.paddle.goto(self.paddle.xcor(), y)
#
#     def go_down(self):
#         """Paddle을 아래로 이동"""
#         y = self.paddle.ycor() - 20
#         self.paddle.goto(self.paddle.xcor(), y)
