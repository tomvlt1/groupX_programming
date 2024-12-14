from graphics import *
from Globals import *
from DataFunctions import *
from graph_1 import *

from FootGameHome import FootGameHomeMain
from Graphsuggest import *
import time



#********FUNCTIONS********

  
def login_user(input1,input2):
    username = input1.getText()  # Get the username from the input field
    password = input2.getText()  # Get the password directly from the input field   
 
    result, vmessage,username, user_id = validate_user(username, password)
    if result:
        setIDUser(user_id)       
        create_dashboard()
        
    else:
        messages(vmessage)
        LoginGUI()
        


def RegisterGUI():
    oldwin=getCurrentWindow()   
    if oldwin:
        oldwin.close()  
    winRegisterGUI = GraphWin("FootViz Registration Page", 1100, 800)
    setCurrentWindow(winRegisterGUI)
    win=getCurrentWindow()    
    win.setBackground("#FFFFFF")  
    left_background = Rectangle(Point(0, 0), Point(500, 800))
    left_background.setFill("#ADEFD1")
    left_background.setOutline("#ADEFD1")
    left_background.draw(win)
    title = create_label(win,"REGISTER",Point(800, 60), 28,"#1E2A39","bold")  
    subtitle= create_label(win,"IT'S COMPLETELY FREE",Point(800, 100), 16,"#1E2A39","normal")  
    drawFootballField(win,Point(30, 100), Point(470, 600))    
    fields = [
        ("FirstName", 140,"First Name"), ("LastName", 190,"Last Name"), ("UserName", 240, "User Name"), ("Password", 290,"Password"),
        ("ShirtNumber", 340, "Shirt Number"), ("PrimaryColor", 390,"Primary Color"), ("SecondaryColor", 430,"Secondary color"), ("DateOfBirth", 470,"Date Of Birth"),
        ("Gender", 520, "Gender"), ("Nationality", 570,"Nationality"), ("FavoriteTeam", 620,"FavoriteTeam")
    ]

    entry_fields = {}
    for label, y,vtext in fields:        
        label_text = create_label(win, vtext,Point(680, y),14,"#1E2A39")
        entry=create_entry(win,Point(900, y), 30,vcolor="#F0F8FF")            
        entry_fields[label] = entry
    submit_button,txt4 = create_button(win, Point(700,650), Point(900,690), "Create Account",  "#2E8B57","white" )
    #back_button,txt5 = create_button(win, Point(700, 700), Point(900, 740), "Back to Login", "#2E8B57","white" )
    back_button,vim= create_image_button(win, Point(500, 0), Point(600, 50), "images/back.png", size=(20, 20), vout="#FFFFFF")
    while True:
        try:
            click = win.getMouse()
             # Check if the submit button is clicked
            if is_click_in_rectangle(click,submit_button):               
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
                result,error=create_user(data)    
                if result:                     
                    LoginGUI() # Go back to the login screen
                    break
                else:
                    messages(error)
                    break
            elif  is_click_in_rectangle(click, back_button):
                LoginGUI() # Go back to the login screen
                break

        except GraphicsError:
            break
        
