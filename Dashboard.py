# Dashboard.py

from graphics import *
from Globals import *
from DataFunctions import *
from FootGameHome import FootGameHomeMain
from GetRandomStats import GetRandomFacts, GetColumnNames
from FootClick import run_footclick
from headsoccer import run_headsoccer
from FileSelect import file_selector
from ChooseDataset import dataset_selector
from ChooseYear import display_year_selection
from ChooseTeam import display_team_selection
from filter import main as filtermain
from main_statistics import *
import time
(screen_width, screen_height, screen_widthHome, screen_heightHome)=screen()
(colorblueBac, colorvlueButtons, colorvlueButtons1, colorgreen, colorcream)=color()

def create_window():
    
    from Login import LoginGUI 
    userid = getIDUser()
    
    if userid:
        oldwin = getCurrentWindow()
        if oldwin:
            oldwin.close()
        winHome = GraphWin("Football Dashboard UI", screen_width, screen_height)
        setCurrentWindow(winHome)
        win = getCurrentWindow()
        win.setBackground(color_rgb(44, 40, 85))
        return win
    else:
        win.close()
        LoginGUI()

def create_sidebar(win):
    sidebar = Rectangle(Point(0, 0), Point(200, 500))
    sidebar.setFill(color_rgb(31, 27, 58))
    sidebar.draw(win)

    p1 = Point(20, 40)
    p2 = Point(180, 80)

    buttons = {}


    back_button, vim = create_image_button(win, Point(0, 0), Point(80, 50), "images/back3.png",
                                           size=(20, 20), vout=colorblueBac)
    buttons["Back"] = back_button

    y_offset = 90
    p1 = Point(p1.getX(), p1.getY() + y_offset)
    p2 = Point(p2.getX(), p2.getY() + y_offset)
    button_titles = [("Import Dataset", "btoImport"),
                     ("Choose Dataset", "btoChoose")]

    for btnlabel, btnid in button_titles:
        btn, txt = create_button(win, p1, p2, btnlabel, colorvlueButtons, colorcream, size=12)
        buttons[btnlabel] = btn
        y_offset = 50
        p1 = Point(p1.getX(), p1.getY() + y_offset)
        p2 = Point(p2.getX(), p2.getY() + y_offset)

    # Now add the new three buttons
    extra_titles = [("FootClick Game", "footclick"),
                    ("HeadSoccer Game", "headsoccer"),
                    ("Main statistics", "btoMainstatistics"),
                    ("Visualize Data", "visualize"),("Profile", "btoProfile")]  
    for btnlabel, btnid in extra_titles:
        btn, txt = create_button(win, p1, p2, btnlabel, colorvlueButtons, colorcream, size=12)
        buttons[btnlabel] = btn
        y_offset = 50
        p1 = Point(p1.getX(), p1.getY() + y_offset)
        p2 = Point(p2.getX(), p2.getY() + y_offset)

    return buttons

def RefreshButton(x, y, win):
    p1 = Point(x - 25, y - 25)
    p2 = Point(x + 25, y + 25)
    color1 = color_rgb(255, 255, 255)
    refreshButton, refresh_icon = create_image_button(win, p1, p2, "images/refresh1.png", size=(30, 30), vout=color1)
    return refreshButton

def PreviewButton(x, y, win):
    p1 = Point(x - 100, y - 40)
    p2 = Point(x + 100, y + 40)
    preview_button, preview_text = create_button(win, p1, p2, "Preview Match", color_rgb(0, 128, 255), "white", size=14)
    lock_text = Text(Point(x, y + 20), "Everything will be locked!")
    lock_text.setSize(10)
    lock_text.setTextColor("white")
    lock_text.draw(win)
    return preview_button, preview_text, lock_text

def WarningMessage(x, y, win):
    warning = Text(Point(x, y), "This will lock the dashboard until the game ends (30 - 60 seconds).")
    warning.setSize(14)
    warning.setTextColor("red")
    warning.setStyle("bold")
    warning.draw(win)
    return warning

def create_overview_section(win):
    overview_boxes = []
    overview_y_start = 20
    x_offset = 220

    for _ in range(3):
        overview_box = Rectangle(Point(x_offset, overview_y_start), Point(x_offset + 180, overview_y_start + 100))
        overview_box.setFill("white")
        overview_box.draw(win)
        overview_boxes.append(overview_box)
        x_offset += 200

    facts = GetRandomFacts(3)
    update_overview_section(win, overview_boxes, facts)
    return overview_boxes

