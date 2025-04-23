# Technical Python Project (Day 15~81)

## 개요
이 저장소는 **Python 부트캠프 : 100개의 프로젝트로 Python 개발 완전 정복** 강의를 듣고 정리한 내용입니다. Day 15부터 Day 72까지의 수업 내용을 포함하며, 프로젝트별 학습 내용을 정리한 파일이 업로드되어 있습니다.

---

## 강의 정보
- **강의명**: Python 부트캠프 : 100개의 프로젝트로 Python 개발 완전 정복
- **강사**: Dr. Angela Yu
- **플랫폼**: Udemy
- **총 학습 시간**: 63시간 이상
- **수료일**: 2025년 2월 6일
- **작성자**: JELKOV

---

## 프로젝트별 학습 내용

### Day 15 ~ 81 주요 프로젝트 및 개념
1. **Day 15**: 커피 머신 프로젝트
2. **Day 16**: OOP 커피 머신 (객체 지향 프로그래밍)
3. **Day 17**: 퀴즈 프로젝트 (OOP 활용)
4. **Day 18**: 터틀 그래픽 및 GUI 인터페이스
5. **Day 19**: 인스턴스, 상태 및 고차함수
6. **Day 20~21**: 뱀 게임 프로젝트
7. **Day 22**: 벽돌깨기 게임
8. **Day 23**: 터틀 크로싱 게임
9. **Day 24**: 파일, 디렉토리 및 경로 관리
10. **Day 25**: CSV 데이터와 Pandas 라이브러리 활용
11. **Day 26**: 리스트 컴프리헨션 및 NATO 알파벳 프로젝트
12. **Day 27**: Tkinter, args, kwargs 및 GUI 프로그래밍
13. **Day 28**: Pomodoro 타이머 GUI 애플리케이션
14. **Day 29**: 패스워드 매니저 GUI 프로젝트
15. **Day 30**: 예외 처리, JSON 데이터 활용 및 패스워드 개선
16. **Day 31**: 플래시 카드 앱 프로젝트
17. **Day 32**: 이메일 전송 및 datetime 활용 프로젝트
18. **Day 33**: API 엔드포인트 및 ISS 머리 위 알리미
19. **Day 34**: API를 활용한 GUI 퀴즈 앱 만들기
20. **Day 35**: API 키 인증 및 SMS 보내기 프로젝트
21. **Day 36**: 주식시장 뉴스 알리미 프로젝트
22. **Day 37**: 습관 추적기 프로젝트 및 API Post Requests 활용
23. **Day 38**: 구글 시트를 이용한 운동 기록 프로젝트
24. **Day 39**: 항공권 특가 검색기
25. **Day 40**: 항공클럽 프로젝트
26. **Day 45**: BeautifulSoup을 활용한 웹 스크래핑
27. **Day 46**: Spotify 플레이리스트 자동 생성
28. **Day 47**: 아마존 상품 가격 자동 추적기
29. **Day 48**: Selenium 웹드라이버를 활용한 웹 자동화
30. **Day 49**: LinkedIn 채용 공고 자동 지원
31. **Day 50**: Tinder 자동 스와이핑 봇
32. **Day 51**: 인터넷 속도 불만 트위터 봇
33. **Day 52**: 인스타그램 팔로워 봇
34. **Day 53**: 웹 스크래핑을 이용한 데이터 입력 자동화
35. **Day 54**: Flask를 활용한 웹 개발 개요
36. **Day 55**: Flask의 HTML 및 URL 파싱, 숫자 업다운 게임
37. **Day 56**: HTML/Static 파일 렌더링 및 웹사이트 템플릿 사용법
38. **Day 57**: Flask에서 Jinja를 활용한 템플레이팅
39. **Day 59**: 블로그 프로젝트 2부 - 스타일 추가
40. **Day 60**: Flask에서 HTML 입력 양식 및 POST 요청 처리
41. **Day 61**: Flask-WTF를 활용한 고급 입력 양식 만들기
42. **Day 62**: Flask, WTForms, 부트스트랩 및 CSV 활용 프로젝트
43. **Day 63**: SQLAlchemy를 활용한 데이터베이스 구축
44. **Day 64**: 영화 웹사이트 프로젝트
45. **Day 66**: RESTful API 라우팅 구현
46. **Day 67**: 블로그 RESTful API 구축
47. **Day 68**: Flask 인증 및 사용자 로그인 구현
48. **Day 69**: 블로그 프로젝트 4부 - 사용자 관리
49. **Day 74**: Lego Dataset Analysis
50. **Day 75**: Google Trends Data Analysis
51. **Day 76**: Plotly for Data Visualization
52. **Day 77**: NumPy & Multi-Dimensional Arrays
53. **Day 78**: Regression Analysis with Seaborn
54. **Day 79**: Nobel Prize Analysis with Matplotlib
55. **Day 80**: Statistical Hypothesis Testing
56. **Day 81**: Capstone Project: House Price Prediction

---

### Day 15 ~ 81 주요 프로젝트 및 개념 

