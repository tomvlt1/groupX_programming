'''
Pseudocode
load the user data from the UserData.csv file into the DataFrame df if it exists
if the UserData.csv file does not exist, create an empty DataFrame with the required columns
after a registration is done, save the updated DataFrame to a csv file to store the data 

- create a main function to call all other functions
- call the LoginGUI function from main
the login function should call the register function 

import pandas in order format a data frame to store the information inpputed on the registration page
import graphics to display the gui 
import os to check the path of the data set 
create a pd dataframe to store the data from each user as they insert in the registration page

- LoginGUI: create a function to display the login page
open, name and set the size of the window 
set the window to a dark green background
draw a title in the page with white text and a custom font
draw a football-themed logo or icon on the background
draw the instructions for the user in the page with white text and a custom font
draw a username instruction in the page with white text and a custom font
draw a password instruction in the page with white text and a custom font
draw a button for login with a rounded rectangle and white text
draw a button for register with a rounded rectangle and white text
create a field for the user to insert their username
create a field for the user to insert their password
create an error message label that will be displayed in red if the login attempt is incorrect
wait for a user mouse click
check if user clicked login button
check if user clicked register button
close the login page if login button clicked
call RegisterGUI if register button clicked

- RegisterGUI: create a function to display the registration page
set the global data frame to store the user data
open, name and set the size of the window 
set the window to a dark green background
draw a title in the page with white text and a custom font
draw a football-themed logo or icon on the background
draw the instructions for the user in the page with white text and a custom font
draw a label for each registration field with white text and a custom font
create fields for the user to input their data
draw a button for submitting the registration form with a rounded rectangle and white text
wait for a user mouse click
check if user clicked register button
retrieve the data from the fields
create a new row for each new user input 
append the data the global data frame 
save the updated DataFrame to a CSV file to keep the data
close the registration page
'''
from graphics import *
import pandas as pd
import os

data_file = "user_data.csv"

if os.path.exists(data_file):
    df = pd.read_csv(data_file)
else:
    columns = ["First Name", "Last Name", "Username", "Password", "Shirt Number", "Shirt Color", "Date of Birth", "Gender", "Nationality", "Favorite Team"]
    df = pd.DataFrame(columns=columns)

def roundButton(win, x1, y1, x2, y2, text, text_color, fill_color, border_color="white", border_width=2):
    button = Rectangle(Point(x1, y1), Point(x2, y2))
    button.setFill(fill_color)
    button.setOutline(border_color)
    button.setWidth(border_width)
    button.draw(win)
    label = Text(Point((x1 + x2) / 2, (y1 + y2) / 2), text)
    label.setTextColor(text_color)
    label.setStyle("bold")
    label.setSize(14)
    label.draw(win)
    return button

def drawFootballField(win):
    field = Rectangle(Point(400, 0), Point(800, 500))
    field.setFill("#2E8B57")
    field.setOutline("#FFFFFF")
    field.setWidth(2)
    field.draw(win)
    outer_boundary = Rectangle(Point(420, 20), Point(780, 480))
    outer_boundary.setOutline("white")
    outer_boundary.setWidth(2)
    outer_boundary.draw(win)
    center_line = Line(Point(420, 250), Point(780, 250))
    center_line.setOutline("white")
    center_line.setWidth(2)
    center_line.draw(win)
    center_circle = Circle(Point(600, 250), 50)
    center_circle.setOutline("white")
    center_circle.setWidth(2)
    center_circle.draw(win)
    center_dot = Circle(Point(600, 250), 3)
    center_dot.setFill("white")
    center_dot.draw(win)
    top_penalty_area = Rectangle(Point(480, 20), Point(720, 120))
    top_penalty_area.setOutline("white")
    top_penalty_area.setWidth(2)
    top_penalty_area.draw(win)
    bottom_penalty_area = Rectangle(Point(480, 380), Point(720, 480))
    bottom_penalty_area.setOutline("white")
    bottom_penalty_area.setWidth(2)
    bottom_penalty_area.draw(win)
    top_goal_area = Rectangle(Point(520, 20), Point(680, 60))
    top_goal_area.setOutline("white")
    top_goal_area.setWidth(2)
    top_goal_area.draw(win)
    bottom_goal_area = Rectangle(Point(520, 440), Point(680, 480))
    bottom_goal_area.setOutline("white")
    bottom_goal_area.setWidth(2)
    bottom_goal_area.draw(win)
    top_goal_dot = Circle(Point(600, 70), 3)
    top_goal_dot.setFill("white")
    top_goal_dot.draw(win)
    bottom_goal_dot = Circle(Point(600, 430), 3)
    bottom_goal_dot.setFill("white")
    bottom_goal_dot.draw(win)

def LoginGUI():
    win = GraphWin("FootViz Login Page", 800, 500)
    win.setBackground("#FFFFFF")
    left_background = Rectangle(Point(0, 0), Point(400, 500))
    left_background.setFill("#F8F9FA")
    left_background.setOutline("#F8F9FA")
    left_background.draw(win)
    title = Text(Point(200, 50), "FOOTVIZ")
    title.setSize(20)
    title.setTextColor("#2E2E2E")
    title.setStyle("bold")
    title.setFace("helvetica")
    title.draw(win)
    subtitle = Text(Point(200, 80), "Login into your FootViz Account")
    subtitle.setSize(12)
    subtitle.setTextColor("#6C757D")
    subtitle.setFace("helvetica")
    subtitle.draw(win)
    username_label = Text(Point(130, 180), "Username")
    username_label.setSize(12)
    username_label.setTextColor("#6C757D")
    username_label.setFace("helvetica")
    username_label.draw(win)
    username_field = Entry(Point(200, 210), 25)
    username_field.setFill("#F0F8FF")
    username_field.draw(win)
    password_label = Text(Point(130, 260), "Password")
    password_label.setSize(12)
    password_label.setTextColor("#6C757D")
    password_label.setFace("helvetica")
    password_label.draw(win)
    password_field = Entry(Point(200, 290), 25)
    password_field.setFill("#F0F8FF")
    password_field.draw(win)
    login_button = roundButton(win, 130, 330, 270, 370, "Login Now", "white", "#2E8B57")
    register_button = roundButton(win, 130, 380, 270, 420, "Register", "white", "#2E8B57")
    error_message = Text(Point(200, 480), "")
    error_message.setSize(12)
    error_message.setTextColor("#FF6347")
    error_message.setFace("helvetica")
    error_message.draw(win)
    drawFootballField(win)
    while True:
        try:
            click = win.getMouse()
            if 130 <= click.x <= 270 and 330 <= click.y <= 370:
                username = username_field.getText()
                password = password_field.getText()
                if ((df['Username'] == username) & (df['Password'] == password)).any():
                    win.close()
                    return
                else:
                    error_message.setText("Incorrect username or password.")
            elif 130 <= click.x <= 270 and 380 <= click.y <= 420:
                win.close()
                if RegisterGUI() == "back_to_login":
                    LoginGUI()
        except GraphicsError:
            break

def main():
    LoginGUI()

main()
