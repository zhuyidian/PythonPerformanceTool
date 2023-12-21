print('hello world')
import turtle

"""
turtle.pensize(20)
turtle.begin_fill()
for i in range(6):
    turtle.seth(i*60)
    turtle.fd(100)
turtle.end_fill()

turtle.done()
"""

def Peach_heart():
    turtle.left(135)
    turtle.fd(100)
    turtle.right(180)
    turtle.circle(50,-180)
    turtle.left(90)
    turtle.circle(50,-180)
    turtle.right(180)
    turtle.fd(100)

turtle.pensize(10)
Peach_heart()
turtle.penup()
turtle.goto(100,30)
turtle.pendown()
turtle.seth(0)
Peach_heart()
turtle.penup()
turtle.goto(-100,30)
turtle.pendown()
turtle.seth(25)
turtle.fd(350)
turtle.done()