1. **Day 15: 커피 머신 프로젝트**
   - 커피 머신을 시뮬레이션하는 프로그램을 작성.
   - 사용자 입력을 받아 음료 선택 및 재료 확인.
   - 동전 투입 시스템 구현 후 가격 비교 기능 추가.

2. **Day 16: OOP 커피 머신 (객체 지향 프로그래밍)**
   - 커피 머신 프로젝트를 OOP 방식으로 리팩토링.
   - `CoffeeMachine`, `Menu`, `MoneyMachine` 클래스를 생성.
   - 클래스 간의 협업을 통해 코드 재사용성 증가.

3. **Day 17: 퀴즈 프로젝트 (OOP 활용)**
   - API를 이용해 퀴즈 데이터를 가져와 사용자에게 질문 제공.
   - 정답 여부 판별 및 점수 계산 기능 추가.
   - `Question`, `QuizBrain` 클래스 활용하여 OOP 설계 적용.

4. **Day 18: 터틀 그래픽 및 GUI 인터페이스**
   - Python `turtle` 모듈을 사용해 그래픽 디자인 실습.
   - 마우스 클릭 및 키보드 이벤트를 활용한 간단한 GUI 제작.

5. **Day 19: 인스턴스, 상태 및 고차함수**
   - `turtle`을 활용한 경주 게임 구현.
   - 상태 관리와 고차함수를 사용하여 레이스 진행.

6. **Day 20~21: 뱀 게임 프로젝트**
   - `turtle`과 `time` 모듈을 활용하여 뱀 게임 구현.
   - 점수를 증가시키고 게임 오버 상태를 관리하는 기능 추가.

7. **Day 22: 벽돌깨기 게임**
   - `turtle`로 벽돌깨기 게임 구현.
   - 공이 튕기는 물리 연산 및 충돌 감지 기능 추가.

8. **Day 23: 터틀 크로싱 게임**
   - 개구리 건너기와 유사한 게임 제작.
   - 플레이어 이동을 조작하고 장애물 회피 기능 추가.

9. **Day 24: 파일, 디렉토리 및 경로 관리**
   - `os` 및 `shutil` 모듈을 활용하여 파일 관리 기능 학습.

10. **Day 25: CSV 데이터와 Pandas 라이브러리 활용**
    - Pandas를 이용해 CSV 파일 읽기, 정리 및 분석 실습.

11. **Day 26: 리스트 컴프리헨션 및 NATO 알파벳 프로젝트**
    - NATO 음성 알파벳 변환기 개발.
    - 리스트 컴프리헨션을 활용한 데이터 변환 적용.

12. **Day 27: Tkinter, *args, **kwargs 및 GUI 프로그래밍**
    - Tkinter를 활용하여 GUI 프로그램 개발.
    - *args, **kwargs를 활용한 함수 유연성 개선.

13. **Day 28: Pomodoro 타이머 GUI 애플리케이션**
    - 생산성 향상을 위한 Pomodoro 타이머 제작.

14. **Day 29: 패스워드 매니저 GUI 프로젝트**
    - 비밀번호 저장 및 관리 프로그램 제작.

15. **Day 30: 예외 처리, JSON 데이터 활용 및 패스워드 개선**
    - JSON 파일을 사용하여 비밀번호 저장 기능 강화.

16. **Day 31: 플래시 카드 앱 프로젝트**
    - 단어 학습을 위한 플래시 카드 프로그램 제작.

17. **Day 32: 이메일 전송 및 datetime 활용 프로젝트**
    - `smtplib`과 `datetime`을 이용한 자동 이메일 전송 기능 개발.

18. **Day 33: API 엔드포인트 및 ISS 머리 위 알리미**
    - API 호출 및 데이터 활용.
    - ISS(국제우주정거장) 위치를 실시간으로 추적하여 사용자에게 알림 제공.

19. **Day 34: API를 활용한 GUI 퀴즈 앱 만들기**
    - Open Trivia DB API를 활용하여 퀴즈 게임 제작.

20. **Day 35: API 키 인증 및 SMS 보내기 프로젝트**
    - Twilio API를 이용한 SMS 발송 기능 구현.

21. **Day 36: 주식시장 뉴스 알리미 프로젝트**
    - 뉴스 API 및 주가 변동 감지를 통한 알림 기능 추가.

22. **Day 37: 습관 추적기 프로젝트 및 API Post Requests 활용**
    - 사용자 습관 데이터를 기록하고 API를 활용하여 자동 입력.

23. **Day 38: 구글 시트를 이용한 운동 기록 프로젝트**
    - Sheety API를 활용해 구글 스프레드시트에 데이터를 저장.

24. **Day 39: 항공권 특가 검색기**
    - Amadeus API를 사용하여 저렴한 항공권을 자동 검색.

25. **Day 40: 항공클럽 프로젝트**
    - 사용자 맞춤형 항공권 정보를 이메일로 제공하는 프로그램 제작.

26. **Day 45: BeautifulSoup을 활용한 웹 스크래핑**
    - 웹페이지에서 원하는 데이터를 추출하는 방법 학습.

