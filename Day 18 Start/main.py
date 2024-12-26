from turtle import Turtle, Screen

timmy_the_turtle  = Turtle()
timmy_the_turtle.shape("turtle")
timmy_the_turtle.color("gold")

def forward100_right90():
    timmy_the_turtle.forward(100)
    timmy_the_turtle.right(90)

for i in range(4):
    forward100_right90()


screen = Screen()
screen.exitonclick()