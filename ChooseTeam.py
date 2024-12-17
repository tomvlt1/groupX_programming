# ChooseTeam.py

from Globals import (
    create_button,
    create_label,
    is_click_in_rectangle,create_image_button,
    screen,color
)
from graphics import GraphWin, Point,Image
from DataFunctions import fetch_teams_for_year
(screen_width, screen_height, screen_widthHome, screen_heightHome)=screen()
(colorblueBac, colorvlueButtons, colorvlueButtons1, colorgreen, colorcream)=color()
def clear_window(win):
    for item in win.items[:]:
        item.undraw()
    win.update()

def display_team_selection(selected_year):
    from Dashboard import create_dashboard
    
    win = GraphWin("Dataset Selector", 800,500)
    win.setBackground("#2c2855")
    
    teams = fetch_teams_for_year(selected_year)
    back_button, vim = create_image_button(win, Point(0, 0), Point(80, 50), "images/back3.png",size=(20, 20), vout= "#2c2855")
    team_label = create_label(win, "Select Team:", Point(100, 70), 16, colorcream, "bold")

    columns = 3 
    rows_per_column = 8 

    team_buttons = []
    icon_objects = []

    for idx, (team_name, icon_filename) in enumerate(teams):
        row = idx % rows_per_column 
        col = idx // rows_per_column  

        x_offset =30 + col * 250
        y_offset = 90 + row * 50  

        btn, txt1 = create_button(
            win,
            Point(x_offset, y_offset),
            Point(x_offset + 250, y_offset + 50),
            team_name,
            "#4682B4",
            "white",
            size=12
        )
        team_buttons.append((team_name, btn, txt1))

        if icon_filename:
            icon_path = f"images/{icon_filename}"
            icon = Image(Point(x_offset + 30, y_offset + 25), icon_path)
            icon.draw(win)
            icon_objects.append(icon)

   
    while True:
        click_point = win.getMouse()
        if is_click_in_rectangle(click_point, back_button):
            create_dashboard()
            return None 
        else:
            for team_name, btn, txt1 in team_buttons:
                if is_click_in_rectangle(click_point, btn):
                    win.close()           
                    return team_name  
