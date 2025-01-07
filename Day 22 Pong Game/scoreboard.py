from turtle import Turtle

class Scoreboard(Turtle):
    """점수를 표시하는 Scoreboard 클래스"""
    def __init__(self):
        super().__init__()
        self.color("white")  # 점수 색상
        self.penup()
        self.hideturtle()  # 거북이 모양 숨기기
        self.left_score = 0  # 왼쪽 플레이어 점수
        self.right_score = 0  # 오른쪽 플레이어 점수
        self.update_scoreboard()  # 초기 점수 표시

    def update_scoreboard(self):
        """현재 점수를 화면에 업데이트"""
        self.clear()  # 이전 점수 지우기
        self.goto(-100, 250)  # 왼쪽 점수 위치
        self.write(self.left_score, align="center", font=("Courier", 36, "normal"))
        self.goto(100, 250)  # 오른쪽 점수 위치
        self.write(self.right_score, align="center", font=("Courier", 36, "normal"))

    def update_score(self, player):
        """
        점수를 업데이트.
        player: "left" 또는 "right"로 점수 증가할 플레이어 지정
        """
        if player == "left":
            self.left_score += 1
        elif player == "right":
            self.right_score += 1
        self.update_scoreboard()  # 점수 변경 후 화면 갱신