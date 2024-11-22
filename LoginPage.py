'''
Pseudocode
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
set the global data frame
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

def roundButton(win, x1, y1, x2, y2, text, text_color, fill_color):
    button = Rectangle(Point(x1, y1), Point(x2, y2))
    button.setFill(fill_color)
    button.setOutline(fill_color)
    button.draw(win)
    label = Text(Point((x1 + x2) / 2, (y1 + y2) / 2), text)
    label.setTextColor(text_color)
    label.setStyle("bold")
    label.setSize(18)
    label.draw(win)
    return button

def LoginGUI():
    win = GraphWin("FootViz Login Page", 1300, 800)
    win.setBackground("dark green")

    title = Text(Point(650, 70), "Welcome to FootViz!")
    title.setSize(36)
    title.setTextColor("white")
    title.setStyle("bold")
    title.setFace("courier")
    title.draw(win)

    subtitle = Text(Point(650, 120), "Please enter your login information below")
    subtitle.setSize(20)
    subtitle.setTextColor("white")
    subtitle.setFace("courier")
    subtitle.draw(win)

    username_label = Text(Point(500, 450), "Username:")
    username_label.setSize(20)
    username_label.setTextColor("white")
    username_label.setFace("courier")
    username_label.draw(win)

    password_label = Text(Point(500, 500), "Password:")
    password_label.setSize(20)
    password_label.setTextColor("white")
    password_label.setFace("courier")
    password_label.draw(win)

    username_field = Entry(Point(800, 450), 30)
    username_field.draw(win)

    password_field = Entry(Point(800, 500), 30)
    password_field.draw(win)

    login_button = roundButton(win, 500, 600, 700, 650, "Login", "white", "dark green")
    register_button = roundButton(win, 750, 600, 950, 650, "Register", "white", "dark green")

    error_message = Text(Point(650, 700), "")
    error_message.setSize(18)
    error_message.setTextColor("red")
    error_message.setFace("courier")
    error_message.draw(win)

    while True:
        try:
            click = win.getMouse()
            if 500 <= click.x <= 700 and 600 <= click.y <= 650:
                username = username_field.getText()
                password = password_field.getText()

                if ((df['Username'] == username) & (df['Password'] == password)).any():
                    win.close()
                    return
                else:
                    error_message.setText("Incorrect username or password. Please try again.")

            elif 750 <= click.x <= 950 and 600 <= click.y <= 650:
                win.close()
                RegisterGUI()  
                return  
        except GraphicsError:
            break

def RegisterGUI():
    global df
    win = GraphWin("FootViz Registration Page", 1300, 800)
    win.setBackground("dark green")

    title = Text(Point(650, 70), "FootViz Registration")
    title.setSize(36)
    title.setTextColor("white")
    title.setStyle("bold")
    title.setFace("courier")
    title.draw(win)

    subtitle = Text(Point(650, 120), "Please complete all the fields below")
    subtitle.setSize(20)
    subtitle.setTextColor("white")
    subtitle.setFace("courier")
    subtitle.draw(win)

    labels = ["First Name:", "Last Name:", "Username:", "Password:", "Age:", 
              "Gender:", "Nationality:", "Favorite Team:"]
    fields = []
    for i, label in enumerate(labels):
        label_text = Text(Point(300, 200 + i * 50), label)
        label_text.setSize(18)
        label_text.setTextColor("white")
        label_text.setFace("courier")
        label_text.draw(win)
        field = Entry(Point(700, 200 + i * 50), 30)
        field.draw(win)
        fields.append(field)
    register_button = roundButton(win, 550, 650, 750, 700, "Register", "white", "dark green")
    while True:
        try:
            click = win.getMouse()
            if 550 <= click.x <= 750 and 650 <= click.y <= 700:
                user_data = [field.getText() for field in fields]
                new_row = pd.DataFrame([user_data], columns=columns)
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(data_file, index=False)  
                print(df)  
                win.close()
                return  
        except GraphicsError:
            break

def main():
    LoginGUI()

main()