def AccountGUI(userId):
    oldwin=getCurrentWindow()   
    if oldwin:
        oldwin.close()  
    winAccountGUI = GraphWin("FootViz Account Page", 1100, 800)
    setCurrentWindow(winAccountGUI)
    win=getCurrentWindow()    
    win.setBackground("#FFFFFF")  
    if userId:
    # Fetch existing user data from the database for modification
        user_data = get_user_data(userId)
        if user_data:         
            
            
            fields = [
            ("FirstName", 140,"First Name",user_data[0]), ("LastName", 190,"Last Name",user_data[1]), ("UserName", 240, "User Name",user_data[2]), ("Password", 290,"Password",user_data[3]),
            ("ShirtNumber", 340, "Shirt Number",user_data[4]), ("PrimaryColor", 390,"Primary Color",user_data[5]), ("SecondaryColor", 430,"Secondary color",user_data[6]), ("DateOfBirth", 470,"Date Of Birth",user_data[7]),
            ("Gender", 520, "Gender",user_data[8]), ("Nationality", 570,"Nationality",user_data[9]), ("FavoriteTeam", 620,"FavoriteTeam",user_data[10])
            ]

         
            entry_fields = {}
            for label, y,vtext,defaultvalue in fields:        
                label_text = create_label(win, vtext,Point(680, y),14,"#1E2A39")
                if label=="UserName":
                    create_label(win,defaultvalue,Point(900, y),14,"#1E2A39")
                else:
                    entry=create_entry(win,Point(900, y), 30,vcolor="#F0F8FF")       
                    entry.setText(defaultvalue)
                    entry_fields[label] = entry
    
            left_background = Rectangle(Point(0, 0), Point(500, 800))
            left_background.setFill("#ADEFD1")
            left_background.setOutline("#ADEFD1")
            left_background.draw(win)
            
            drawFootballField(win,Point(30, 100), Point(470, 600))  
            title = create_label(win,"YOUR PROFILE",Point(800, 60), 28,"#1E2A39","bold")  
            vcolorbutton="#2E8B57"
            submit_button,txt6 = create_button(win, Point(700,650), Point(810, 700), "Save",  vcolorbutton,"white" )    
            delete_button,txt7= create_button(win, Point(850, 650), Point(960, 700), "Delete",vcolorbutton,"white" ) 
            back_button,vim= create_image_button(win, Point(0, 0), Point(100, 50), "images/back.png", size=(20, 20), vout="#ADEFD1")
            
            while True:
                try:
                    click = win.getMouse()
                    # Check if the submit button is clicked
                    if is_click_in_rectangle(click,submit_button):               
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
                        result,error=modify_user(int(userId), data)
                        if result:                     
                            create_dashboard() # Go back to the login screen
                            break
                        else:
                            messages(error)
                            create_dashboard() # Go back to the login screen
                            break                          
                    elif  is_click_in_rectangle(click, back_button):
                        create_dashboard() # Go back to the login screen
                        break
                    elif  is_click_in_rectangle(click, delete_button):
                        result,error=delete_user(int(userId)) # Go back to the login screen
                        messages(error)
                        if result:
                            LoginGUI()
                          
                        
                        break                    
                except:
                    LoginGUI() # Go back to the login screen
                    break                    
        else:
            messages(error)
            LoginGUI() # Go back to the login screen

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

    team_buttons = []  # To keep track of the team buttons and clear them when needed
    team_menu_shown = False  # Track if the team menu is shown

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

                    # Fetch years and display selection
                    years = fetch_years()
                    if years:
                        selected_year = display_year_selection(win, years)
                        if selected_year:
                            teams = fetch_teams_for_year(selected_year)
                            if teams:                              
                                selected_team= display_team_selection(win, teams)                               
                                # Generate graph for selected team and year
                                if selected_team:
                                    generate_graphs_1(selected_year, selected_team)     
                elif is_click_in_rectangle(click, gr2_button):
               
                     # Fetch years and display selection
                    years = fetch_years()
                    if years:
                        selected_year = display_year_selection(win, years)
                        if selected_year:
                            teams = fetch_teams_for_year(selected_year)
                            if teams:                              
                                selected_team= display_team_selection(win, teams)                               
                                # Generate graph for selected team and year
                                if selected_team:
                                    generate_graphs_2(selected_year, selected_team)         
                elif is_click_in_rectangle(click, gr3_button):               
                     # Fetch years and display selection
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
    # Label for selecting year
    year_label = create_label(win, "Select Year:", Point(620, 100), 16, "#1E2A39", "bold")
    year_buttons = []

    # Add buttons for each year
    for idx, year in enumerate(years):
        btn, txt13 = create_button(win, Point(550, 130 + (idx * 40)), Point(750, 170 + (idx * 40)), str(year), "#4682B4", "white")
        year_buttons.append((year, btn, txt13))
    
    # Create the "X" to close the selection
    close_button = Rectangle(Point(720, 90), Point(740, 110))  # Position of the "X"
    close_button.setFill("#4682B4")
    close_button.setOutline("#4682B4")
    close_button.draw(win)

    # Create the "X" text inside the button
    close_text = Text(Point(730, 100), "X")
    close_text.setSize(16)
    close_text.setTextColor("white")
    close_text.draw(win)

    # Wait for the user to click
    while True:
        click = win.getMouse()

        # Check if the "X" was clicked
        if is_click_in_rectangle(click, close_button):
            # Undraw the buttons, label, and "X" when closing
            for _, b, c in year_buttons:
                b.undraw()
                c.undraw()
            year_label.undraw()
            close_button.undraw()
            close_text.undraw()
            return None  # Return None if the selection is closed
        
        # Check if a year button was clicked
        for year, btn, vtxt in year_buttons:
            if is_click_in_rectangle(click, btn):
                # Undraw all buttons and the label when a year is selected
                for _, b, c in year_buttons:
                    b.undraw()
                    c.undraw()
                year_label.undraw()
                close_button.undraw()
                close_text.undraw()
                return year  # Return the selected year


