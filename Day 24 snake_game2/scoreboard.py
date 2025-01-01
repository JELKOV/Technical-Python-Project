from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Arial", 16, "bold")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        with open("data.txt", mode="r") as read_obj:
            self.high_score = int(read_obj.read())
        self.penup()
        self.hideturtle()
        self.color("white")
        # 화면 상단 중앙에 점수 표시
        self.goto(0, 270)
        self.update_score()

    def update_score(self):
        """현재 점수를 화면에 업데이트"""
        self.clear()  # 기존 점수 지우기
        self.write(f"Score: {self.score} HighScore: {self.high_score}", align=ALIGNMENT, font=FONT)

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("data.txt", mode="w") as write_obj:
                write_obj.write(str(self.high_score))
        self.score = 0
        self.update_score()

    # def game_over(self):
    #     self.goto(0, 0)
    #     self.write("Game_Over", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        """점수를 증가시키고 화면에 업데이트"""
        self.score += 1
        self.update_score()
