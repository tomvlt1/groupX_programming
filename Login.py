from graphics import *
from Globals import *
from DataFunctions import *
from jersey import draw_custom_jersey
from Dashboard import create_dashboard


  
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
    teams = {
        "MÁLAGA": {"primary": "#4AADD4", "secondary": "#FFFFFF"},
        "SEVILLA FC": {"primary": "#D71A28", "secondary": "#FFFFFF"},
        "GRANADA": {"primary": "#E30613", "secondary": "#FFFFFF"},
        "ALMERÍA": {"primary": "#FF0000", "secondary": "#FFFFFF"},
        "EIBAR": {"primary": "#800000", "secondary": "#0044FF"},
        "BARCELONA": {"primary": "#A50044", "secondary": "#004D98"},
        "CELTA": {"primary": "#C0E6F1", "secondary": "#FFFFFF"},
        "LEVANTE": {"primary": "#003DA5", "secondary": "#ED1C24"},
        "REAL MADRID": {"primary": "#FFFFFF", "secondary": "#FEBE10"},
        "RAYO VALLECANO": {"primary": "#FFFFFF", "secondary": "#FF0000"},
        "GETAFE": {"primary": "#003DA5", "secondary": "#FFFFFF"},
        "VALENCIA": {"primary": "#FFFFFF", "secondary": "#FF8800"},
        "ATHLETIC": {"primary": "#D6001C", "secondary": "#FFFFFF"},
        "CÓRDOBA": {"primary": "#339933", "secondary": "#FFFFFF"},
        "ATLETICO MADRID": {"primary": "#D81920", "secondary": "#FFFFFF"},
        "ESPANYOL": {"primary": "#005CB9", "secondary": "#FFFFFF"},
        "VILLARREAL": {"primary": "#FFEF00", "secondary": "#005BAC"},
        "DEPORTIVO": {"primary": "#0071C5", "secondary": "#FFFFFF"},
        "REAL SOCIEDAD": {"primary": "#005BAC", "secondary": "#FFFFFF"},
        "ELCHE": {"primary": "#008542", "secondary": "#FFFFFF"},
        "GIJÓN": {"primary": "#D6001C", "secondary": "#FFFFFF"},
        "REAL BETIS": {"primary": "#008542", "secondary": "#FFFFFF"},
        "LAS PALMAS": {"primary": "#FFD700", "secondary": "#0070C0"},
        "OSASUNA": {"primary": "#D6001C", "secondary": "#001E62"},
        "LEGANÉS": {"primary": "#0044FF", "secondary": "#FFFFFF"},
        "ALAVÉS": {"primary": "#0044FF", "secondary": "#FFFFFF"},
        "GIRONA": {"primary": "#D6001C", "secondary": "#FFFFFF"},
        "VALLADOLID": {"primary": "#4A2C81", "secondary": "#FFFFFF"},
        "HUESCA": {"primary": "#900C3F", "secondary": "#0044FF"},
        "MALLORCA": {"primary": "#D6001C", "secondary": "#000000"},
        "CÁDIZ CF": {"primary": "#FFD700", "secondary": "#0000FF"}
    }

    team_names = list(teams.keys())
    
    oldwin = getCurrentWindow()
    if oldwin:
        oldwin.close()

    winRegisterGUI = GraphWin("FootViz Registration Page", screen_widthHome, screen_heightHome)
    setCurrentWindow(winRegisterGUI)
    win = getCurrentWindow()
    win.setBackground(colorcream)


    title = create_label(win, "REGISTER", Point(550, 30), 20, colorblueBac, "bold")
    subtitle = create_label(win, "Return to your profile from the home page to see your customized shirt!!!", Point(550, 60), 12, colorblueBac, "normal")

    left_background, image_left_background = create_image_button(win, Point(0, 0), Point(350, 500), "images/BackgroundRegister1.png", size=(350, 500), vout=colorblueBac)
    jersey_objects = []
    jersey_objects = draw_custom_jersey(win, Point(100, 180), Point(250, 370), "base", "FOOTVIZ", "0", jersey_objects)

    fields = [
        ("FirstName", 100, "First Name"),
        ("LastName", 140, "Last Name"),
        ("UserName", 180, "User Name"),
        ("Password", 220, "Password"),
        ("ShirtNumber", 260, "Shirt Number"),
        ("DateOfBirth", 300, "Date of Birth"),
        ("Gender", 340, "Gender"),
        ("Nationality", 380, "Nationality"),
        ("Fav", 420, "FavoriteTeam")
    ]

    entry_fields = {}
    favorite_team_selected = None  

    for label, y, vtext in fields:
        create_label(win, vtext, Point(460, y), 12, colorblueBac)
        if label == "Fav":
            dropdown_position = Point(670, y)
            selected_team = create_scrollable_dropdown(
                win,
                label="Favorite Team",
                options=team_names,
                position=dropdown_position,
                width=15,
                visible_count=3
            )
            entry_fields[label] = selected_team  
        else:
            entry = create_entry(win, Point(670, y), 25, 12, vfill="#F0F8FF")
            entry_fields[label] = entry

    submit_button, txt_submit = create_button(win, Point(460, 450), Point(670, 490), "Create Account", colorvlueButtons, colorcream)
    back_button, vim = create_image_button(win, Point(0, 0), Point(80, 50), "images/back3.png", size=(20, 20), vout=colorblueBac)

    while True:
        try:
            click = win.getMouse()
            
            if is_click_in_rectangle(click, submit_button):
                data = []
                for field in fields:
                    if field[0] == "Fav":
                        selected_team = entry_fields["Fav"]  
                        data.append(selected_team)
                    else:
                        text = entry_fields[field[0]].getText()
                        data.append(text)

                result, error = create_user(data)
                if result:
                    LoginGUI()  
                else:
                    messages(error)
            elif is_click_in_rectangle(click, back_button):
                LoginGUI()

        except GraphicsError:
            break


