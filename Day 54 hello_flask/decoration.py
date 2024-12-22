import time  # 시간 측정을 위한 time 모듈 가져오기

# 현재 시간을 초 단위로 출력 (1970년 1월 1일부터 경과한 초)
current_time = time.time()
print(current_time)  # 현재 시간을 초 단위로 출력

# 데코레이터 함수 정의
def speed_calc_decorator(function):
    def wrapper_function():
        start_time = time.time()  # 함수 실행 시작 시간 기록
        function()  # 원래 함수 실행
        end_time = time.time()  # 함수 실행 종료 시간 기록
        playing_time = end_time - start_time  # 실행 시간 계산
        print(f"{function.__name__} 실행시간: {playing_time}초")  # 함수 이름과 실행 시간 출력
    return wrapper_function  # 데코레이터로 사용하기 위해 래퍼 함수 반환

# 빠르게 실행되는 함수 정의
def fast_function():
    for i in range(1000000):  # 1,000,000번 반복
        i * i  # i를 자기 자신과 곱하기 (계산만 하고 결과는 사용하지 않음)

# 느리게 실행되는 함수 정의
def slow_function():
    for i in range(10000000):  # 10,000,000번 반복
        i * i  # i를 자기 자신과 곱하기 (계산만 하고 결과는 사용하지 않음)

# 데코레이터를 수동으로 적용
fast_function = speed_calc_decorator(fast_function)  # fast_function에 데코레이터 적용
slow_function = speed_calc_decorator(slow_function)  # slow_function에 데코레이터 적용

# 함수 실행 및 실행 시간 출력
fast_function()  # fast_function 실행 -> 실행 시간 출력
slow_function()  # slow_function 실행 -> 실행 시간 출력
