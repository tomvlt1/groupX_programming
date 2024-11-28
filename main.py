import time
from graphics import *
from FootGameHome import FootGameHomeMain 


def create_window():
    win = GraphWin("Football Dashboard UI", 900, 500)
    win.setBackground(color_rgb(44, 40, 85))
    return win

def create_sidebar(win):
    sidebar = Rectangle(Point(0, 0), Point(200, 500))
    sidebar.setFill(color_rgb(31, 27, 58))
    sidebar.draw(win)

    new_button = Rectangle(Point(20, 20), Point(180, 60))
    new_button.setFill(color_rgb(28, 195, 170))
    new_button.draw(win)
    new_button_text = Text(new_button.getCenter(), "New Match")
    new_button_text.setTextColor("white")
    new_button_text.setSize(12)
    new_button_text.draw(win)

    button_titles = ["Dashboard", "Matches", "Players", "Teams"]
    y_offset = 90
    for btn in button_titles:
        button = Rectangle(Point(20, y_offset), Point(180, y_offset + 40))
        button.setFill(color_rgb(44, 40, 85))
        button.draw(win)
        button_text = Text(button.getCenter(), btn)
        button_text.setTextColor("white")
        button_text.setSize(12)
        button_text.draw(win)
        y_offset += 50

def create_overview_section(win):
    overview_y_start = 20
    overview_titles = [
        {"title": "Upcoming Matches", "number": "5"},
        {"title": "Matches Played", "number": "12"},
        {"title": "Goals Scored", "number": "34"}
    ]
    x_offset = 220
    for overview in overview_titles:
        overview_box = Rectangle(Point(x_offset, overview_y_start), Point(x_offset + 180, overview_y_start + 100))
        overview_box.setFill("white")
        overview_box.draw(win)

        title_text = Text(Point(x_offset + 90, overview_y_start + 30), overview['title'])
        title_text.setTextColor(color_rgb(51, 51, 51))
        title_text.setSize(10)
        title_text.draw(win)

        number_text = Text(Point(x_offset + 90, overview_y_start + 70), overview['number'])
        number_text.setTextColor(color_rgb(44, 40, 85))
        number_text.setSize(20)
        number_text.setStyle('bold')
        number_text.draw(win)

        x_offset += 200

def create_mini_game_area(win):
    # Define the mini-game area coordinates
    mini_game_left = 220
    mini_game_top = 140
    mini_game_right = 880
    mini_game_bottom = 480

    # Draw the rectangle for the mini-game area
    mini_game_area = Rectangle(Point(mini_game_left, mini_game_top), Point(mini_game_right, mini_game_bottom))
    mini_game_area.setFill(color_rgb(224, 224, 224))
    mini_game_area.draw(win)

    # Start the mini-game within this area
    FootGameHomeMain(win)

def create_dashboard():
    win = create_window()
    create_sidebar(win)
    create_overview_section(win)
    create_mini_game_area(win)

    win.getMouse()  # Wait for user interaction before closing
    win.close()

if __name__ == "__main__":
    create_dashboard()