# Function to display teams for selection (without pagination)
def display_team_selection(win, teams):
    # Label for selecting a team
    team_label = create_label(win, "Select Team:", Point(620, 100), 16, "#1E2A39", "bold")

    # Number of columns and rows
    columns = 3  # 3 columns
    rows_per_column = 10  # 10 rows per column

    # List to store buttons and icons
    team_buttons = []
    icon_objects = []  # List to store icon objects

    # Create a button for each team and display its icon if available
    for idx, (team_name, icon_filename) in enumerate(teams):
        # Calculate the row and column for the current team
        row = idx % rows_per_column  # Row within the column
        col = idx // rows_per_column  # Column index (0, 1, 2)

        # Calculate the position for the button
        x_offset = 550 + col * 250  # X-axis offset for columns
        y_offset = 130 + row * 50  # Y-axis offset for rows

        # Create the button for the team
        btn, txt1 = create_button(
            win,
            Point(x_offset, y_offset),
            Point(x_offset + 250, y_offset + 50),
            team_name,
            "#4682B4",
            "white",
            size=12
        )
        team_buttons.append((team_name, btn, txt1))  # Add the button to the list

        # Draw the icon if the filename is provided
        if icon_filename:
            # Assume the icon exists if a filename is provided
            icon_path = f"images/{icon_filename}"  # Construct the path for the icon
            icon = Image(Point(x_offset + 30, y_offset + 25), icon_path)  # Position the icon
            icon.draw(win)
            icon_objects.append(icon)

    # Create the "X" to close the team selection
    close_button = Rectangle(Point(720, 90), Point(740, 110))  # Position of the "X"
    close_button.setFill("#4682B4")
    close_button.setOutline("#4682B4")
    close_button.draw(win)

    # Create the "X" text inside the button
    close_text = Text(Point(730, 100), "X")
    close_text.setSize(16)
    close_text.setTextColor("white")
    close_text.draw(win)

    # Wait for the user to click on a team or close the selection
    while True:
        click_point = win.getMouse()

        # Check if the "X" was clicked
        if is_click_in_rectangle(click_point, close_button):
            # Undraw all buttons, icons, and the label when closing
            for _, b, c in team_buttons:
                b.undraw()
                c.undraw()
            for icon in icon_objects:
                icon.undraw()
            team_label.undraw()
            close_button.undraw()
            close_text.undraw()
            return None  # Return None if the selection is closed

        # Check if a team button was clicked
        for team_name, btn, txt1 in team_buttons:
            if is_click_in_rectangle(click_point, btn):
                # Undraw all buttons, icons, and the label when a team is selected
                for _, b, c in team_buttons:
                    b.undraw()
                    c.undraw()
                for icon in icon_objects:
                    icon.undraw()
                team_label.undraw()
                close_button.undraw()
                close_text.undraw()
                return team_name  # Return the selected team

