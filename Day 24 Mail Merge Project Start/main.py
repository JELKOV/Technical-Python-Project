# TODO: Create personalized letters for each name using starting_letter.txt template
# Replace the placeholder [name] with the actual names from invited_names.txt
# Save the personalized letters in the "ReadyToSend" folder

# 파일 경로 정의
TEMPLATE_FILE = "./Input/Letters/starting_letter.txt"  # 편지 템플릿 파일 경로
NAMES_FILE = "./Input/Names/invited_names.txt"  # 초대받을 이름 파일 경로
OUTPUT_DIRECTORY = "./Output/ReadyToSend/"  # 결과 파일 저장 디렉토리 경로

# 이름 리스트 읽기
with open(NAMES_FILE, "r") as file:
    name_list = file.readlines()  # 파일의 각 줄을 리스트로 읽기

# 템플릿 파일 읽기
with open(TEMPLATE_FILE, "r") as file:
    letter_template = file.read()  # 편지 템플릿 내용을 문자열로 읽기

# 개인화된 편지 생성 및 저장
for name in name_list:
    clean_name = name.strip()  # 이름에서 앞뒤 공백 제거
    personalized_letter = letter_template.replace("[name]", clean_name)  # [name]을 실제 이름으로 대체

    # 개인화된 편지 저장
    output_path = f"{OUTPUT_DIRECTORY}Dear_{clean_name}.txt"  # 저장할 파일 경로 생성
    with open(output_path, "w") as output_file:
        output_file.write(personalized_letter)  # 파일에 개인화된 편지 작성

# 완료 메시지 출력
print("모든 개인화된 편지가 성공적으로 생성되었습니다!")
