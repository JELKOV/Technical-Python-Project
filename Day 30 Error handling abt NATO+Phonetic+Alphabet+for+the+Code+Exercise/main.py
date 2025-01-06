# Keyword Method with iterrows()
# {new_key:new_value for (index, row) in df.iterrows()}

import pandas

data = pandas.read_csv("nato_phonetic_alphabet.csv")
#TODO 1. Create a dictionary in this format:
phonetic_dict = {row.letter: row.code for (index, row) in data.iterrows()}
print(f"Line9:{phonetic_dict}")


"""
--------------------Day 30 수정 부분--------------------
"""
#TODO 2. Create a list of the phonetic code words from a word that the user inputs.

# 최종 수정
def generate_phonetic():
    while True:
        word = input("Enter a word: ").upper()
        try:
            output_list = [phonetic_dict[letter] for letter in word]
        except KeyError:
            print("Sorry, only letters in the alphabet please.")
        else:
            print(output_list)
            break  # 유효한 입력이 들어오면 반복 종료

generate_phonetic()

# 내가 만든 코드
# while True:
#     word = input("Enter a word: ").upper()
#     try:
#         output_list = [phonetic_dict[letter] for letter in word]
#         print(output_list)
#         break
#     except KeyError:
#         print("Sorry, no such word found")


# 참고코드
# def generate_phonetic():
#     word = input("Enter a word: ").upper()
#     try:
#         output_list = [phonetic_dict[letter] for letter in word]
#     except KeyError:
#         print("Sorry, no such word found")
#         generate_phonetic()
#     else:
#         print(output_list)

# generate_phonetic()