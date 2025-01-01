from turtle import Turtle, Screen

ahn = Turtle()
screen = Screen()
screen.title("etch-A-Sketch App")
screen.setup(800, 600)


ahn.speed("fastest")

def move_forward():
    #M
    ahn.forward(10)

def move_backward():
    #S
    ahn.backward(10)

def move_left():
    #A
    new_heading = ahn.heading() + 10
    ahn.setheading(new_heading)

def move_right():
    #D
    new_heading = ahn.heading() - 10
    ahn.setheading(new_heading)

def clear_screen():
    #C
    ahn.clear()
    ahn.penup()
    ahn.home()
    ahn.pendown()


screen.listen()
screen.onkey(move_forward, "w")  # W 키와 앞으로 이동 함수 연결
screen.onkey(move_backward, "s")  # S 키와 뒤로 이동 함수 연결
screen.onkey(move_left, "a")  # A 키와 왼쪽 회전 함수 연결
screen.onkey(move_right, "d")  # D 키와 오른쪽 회전 함수 연결
screen.onkey(clear_screen, "c")  # C 키와 화면 초기화 함수 연결


screen.exitonclick()