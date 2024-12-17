# PostFilter.py
from graphics import *
from Globals import create_button, is_click_in_rectangle, create_label
from GraphChoiceSelect import main as GraphChoiceSelect_main
from Graphsuggest import main as GraphSuggestions_main

def GraphOptions():
    from filter import main as fmain
    from Dashboard import create_dashboard
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
    
    back_arrow = Line(Point(50, 57), Point(100, 57))
    back_arrow.setArrow('first')
    back_arrow.setWidth(3)
    back_arrow.setFill("white")
    back_arrow.draw(win)
 
    back_button, vim = create_button(win, Point(300, 520), Point(500, 570), "Go to Dashboard","lightgreen", "Darkgreen",size=12)   
  

    while True:
        click = win.getMouse()

        if is_click_in_rectangle(click, button1):
            win.close()
            GraphSuggestions_main()

        elif is_click_in_rectangle(click, button2):
            #graph to variable
            win.close()
            GraphChoiceSelect_main()
        elif is_click_in_rectangle(click, back_button):
            win.close()
            create_dashboard()
        elif 50 < click.x < 100 and 55 < click.y < 58:  # Back arrow region  # If the back button is clicked            
            win.close()
            create_dashboard()

if __name__ == "__main__":
    selected_option = GraphOptions()
    print(f"Selected Option: {selected_option}")