def LoginGUI():
    oldwin=getCurrentWindow()    
    if oldwin:
        oldwin.close()
    winLoginGUI = GraphWin("FootViz Login Page", 800, 500)
    setCurrentWindow(winLoginGUI)
    win=getCurrentWindow()
    win.setBackground("#FFFFFF")
    left_background = Rectangle(Point(0, 0), Point(400, 500))
    left_background.setFill("#F8F9FA")
    left_background.setOutline("#F8F9FA")
    left_background.draw(win)
    title = create_label(win, "FOOTVIZ",Point(200, 50),20,"#2E2E2E","bold")
    subtitle = create_label(win,"Login into your FootViz Account",Point(200, 80), 12,"#6C757D","normal")
    username_label=create_label( win,"Username",Point(130, 180),12,"#6C757D")
    username_field=create_entry(win,Point(200, 210),25,12,vfill="#F0F8FF")
    password_label=create_label( win,"Password",Point(130, 260),12,"#6C757D")
    password_field =create_entry(win,Point(200, 290),25,12,vfill="#F0F8FF")  
    login_button,txt2 = create_button(win, Point(130, 330),Point(270, 370), "Login Now",  "#2E8B57","white",)
    register_button,txt3 = create_button(win, Point(130, 380), Point(270, 420), "Register",  "#2E8B57","white")
    error_message = create_label (win,"",Point(200, 480),12,"#FF6347")
    
    drawFootballField(win,Point(400, 0), Point(800, 500))
    
     # Event loop for login interaction
    while True:
        click_point = win.checkMouse()  # Detect mouse clicks
        # Check if the login button is clicked
        if is_click_in_rectangle(click_point,login_button):
            login_user(username_field,password_field)
            break
        elif is_click_in_rectangle(click_point,register_button):
            RegisterGUI()   
            break       
        
#dashboard  ####################################################################  

def create_window():
    """Create the main application window."""
    userid=getIDUser()
    if  userid:
        oldwin=getCurrentWindow()   
        if oldwin:
            oldwin.close()  
        winHome = GraphWin("Football Dashboard UI", screen_widthHome, screen_heightHome )
        setCurrentWindow(winHome)
        win=getCurrentWindow()  
        win.setBackground(color_rgb(44, 40, 85))    
        return win
    else:
        LoginGUI()
        

def create_sidebar(win):
    """Create the sidebar with navigation buttons."""
    sidebar = Rectangle(Point(0, 0), Point(200, 500))
    sidebar.setFill(color_rgb(31, 27, 58))
    sidebar.draw(win)

    p1=Point(20, 90)
    p2=Point(180, 130)
    
    buttons = []  
    new_button,new_buttontxt =create_button(win,p1, p2, "New Match", color_rgb(28, 195, 170), "white",12)
    buttons.append(new_button)
    back_button,vim= create_image_button(win, Point(0, 0), Point(80, 50), "images/back.png", size=(20, 20), vout=color_rgb(28, 195, 170))
    buttons.append(back_button)
   
    y_offset = 90
    p1=Point(p1.getX(), p1.getY()+ y_offset)
    p2=Point(p2.getX(), p2.getY()+ y_offset)
    button_titles = [("Import Dataset","btoImport"), ("Choose Dataset","btoChoose"), ("Visualize","btoVisualize"),("Profile","btoProfile")]
   
    for btnlabel,btnid in button_titles:        
        btnname = btnid   
        btntxt = f"{btnid}txt"          
        btnname,btntxt =create_button(win,p1,p2,  btnlabel, color_rgb(44, 40, 85), "white",12)           
        y_offset = 50
        p1=Point(p1.getX(), p1.getY()+ y_offset)
        p2=Point(p2.getX(), p2.getY()+ y_offset)
        buttons.append((btnname))        
        
    return buttons

def RefreshButton(x, y, win):
    """Create a refresh button."""
    p1=Point(x - 25, y - 25)
    p2= Point(x + 25, y + 25)
    color1=color_rgb(255, 255, 255)
    refreshButton, refresh_icon =  create_image_button(win, p1, p2,"images/refresh1.png", size=(30, 30),vout=color1)
  
    return refreshButton

def PreviewButton(x, y, win):
    p1=Point(x - 100, y - 40)
    p2= Point(x + 100, y + 40)
    preview_button,preview_text =create_button(win,p1, p2,  "Preview Match", color_rgb(0, 128, 255), "white",14)
    lock_text = Text(Point(x, y + 20), "Everything will be locked!")
    lock_text.setSize(10)
    lock_text.setTextColor("white")
    lock_text.draw(win)

    return preview_button, preview_text, lock_text


