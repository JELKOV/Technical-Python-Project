#FileNotFound
#with open("a_file_txt") as file:
#   file.read()

#KeyError
# a_dictionary = {"key": "value"}
# value = a_dictionary["non_existent_key"]

#IndexError
# fruit_list = ["apple", "banana", "orange"]
# fruit = fruit_list[3]

#TypeError
# text = "abc"
# print(text + 5)


## 아래와 같이 예외처리를 할 경우 모든 코드가 실행이된다.
try:
    # 1. 'a_a_file.txt' 파일을 읽기 모드('r')로 열려고 시도합니다.
    #    파일이 없을 경우 FileNotFoundError 예외가 발생합니다.
    file = open("a_file.txt", "r")

    # 2. 딕셔너리에서 "ke"라는 키를 사용해 값을 가져오려고 시도합니다.
    #    해당 키가 없을 경우 KeyError 예외가 발생합니다.
    a_dictionary = {"key": "value"}
    print(a_dictionary["key"])  # KeyError 발생 가능

except FileNotFoundError:
    # 3. 파일이 없을 경우 이 블록이 실행됩니다.
    #    - 새로운 파일 'a_file.txt'를 생성하고 내용을 씁니다.
    #    - 메시지를 출력합니다.
    file = open("a_file.txt", "w")
    file.write("something")
    print("File not found. A new file has been created.")

except KeyError as error_message:
    # 4. 딕셔너리에 존재하지 않는 키를 참조했을 경우 이 블록이 실행됩니다.
    #    - 발생한 KeyError의 메시지를 출력합니다.
    print(f"The key '{error_message}' is not in the dictionary")

else:
    # 5. try 블록에서 예외가 발생하지 않았을 경우 실행됩니다.
    #    - 파일 내용을 읽고 출력합니다.
    content = file.read()
    print(content)

finally:
    # 6. try, except, else 블록에서 어떤 일이 발생하든 항상 실행됩니다.
    #    - 예외가 발생해도 이 블록은 반드시 실행됩니다.
    #    - 자원을 정리하거나 추가 작업을 수행하는 데 사용됩니다.
    print("This is the finally block.")
    # 나만의 에러처리
    # raise TypeError("This is an error that i made up")


# 나만의 에러 처리 예시
# BMI 구하기

height = float(input("Enter your height in m: "))
weight = float(input("Enter your weight in kg: "))

# 터무늬 없이 클경우
if height > 300:
    raise ValueError("Height is too high")

bmi = weight / height ** 2
print(bmi)