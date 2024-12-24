"""
main.py

이 파일은 퀴즈 게임의 메인 실행 파일입니다.
프로그램의 전체 흐름을 제어하며, 다음 작업을 수행합니다:
1. 질문 데이터를 가져와 Question 객체 리스트(question_bank)를 생성.
2. QuizBrain 클래스를 초기화하여 퀴즈 로직을 실행.
3. 모든 질문이 완료된 후 최종 점수를 출력.

Modules:
- question_model: Question 클래스 정의
- data: 질문 데이터를 포함하는 question_data 리스트
- quiz_brain: QuizBrain 클래스 정의

Usage:
python main.py

Author:
[Your Name]

Date:
[Today's Date]
"""

from question_model import Question  # Question 클래스 가져오기
from data import question_data  # 질문 데이터 가져오기
from quiz_brain import QuizBrain  # QuizBrain 클래스 가져오기

# Step 1: Question 객체 리스트 생성
"""
question_data (list of dict)를 반복하며 각 질문을 Question 객체로 변환.
변환된 Question 객체는 question_bank 리스트에 추가.
"""
question_bank = []
for question in question_data:
    question_text = question["question"]  # 질문 텍스트
    question_answer = question["correct_answer"]  # 질문 정답
    new_question = Question(q_text=question_text, q_answer=question_answer)  # Question 객체 생성
    question_bank.append(new_question)  # 리스트에 추가

# Step 2: QuizBrain 클래스 초기화
"""
QuizBrain 클래스에 question_bank 전달하여 퀴즈 로직 초기화.
"""
quiz = QuizBrain(question_bank)

# Step 3: 퀴즈 실행 루프
"""
QuizBrain의 still_remain_question() 메서드를 사용하여
남은 질문이 있을 때까지 next_question() 메서드를 반복 호출.
"""
while quiz.still_remain_question():
    quiz.next_question()

# Step 4: 최종 결과 출력
"""
모든 질문이 완료되면 최종 점수를 출력.
"""
print(f"You've completed the quiz! Your final score was: {quiz.score}/{len(question_bank)}")