def WarningMessage(x, y, win):
    """Create a warning message inside the match box."""
    warning = Text(Point(x, y), "This will lock the dashboard until the game ends (30 - 60 seconds).")
    warning.setSize(14)
    warning.setTextColor("red")
    warning.setStyle("bold")
    warning.draw(win)
    return warning


def create_overview_section(win):
    """Create the initial overview section."""
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
    """Update the overview section with new facts."""
    for i, fact in enumerate(facts):
        overview_boxes[i].setFill("white")  
        for item in win.items[:]:
            if isinstance(item, Text):
                if overview_boxes[i].getP1().x <= item.getAnchor().x <= overview_boxes[i].getP2().x and \
                        overview_boxes[i].getP1().y <= item.getAnchor().y <= overview_boxes[i].getP2().y:
                    item.undraw()

        # Extract the description, match info, and value
        try:
            description, match_info, value = fact.split("\n")
        except ValueError:
            description, match_info, value = "N/A", "N/A", "N/A"

        # Always prepend "Match with most -" for consistency
        title_line1 = "Match with most -"
        title_line2 = description

        # Draw the updated fact in the box
        title_text1 = Text(Point(overview_boxes[i].getP1().x + 90, overview_boxes[i].getP1().y + 20), title_line1)
        title_text2 = Text(Point(overview_boxes[i].getP1().x + 90, overview_boxes[i].getP1().y + 35), title_line2)
        match_text = Text(Point(overview_boxes[i].getP1().x + 90, overview_boxes[i].getP1().y + 55), match_info)
        value_text = Text(Point(overview_boxes[i].getP1().x + 90, overview_boxes[i].getP1().y + 75), value)

        for text in [title_text1, title_text2, match_text, value_text]:
            text.setTextColor(color_rgb(44, 40, 85))
            text.setSize(10)
            text.draw(win)

def create_mini_game_area(win):
    """Create the mini-game area."""
    mini_game_left = 220
    mini_game_top = 140
    mini_game_right = 880
    mini_game_bottom = 480

    mini_game_area = Rectangle(Point(mini_game_left, mini_game_top), Point(mini_game_right, mini_game_bottom))
    mini_game_area.setFill(color_rgb(224, 224, 224))
    mini_game_area.draw(win)

    return mini_game_area, mini_game_left, mini_game_top, mini_game_right, mini_game_bottom


