# Chooseyear.py

from Globals import (
    create_button,
    create_label,
    is_click_in_rectangle,create_image_button,screen,color
)
from graphics import GraphWin, Point
from DataFunctions import fetch_years
(screen_width, screen_height, screen_widthHome, screen_heightHome)=screen()
(colorblueBac, colorvlueButtons, colorvlueButtons1, colorgreen, colorcream)=color()

def clear_window(win):
    for item in win.items[:]:
        item.undraw()
    win.update()

def display_year_selection():
    from Dashboard import create_dashboard
    
    years = fetch_years()
    if years:
        required_height = 200 + len(years) * 60
        win_height = max(200, min(required_height, 800))     
    else:
        win_height = 200
   
    win = GraphWin("Dataset Selector", 200, win_height)
    win.setBackground("#2c2855")
  
    back_button, vim = create_image_button(win, Point(0, 0), Point(80, 50), "images/back3.png",size=(20, 20), vout= "#2c2855")
    if years:
        year_label = create_label(win, "Select Year:", Point(100, 120), 16, colorcream, "bold")
        year_buttons = []
        for idx, year in enumerate(years):
            btn, txt13 = create_button(win, Point(30, 160 + (idx * 40)), Point(150, 200 + (idx * 40)), str(year), "#4682B4", "white")
            year_buttons.append((year, btn, txt13))
    else:
        year_label = create_label(win, "No data available", Point(620, 100),"#1E2A39", "normal")
        return None 

    while True:
        click = win.getMouse()
        if is_click_in_rectangle(click, back_button):
            create_dashboard() 
            
        else:            
            for year, btn, vtxt in year_buttons:
                if is_click_in_rectangle(click, btn):
                    for _, b, c in year_buttons:
                        b.undraw()
                        c.undraw()
                    year_label.undraw()    
                    win.close()           
                    return year 
