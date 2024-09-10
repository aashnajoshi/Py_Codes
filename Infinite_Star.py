import turtle

col=('yellow', 'red', 'green', 'orange', 'blue', 'white')
t = turtle.Turtle()
screen=turtle.Screen()
screen.bgcolor('Black')
t.speed(30)

for i in range (150):
    t.color(col[i%6])
    t.forward(i*4)
    t.left(150)
    t.width(2)
    
turtle.done()