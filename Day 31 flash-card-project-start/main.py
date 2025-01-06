from tkinter import *
import pandas as pd
import random
import os

# --------------------- 배경색 및 타이머 초기화 ------------------------------
BACKGROUND_COLOR = "#B1DDC6"  # 배경 색상
flip_timer = None  # 타이머를 저장하는 변수 초기화
current_word = {}  # 현재 단어를 저장하는 딕셔너리
word_list = []

# --------------------- CSV 파일 로드 및 데이터 변환 ------------------------------
# CSV 파일을 읽어 데이터프레임 생성
try:
    need_study = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/korean_words.csv")
    # 데이터프레임을 리스트 형태의 딕셔너리로 변환
    word_list = data.to_dict(orient="records")  # [{"Korean": "것", "English": "thing"}, ...]
    print("korean words loaded")
else:
    word_list = need_study.to_dict(orient="records")
    print("words_to_learn.csv loaded")


# --------------------- 랜덤 단어 함수 ------------------------------
def get_random_word(answer=None):
    """랜덤으로 단어를 선택하고 카드 앞면을 업데이트하는 함수"""
    global current_word, flip_timer, word_list
    if flip_timer:  # 이전 타이머가 있다면 취소
        window.after_cancel(flip_timer)
    current_word = random.choice(word_list)  # 랜덤으로 한 단어 선택
    korean_word = current_word["Korean"]  # 선택된 단어의 한국어
    # 캔버스에 한국어 단어와 제목 업데이트
    canvas.itemconfig(title_text_id, text="Korean", fill="black")
    canvas.itemconfig(word_text_id, text=korean_word, fill="black")
    canvas.itemconfig(card_image, image=front_image)  # 카드 앞면 표시
    flip_timer = window.after(3000, flip_card)  # 3초 후 카드 뒤집기
    if answer == "yes":
        word_list.remove(current_word)
        df = pd.DataFrame(word_list)
        df.to_csv("data/words_to_learn.csv", index=False)
        print(f"csv파일 생성되었습니다 남은 단어수: {len(word_list)}")


def flip_card():
    """현재 단어의 영어 의미를 카드 뒷면에 표시하는 함수"""
    english_word = current_word["English"]  # 선택된 단어의 영어
    # 캔버스에 영어 단어와 제목 업데이트
    canvas.itemconfig(title_text_id, text="English", fill="white")
    canvas.itemconfig(word_text_id, text=english_word, fill="white")
    canvas.itemconfig(card_image, image=back_image)  # 카드 뒷면 표시

# --------------------- 리셋 함수 ------------------------------
def reset_words():
    """words_to_learn.csv 파일을 삭제하고 word_list를 초기화"""
    global word_list
    if os.path.exists("data/words_to_learn.csv"):
        os.remove("data/words_to_learn.csv")
        print("words_to_learn.csv 삭제 완료")
    reset_data = pd.read_csv("data/korean_words.csv")
    word_list = reset_data.to_dict(orient="records")
    get_random_word()
    print("word_list 초기화 완료")

# --------------------- UI 설정 ------------------------------
# 메인 윈도우 설정
window = Tk()
window.title("Flashy")  # 윈도우 제목
window.config(background=BACKGROUND_COLOR, padx=50, pady=50)  # 배경 및 여백 설정

# 캔버스 생성 (이미지와 텍스트 표시용)
canvas = Canvas(width=800, height=526, highlightthickness=0)

# 이미지 파일 로드
front_image = PhotoImage(file="images/card_front.png")  # 카드 앞면
back_image = PhotoImage(file="images/card_back.png")  # 카드 뒷면
right_image = PhotoImage(file="images/right.png")  # 정답 버튼 이미지
wrong_image = PhotoImage(file="images/wrong.png")  # 오답 버튼 이미지

# 배경색 설정 및 이미지 추가
canvas.config(bg=BACKGROUND_COLOR)
card_image = canvas.create_image(400, 263, image=front_image)

# 캔버스에 텍스트 추가 (제목과 단어)
title_text_id = canvas.create_text(400, 150, text="title", font=("Ariel", 40, "italic"))
word_text_id = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# 버튼 생성 (정답/오답)
x_button = Button(image=wrong_image, highlightthickness=0, command=get_random_word)
x_button.grid(row=1, column=0)
o_button = Button(image=right_image, highlightthickness=0, command=lambda: get_random_word("yes"))
o_button.grid(row=1, column=1)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_words)
reset_button.grid(row=2, column=0, columnspan=2)

# --------------------- 초기 설정 ------------------------------
# 초기 단어 표시
get_random_word()

# --------------------- 메인 루프 ------------------------------
window.mainloop()
