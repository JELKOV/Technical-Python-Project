from tkinter import *

# 새 창 생성 및 설정
window = Tk()
window.title("Widget Examples")
window.minsize(width=500, height=500)

# 레이블 생성 및 설정
label = Label(text="This is old text")
label.config(text="This is new text")
label.pack()

# 버튼 클릭 시 동작 정의
def action():
    print("작업 수행")

# 버튼 생성 및 클릭 시 action 함수 호출
button = Button(text="Click Me", command=action)
button.pack()

# 입력창 생성
entry = Entry(width=30)
# 기본 텍스트 삽입
entry.insert(END, string="Some text to begin with.")
# 입력창의 텍스트 가져오기
print(entry.get())
entry.pack()

# 텍스트 박스 생성
text = Text(height=5, width=30)
# 텍스트 박스에 커서 위치시키기
text.focus()
# 기본 텍스트 삽입
text.insert(END, "Example of multi-line text entry.")
# 텍스트 박스 내용 가져오기 (1행 0열부터 끝까지)
print(text.get("1.0", END))
text.pack()

# 스핀박스 값 출력
def spinbox_used():
    # 스핀박스의 현재 값 가져오기
    print(spinbox.get())
spinbox = Spinbox(from_=0, to=10, width=5, command=spinbox_used)
spinbox.pack()

# 스케일 값 출력
def scale_used(value):
    print(value)  # 스케일의 현재 값 출력
scale = Scale(from_=0, to=100, command=scale_used)
scale.pack()

# 체크박스 상태 출력
def checkbutton_used():
    # 체크박스 상태 가져오기 (1: 체크됨, 0: 체크 안 됨)
    print(checked_state.get())
checked_state = IntVar()
checkbutton = Checkbutton(text="Is On?", variable=checked_state, command=checkbutton_used)
checked_state.get()
checkbutton.pack()

# 라디오버튼 상태 출력
def radio_used():
    print(radio_state.get())
radio_state = IntVar()
radiobutton1 = Radiobutton(text="Option1", value=1, variable=radio_state, command=radio_used)
radiobutton2 = Radiobutton(text="Option2", value=2, variable=radio_state, command=radio_used)
radiobutton1.pack()
radiobutton2.pack()

# 리스트박스 선택 내용 출력
def listbox_used(event):
    # 리스트박스에서 현재 선택된 항목 가져오기
    print(listbox.get(listbox.curselection()))

listbox = Listbox(height=4)
fruits = ["Apple", "Pear", "Orange", "Banana"]
for item in fruits:
    listbox.insert(fruits.index(item), item)
listbox.bind("<<ListboxSelect>>", listbox_used)
listbox.pack()
window.mainloop()
