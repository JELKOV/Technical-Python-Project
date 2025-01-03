from tkinter import *

window = Tk()
window.title("Mile to Km Converter")
#padding
window.config(padx=20, pady=20)

# 라벨 설정
first_label = Label(text="is equal to")
first_label.grid(row=1, column=0)

input_mile = Entry(width=7)
input_mile.grid(row=0, column=1)

second_label = Label(text="mile")
second_label.grid(row=0, column=2)

third_label = Label(text="0")
third_label.grid(row=1, column=1)

fourth_label = Label(text="KM")
fourth_label.grid(row=1, column=2)

# 함수
def convert_km():
    input_int = float(input_mile.get())
    input_km = input_int * 1.60934
    third_label.config(text=f"{input_km:.2f}")  # 소수점 2자리로 표시

calculate_button = Button(text="Calculate", command=convert_km)
calculate_button.grid(row=3, column=1)

window.mainloop()