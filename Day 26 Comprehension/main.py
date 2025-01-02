# 학생 이름 목록
names = ['Alex', 'Beth', 'Caroline', 'Dave', 'Eleanor', 'Freddie']

# 랜덤 숫자를 생성하기 위해 random 모듈 가져오기
import random

# 각 학생에게 1부터 100 사이의 점수를 랜덤으로 생성하여 student_scores 딕셔너리에 저장
# 딕셔너리 컴프리헨션 사용
student_scores = {student: random.randint(1, 100) for student in names}

# 학생별 점수 출력
print(student_scores)

# 점수가 60 이상인 학생들만 필터링하여 passed_students 딕셔너리에 저장
# student_scores.items()를 사용해 키(학생 이름)와 값(점수)을 반복
passed_students = {student: score for student, score in student_scores.items() if score >= 60}

# 전체 학생의 점수 출력
print("All students' scores:", student_scores)

# 60점 이상 통과한 학생들 출력
print("Passed students:", passed_students)