def AccountGUI(userId):
    oldwin = getCurrentWindow()   
    if oldwin:
        oldwin.close()  
    winAccountGUI = GraphWin("FootViz Account Page", screen_widthHome, screen_heightHome)
    setCurrentWindow(winAccountGUI)
    win = getCurrentWindow()    
    win.setBackground(colorcream)  

    if userId:
        # Fetch existing user data from the database for modification
        user_data = get_user_data(userId)
        try:
            date_string = user_data[5].strftime('%Y-%m-%d').strip()       
            dob = datetime.strptime(date_string, '%Y-%m-%d').date()  # Ensure the date is in the format yyyy-mm-dd     
        except ValueError:
            dob =None
        if user_data:
            fields = [
                ("FirstName", 100, "First Name", user_data[0]),
                ("LastName", 140, "Last Name", user_data[1]),
                ("UserName", 180, "User Name", user_data[2]),
                ("Password", 220, "Password", user_data[3]),
                ("ShirtNumber", 260, "Shirt Number", user_data[4]),
                ("DateOfBirth", 300, "Date of Birth", dob),
                ("Gender", 340, "Gender", user_data[6]),
                ("Nationality", 380, "Nationality", user_data[7]),
                ("FavoriteTeam", 420, "Favorite Team", user_data[8])
            ]

            # Create Entry fields for each data item
            entry_fields = {}
            for label, y, vtext, defaultvalue in fields:      
                if label=="UserName":
                    create_label(win,defaultvalue,Point(480, y),12,colorblueBac,"bold")
                else:  
                    label_text = create_label(win, vtext, Point(460, y), 12, colorblueBac)
                    entry = create_entry(win, Point(670, y), 25, 12, vfill="#F0F8FF")       
                    entry.setText(defaultvalue)
                    entry_fields[label] = entry
                    
            left_background,image_left_background=create_image_button(win, Point(0, 0), Point(350, 500), "images/BackgroundRegister1.png", size=(350, 500), vout=colorblueBac)

            jersey_objects=[]
               # Draw jersey
            jersey_objects =draw_custom_jersey(win,Point(100, 180), Point(250, 370),user_data[8] ,user_data[2],user_data[4],jersey_objects)

            # Titles
            title = create_label(win, "YOUR PROFILE", Point(550, 30), 20, colorblueBac, "bold")
            subtitle = create_label(win, "Modify your details", Point(550, 60), 12, colorblueBac, "normal")

            # Buttons
            submit_button, txt6 = create_button(win, Point(370, 450), Point(560, 490), "Save", colorvlueButtons, colorcream)
            delete_button, txt7 = create_button(win, Point(590, 450), Point(790, 490), "Delete Account", colorvlueButtons, colorcream)            
            back_button, vim = create_image_button(win, Point(0, 0), Point(80, 50), "images/back3.png",size=(20, 20), vout= colorblueBac)
  
            while True:
                try:
                    click = win.getMouse()
                    # Check if the submit button is clicked
                    if is_click_in_rectangle(click, submit_button):
                        data = [
                            entry_fields["FirstName"].getText(),
                            entry_fields["LastName"].getText(),
                            user_data[2],  # UserName cannot be modified
                            entry_fields["Password"].getText(),
                            entry_fields["ShirtNumber"].getText(),
                            entry_fields["DateOfBirth"].getText(),
                            entry_fields["Gender"].getText(),
                            entry_fields["Nationality"].getText(),
                            entry_fields["FavoriteTeam"].getText()
                        ]
                        result, error = modify_user(int(userId), data)         
                        messages(error)                      
                        if result==True:  
                            #refresh data and jersey
                            user_data = get_user_data(userId)
                            if jersey_objects:
                                for obj in jersey_objects:
                                    obj.undraw()  # Eliminar el objeto previamente dibujado
                            draw_custom_jersey(win,Point(100, 180), Point(250, 370),user_data[8] ,user_data[2],user_data[4],jersey_objects )                                        
                  
                       
                    elif is_click_in_rectangle(click, back_button):
                        create_dashboard()  # Go back to the dashboard
                        break

                    elif is_click_in_rectangle(click, delete_button):
                        result, error = delete_user(int(userId))  # Delete user
                        messages(error)
                        if result:
                            LoginGUI()  # Go back to the login screen
                        break

                except:
                    LoginGUI()  # In case of error, go back to login screen
                    break

        else:
            messages("Error retrieving user data")
            LoginGUI()  # Go back to the login screen



