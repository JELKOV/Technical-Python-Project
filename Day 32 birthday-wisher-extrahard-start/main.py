##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.
import smtplib, random
import datetime as dt
import csv

# 이메일 전송 함수
def sending_birthday(letters, email_temp):
    my_email = "myemail@gmail.com"
    password = "password"

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=email_temp,
            msg=f"Subject:Happy Birthday\n\n{letters}"  # 제목과 본문 사이 줄바꿈
        )
        print(f"이메일 전송 완료: {email_temp}")

def pick_random_letter():
    #파일 리스트 생성
    letters = ["letter_1.txt", "letter_2.txt", "letter_3.txt"]

    #random으로 편지선택
    random_letter = random.choice(letters)

    return f"letter_templates/{random_letter}"

def read_replace_letter(files_path, name_check):
    with open(files_path, "r", encoding="utf-8") as file_letter:
        letter_content = file_letter.read()
        return letter_content.replace("[NAME]", name_check)


#오늘 날짜 가져오기
today = dt.datetime.now()
current_month = today.month
current_day = today.day

print(f"오늘 날짜: {today} (월: {current_month}, 일: {current_day})")

#CSV 생일 목록 파일에서 가져오기
file_path = "birthdays.csv"

with open(file_path, "r", encoding="utf-8") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        # CSV에서 생일 데이터 추출
        name = row["name"]
        print(name)
        email = row["email"]
        print(email)
        birth_month = int(row["month"])
        print(birth_month)
        birth_day = int(row["day"])
        print(birth_day)

        print(f"확인 중: {name} ({birth_month}/{birth_day})")

        # 생일이 오늘인지 확인
        if name and email and birth_month and birth_day:
            if birth_month == current_month and birth_day == current_day:
                print(f"🎉 오늘은 {name}님의 생일입니다! ({email})")
                letter_temp = pick_random_letter()
                letter_set = read_replace_letter(letter_temp, name)
                sending_birthday(letter_set, email)
            else:
                print("오늘 생일인 사람이 없습니다")
        else:
            print("CSV파일에 문제가 있습니다.")


