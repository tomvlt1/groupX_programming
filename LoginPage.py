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
    columns = ["First Name", "Last Name", "Username", "Password", "Age", "Gender", "Nationality", "Favorite Team"]
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

def drawFootballField(win, x_start, y_start, width, height):
    field = Rectangle(Point(x_start, y_start), Point(x_start + width, y_start + height))
    field.setOutline("white")
    field.setWidth(2)
    field.draw(win)
    center_circle = Circle(Point(x_start + width / 2, y_start + height / 2), width / 6)
    center_circle.setOutline("white")
    center_circle.setWidth(2)
    center_circle.draw(win)
    center_line = Line(Point(x_start + width / 2, y_start), Point(x_start + width / 2, y_start + height))
    center_line.setOutline("white")
    center_line.setWidth(2)
    center_line.draw(win)
    left_penalty = Rectangle(Point(x_start, y_start + height / 4), Point(x_start + width / 5, y_start + 3 * height / 4))
    left_penalty.setOutline("white")
    left_penalty.setWidth(2)
    left_penalty.draw(win)
    right_penalty = Rectangle(Point(x_start + 4 * width / 5, y_start + height / 4), Point(x_start + width, y_start + 3 * height / 4))
    right_penalty.setOutline("white")
    right_penalty.setWidth(2)
    right_penalty.draw(win)

def RegisterGUI():
    win = GraphWin("FootViz Registration Page", 800, 500)
    win.setBackground("#FFFFFF")
    left_background = Rectangle(Point(0, 0), Point(400, 500))
    left_background.setFill("#ADEFD1")
    left_background.setOutline("#ADEFD1")
    left_background.draw(win)
    logo = Text(Point(200, 250), "COMPANY\nLOGO")
    logo.setTextColor("#1E2A39")
    logo.setStyle("bold")
    logo.setSize(24)
    logo.draw(win)
    title = Text(Point(600, 50), "REGISTER")
    title.setSize(20)
    title.setTextColor("#1E2A39")
    title.setStyle("bold")
    title.setFace("helvetica")
    title.draw(win)
    subtitle = Text(Point(600, 80), "IT'S COMPLETELY FREE")
    subtitle.setSize(12)
    subtitle.setTextColor("#1E2A39")
    subtitle.setFace("helvetica")
    subtitle.draw(win)
    fields = [("Name", 150), ("Username", 200), ("Email", 250), ("Password", 300), ("Confirm Password", 350)]
    entry_fields = {}
    for label, y in fields:
        label_text = Text(Point(500, y), label)
        label_text.setSize(12)
        label_text.setTextColor("#1E2A39")
        label_text.setFace("helvetica")
        label_text.draw(win)
        entry = Entry(Point(650, y), 25)
        entry.setFill("#F0F8FF")
        entry.draw(win)
        entry_fields[label] = entry
    create_button = roundButton(win, 550, 400, 700, 440, "Create Account", "white", "#2E8B57")
    back_button = roundButton(win, 550, 450, 700, 490, "Back to Login", "white", "#2E8B57")
    while True:
        try:
            click = win.getMouse()
            if 550 <= click.x <= 700 and 400 <= click.y <= 440:
                name = entry_fields["Name"].getText()
                username = entry_fields["Username"].getText()
                email = entry_fields["Email"].getText()
                password = entry_fields["Password"].getText()
                confirm_password = entry_fields["Confirm Password"].getText()
                if password != confirm_password:
                    error_message = Text(Point(600, 470), "Passwords do not match.")
                    error_message.setSize(12)
                    error_message.setTextColor("#FF6347")
                    error_message.setFace("helvetica")
                    error_message.draw(win)
                else:
                    df.loc[len(df)] = [name.split()[0], name.split()[-1], username, password, None, None, None, None]
                    df.to_csv(data_file, index=False)
                    win.close()
                    return "back_to_login"
            elif 550 <= click.x <= 700 and 450 <= click.y <= 490:
                win.close()
                return "back_to_login"
        except GraphicsError:
            break

def LoginGUI():
    win = GraphWin("FootViz Login Page", 800, 500)
    win.setBackground("#FFFFFF")
    left_background = Rectangle(Point(0, 0), Point(400, 500))
    left_background.setFill("#F8F9FA")
    left_background.setOutline("#F8F9FA")
    left_background.draw(win)
    title = Text(Point(200, 50), "LOGIN")
    title.setSize(20)
    title.setTextColor("#2E2E2E")
    title.setStyle("bold")
    title.setFace("helvetica")
    title.draw(win)
    subtitle = Text(Point(200, 80), "How to get started lorem ipsum dolor at?")
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
    right_background = Rectangle(Point(400, 0), Point(800, 500))
    right_background.setFill("#2E8B57")
    right_background.setOutline("#2E8B57")
    right_background.draw(win)
    drawFootballField(win, 450, 100, 300, 300)
    error_message = Text(Point(200, 480), "")
    error_message.setSize(12)
    error_message.setTextColor("#FF6347")
    error_message.setFace("helvetica")
    error_message.draw(win)
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
