# HeadSoccer.py
from graphics import *
import time
import random


def run_headsoccer():
    # Create the main window
    win = GraphWin("Penalty Kick Challenge", 600, 400)
    win.setBackground("green")

    # Draw the goal area
    goal = Rectangle(Point(200, 50), Point(400, 150))
    goal.setFill("white")
    goal.draw(win)

    # Initial goalkeeper position
    goalie_start_p1 = Point(280, 60)
    goalie_start_p2 = Point(320, 150)

    # Draw the goalkeeper
    goalie = Rectangle(goalie_start_p1, goalie_start_p2)
    goalie.setFill("blue")
    goalie.draw(win)

    # Draw the ball
    ball = Circle(Point(300, 350), 10)
    ball.setFill("white")
    ball.draw(win)

    # Goalkeeper's movement speed
    goalie_speed = 6

    # Function to animate the ball towards the clicked point and move the goalkeeper simultaneously
    def animate_ball_and_goalie(target_x, target_y, power):
        nonlocal shot_out_of_control
        start_x, start_y = 300, 350

        if power > 100:
            print("You overshot the ball! The shot went out of control!")
            shot_out_of_control = True
            # Ball goes in a random bad direction if overpower
            target_x += random.choice([-100, 100])
            target_y += random.choice([-50, 50])
            num_steps = 50
        else:
            shot_out_of_control = False
            num_steps = int(30 - power / 5)
            if num_steps <= 0:
                num_steps = 1  # Ensure at least one step to avoid division by zero

        dx = (target_x - start_x) / num_steps
        dy = (target_y - start_y) / num_steps

        for i in range(num_steps):
            # Move the ball
            ball.move(dx, dy)

            # Move the goalkeeper towards the ball, keeping within bounds
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

    # Draw the power bar
    power_bar_outline = Rectangle(Point(450, 300), Point(550, 350))
    power_bar_outline.setFill("white")
    power_bar_outline.draw(win)

    power_bar = Rectangle(Point(450, 300), Point(450, 350))
    power_bar.setFill("red")
    power_bar.draw(win)

    # Game loop
    power = 0
    powering = False
    click_start_time = None
    shot_out_of_control = False
    score = 0
    while score < 3:
        # Detect mouse click for power bar
        mouse_pressed = win.checkMouse()
        if mouse_pressed:
            if not powering:
                powering = True
                click_start_time = time.time()
            else:
                # Kick the ball after releasing the click
                target_x = mouse_pressed.getX()
                target_y = mouse_pressed.getY()

                # Animate the ball and goalkeeper simultaneously
                animate_ball_and_goalie(target_x, target_y, power)

                # Check if the ball is intercepted by the goalkeeper or inside the goal box
                goalie_x1 = goalie.getP1().getX()
                goalie_x2 = goalie.getP2().getX()
                ball_x = ball.getCenter().getX()
                ball_y = ball.getCenter().getY()

                if shot_out_of_control:
                    print("Missed! The shot was outside the goal area due to overpower.")
                elif 200 <= ball_x <= 400 and 50 <= ball_y <= 150:
                    # Adding 1-second delay to determine goal status
                    time.sleep(1)
                    # Re-check if the goalkeeper is touching the ball after delay
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

                # Reset ball position and power
                ball.move(300 - ball.getCenter().getX(), 350 - ball.getCenter().getY())
                power = 0
                power_bar.undraw()
                power_bar = Rectangle(Point(450, 300), Point(450, 350))
                power_bar.setFill("red")
                power_bar.draw(win)
                powering = False

                # Reset goalkeeper position
                current_goalie_center_x = (goalie.getP1().getX() + goalie.getP2().getX()) / 2
                initial_goalie_center_x = (280 + 320) / 2  # Average of goalie_start_p1.x and goalie_start_p2.x
                dx = initial_goalie_center_x - current_goalie_center_x
                goalie.move(dx, 0)

        if powering:
            # Calculate power based on how long the mouse is held
            power = min(120, (time.time() - click_start_time) * 150)

            # Update power bar
            power_bar.undraw()
            power_bar = Rectangle(Point(450, 300), Point(450 + power, 350))
            power_bar.setFill("red")
            power_bar.draw(win)

        # Delay for frame rate
        time.sleep(0.01)

    win.close()

if __name__ == "__main__":
    run_headsoccer()
