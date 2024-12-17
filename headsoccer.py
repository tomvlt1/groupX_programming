# HeadSoccer.py
from graphics import *
import time
import random
import math

def run_headsoccer():
    win = GraphWin("Penalty Kick Challenge", 600, 400)
    win.setBackground("green")

    goal = Rectangle(Point(200, 50), Point(400, 150))
    goal.setFill("white")
    goal.draw(win)

    goalie_start_p1 = Point(280, 60)
    goalie_start_p2 = Point(320, 150)

    goalie = Rectangle(goalie_start_p1, goalie_start_p2)
    goalie.setFill("blue")
    goalie.draw(win)

    ball = Circle(Point(300, 350), 10)
    ball.setFill("white")
    ball.draw(win)

    goalie_speed = 6

    def animate_ball_and_goalie(target_x, target_y, power):
        nonlocal shot_out_of_control
        start_x, start_y = 300, 350

        if power > 100:
            print("You overshot the ball! The shot went out of control!")
            shot_out_of_control = True
            target_x += random.choice([-100, 100])
            target_y += random.choice([-50, 50])
            num_steps = 50
        else:
            shot_out_of_control = False
            num_steps = int(30 - power / 5)
            if num_steps <= 0:
                num_steps = 1  

        dx = (target_x - start_x) / num_steps
        dy = (target_y - start_y) / num_steps

        for i in range(num_steps):
            ball.move(dx, dy)

            goalie_center_x = (goalie.getP1().getX() + goalie.getP2().getX()) / 2
            if goalie_center_x < target_x:
                move_amount = min(goalie_speed, target_x - goalie_center_x)
                if goalie.getP2().getX() + move_amount <= 400:
                    goalie.move(move_amount, 0)
            elif goalie_center_x > target_x:
                move_amount = min(goalie_speed, goalie_center_x - target_x)
                if goalie.getP1().getX() - move_amount >= 200:
                    goalie.move(-move_amount, 0)

            time.sleep(0.02)

    power_bar_outline = Rectangle(Point(450, 300), Point(550, 350))
    power_bar_outline.setFill("white")
    power_bar_outline.draw(win)

    power_bar = Rectangle(Point(450, 300), Point(450, 350))
    power_bar.setFill("red")
    power_bar.draw(win)

    power = 0
    powering = False
    click_start_time = None
    shot_out_of_control = False
    score = 0
    while score < 3:
        mouse_pressed = win.checkMouse()
        if mouse_pressed:
            if not powering:
                powering = True
                click_start_time = time.time()
            else:
                target_x = mouse_pressed.getX()
                target_y = mouse_pressed.getY()

                animate_ball_and_goalie(target_x, target_y, power)

                goalie_x1 = goalie.getP1().getX()
                goalie_x2 = goalie.getP2().getX()
                ball_x = ball.getCenter().getX()
                ball_y = ball.getCenter().getY()

                if shot_out_of_control:
                    print("Missed! The shot was outside the goal area due to overpower.")
                elif 200 <= ball_x <= 400 and 50 <= ball_y <= 150:
                    time.sleep(1)
                    goalie_x1 = goalie.getP1().getX()
                    goalie_x2 = goalie.getP2().getX()
                    ball_x = ball.getCenter().getX()
                    ball_y = ball.getCenter().getY()

                    if goalie_x1 <= ball_x <= goalie_x2 and 60 <= ball_y <= 150:
                        print("Goalkeeper saved it!")
                    else:
                        score += 1
                        print("GOAL!!!")
                else:
                    print("Missed! The shot was outside the goal area.")

                ball.move(300 - ball.getCenter().getX(), 350 - ball.getCenter().getY())
                power = 0
                power_bar.undraw()
                power_bar = Rectangle(Point(450, 300), Point(450, 350))
                power_bar.setFill("red")
                power_bar.draw(win)
                powering = False

                current_goalie_center_x = (goalie.getP1().getX() + goalie.getP2().getX()) / 2
                initial_goalie_center_x = (280 + 320) / 2  
                dx = initial_goalie_center_x - current_goalie_center_x
                goalie.move(dx, 0)

        if powering:
            power = min(120, (time.time() - click_start_time) * 150)

            power_bar.undraw()
            power_bar = Rectangle(Point(450, 300), Point(450 + power, 350))
            power_bar.setFill("red")
            power_bar.draw(win)

        time.sleep(0.01)

    win.close()

if __name__ == "__main__":
    run_headsoccer()
