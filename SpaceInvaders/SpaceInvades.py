'''
Space Invaders part 1: Set up the screen
Python 3.6 on Windows
'''

import turtle
import os
import math
import random

#Set up the screen
window = turtle.Screen()
window.bgcolor("black")
window.title("Kill the moez")
window.bgpic("bg.gif")

#Register the shape
turtle.register_shape("MiniMike.gif"),
turtle.register_shape("MiniMoiz.gif")
turtle.register_shape("FarkasMini.gif")
turtle.register_shape("MiniThomas.gif")
turtle.register_shape("MiniSteve.gif")
turtle.register_shape("MiniMike.gif")
turtle.register_shape("F.gif")
baddieList = ["MiniMike.gif", "MiniMoiz.gif", "MiniSteve.gif", "MiniThomas.gif"]

#Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

#Set and draw score
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 270)
scorestring = "Score : %s" %score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

#Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("FarkasMini.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

playerspeed = 15

#Move player left
def move_left():
    x = player.xcor()
    x -= playerspeed
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    player.setx(x)

def fire_bullet():
    #Declare bulletstate as a global if it needs to be changed
    global bulletstate
    if bulletstate == "ready":
        bulletstate = "firing"
        #Move bullet to player
        x = player.xcor()
        y = player.ycor() + 45
        bullet.setposition(x, y)
        bullet.showturtle()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow((t1.xcor()) - t2.xcor(), 2) + (math.pow(t1.ycor() - t2.ycor(), 2)))
    if distance < 30:
        return True
    else:
        return False

#Create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

enemyspeed = 4

#Choose number of enemies
number_of_enemies = 8
enemies = []

for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

for enemy in enemies:
    #Create the enemy
    enemy.shape(baddieList[random.randint(0, len(baddieList)-1)])
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-250, 250)
    y = random.randint(150, 250)
    enemy.setposition(x, y)

#Create the weapon
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("F.gif")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.25, 0.25)
bullet.hideturtle()

bulletspeed = 10
bulletstate = "ready"

#Main game loop
#Move the enemy
while True:

    for enemy in enemies:
        x = enemy.xcor()
        x+= enemyspeed
        enemy.setx(x)

        #Move enemy back and down
        if enemy.xcor() > 280:
            enemyspeed *= -1
            for n in range(1,20):
                for e in enemies:
                    y = e.ycor()
                    y -= 2.5
                    e.sety(y)

        if enemy.xcor() < -280:
            enemyspeed *= -1
            for n in range(1,20):
                for e in enemies:
                    y = e.ycor()
                    y -= 2.5
                    e.sety(y)

    #Move the bullet
    y = bullet.ycor()
    y += bulletspeed
    bullet.sety(y)

    #Check to see if bullet has reached the top
    if bullet.ycor() > 300:
        bullet.hideturtle()
        bulletstate = "ready"

    #Check to see if the bullet has hit the enemy
    for enemy in enemies:
        if isCollision(bullet, enemy):
            #Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
            #Update the score
            score += 10
            scorestring = "Score: %s" %score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

        if isCollision(player, enemy) or enemy.ycor() < -250:
            player.hideturtle()
            enemy.hideturtle()
            gameOver = turtle.Turtle()
            gameOver.speed(0)
            gameOver.color("red")
            gameOver.penup()
            gameOver.setposition(0, 0)
            gameOverString = "FIN"
            gameOver.write(gameOverString, False, align="left", font=("comic sans", 30, "normal"))
            gameOver.hideturtle()
            break


