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
    oldwin = getCurrentWindow()
    if oldwin:
        oldwin.close()

    winRegisterGUI = GraphWin("FootViz Registration Page", screen_widthHome, screen_heightHome)
    setCurrentWindow(winRegisterGUI)
    win = getCurrentWindow()
    win.setBackground(colorcream)



    # Titles
    title = create_label(win, "REGISTER", Point(550, 30), 20, colorblueBac, "bold")
    subtitle = create_label(win, "IT'S COMPLETELY FREE", Point(550, 60), 12, colorblueBac, "normal")

    left_background,image_left_background=create_image_button(win, Point(0, 0), Point(350, 500), "images/BackgroundRegister1.png", size=(350, 500), vout=colorblueBac)
    jersey_objects=[]
    # Draw jersey
    jersey_objects =draw_custom_jersey(win,Point(100, 180), Point(250, 370),"base" ,"FOOTVIZ","0",jersey_objects)
    # Registration fields
    fields = [
        ("FirstName", 100, "First Name"),
        ("LastName", 140, "Last Name"),
        ("UserName", 180, "User Name"),
        ("Password", 220, "Password"),
        ("ShirtNumber", 260, "Shirt Number"),
        ("DateOfBirth", 300, "Date of Birth"),
        ("Gender", 340, "Gender"),
        ("Nationality", 380, "Nationality"),
        ("FavoriteTeam", 420, "Favorite Team")
    ]

    entry_fields = {}
    for label, y, vtext in fields:
        label_text = create_label(win, vtext, Point(460, y), 12, colorblueBac)
        entry = create_entry(win, Point(670, y), 25, 12, vfill="#F0F8FF")
        entry_fields[label] = entry

    # Buttons
    submit_button, txt_submit = create_button(win, Point(460, 450), Point(670, 490), "Create Account", colorvlueButtons, colorcream)    
    back_button, vim = create_image_button(win, Point(0, 0), Point(80, 50), "images/back3.png",size=(20, 20), vout=colorblueBac)
  
    while True:
        try:
            click = win.getMouse()
            # Check if the submit button is clicked
            if is_click_in_rectangle(click, submit_button):
                data = [
                    entry_fields["FirstName"].getText(),
                    entry_fields["LastName"].getText(),
                    entry_fields["UserName"].getText(),
                    entry_fields["Password"].getText(),
                    entry_fields["ShirtNumber"].getText(),
                    entry_fields["DateOfBirth"].getText(),
                    entry_fields["Gender"].getText(),
                    entry_fields["Nationality"].getText(),
                    entry_fields["FavoriteTeam"].getText()
                ]
                result, error = create_user(data)
                if result:
                    LoginGUI()  # Go back to the login screen
                   
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
    session.clear
    
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
            win.close()
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
            win.close()
            RegisterGUI()   
            break       

LoginGUI()