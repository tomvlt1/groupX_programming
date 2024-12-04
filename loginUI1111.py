from graphics import *
from Globals import *
from DataFunctions import *
from tkinter import messagebox  # To message user
from tkinter.filedialog import askopenfilename  # To import files
from jejjejejejej import *

# Screen dimensions
screen_width = 1280  # Width
screen_height = 720  # Height

# Function to handle user login
def login_user(input1, input2):
    username = input1.getText()  # Get the username from the input field
    password = input2.getText()  # Get the password directly from the input field
    
    result, vmessage, username, user_id = validate_user(username, password)
    if result:
        # Display the message on the screen
        messagebox.showinfo(getCurrentWindow(), vmessage)
        show_user_screen(username, user_id)
    else:
        messagebox.showerror(getCurrentWindow(), vmessage)

# Function to open the login screen
def open_login_screen():
    setIDUser(None)  
    win = getCurrentWindow()
    if win is not None:
        win.close()
    
    # Create a new login window
    login_window = GraphWin("FootViz Login", screen_width, screen_height)
    login_window.setBackground("white")
    setCurrentWindow(login_window)
    
    # Left section (Login Form)
    left_section_width = screen_width * 0.5
    right_section_x_start = left_section_width + 1
    
    # Create left background
    left_bg = Rectangle(Point(0, 0), Point(left_section_width, screen_height))
    left_bg.setFill("white")
    left_bg.draw(login_window)

    # Title
    title = Text(Point(left_section_width / 2, 100), "FOOTVIZ")
    title.setSize(26)
    title.setStyle("bold")
    title.setTextColor("black")
    title.draw(login_window)

    # Subtitle
    subtitle = Text(Point(left_section_width / 2, 140), "Login into your FootViz Account")
    subtitle.setSize(16)
    subtitle.setTextColor("gray")
    subtitle.draw(login_window)

    # Username field
    username_label = Text(Point(left_section_width / 2 - 100, screen_height / 2 - 100), "Username:")
    username_label.setSize(18)
    username_label.setTextColor("black")
    username_label.draw(login_window)
    username_input = Entry(Point(left_section_width / 2 + 50, screen_height / 2 - 100), 30)
    username_input.setFill("white")
    username_input.draw(login_window)

    # Password field
    password_label = Text(Point(left_section_width / 2 - 100, screen_height / 2 - 50), "Password:")
    password_label.setSize(18)
    password_label.setTextColor("black")
    password_label.draw(login_window)
    password_input = Entry(Point(left_section_width / 2 + 50, screen_height / 2 - 50), 30)
    password_input.setFill("white")
    password_input.draw(login_window)

    # Login button
    login_button = Rectangle(Point(left_section_width / 2 - 75, screen_height / 2 + 50),
                             Point(left_section_width / 2 + 75, screen_height / 2 + 90))
    login_button.setFill("green")
    login_button.setOutline("darkgreen")
    login_button.setWidth(2)
    login_button.draw(login_window)
    login_button_text = Text(Point(left_section_width / 2, screen_height / 2 + 70), "Login Now")
    login_button_text.setSize(18)
    login_button_text.setStyle("bold")
    login_button_text.setTextColor("white")
    login_button_text.draw(login_window)

    # Register button
    register_button = Rectangle(Point(left_section_width / 2 - 75, screen_height / 2 + 120),
                                Point(left_section_width / 2 + 75, screen_height / 2 + 160))
    register_button.setFill("green")
    register_button.setOutline("darkgreen")
    register_button.setWidth(2)
    register_button.draw(login_window)
    register_button_text = Text(Point(left_section_width / 2, screen_height / 2 + 140), "Register")
    register_button_text.setSize(18)
    register_button_text.setStyle("bold")
    register_button_text.setTextColor("white")
    register_button_text.draw(login_window)

    # Right section (Soccer Field)
    soccer_field = Rectangle(Point(right_section_x_start, 0), Point(screen_width, screen_height))
    soccer_field.setFill("green")
    soccer_field.draw(login_window)
    
    # Draw soccer field lines
    center_line = Line(Point(right_section_x_start + (screen_width - right_section_x_start) / 2, 0),
                       Point(right_section_x_start + (screen_width - right_section_x_start) / 2, screen_height))
    center_line.setWidth(3)
    center_line.setOutline("white")
    center_line.draw(login_window)

    circle = Circle(Point(right_section_x_start + (screen_width - right_section_x_start) / 2, screen_height / 2), 50)
    circle.setWidth(3)
    circle.setOutline("white")
    circle.draw(login_window)

    penalty_area_top = Rectangle(Point(right_section_x_start + 150, 0),
                                 Point(screen_width - 150, 200))
    penalty_area_top.setWidth(3)
    penalty_area_top.setOutline("white")
    penalty_area_top.draw(login_window)

    penalty_area_bottom = Rectangle(Point(right_section_x_start + 150, screen_height - 200),
                                    Point(screen_width - 150, screen_height))
    penalty_area_bottom.setWidth(3)
    penalty_area_bottom.setOutline("white")
    penalty_area_bottom.draw(login_window)

    # Event loop for login interaction
    while True:
        click_point = login_window.checkMouse()
        if click_point:
            # Check if login button is clicked
            if (left_section_width / 2 - 75 <= click_point.getX() <= left_section_width / 2 + 75 and
                    screen_height / 2 + 50 <= click_point.getY() <= screen_height / 2 + 90):
                login_user(username_input, password_input)
            # Check if register button is clicked
            if (left_section_width / 2 - 75 <= click_point.getX() <= left_section_width / 2 + 75 and
                    screen_height / 2 + 120 <= click_point.getY() <= screen_height / 2 + 160):
                open_user_creation_screen()

# Initialize application
open_login_screen()