def create_dashboard():
    """Create the main dashboard."""
    win = create_window()
    buttons=create_sidebar(win)
    overview_boxes = create_overview_section(win)
    refresh_button = RefreshButton(850, 60, win)  # Refresh button

    mini_game_area, left, top, right, bottom = create_mini_game_area(win)
    preview_button, preview_text, lock_message = PreviewButton((left + right) // 2, (top + bottom) // 2, win)
    warning = WarningMessage((left + right) // 2, (top + bottom) // 2 + 60, win)

    mini_game_active = False  # Track if the mini-game is active
          
    while True:
        click = win.checkMouse()  # Non-blocking mouse click check

        if click:          

            # Check if preview button is clicked
            
            if not mini_game_active and  is_click_in_rectangle(click,preview_button):
                print("Preview button clicked.")
                mini_game_active = True

                preview_button.undraw()
                preview_text.undraw()
                lock_message.undraw()
                warning.undraw()

                # Start the mini-game
                FootGameHomeMain(win)

                preview_button.draw(win)
                preview_text.draw(win)
                lock_message.draw(win)
                warning.draw(win)
                mini_game_active = False

            # Check if refresh button is clicked
            if  is_click_in_rectangle(click,refresh_button):
                print("Refresh button clicked.")
                facts = GetRandomFacts(3)
                update_overview_section(win, overview_boxes, facts)
            
            elif  is_click_in_rectangle(click,buttons[2]): 
                userId=getIDUser()
                # Create a button to trigger the file selection dialog
                
                if userId:
                    vectorobjects = show_import_message(win, Point(520, 70))            
                    if vectorobjects:
                        while True:                                 
                            click_point = win.getMouse()   
                            if is_click_in_rectangle(click_point, vectorobjects[4]):
                                for obj in vectorobjects:
                                    obj.undraw()
                                file_path = "files/file_to_import.csv"
                                result1, verror = check_csv_file(file_path)  
                                                              
                                if result1:
                                    result, last_insert_id, vmessage = create_load_record(userId, file_path)
                                   
                                    if result:  
                                        result1, vmessage = import_csv_to_database(file_path, int(userId), int(last_insert_id))
                                        if result1:                                           
                                            messages(vmessage)
                                            break            
                                        else:
                                            messages(vmessage)
                                            break
                                    else:
                                        messages(verror)
                                        break
                            elif is_click_in_rectangle(click_point, vectorobjects[5]):
                                for obj in vectorobjects:
                                    obj.undraw()
                                break   
                    
            elif  is_click_in_rectangle(click,buttons[4]):   
                iduser= getIDUser()
                if  iduser:   
                    statistics(iduser)    
            elif  is_click_in_rectangle(click,buttons[5]):   
                iduser= getIDUser()
                if iduser:           
                    AccountGUI(iduser)   
            elif  is_click_in_rectangle(click,buttons[1]): 
                LoginGUI()  
    
        time.sleep(0.05)  

    win.close()
    

def Graphsuggest_main():
    while True:
        selected_variables = VariableSelection()

        if selected_variables:
            while True:  # Add an inner loop for navigation between variable and graph selection
                selected_graph, selected_variables = GraphOptions(selected_variables)

                if selected_graph is None:  # Back arrow clicked
                    break  # Go back to the variable selection screen

                # Generate and display the selected graph
                if selected_graph == "Histogram":
                    Histogram(selected_variables[0], "graph.png")
                    title_text = f"Histogram of {selected_variables[0]}"
                elif selected_graph == "Boxplot":
                    Boxplot(selected_variables[0], "graph.png")
                    title_text = f"Box Plot of {selected_variables[0]}"
                elif selected_graph == "Bar Chart":
                    Barchart(selected_variables[0], "graph.png")
                    title_text = f"Bar Chart of {selected_variables[0]}"
                elif selected_graph == "Pie Chart":
                    Piechart(selected_variables[0], "graph.png")
                    title_text = f"Pie Chart of {selected_variables[0]}"
                elif selected_graph == "Scatter Plot":
                    ScatterPlot(selected_variables[0], selected_variables[1], "graph.png")
                    title_text = f"Scatter Plot: {selected_variables[0]} vs {selected_variables[1]}"
                elif selected_graph == "Line Chart":
                    LineChart(selected_variables[0], selected_variables[1], "graph.png")
                    title_text = f"Line Chart: {selected_variables[0]} vs {selected_variables[1]}"
                elif selected_graph == "Stacked Bar Chart":
                    StackedBarChart(selected_variables[0], selected_variables[1], "graph.png")
                    title_text = f"Stacked Bar Chart: {selected_variables[0]} vs {selected_variables[1]}"
                elif selected_graph == "Heatmap":
                    Heatmap(selected_variables[0], selected_variables[1], "graph.png")
                    title_text = f"Heatmap: {selected_variables[0]} vs {selected_variables[1]}"
                elif selected_graph == "3D Scatterplot":
                    ThreeDScatterplot(selected_variables[0], selected_variables[1],selected_variables[2],"graph.png",data=data)
                    title_text = f"3D Scatter Plot for {selected_variables[0]} vs {selected_variables[1]} vs {selected_variables[2]} "
                elif selected_graph == "Heatmap With Two Numericals":
                    HeatmapWithTwoNumericals(selected_variables[0], selected_variables[1], selected_variables[2], "graph.png", data=data, agg_func='mean')
                    title_text = f"Heatmap: {selected_variables[0]} vs {selected_variables[1]} vs {selected_variables[2]}"

                else:
                    print("Graph type not implemented!")

                if DisplayGraph("graph.png", title_text):
                    continue  # User clicked back in the graph viewer, return to graph options
                else:
                    break


def select_file():
    # Open a file selection dialog
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("Text Files", "*.csv"),  # Filter by file type
                   ("All Files", "*.*"))
    )
    
    if file_path:  # If a file is selected
       return (file_path)
    else:
       return (None)


if __name__ == "__main__":
    create_dashboard()
