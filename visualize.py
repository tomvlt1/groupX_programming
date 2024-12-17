from Globals import *
from Graphsuggest import Graphsuggest_main
from DataFunctions import *
from main_statistics import *
from Login import LoginGUI
(screen_width, screen_height, screen_widthHome, screen_heightHome)=screen()
(colorblueBac, colorvlueButtons, colorvlueButtons1, colorgreen, colorcream)=color()

def statistics(userId):   
    oldwin = getCurrentWindow()   
    if oldwin:
        oldwin.close()  
    winStatistics = GraphWin("Statistics Page", 1100, 800)
    setCurrentWindow(winStatistics)
    win = getCurrentWindow()    
    win.setBackground("#FFFFFF")  
    left_background = Rectangle(Point(0, 0), Point(500, 800))
    left_background.setFill("#ADEFD1")
    left_background.setOutline("#ADEFD1")
    left_background.draw(win)
    
    drawFootballField(win,Point(550, 150), Point(950, 700))  
    
    title = create_label(win, "STATISTICS", Point(250, 60), 24, "#1E2A39", "bold")  
    vcolorbutton = "#2E8B57"

    team_buttons = []  
    team_menu_shown = False  

    if userId:   
         
       
        gr1_button,txt11 = create_button(win, Point(100, 270), Point(350, 320), "Team Performance", vcolorbutton, "white")
        gr2_button,txt111 = create_button(win, Point(100, 330), Point(350, 380), "Possession vs effectiveness", vcolorbutton, "white")
        gr3_button,txt112 = create_button(win, Point(100, 390), Point(350, 440), "Shooting Statistics", vcolorbutton, "white")
        gr4_button,txt113 = create_button(win, Point(100, 450), Point(350, 480), "Dinamics graphs", vcolorbutton, "white")
        back_button,vim= create_image_button(win, Point(0, 0), Point(100, 50), "images/back.png", size=(20, 20), vout="#ADEFD1")
        
        while True:
            try:
                click = win.getMouse()

                if is_click_in_rectangle(click, back_button):
                    LoginGUI()
                    break

                elif is_click_in_rectangle(click, gr1_button):                  

                    years = fetch_years()
                    if years:
                        selected_year = display_year_selection(win, years)
                        if selected_year:
                            teams = fetch_teams_for_year(selected_year)
                            if teams:                              
                                selected_team= display_team_selection(win, teams)                               
                                if selected_team:
                                    generate_graphs_1(selected_year, selected_team)     
                elif is_click_in_rectangle(click, gr2_button):
               
                    years = fetch_years()
                    if years:
                        selected_year = display_year_selection(win, years)
                        if selected_year:
                            teams = fetch_teams_for_year(selected_year)
                            if teams:                              
                                selected_team= display_team_selection(win, teams)                               
                                if selected_team:
                                    generate_graphs_2(selected_year, selected_team)         
                elif is_click_in_rectangle(click, gr3_button):               
                    years = fetch_years()
                    if years:
                      selected_year = display_year_selection(win, years)
                      plot_shots(selected_year)    
                elif is_click_in_rectangle(click, gr4_button): 

                    Graphsuggest_main()                                     
            except Exception as e:
                print(f"Error occurred: {e}")
                LoginGUI()
                break
    else:        
        LoginGUI()
        
        
def display_year_selection(win, years):
    year_label = create_label(win, "Select Year:", Point(620, 100), 16, "#1E2A39", "bold")
    year_buttons = []

    for idx, year in enumerate(years):
        btn, txt13 = create_button(win, Point(550, 130 + (idx * 40)), Point(750, 170 + (idx * 40)), str(year), "#4682B4", "white")
        year_buttons.append((year, btn, txt13))
    
    close_button = Rectangle(Point(720, 90), Point(740, 110))  
    close_button.setFill("#4682B4")
    close_button.setOutline("#4682B4")
    close_button.draw(win)

    close_text = Text(Point(730, 100), "X")
    close_text.setSize(16)
    close_text.setTextColor("white")
    close_text.draw(win)

    while True:
        click = win.getMouse()

        if is_click_in_rectangle(click, close_button):
            for _, b, c in year_buttons:
                b.undraw()
                c.undraw()
            year_label.undraw()
            close_button.undraw()
            close_text.undraw()
            return None  
        
        for year, btn, vtxt in year_buttons:
            if is_click_in_rectangle(click, btn):
                for _, b, c in year_buttons:
                    b.undraw()
                    c.undraw()
                year_label.undraw()
                close_button.undraw()
                close_text.undraw()
                return year  

def display_team_selection(win, teams):
    team_label = create_label(win, "Select Team:", Point(620, 100), 16, "#1E2A39", "bold")

    columns = 3  
    rows_per_column = 10  

    team_buttons = []
    icon_objects = []  

    for idx, (team_name, icon_filename) in enumerate(teams):
        row = idx % rows_per_column  
        col = idx // rows_per_column  

        x_offset = 550 + col * 250  
        y_offset = 130 + row * 50  

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

    close_button = Rectangle(Point(720, 90), Point(740, 110)) 
    close_button.setFill("#4682B4")
    close_button.setOutline("#4682B4")
    close_button.draw(win)

    close_text = Text(Point(730, 100), "X")
    close_text.setSize(16)
    close_text.setTextColor("white")
    close_text.draw(win)

    while True:
        click_point = win.getMouse()

        if is_click_in_rectangle(click_point, close_button):
            for _, b, c in team_buttons:
                b.undraw()
                c.undraw()
            for icon in icon_objects:
                icon.undraw()
            team_label.undraw()
            close_button.undraw()
            close_text.undraw()
            return None  

        for team_name, btn, txt1 in team_buttons:
            if is_click_in_rectangle(click_point, btn):
                for _, b, c in team_buttons:
                    b.undraw()
                    c.undraw()
                for icon in icon_objects:
                    icon.undraw()
                team_label.undraw()
                close_button.undraw()
                close_text.undraw()
                return team_name  
