from tkinter import *
from tkinter import messagebox
import random
import string
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = string.ascii_letters  # 대문자 + 소문자
    digits = string.digits  # 숫자 0-9
    special_chars = string.punctuation  # 특수문자 (!, @, # 등)

    # 비밀번호 길이 설정
    password_length = 12
    num_letters = random.randint(6, 8)  # 알파벳 6~8개
    num_digits = random.randint(2, 4)   # 숫자 2~4개
    num_specials = password_length - num_letters - num_digits  # 나머지는 특수문자

    # 랜덤하게 비밀번호 구성 요소 선택
    password_letters = [random.choice(letters) for _ in range(num_letters)]
    password_digits = [random.choice(digits) for _ in range(num_digits)]
    password_specials = [random.choice(special_chars) for _ in range(num_specials)]

    # 구성 요소 합치고 섞기
    password_list = password_letters + password_digits + password_specials
    random.shuffle(password_list)
    # ex) ['E', '(', 'R', 'D', '1', 'L', 'u', '/', 'I', '6', '0', 'L']
    print(password_list)

    # 비밀번호 완성 join() 메서드는 Python의 문자열 메서드로, 문자열 리스트(또는 다른 반복 가능한 객체)를 하나의 문자열로 결합하는 데 사용됩니다.
    password = ''.join(password_list)
    # ex) E(RD1Lu/I60L
    print(password)

    # Entry에 생성된 비밀번호 표시
    password_entry.delete(0, END)  # 기존 내용 삭제
    password_entry.insert(0, password)  # 새로운 비밀번호 삽입
# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    website_string = website_entry.get()
    email_username_string = email_Username_entry.get()
    password_string = password_entry.get()

    if website_string == '' or email_username_string == '' or password_string == '':
        messagebox.showinfo(title='Error', message='Please fill all fields')
        return

    is_ok = messagebox.askokcancel(title=website_string, message=f"email:{email_username_string}, password:{password_string}")

    if is_ok:
        with open("data.txt", "a") as file:
            file.write(f"{website_string} | {email_username_string} | {password_string}\n")
            file.close()
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            messagebox.showinfo(title='Success', message='Password added')

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()

window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas 생성
canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

#Label 생성
website_label = Label(window, text="Website:")
website_label.grid(row=1, column=0)

email_Username_label = Label(window, text="Email/Username:")
email_Username_label.grid(row=2, column=0)

password_label = Label(window, text="Password:")
password_label.grid(row=3, column=0)

#Entry 생성
website_entry = Entry(width=36)
website_entry.grid(row=1, column=1, columnspan=2, sticky="W")

email_Username_entry = Entry(width=36)
email_Username_entry.grid(row=2, column=1, columnspan=2, sticky="W")
email_Username_entry.insert(0, "ajh4234@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="W")

#Button 생성
generated_password = Button(text="Generate Password", command=generate_password)
generated_password.grid(row=3, column=2, sticky="W")

add_button = Button(text="Add", width=36, command=add_password)
add_button.grid(row=4, column=1, columnspan=2, sticky="W")

window.mainloop()