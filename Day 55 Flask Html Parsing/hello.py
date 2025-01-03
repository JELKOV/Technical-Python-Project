# --- 주석에서 추가된 개념 ---
# 1. **데코레이터 사용 순서**: 데코레이터는 아래에서 위로 적용됩니다.
#    - @make_underlined -> @make_emphasis -> @make_bold 순으로 실행됩니다.
#    - 이는 Python이 데코레이터를 스택 구조처럼 처리하기 때문입니다.
# 2. **데코레이터 동작 원리**: 함수 `say_bye`의 반환값이 wrapper 함수의 반환값으로 대체됩니다.
#    - 예를 들어, "Say Good bye!" -> "<u><em><b>Say Good bye!</b></em></u>"로 변환됩니다.
# 3. **Flask 라우트**: Flask의 `@app.route()` 데코레이터는 URL 경로와 함수를 연결합니다.
#    - 이 코드는 "/bye" 경로에 접속하면 HTML 태그가 적용된 텍스트를 반환합니다.
# 4. **Flask 서버 실행**: `app.run()`은 개발 서버를 시작하며 기본적으로 `localhost:5000`에서 실행됩니다.

from flask import Flask

# 1. Flask 애플리케이션 생성
# Flask 클래스의 인스턴스를 생성하여 앱 초기화
app = Flask(__name__)

# 2. 현재 모듈의 이름 출력
# "__main__"을 출력하여 현재 실행 중인 파일이 직접 실행되었는지 확인
print(__name__)

# 3. 데코레이터 정의
# HTML 태그를 적용하는 데코레이터들 정의

# 텍스트를 <b> 태그로 감싸서 굵게 만드는 데코레이터
def make_bold(func):
    def wrapper(*args, **kwargs):
        # 원래 함수의 반환값을 <b> 태그로 감싼 후 반환
        return f'<b>{func(*args, **kwargs)}</b>'
    return wrapper

# 텍스트를 <em> 태그로 감싸서 이탤릭체로 만드는 데코레이터
def make_emphasis(func):
    def wrapper(*args, **kwargs):
        # 원래 함수의 반환값을 <em> 태그로 감싼 후 반환
        return f'<em>{func(*args, **kwargs)}</em>'
    return wrapper

# 텍스트를 <u> 태그로 감싸서 밑줄을 추가하는 데코레이터
def make_underlined(func):
    def wrapper(*args, **kwargs):
        # 원래 함수의 반환값을 <u> 태그로 감싼 후 반환
        return f'<u>{func(*args, **kwargs)}</u>'
    return wrapper

# 4. 루트 URL("/") 라우트 설정
# 사용자가 루트 경로로 접속했을 때 표시되는 내용
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# 5. "/bye" 경로에 대한 라우트 설정
# 이 함수는 여러 데코레이터를 통해 HTML 태그가 적용된 응답을 반환
@app.route("/bye")
@make_bold        # 응답을 굵게 표시
@make_emphasis    # 응답을 이탤릭체로 표시
@make_underlined  # 응답에 밑줄 추가
def say_bye():
    return "Say Good bye!"  # 원래 반환값

# 6. Flask 애플리케이션 실행
# 현재 파일이 직접 실행되었을 경우 Flask 개발 서버를 시작
if __name__ == "__main__":
    app.run()


