# PostFilter.py

from graphics import *
from Globals import create_button, is_click_in_rectangle, create_label

def GraphOptions():
    """
    A window with two buttons: 'Variable to Graph' and 'Graph to Variable'.
    """
    win = GraphWin("Graph Options", 800, 600)
    win.setBackground("darkgreen")

    bg_image = Image(Point(400, 300), "images/pic.gif")
    bg_image.draw(win)

    create_label(win, "Graph Options", Point(400, 50), size=18, vcolor="white", style="bold")

    button1, button1_text = create_button(win, Point(300, 200), Point(500, 270),
                                          "Variable to Graph", fill_color="lightgreen", text_color="black", size=14)
    button2, button2_text = create_button(win, Point(300, 350), Point(500, 420),
                                          "Graph to Variable", fill_color="lightgreen", text_color="black", size=14)

    while True:
        click = win.getMouse()

        if is_click_in_rectangle(click, button1):
            win.close()
            return "Variable to Graph"

        if is_click_in_rectangle(click, button2):
            win.close()
            return "Graph to Variable"

if __name__ == "__main__":
    selected_option = GraphOptions()
    print(f"Selected Option: {selected_option}")
