student_dict = {
    "student": ["Angela", "James", "Lily"],
    "score": [56, 76, 98]
}

for key, value in student_dict.items():
    print(key, value)

import pandas as pd

student_data_frame = pd.DataFrame(student_dict)
print(student_data_frame)


for index, row in student_data_frame.iterrows():
    print(f"시작: {index}")
    if row.student == "Angela":
        print(f"{row.student}'s score is {row.score}")
    print(row.student)  # 학생 이름 출력
    print(row.score)    # 학생 점수 출력
    print(f"Index: {index}")
    print(f"Row Data:\n{row}")