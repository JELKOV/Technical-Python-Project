from turtle import Turtle

FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.hideturtle()
        self.penup()
        self.goto(-200, 260)
        self.update_score()

    def update_score(self):
        """현재 레벨 표시"""
        self.clear()
        self.write(f"Level: {self.level}", align="center", font=("Arial", 16, "normal"))

    def increase_level(self):
        """레벨 증가"""
        self.level += 1
        self.update_score()

    def game_over(self):
        """게임 종료 메시지 표시"""
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=("Arial", 24, "normal"))