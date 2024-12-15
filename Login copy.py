from graphics import *
from Globals import *
from DataFunctions import *
from Dashboard import create_dashboard
import time
from jersey import draw_custom_jersey
def login_user(input1, input2):
    username = input1.getText()  # Get the username from the input field
    password = input2.getText()  # Get the password from the input field   
 
    result, vmessage, username, user_id = validate_user(username, password)
    if result:
        setIDUser(user_id)       
        create_dashboard()  # We'll import this from Dashboard once we're in main.py
    else:
        messages(vmessage)
        LoginGUI()

def RegisterGUI():
    oldwin = getCurrentWindow()   
    if oldwin:
        oldwin.close()  

    winRegisterGUI = GraphWin("FootViz Registration Page", 1100, 800)
    setCurrentWindow(winRegisterGUI)
    win = getCurrentWindow()    
    win.setBackground("#FFFFFF")  

    left_background = Rectangle(Point(0, 0), Point(500, 800))
    left_background.setFill("#ADEFD1")
    left_background.setOutline("#ADEFD1")
    left_background.draw(win)

    title = create_label(win, "REGISTER", Point(800, 60), 28, "#1E2A39", "bold")  
    subtitle = create_label(win, "IT'S COMPLETELY FREE", Point(800, 100), 16, "#1E2A39", "normal")  

    draw_custom_jersey(win,Point(30, 100), Point(470, 600),"BASE" ,"Username","0")

    fields = [
        ("FirstName", 140, "First Name"),
        ("LastName", 190, "Last Name"),
        ("UserName", 240, "User Name"),
        ("Password", 290, "Password"),
        ("ShirtNumber", 340, "Shirt Number"),
        ("PrimaryColor", 390, "Primary Color"),
        ("SecondaryColor", 430, "Secondary Color"),
        ("DateOfBirth", 470, "Date Of Birth"),
        ("Gender", 520, "Gender"),
        ("Nationality", 570, "Nationality"),
        ("FavoriteTeam", 620, "FavoriteTeam")
    ]

    entry_fields = {}
    for label, y, vtext in fields:
        create_label(win, vtext, Point(680, y), 14, "#1E2A39")
        entry = create_entry(win, Point(900, y), 30, vcolor="#F0F8FF")
        entry_fields[label] = entry

    submit_button, txt4 = create_button(win, Point(700, 650), Point(900, 690), "Create Account", "#2E8B57", "white")
    back_button, vim = create_image_button(win, Point(500, 0), Point(600, 50), "images/back.png", size=(20, 20), vout="#FFFFFF")

    while True:
        try:
            click = win.getMouse()
            if is_click_in_rectangle(click, submit_button):
                data = [
                    entry_fields["FirstName"].getText(),
                    entry_fields["LastName"].getText(),
                    entry_fields["UserName"].getText(),
                    entry_fields["Password"].getText(),
                    entry_fields["ShirtNumber"].getText(),
                    entry_fields["PrimaryColor"].getText(),
                    entry_fields["SecondaryColor"].getText(),
                    entry_fields["DateOfBirth"].getText(),
                    entry_fields["Gender"].getText(),
                    entry_fields["Nationality"].getText(),
                    entry_fields["FavoriteTeam"].getText()
                ]
                result, error = create_user(data)
                if result:
                    LoginGUI()
                    break
                else:
                    messages(error)
                    break

            elif is_click_in_rectangle(click, back_button):
                LoginGUI()
                break

        except GraphicsError:
            break