def update_overview_section(win, overview_boxes, facts):
    for i, fact in enumerate(facts):
        overview_boxes[i].setFill("white")
        for item in win.items[:]:
            if isinstance(item, Text):
                if (overview_boxes[i].getP1().x <= item.getAnchor().x <= overview_boxes[i].getP2().x and
                        overview_boxes[i].getP1().y <= item.getAnchor().y <= overview_boxes[i].getP2().y):
                    item.undraw()

        # facts are returned in the form "description\nHomeTeam - AwayTeam\nColumn: value"
        try:
            description, match_info, value = fact.split("\n")
        except ValueError:
            description, match_info, value = "N/A", "N/A", "N/A"

        title_line1 = "Match with most -"
        title_line2 = description

        title_text1 = Text(Point(overview_boxes[i].getP1().x + 90, overview_boxes[i].getP1().y + 20), title_line1)
        title_text2 = Text(Point(overview_boxes[i].getP1().x + 90, overview_boxes[i].getP1().y + 35), title_line2)
        match_text = Text(Point(overview_boxes[i].getP1().x + 90, overview_boxes[i].getP1().y + 55), match_info)
        value_text = Text(Point(overview_boxes[i].getP1().x + 90, overview_boxes[i].getP1().y + 75), value)

        for text_obj in [title_text1, title_text2, match_text, value_text]:
            text_obj.setTextColor(color_rgb(44, 40, 85))
            text_obj.setSize(10)
            text_obj.draw(win)

def create_mini_game_area(win):
    mini_game_left = 220
    mini_game_top = 140
    mini_game_right = 880
    mini_game_bottom = 480

    mini_game_area = Rectangle(Point(mini_game_left, mini_game_top), Point(mini_game_right, mini_game_bottom))
    mini_game_area.setFill(color_rgb(224, 224, 224))
    mini_game_area.draw(win)

    return mini_game_area, mini_game_left, mini_game_top, mini_game_right, mini_game_bottom


def statistics(userId):   
    from Login import LoginGUI 
    oldwin = getCurrentWindow()   
    if oldwin:
        oldwin.close()  
    winStatistics = GraphWin("Statistics Page", screen_widthHome, screen_heightHome)
    setCurrentWindow(winStatistics)
    win = getCurrentWindow()    
    win.setBackground(colorcream) 
    left_background = Rectangle(Point(0, 0), Point(400, 500))
    left_background.setFill(colorblueBac)
    left_background.setOutline(colorblueBac)
    left_background.draw(win)
    
    drawFootballField(win,Point(400, 0), Point(800, 500)) 
    title = create_label(win, "MAIN STATISTICS",Point(200, 50),20,colorcream,"bold")
 

    team_buttons = []  
    team_menu_shown = False 

    if userId:   
        gr1_button,txt11 = create_button(win, Point(80, 100), Point(330, 150), "Team Performance", colorvlueButtons,colorcream)
        gr2_button,txt111 = create_button(win, Point(80, 160), Point(330, 210), "Possession vs effectiveness", colorvlueButtons,colorcream)
        gr3_button,txt112 = create_button(win, Point(80, 220), Point(330, 270), "Shooting Statistics", colorvlueButtons,colorcream)
        
        back_button, vim = create_image_button(win, Point(0, 0), Point(80, 50), "images/back3.png",size=(20, 20), vout= colorblueBac)
   
        while True:
            try:
                click = win.getMouse()

                if is_click_in_rectangle(click, back_button):
                    win.close()
                    create_dashboard()
                    break
                elif is_click_in_rectangle(click, gr1_button):                  

                       selected_year = display_year_selection()
                       if selected_year is not None:   
                            selected_team= display_team_selection(selected_year)                               
                            
                            if selected_team:
                                generate_graphs_1(selected_year, selected_team)     
                elif is_click_in_rectangle(click, gr2_button):
                        selected_year = display_year_selection()
                        if selected_year is not None:
                            selected_team= display_team_selection(selected_year)                               
                            
                            if selected_team:
                                generate_graphs_2(selected_year, selected_team)         
                elif is_click_in_rectangle(click, gr3_button):               
                     
                    selected_year = display_year_selection()
                    if selected_year is not None:
                        plot_shots(selected_year)    
                                   
            except Exception as e:
                print(f"Error occurred: {e}")
                win.close()
                create_dashboard()
                break
    else: 
        win.close()       
        LoginGUI()
       