def LoginGUI():
    oldwin=getCurrentWindow()    
    if oldwin:
        oldwin.close()
    winLoginGUI = GraphWin("FootViz Login Page", screen_widthHome, screen_heightHome)
    setCurrentWindow(winLoginGUI)
    win=getCurrentWindow()
    win.setBackground(colorcream)
    
    left_background = Rectangle(Point(0, 0), Point(400, 500))
    left_background.setFill(colorblueBac)
    left_background.setOutline(colorblueBac)    
    left_background.draw(win)
    title = create_label(win, "FOOTVIZ",Point(200, 50),20,colorcream,"bold")
    subtitle = create_label(win,"Login into your FootViz Account",Point(200, 80), 12,colorcream,"normal")
    username_label=create_label( win,"Username",Point(130, 180),12,colorcream)
    username_field=create_entry(win,Point(200, 210),25,12,vfill="#F0F8FF")
    password_label=create_label( win,"Password",Point(130, 260),12,colorcream)
    password_field =create_entry(win,Point(200, 290),25,12,vfill="#F0F8FF")  
    login_button,txt2 = create_button(win, Point(130, 330),Point(270, 370), "Login Now",  colorvlueButtons,colorcream)
    register_button,txt3 = create_button(win, Point(130, 380), Point(270, 420), "Register",  colorvlueButtons,colorcream)
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

LoginGUI()