## ********Day 54 Start**********
### 함수는 입력값/기능/출력값을 가질 수 있다.
def add(n1, n2):
    return n1 + n2  # 두 숫자를 더한 결과를 반환

def subtract(n1, n2):
    return n1 - n2  # 두 숫자를 뺀 결과를 반환

def multiply(n1, n2):
    return n1 * n2  # 두 숫자를 곱한 결과를 반환

def divide(n1, n2):
    return n1 / n2  # 두 숫자를 나눈 결과를 반환

## 함수는 일급 객체로 취급되어 다른 함수의 인자로 전달될 수 있다.
## 예를 들어 int/string/float처럼 함수도 전달 가능

def calculate(calc_function, n1, n2):
    return calc_function(n1, n2)  # 전달된 함수(calc_function)를 실행

result = calculate(add, 2, 3)  # add 함수와 숫자 2, 3을 전달
print(result)  # 출력: 5 (2 + 3)

## 함수는 다른 함수 안에서 중첩될 수 있다.
def outer_function():
    print("I'm outer")  # 외부 함수의 출력

    def nested_function():
        print("I'm inner")  # 내부 함수의 출력

    nested_function()  # 내부 함수 호출

outer_function()  # outer_function 실행 -> "I'm outer", "I'm inner" 출력

## 함수는 다른 함수로부터 반환될 수 있다.
def outer_function():
    print("I'm outer")  # 외부 함수의 출력

    def nested_function():
        print("I'm inner")  # 내부 함수의 출력

    return nested_function  # 내부 함수를 반환

inner_function = outer_function()  # nested_function 반환
inner_function()  # nested_function 실행 -> "I'm inner" 출력

## Python 데코레이터 함수
import time  # 시간 지연을 위해 time 모듈 임포트

def delay_decorator(function):
    def wrapper_function():
        time.sleep(2)  # 2초 동안 대기
        # 원래 함수 실행 전 작업
        function()  # 원래 함수 실행 (첫 번째 호출)
        function()  # 원래 함수 실행 (두 번째 호출)
        # 원래 함수 실행 후 작업
    return wrapper_function  # 감싸는(wrapper) 함수를 반환

# 데코레이터를 사용하는 방법 (@ 문법 사용)
@delay_decorator
def say_hello():
    print("Hello")  # "Hello" 출력

# 데코레이터를 사용하는 또 다른 함수
@delay_decorator
def say_bye():
    print("Bye")  # "Bye" 출력

# 데코레이터를 직접 함수에 전달하여 사용하는 방법
def say_greeting():
    print("How are you?")  # "How are you?" 출력

decorated_function = delay_decorator(say_greeting)  # delay_decorator로 say_greeting 감싸기
decorated_function()  # 감싸진 함수 실행 -> 2초 대기 후 "How are you?" 두 번 출력