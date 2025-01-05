from tkinter import *
import math  # 수학적 계산 (소수점 버림 등)을 위한 math 모듈 사용

# ---------------------------- CONSTANTS ------------------------------- #
# 색상, 글꼴, 타이머 설정과 관련된 상수 값 정의
PINK = "#e2979c"  # 핑크색 (짧은 휴식용)
RED = "#e7305b"  # 빨간색 (긴 휴식용)
GREEN = "#9bdeac"  # 녹색 (작업용)
YELLOW = "#f7f5dd"  # 노란색 (배경색)
FONT_NAME = "Courier"  # 타이머에 사용할 글꼴 이름
WORK_MIN = 25  # 작업 시간 (분 단위)
SHORT_BREAK_MIN = 5  # 짧은 휴식 시간 (분 단위)
LONG_BREAK_MIN = 20  # 긴 휴식 시간 (분 단위)
reps = 0 # 횟수 추적
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
# 타이머를 초기 상태로 재설정하는 함수 (구현 필요)
def reset_timer():
    global timer
    print(f"DEBUG: Before reset, timer = {timer}")  # 디버깅 출력
    if timer is not None:
        window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN)
    check_marks.config(text="")
    global reps
    reps = 0
    timer = None  # 타이머 초기화
    print(f"DEBUG: After reset, timer = {timer}")  # 디버깅 출력

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    work_sec = WORK_MIN * 60
    break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    reps += 1

    if reps % 8 == 0:  # 8번째 주기마다 긴 휴식
        count_down(long_break_sec)
        title_label.config(text="Long Break", fg=RED)
    elif reps % 2 == 0:  # 짝수 주기에는 짧은 휴식
        count_down(break_sec)
        title_label.config(text="Short Break", fg=PINK)
    else:  # 홀수 주기에는 작업
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    """
    재귀적으로 호출하여 카운트다운을 진행.
    매 1초마다 시간을 줄이고 캔버스에 업데이트.
    """
    # 분(minute) 계산 (정수 나눗셈 사용)
    count_min = math.floor(count / 60)
    # 초(second) 계산 (나머지 연산 사용)
    # [동적타이핑] int 형
    count_sec = count % 60

    # 초가 한 자리일 경우 "05" 형식으로 표시되도록 문자열 포맷팅
    if count_sec < 10:
        #[동적타이핑] 문자열
        count_sec = f"0{count_sec}"

    # 캔버스에 텍스트 업데이트
    # [동적타이핑] 문자열
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    # 카운트다운이 0보다 크면 1초 후에 자신을 다시 호출
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else :
        start_timer()  # 다음 타이머 주기 시작
        marks = ""
        work_sessions = math.floor(reps / 2)  # 완료된 작업 세션 수 계산

        # 디버깅: reps와 work_sessions 값 출력
        print(f"DEBUG: reps = {reps}, work_sessions = {work_sessions}")

        for _ in range(work_sessions):
            marks += "✔"
            # 디버깅: 각 체크마크 추가 시 상태 출력
            print(f"DEBUG: marks = {marks}")

        # 체크마크 업데이트
        check_marks.config(text=marks)
        print(f"DEBUG: Updated check_marks text = {marks}")


# ---------------------------- UI SETUP ------------------------------- #
# Tk()는 tkinter 모듈의 기본 윈도우를 생성하는 함수입니다.
# 이것이 GUI 애플리케이션의 "메인 윈도우" 역할을 합니다.
window = Tk()

# 윈도우의 제목을 설정합니다. 창 상단에 표시됩니다.
window.title("Pomodoro")

# `config()` 메서드를 사용해 창의 설정을 변경합니다.
# `padx=100, pady=50`는 창 내부 요소들에 대해 좌우(padx)와 위아래(pady) 여백을 100과 50 픽셀씩 추가합니다.
# 여유 공간을 만들어 디자인적으로 더 보기 좋게 만듭니다.
window.config(padx=100, pady=50, bg=YELLOW)

# ---------------------------- Label 생성 ------------------------------- #
title_label = Label(window, text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
# Label의 위치를 grid로 설정. row=0, column=1은 창 중앙 상단에 배치.
title_label.grid(row=0, column=1)

# ---------------------------- Canvas 생성 ------------------------------- #
# Canvas 위젯은 그래픽 요소를 그리기 위한 공간을 제공합니다.
# `width=200`, `height=224`는 캔버스의 너비와 높이를 각각 200과 224 픽셀로 설정합니다.
# `highlightthickness=0`는 캔버스의 외곽선을 제거합니다.
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)

# ---------------------------- 이미지 추가 ------------------------------- #
# `PhotoImage()`를 사용하여 이미지 파일을 로드합니다.
# "tomato.png"는 타이머와 관련된 디자인 요소로 사용됩니다.
# 이미지는 프로그램과 동일한 디렉토리에 있어야 합니다.
image = PhotoImage(file="tomato.png")

# 캔버스에 이미지를 생성합니다.
# `create_image(x, y, image=image)` 메서드는 캔버스에 이미지를 그립니다.
# `(x, y)` 좌표는 캔버스 내에서 이미지를 배치할 기준점을 나타냅니다.
canvas.create_image(100, 112, image=image)

# ---------------------------- 텍스트 추가 ------------------------------- #
# 타이머 디스플레이를 위한 기본 텍스트 추가 ("00:00" 형식).
# 글꼴 크기와 색상 설정.
timer_text = canvas.create_text(100, 130, text="00:00", font=(FONT_NAME, 35, "bold"), fill="white")

# ---------------------------- Canvas 배치 ------------------------------- #
# 캔버스를 창 내에서 grid를 사용해 배치.
# row=1, column=1은 창의 중앙 영역에 배치.
canvas.grid(row=1, column=1)

# ---------------------------- Button 만들기 ------------------------------- #
# Start 버튼 생성 (녹색 텍스트)
# 버튼 클릭 시 `start_timer` 함수 호출.
start_button = Button(text="Start", fg=GREEN, bg=YELLOW, highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)

# Reset 버튼 생성 (빨간색 텍스트)
# 현재는 클릭 시 아무 동작도 하지 않음.
reset_button = Button(text="Reset", fg=RED, bg=YELLOW, highlightthickness=0, command=reset_timer)
reset_button.grid(row=2, column=2)

# ---------------------------- Check mark 만들기 ------------------------------- #
# 작업 완료를 나타내는 체크마크 라벨 생성.
# 현재는 고정된 텍스트 "✔"만 표시. 이후 동적으로 업데이트 가능.
check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(row=3, column=1)

# ---------------------------- 메인 루프 ------------------------------- #
# `mainloop()`는 Tkinter 프로그램의 이벤트 루프를 시작합니다.
# 프로그램이 종료될 때까지 사용자 이벤트(버튼 클릭, 창 닫기 등)를 대기하며 처리합니다.
window.mainloop()
