from tkinter import *

# tkinter 불러오기
root = Tk()
# root 이름 정하기
root.title("A's Tkinter")
# root 사이즈 정하기
root.minsize(400, 400)
root.geometry("1000x1000")
# padding 주기
root.config(padx=10, pady=10)

# 버튼 만들기
def button_clicked():
    input_string = input_word.get()
    my_label.config(text=f"{input_string}:your input", font=("Arial", 10, "bold"))

button = Button(text="Close Tkinter", command=root.destroy)
second_button = Button(text="Enter Input", command=button_clicked)
button.grid(column=3, row=0)


#Label
my_label = Label(text="Hello", font=("Arial", 20,))
my_label.config(padx=10, pady=10)
#layout(pack): 스크린에 컴포넌트를 배치하고 중앙으로 가게 만든다.
# my_label.pack(side='left')
# my_label.pack(expand = 1) # 중앙
# my_label.pack(side="left")

#layout(place): 정확한 위치를 지정하려면 Place
# my_label.place(x=0,y=0)

#layout(grid)
my_label.grid(column=0, row=0)

# label 변경 해보기
# my_label['text'] = "Bye"
# my_label.config(text="See you", font=("Arial", 40, "bold"))

# 엔트리 컴포넌트
input_word = Entry(width=10)
# 인풋 값을 얻으려면 어떻게 해야 하는가 ??
print(input_word.get())
input_word.grid(column=4, row=3)

second_button.grid(column=2, row=2)

# 스크린에서 루트가 유지 되게 에 어떻게 해야하는가 ??
root.mainloop()