def display_files_selection(win, vfiles):
    # Label for selecting year
    files_label = create_label(win, "Select file:", Point(250, 150), 16, "#1E2A39", "bold")
    files_buttons = []
    idx=1
  
    for i in range(len(vfiles)):
        idload,vfile, vdata = vfiles[i]
        btn, txt13 = create_button(win, Point(200, 130 + (idx * 40)), Point(750, 170 + (idx * 40)), str(vfile + ' ' + str(vdata)), "#4682B4", "white",size=9)
        idx+=1
        files_buttons.append((idload, btn, txt13))
    
    close_button = Rectangle(Point(330, 140), Point(350,160)) 
    close_button.setFill("#4682B4")
    close_button.setOutline("#4682B4")
    close_button.draw(win)

    close_text = Text(Point(340, 150), "X")
    close_text.setSize(16)
    close_text.setTextColor("white")
    close_text.draw(win)

    # Wait for the user to click
    while True:
        click = win.getMouse()

        if is_click_in_rectangle(click, close_button):
            for _, b, c in files_buttons:
                b.undraw()
                c.undraw()
            files_label.undraw()
            close_button.undraw()
            close_text.undraw()
            return None  
        
        for idload, btn, vtxt in files_buttons:
            if is_click_in_rectangle(click, btn):
                for _, b, c in files_buttons:
                    b.undraw()
                    c.undraw()
                files_label.undraw()
                close_button.undraw()
                close_text.undraw()
                return idload 


def create_dashboard():
    from Login import LoginGUI, AccountGUI  
    win = create_window()
    if not win:
        return

    buttons = create_sidebar(win)  
    overview_boxes = create_overview_section(win)
    refresh_button = RefreshButton(850, 60, win)

    mini_game_area, left, top, right, bottom = create_mini_game_area(win)
    preview_button, preview_text, lock_message = PreviewButton((left + right) // 2, (top + bottom) // 2, win)
    warning = WarningMessage((left + right) // 2, (top + bottom) // 2 + 60, win)

    mini_game_active = False

    while True:
        click = win.checkMouse()
        if click:
            if not mini_game_active and is_click_in_rectangle(click, preview_button):
                mini_game_active = True
                preview_button.undraw()
                preview_text.undraw()
                lock_message.undraw()
                warning.undraw()

                FootGameHomeMain(win)

                preview_button.draw(win)
                preview_text.draw(win)
                lock_message.draw(win)
                warning.draw(win)
                mini_game_active = False

            elif is_click_in_rectangle(click, refresh_button):
                new_facts = GetRandomFacts(3)
                update_overview_section(win, overview_boxes, new_facts)

            elif is_click_in_rectangle(click, buttons.get("Import Dataset")):
                userId = getIDUser()
                if userId:
                    try:
                        selected_file, selected_fileName= file_selector("target_folder",500,400)  
                        print(selected_file)
                        result1, verror = check_csv_file(selected_file)
                        if result1:
                            result, last_insert_id, vmessage = create_load_record(userId,selected_fileName)
                            if result:
                                result1, vmessage = import_csv_to_database(selected_file, int(userId), int(last_insert_id))
                                if result1:
                                    messages(vmessage)
                                else:
                                    messages(vmessage)
                            else:
                                messages(verror)
                        else:
                            messages("Invalid CSV file.")
                    except FileNotFoundError as e:
                        messages(str(e))
                    except Exception as e:
                        messages(f"An error occurred: {str(e)}")


            elif is_click_in_rectangle(click, buttons.get("Visualize Data")):
                if getDataset() =="":
                    messages("Select Dataset")
                else:
                    result_df = filtermain() 
                    if result_df is not None:
                        print("Filtered DataFrame:", result_df)

            elif is_click_in_rectangle(click, buttons.get("Choose Dataset")):
                userId = getIDUser()
                if userId:
                    idload,vtxt=dataset_selector(320,600)
                    setDataset(idload) 
                    messages(f'your dataset for the study will be {vtxt}') 
                   
            elif is_click_in_rectangle(click, buttons.get("FootClick Game")):
                run_footclick()
            elif is_click_in_rectangle(click, buttons.get("HeadSoccer Game")):
                run_headsoccer()
            elif is_click_in_rectangle(click, buttons.get("Back")):
                session.clear
                win.close()
                LoginGUI()
            elif is_click_in_rectangle(click, buttons.get("Main statistics")):
                if getDataset() =="":
                    messages("Select Dataset")
                else:
                    statistics(getIDUser())
            elif is_click_in_rectangle(click, buttons.get("Profile")):
                AccountGUI(getIDUser())       
            

        time.sleep(0.05)

    win.close()