def AccountGUI(userId):
    oldwin = getCurrentWindow()
    if oldwin:
        oldwin.close()

    winAccountGUI = GraphWin("FootViz Account Page", 1100, 800)
    setCurrentWindow(winAccountGUI)
    win = getCurrentWindow()
    win.setBackground("#FFFFFF")

    if userId:
        user_data = get_user_data(userId)
        if user_data:
            fields = [
                ("FirstName", 140, "First Name", user_data[0]),
                ("LastName", 190, "Last Name", user_data[1]),
                ("UserName", 240, "User Name", user_data[2]),
                ("Password", 290, "Password", user_data[3]),
                ("ShirtNumber", 340, "Shirt Number", user_data[4]),
                ("PrimaryColor", 390, "Primary Color", user_data[5]),
                ("SecondaryColor", 430, "Secondary color", user_data[6]),
                ("DateOfBirth", 470, "Date Of Birth", user_data[7]),
                ("Gender", 520, "Gender", user_data[8]),
                ("Nationality", 570, "Nationality", user_data[9]),
                ("FavoriteTeam", 620, "FavoriteTeam", user_data[10])
            ]

            entry_fields = {}
            for label, y, vtext, defaultvalue in fields:
                create_label(win, vtext, Point(680, y), 14, "#1E2A39")
                if label == "UserName":
                    create_label(win, defaultvalue, Point(900, y), 14, "#1E2A39")
                else:
                    entry = create_entry(win, Point(900, y), 30, vcolor="#F0F8FF")
                    entry.setText(defaultvalue)
                    entry_fields[label] = entry

            left_background = Rectangle(Point(0, 0), Point(500, 800))
            left_background.setFill("#ADEFD1")
            left_background.setOutline("#ADEFD1")
            left_background.draw(win)
            draw_custom_jersey(win,Point(30, 100), Point(470, 600), user_data[10].upper, user_data[2], user_data[4])
            title = create_label(win, "YOUR PROFILE", Point(800, 60), 28, "#1E2A39", "bold")
            vcolorbutton = "#2E8B57"
            submit_button, txt6 = create_button(win, Point(700, 650), Point(810, 700), "Save", vcolorbutton, "white")
            delete_button, txt7 = create_button(win, Point(850, 650), Point(960, 700), "Delete", vcolorbutton, "white")
            back_button, vim = create_image_button(win, Point(0, 0), Point(100, 50), "images/back.png", size=(20, 20), vout="#ADEFD1")

            while True:
                try:
                    click = win.getMouse()
                    if is_click_in_rectangle(click, submit_button):
                        data = [
                            entry_fields["FirstName"].getText(),
                            entry_fields["LastName"].getText(),
                            user_data[2],
                            entry_fields["Password"].getText(),
                            entry_fields["ShirtNumber"].getText(),
                            entry_fields["PrimaryColor"].getText(),
                            entry_fields["SecondaryColor"].getText(),
                            entry_fields["DateOfBirth"].getText(),
                            entry_fields["Gender"].getText(),
                            entry_fields["Nationality"].getText(),
                            entry_fields["FavoriteTeam"].getText()
                        ]
                        result, error = modify_user(int(userId), data)
                        if result:
                            create_dashboard() 
                            break
                        else:
                            messages(error)
                            create_dashboard()
                            break

                    elif is_click_in_rectangle(click, back_button):
                        create_dashboard()
                        break

                    elif is_click_in_rectangle(click, delete_button):
                        result, error = delete_user(int(userId))
                        messages(error)
                        if result:
                            LoginGUI()
                        break

                except:
                    LoginGUI()
                    break
        else:
            messages("Error retrieving user data.")
            LoginGUI()
    else:
        LoginGUI()

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

    drawFootballField(win, Point(550, 150), Point(950, 700))

    title = create_label(win, "STATISTICS", Point(250, 60), 24, "#1E2A39", "bold")
    vcolorbutton = "#2E8B57"

    if userId:
        gr1_button, txt11 = create_button(win, Point(100, 270), Point(350, 320), "Team Performance", vcolorbutton, "white")
        gr2_button, txt111 = create_button(win, Point(100, 330), Point(350, 380), "Possession vs effectiveness", vcolorbutton, "white")
        gr3_button, txt112 = create_button(win, Point(100, 390), Point(350, 440), "Shooting Statistics", vcolorbutton, "white")
        gr4_button, txt113 = create_button(win, Point(100, 450), Point(350, 480), "Dynamics graphs", vcolorbutton, "white")
        back_button, vim = create_image_button(win, Point(0, 0), Point(100, 50), "images/back.png", size=(20, 20), vout="#ADEFD1")

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
                                selected_team = display_team_selection(win, teams)
                                if selected_team:
                                    generate_graphs_1(selected_year, selected_team)

                elif is_click_in_rectangle(click, gr2_button):
                    years = fetch_years()
                    if years:
                        selected_year = display_year_selection(win, years)
                        if selected_year:
                            teams = fetch_teams_for_year(selected_year)
                            if teams:
                                selected_team = display_team_selection(win, teams)
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

def LoginGUI():
    oldwin = getCurrentWindow()
    if oldwin:
        oldwin.close()

    winLoginGUI = GraphWin("FootViz Login Page", 800, 500)
    setCurrentWindow(winLoginGUI)
    win = getCurrentWindow()
    win.setBackground("#FFFFFF")

    left_background = Rectangle(Point(0, 0), Point(400, 500))
    left_background.setFill("#F8F9FA")
    left_background.setOutline("#F8F9FA")
    left_background.draw(win)

    title = create_label(win, "FOOTVIZ", Point(200, 50), 20, "#2E2E2E", "bold")
    subtitle = create_label(win, "Login into your FootViz Account", Point(200, 80), 12, "#6C757D", "normal")

    username_label = create_label(win, "Username", Point(130, 180), 12, "#6C757D")
    username_field = create_entry(win, Point(200, 210), 25, 12, vfill="#F0F8FF")

    password_label = create_label(win, "Password", Point(130, 260), 12, "#6C757D")
    password_field = create_entry(win, Point(200, 290), 25, 12, vfill="#F0F8FF")

    login_button, txt2 = create_button(win, Point(130, 330), Point(270, 370), "Login Now", "#2E8B57", "white")
    register_button, txt3 = create_button(win, Point(130, 380), Point(270, 420), "Register", "#2E8B57", "white")

    error_message = create_label(win, "", Point(200, 480), 12, "#FF6347")

    drawFootballField(win, Point(400, 0), Point(800, 500))

    while True:
        click_point = win.checkMouse()
        if is_click_in_rectangle(click_point, login_button):
            login_user(username_field, password_field)
            break
        elif is_click_in_rectangle(click_point, register_button):
            RegisterGUI()
            break
