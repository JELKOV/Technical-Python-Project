import turtle
import pandas as pd
import time

# 스크린 생성
screen = turtle.Screen()
screen.title("U.S. States Game")

# 지도 이미지 설정
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

# 데이터 읽기
data = pd.read_csv("50_states.csv")
all_states = data["state"].to_list()  # 모든 주 리스트
guessed_states = []  # 맞춘 주 리스트

# 난이도 설정
difficulty = screen.textinput(
    title="Select Difficulty",
    prompt="Choose difficulty: Easy, Medium, or Hard"
).lower()

# 난이도별 설정
time_limit = None
hint_enabled = False
max_hints = 3  # 최대 힌트 개수
hints_used = 0  # 사용된 힌트 개수
hint_level = 0  # 힌트 세부 정보 수준

if difficulty == "easy":
    hint_enabled = True  # Easy 모드: 힌트 항상 사용 가능
    max_hints = 10  # 힌트 제한 없음
elif difficulty == "medium":
    hint_enabled = True  # Medium 모드: 힌트 요청 시만 사용 가능
    max_hints = 5  # 최대 5회 힌트 가능
    time_limit = 300  # 시간 제한 5분
elif difficulty == "hard":
    hint_enabled = False  # Hard 모드: 힌트 사용 불가
    time_limit = 180  # 시간 제한 3분

# 타이머 시작
start_time = time.time()

# 힌트 제공 함수
def provide_hint(state):
    """
    점진적으로 힌트를 제공하는 함수.
    힌트 레벨에 따라 더 자세한 정보를 제공.
    """
    global hint_level
    if hint_level == 0:
        return f"The first letter of the state is: {state[0]}"
    elif hint_level == 1:
        return f"The first two letters of the state are: {state[:2]}"
    elif hint_level == 2:
        return f"The state has {len(state)} letters."
    elif hint_level == 3:
        x, y = int(data[data.state == state].x), int(data[data.state == state].y)
        region = "West" if x < 0 else "East"
        return f"This state is in the {region} region."
    else:
        return "No more hints available!"

# 게임 루프
while len(guessed_states) < len(all_states):
    # 남은 시간 계산
    if time_limit:
        elapsed_time = time.time() - start_time
        remaining_time = time_limit - elapsed_time
        if remaining_time <= 0:
            break  # 시간 초과로 게임 종료
        title = f"{len(guessed_states)}/{len(all_states)} States Correct - Time Left: {int(remaining_time)}s"
    else:
        title = f"{len(guessed_states)}/{len(all_states)} States Correct"

    # 정답 입력받기
    answer_state = screen.textinput(
        title=title,
        prompt=f"What's another state's name? (Type 'Hint' for help | Used: {hints_used}/{max_hints})"
    )

    # 종료 조건
    if answer_state is None or answer_state.lower() == "exit":
        break

    # 힌트 요청 처리
    if hint_enabled and answer_state.lower() == "hint":
        if hints_used < max_hints:
            for state in all_states:
                if state not in guessed_states:
                    hint = provide_hint(state)  # 힌트 생성
                    screen.textinput(title="Hint", prompt=hint)
                    hints_used += 1  # 사용된 힌트 개수 증가
                    hint_level = (hint_level + 1) % 4  # 힌트 레벨 순환
                    break
        else:
            screen.textinput(title="Hint Limit", prompt="You have used all available hints.")
        continue

    # 입력값 처리
    answer_state = answer_state.title()

    # 정답 체크
    if answer_state in all_states and answer_state not in guessed_states:
        guessed_states.append(answer_state)  # 정답 저장
        state_data = data[data.state == answer_state]  # 정답 주의 데이터 가져오기

        # 지도에 정답 표시
        t = turtle.Turtle()
        t.hideturtle()  # 터틀 모양 숨김
        t.penup()  # 선 그리지 않도록 펜 올리기
        t.goto(int(state_data.x), int(state_data.y))  # 주의 좌표로 이동
        t.write(answer_state)  # 주 이름 지도에 표시
    elif answer_state in guessed_states:
        # 중복된 답을 입력한 경우 경고 메시지 표시
        screen.textinput(
            title="Duplicate Answer",
            prompt=f"You already guessed '{answer_state}'. Try a different state."
        )
    else:
        # 잘못된 답을 입력한 경우 경고 메시지 표시
        screen.textinput(
            title="Incorrect Answer",
            prompt=f"'{answer_state}' is not a valid state name. Try again!"
        )

# 게임 종료: 맞추지 못한 주 저장
missing_states = [state for state in all_states if state not in guessed_states]
pd.DataFrame(missing_states).to_csv("states_to_learn.csv", index=False, header=["state"])

# 통계 요약 출력
print(f"게임 종료! 맞춘 주 수: {len(guessed_states)}/{len(all_states)}")
print(f"맞추지 못한 주 리스트가 'states_to_learn.csv'에 저장되었습니다.")
print(f"맞추지 못한 주: {missing_states}")

# GUI 종료 대기
screen.mainloop()

# # 함수 정의: 마우스 클릭 시 좌표를 출력
# def get_mouse_click_coordinates(x, y):
#     """
#     사용자가 GUI 창에서 클릭한 위치의 좌표를 출력.
#     x: 클릭한 x 좌표
#     y: 클릭한 y 좌표
#     """
#     print(x, y)  # 클릭한 x, y 좌표를 출력
#
# # turtle 객체에 마우스 클릭 이벤트 연결
# # 사용자가 GUI 창을 클릭하면 get_mouse_click_coordinates 함수가 호출됨
# turtle.onscreenclick(get_mouse_click_coordinates)
#
# # 이벤트 대기를 위해 turtle 메인 루프 실행 (화면이 계속 열려있게 만들어줌)
# turtle.mainloop()

# # GUI 종료 대기 (이 코드가 실행되지 않음 - mainloop()가 이미 루프를 대기)
# screen.exitonclick()
