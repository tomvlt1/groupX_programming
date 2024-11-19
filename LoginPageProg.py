from graphics import *

'''
Pseudocode
- loginGUI: create a function to display the login page
open, name and set the size of the window 
set the window to a white background
draw a title in the page
draw the instructions for the user in the page
draw a username instruction in the page
draw a password instruction in the page
draw a registration instruction in the page
create a field for the user to insert their username
set the value of the field equal to 0 in the case the user does not type in it
draw the box for the user to insert their username
create a field for the user to insert their password
set the value of the field equal to 0 in the case the user does not type in it
draw the box for the user to insert their password
draw a buttom for the user to click to login 
draw a buttom for the user to click to register 


- Register GUI: create a function to display the login page
open, name and set the size of the window 
set the window to a white background
draw a title in the page
draw the instructions for the user in the page
draw a username instruction in the page
draw a password instruction in the page
draw a registration instruction in the page
create a field for the user to insert their username
set the value of the field equal to 0 in the case the user does not type in it
draw the box for the user to insert their username
create a field for the user to insert their password
set the value of the field equal to 0 in the case the user does not type in it
draw the box for the user to insert their password
draw a buttom for the user to click to login 
draw a buttom for the user to click to register 





'''

def RegisterGUI():
    win = GraphWin("Registration Page", 1300, 800)
    win.setBackground("dark green")
    # Draw the interface
    Text(Point(650, 70), "TableauV2 Registration").draw(win).setSize(35)
    Text(Point(650, 100), "Please complete all of the following fields").draw(win)
    Text(Point(650, 150), "Set your username:").draw(win)
    Text(Point(650, 200), "Set your password:").draw(win)
    Text(Point(650, 400), "Register here: ").draw(win)
    InputUsername = Entry(Point(650, 2), 5)
    InputUsername.setText("0.0")
    InputUsername.draw(win)
    InputPassword = Entry(Point(650, 2), 5)
    InputPassword.setText("0.0")
    InputPassword.draw(win)
    outputText = Text(Point(650, 1),"")
    outputText.draw(win)
    button = Text(Point(800, 2.0), "Convert It")
    button.draw(win)
    Rectangle(Point(1, 1.5), Point(2, 2.5)).draw(win)

# wait for a mouse click
    win.getMouse()
    # convert input
    celsius = float(inputText.getText())
    fahrenheit = 9.0 / 5.0 * celsius + 32
    # display output and change button
    outputText.setText(round(fahrenheit, 2))
    button.setText("Quit")
    # wait for click and then quit
    win.getMouse()
    win.close()

LoginGUI()

def LoginGUI():
    win = GraphWin("Login Page", 1300, 800)
    win.setBackground("white")
    # Draw the interface
    Text(Point(650, 70), "Welcome to Tableauv2!").draw(win).setSize(35)
    Text(Point(650, 100), "Please enter your login information below").draw(win)
    Text(Point(650, 150), "Username:").draw(win)
    Text(Point(650, 200), "Password:").draw(win)
    Text(Point(650, 400), "Register here: ").draw(win)
    InputUsername = Entry(Point(650, 2), 5)
    InputUsername.setText("0.0")
    InputUsername.draw(win)
    InputPassword = Entry(Point(650, 2), 5)
    InputPassword.setText("0.0")
    InputPassword.draw(win)
    outputText = Text(Point(650, 1),"")
    outputText.draw(win)
    button = Text(Point(800, 2.0), "Convert It")
    button.draw(win)
    Rectangle(Point(1, 1.5), Point(2, 2.5)).draw(win)

# wait for a mouse click
    win.getMouse()
    # convert input
    celsius = float(inputText.getText())
    fahrenheit = 9.0 / 5.0 * celsius + 32
    # display output and change button
    outputText.setText(round(fahrenheit, 2))
    button.setText("Quit")
    # wait for click and then quit
    win.getMouse()
    win.close()

LoginGUI()