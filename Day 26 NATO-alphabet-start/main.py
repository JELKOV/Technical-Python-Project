student_dict = {
    "student": ["Angela", "James", "Lily"], 
    "score": [56, 76, 98]
}

# 딕셔너리 반복 처리:
for (key, value) in student_dict.items():
    # 키와 값을 접근
    pass

import pandas
student_data_frame = pandas.DataFrame(student_dict)

# 데이터프레임의 각 행 반복 처리
for (index, row) in student_data_frame.iterrows():
    # 인덱스와 행 접근
    # 행의 student나 score 열 접근
    pass

# iterrows()와 함께 키워드 메서드 사용
# {new_key:new_value for (index, row) in df.iterrows()}

# TODO 1. 다음 형식의 딕셔너리 생성:
# {"A": "Alfa", "B": "Bravo"}
nato_data = pandas.read_csv("nato_phonetic_alphabet.csv")
# print(nato_data.to_dict())

nato_dick = {row.letter:row.code for (index, row) in nato_data.iterrows()}
print(nato_dick)

# TODO 2. 사용자가 입력한 단어로부터 음성 코드 단어의 리스트 생성

user_input = input("Enter a word: ").upper()
phonetic_list = [nato_dick[letter] for letter in user_input if letter in nato_dick]
print(phonetic_list)