27. **Day 46: Spotify 플레이리스트 자동 생성**
    - 사용자의 음악 취향을 분석하여 자동 플레이리스트 생성.

28. **Day 47: 아마존 상품 가격 자동 추적기**
    - 특정 제품의 가격 변동을 감지하고 알림을 제공하는 프로그램 제작.

29. **Day 48: Selenium 웹드라이버를 활용한 웹 자동화**
    - 자동화된 웹사이트 탐색 및 데이터 입력 기능 개발.

30. **Day 49: LinkedIn 채용 공고 자동 지원**
    - Selenium을 활용하여 자동으로 채용 공고에 지원하는 기능 구현.

31. **Day 50: Tinder 자동 스와이핑 봇**
    - Tinder에서 자동으로 스와이프하는 봇 제작.

32. **Day 51: 인터넷 속도 불만 트위터 봇**
    - 인터넷 속도를 측정하고 트위터에 자동으로 불만을 게시하는 프로그램.

33. **Day 52: 인스타그램 팔로워 봇**
    - 특정 계정의 팔로워를 자동으로 늘려주는 봇 제작.

34. **Day 53: 웹 스크래핑을 이용한 데이터 입력 자동화**
    - Selenium과 BeautifulSoup을 활용한 자동화 프로그램.

35. **Day 54: Flask를 활용한 웹 개발 개요**
    - Flask를 사용한 기본적인 웹 애플리케이션 구축.

36. **Day 55: Flask의 HTML 및 URL 파싱, 숫자 업다운 게임**
    - Flask를 활용하여 동적인 HTML 페이지 렌더링.

37. **Day 56: HTML/Static 파일 렌더링 및 웹사이트 템플릿 사용법**
    - Flask에서 정적 및 동적 웹사이트 개발.

38. **Day 57: Flask에서 Jinja를 활용한 템플레이팅**
    - 웹사이트에서 템플릿 엔진을 활용하는 방법 학습.

39. **Day 59: 블로그 프로젝트 2부 - 스타일 추가**
    - Flask 블로그 프로젝트의 UI 개선.

40. **Day 60: Flask에서 HTML 입력 양식 및 POST 요청 처리**
    - Flask에서 사용자 입력을 처리하는 폼 제작.

41. **Day 61: Flask-WTF를 활용한 고급 입력 양식 만들기**
    - 입력 데이터 유효성 검사 및 폼 유동성 개선.

42. **Day 62: Flask, WTForms, 부트스트랩 및 CSV 활용 프로젝트**
    - 부트스트랩을 활용하여 스타일링된 웹 애플리케이션 제작.

43. **Day 63: SQLAlchemy를 활용한 데이터베이스 구축**
    - ORM을 이용하여 데이터베이스를 효과적으로 관리.

44. **Day 64: 영화 웹사이트 프로젝트**
    - CRUD 기능이 포함된 영화 추천 웹사이트 구축.

45. **Day 66: RESTful API 라우팅 구현**
    - REST API의 기초 및 CRUD 기능을 구현하는 방법 학습.

46. **Day 67: 블로그 RESTful API 구축**
    - RESTful API를 활용한 블로그 게시판 구현.

47. **Day 68: Flask 인증 및 사용자 로그인 구현**
    - 사용자 로그인, 회원가입, 암호화 및 인증 기능 추가.

48. **Day 69: 블로그 프로젝트 4부 - 사용자 관리**
    - 블로그 프로젝트에 사용자 인증 및 관리 기능 추가.

49. **Day 74: Lego Dataset Analysis**
    - Pandas를 이용한 레고 데이터 분석.

50. **Day 81: Capstone Project: House Price Prediction**
    - 머신러닝을 활용하여 주택 가격 예측 모델 개발.

---

## 🚀 사용 기술
- Python
- Pandas, NumPy, Matplotlib, Seaborn
- Flask, Jinja, REST API
- SQLAlchemy, SQLite
- Tkinter (GUI 개발)
- Selenium, BeautifulSoup (웹 스크래핑)
- API 활용 (Google Sheets API, Twilio, Spotify API 등)
- Git & GitHub

---

## 🏆 주요 학습 내용
- ✅ Python 기본 문법 및 객체 지향 프로그래밍(OOP)
- ✅ GUI 프로그래밍 (Tkinter)
- ✅ 데이터 분석 및 시각화 (Pandas, Matplotlib, Seaborn, Plotly)
- ✅ Flask를 활용한 웹 개발
- ✅ REST API 설계 및 구현
- ✅ 웹 스크래핑 (BeautifulSoup, Selenium)
- ✅ 머신러닝 기초 개념 및 통계 분석
- ✅ Git을 활용한 버전 관리 및 배포

---

## 사용법
- 각 폴더(Day XX)에는 해당 날짜의 학습 코드와 설명이 포함되어 있습니다.
- `README.md` 파일을 참고하여 학습 내용을 확인하세요.

---

## 참고
이 저장소는 개인 학습 목적으로 정리된 내용이며, 강의의 모든 내용을 포함하지 않을 수 있습니다.









