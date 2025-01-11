from tkinter import *
from quiz_brain import QuizBrain
THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        self.window = Tk()
        self.window.title("Quizler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_label = Label(text="Score: 0", bg=THEME_COLOR, fg="white")
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(width=300, height=250, highlightthickness=0, bg="white")
        self.question_text = self.canvas.create_text(
            150,
            125,
            width= 280,
            text="Some Question Text",
            fill=THEME_COLOR,
            font=("Arial",20,"italic"))
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)
        # 이미지 파일 로드
        true_image = PhotoImage(file="images/true.png")
        self.true_button = Button(image=true_image,
                                  highlightthickness=0,
                                  bg="white",
                                  fg="black",
                                  command=lambda: self.get_check_answer(answer="True"))
        self.true_button.grid(row=2, column=0)

        false_image = PhotoImage(file="images/false.png")
        self.false_button = Button(image=false_image,
                                   highlightthickness=0,
                                   bg="white",
                                   command=lambda: self.get_check_answer(answer="False"))
        self.false_button.grid(row=2, column=1)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="게임이 종료되었습니다.")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")


    def get_check_answer(self, answer):
        self.give_feedback(self.quiz.check_answer(answer))

    def give_feedback(self, is_answer):
        if is_answer:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, self.reset_canvas)

    def reset_canvas(self):
        self.canvas.config(bg="white")
        self.get_next_question()

