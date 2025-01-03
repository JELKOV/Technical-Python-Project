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
