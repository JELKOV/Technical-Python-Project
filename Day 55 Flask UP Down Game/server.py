"""
Flask에서 <int:variable>의 동작 원리
@app.route("/<int:guess>")의 역할:

/<int:guess>는 URL에서 특정 위치에 있는 값을 추출하는 데 사용됩니다.
<int:guess>는 경로에 입력된 값을 정수(int)로 변환한 뒤, 뷰 함수(여기서는 guess_number)에 전달합니다.
예를 들어, URL이 /5라면, guess_number 함수는 guess=5로 호출됩니다.
int 변환기:

int는 경로 변환기 중 하나입니다. Flask는 기본적으로 여러 변환기를 제공합니다:
int: 정수 값으로 변환합니다.
float: 실수 값으로 변환합니다.
path: 문자열을 포함한 경로를 추출합니다(슬래시 포함 가능).
string: 기본값으로, 슬래시를 제외한 문자열을 추출합니다.
uuid: UUID 값을 추출합니다.
동작 방식:

사용자가 URL을 통해 /3처럼 숫자를 입력하면:
Flask는 <int:guess>를 인식하고, 숫자 부분(3)을 정수로 변환합니다.
변환된 값은 함수의 guess 매개변수로 전달됩니다.
변환 실패 시(예: /abc 같은 경우):
Flask는 404 Not Found 오류를 반환합니다.
작동 예제:

URL: /3
guess = 3 (정수로 변환됨)
guess_number 함수 호출: guess_number(guess=3)
URL: /abc
정수 변환 실패 → 404 에러 발생.
"""
from flask import Flask
import random

# Flask 애플리케이션 생성
app = Flask(__name__)

# 무작위 숫자 생성
random_number = random.randint(0, 9)

# 홈 경로 설정
@app.route("/")
def home():
    return '''
    <h1>0과 9 사이의 숫자를 맞추세요!</h1>
    <img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" alt="Guess a number">
    '''

# 숫자 입력 경로
@app.route("/<int:guess>")
def guess_number(guess):
    if guess < random_number:
        return '''
        <h1 style="color: blue;">너무 작아요!</h1>
        <img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif" alt="Too low">
        '''
    elif guess > random_number:
        return '''
        <h1 style="color: red;">너무 커요!</h1>
        <img src="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif" alt="Too high">
        '''
    else:
        return '''
        <h1 style="color: green;">정답입니다!</h1>
        <img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif" alt="Correct!">
        '''

# Flask 애플리케이션 실행
if __name__ == "__main__":
    app.run(debug=True)
