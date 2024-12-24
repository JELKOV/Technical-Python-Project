class QuizBrain:
    """
    QuizBrain 클래스는 퀴즈 게임의 핵심 로직을 처리합니다.
    - 질문 리스트를 관리합니다.
    - 현재 진행 중인 질문 번호를 추적합니다.
    - 사용자의 점수를 계산합니다.
    """

    def __init__(self, q_question_list):
        """
        QuizBrain 클래스의 초기화 메서드.

        Args:
        q_question_list (list): Question 객체 리스트. 퀴즈에 사용될 질문들을 저장.
        """
        self.question_list = q_question_list  # 질문 리스트 저장
        self.question_number = 0  # 현재 질문 번호 초기화
        self.score = 0  # 사용자 점수 초기화

    def next_question(self):
        """
        다음 질문을 출력하고 사용자 입력을 받아 정답 여부를 확인합니다.

        - 현재 질문 리스트에서 질문을 가져와 출력합니다.
        - 사용자 입력을 받아 `checking_answer` 메서드로 정답 여부를 확인합니다.
        """
        current_question = self.question_list[self.question_number]  # 현재 질문 가져오기
        self.question_number += 1  # 질문 번호 증가
        # 사용자에게 질문 출력
        user_answer = input(f"Q.{self.question_number}: {current_question.text} (True/False): ")
        # 사용자 답변과 정답 비교
        self.checking_answer(user_answer, current_question.answer)

    def still_remain_question(self):
        """
        남은 질문이 있는지 확인하는 메서드.

        Returns:
        bool: 남은 질문이 있으면 True, 없으면 False.
        """
        # 현재 질문 번호가 질문 리스트 길이보다 작으면 질문이 남아 있음
        return self.question_number < len(self.question_list)

    def checking_answer(self, user_answer, answer):
        """
        사용자의 답변을 정답과 비교하여 점수를 계산합니다.

        Args:
        user_answer (str): 사용자가 입력한 답변.
        answer (str): 질문의 실제 정답.

        - 사용자의 답변과 정답을 대소문자 무시하고 비교합니다.
        - 정답일 경우 점수를 증가시키고 "정답" 메시지를 출력합니다.
        - 오답일 경우 "잘못된 대답" 메시지를 출력하고 정답을 보여줍니다.
        """
        if user_answer.lower() == answer.lower():  # 대소문자 무시하고 비교
            self.score += 1  # 정답일 경우 점수 증가
            print("정답")
        else:
            print("잘못된 대답")
            print(f"정답: {answer}")  # 정답 출력
        # 현재 점수와 공백 출력
        print(f"현재 점수: {self.score}/{self.question_number}")
        print("\n")