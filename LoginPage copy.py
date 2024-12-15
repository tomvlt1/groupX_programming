from graphics import *
from Globals import *
from DataFunctions import *
fom 

# Screen dimensions
screen_width = 1280  # Width
screen_height = 720  # Height
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
 


def drawFootballField(win):
    field = Rectangle(Point(400, 0), Point(800, 500))
    field.setFill("#2E8B57")
    field.setOutline("#FFFFFF")
    field.setWidth(2)
    field.draw(win)
    outer_boundary = Rectangle(Point(420, 20), Point(780, 480))
    outer_boundary.setOutline("white")
    outer_boundary.setWidth(2)
    outer_boundary.draw(win)
    center_line = Line(Point(400, 250), Point(800, 250))
    center_line.setOutline("white")
    center_line.setWidth(2)
    center_line.draw(win)
    center_circle = Circle(Point(600, 250), 50)
    center_circle.setOutline("white")
    center_circle.setWidth(2)
    center_circle.draw(win)
    center_dot = Circle(Point(600, 250), 3)
    center_dot.setFill("white")
    center_dot.draw(win)
    top_penalty_area = Rectangle(Point(480, 20), Point(720, 120))
    top_penalty_area.setOutline("white")
    top_penalty_area.setWidth(2)
    top_penalty_area.draw(win)
    bottom_penalty_area = Rectangle(Point(480, 380), Point(720, 480))
    bottom_penalty_area.setOutline("white")
    bottom_penalty_area.setWidth(2)
    bottom_penalty_area.draw(win)
    top_goal_area = Rectangle(Point(520, 20), Point(680, 60))
    top_goal_area.setOutline("white")
    top_goal_area.setWidth(2)
    top_goal_area.draw(win)
    bottom_goal_area = Rectangle(Point(520, 440), Point(680, 480))
    bottom_goal_area.setOutline("white")
    bottom_goal_area.setWidth(2)
    bottom_goal_area.draw(win)
    top_goal_dot = Circle(Point(600, 70), 3)
    top_goal_dot.setFill("white")
    top_goal_dot.draw(win)
    bottom_goal_dot = Circle(Point(600, 430), 3)
    bottom_goal_dot.setFill("white")
    bottom_goal_dot.draw(win)

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
    submit_button = create_button(win, Point(700,650), Point(900, 690), "Create Account",  "#2E8B57","white" )
    back_button = create_button(win, Point(700, 700), Point(900, 740), "Back to Login", "#2E8B57","white" )
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
            title = create_label(win,"YOUR PROFILE",Point(800, 60), 28,"#1E2A39","bold")  
            
            submit_button = create_button(win, Point(700,650), Point(900, 690), "Save",  "#2E8B57","white" )
            back_button = create_button(win, Point(700, 700), Point(900, 740), "Back to Login", "#2E8B57","white" )
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
                            LoginGUI() # Go back to the login screen
                            break
                        else:
                            messages(error)
                            break
                    elif  is_click_in_rectangle(click, back_button):
                        LoginGUI() # Go back to the login screen
                        break
                except:
                    LoginGUI() # Go back to the login screen
                    break                    
        else:
            messages(error)
            LoginGUI() # Go back to the login screen

              

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
    login_button = create_button(win, Point(130, 330),Point(270, 370), "Login Now",  "#2E8B57","white",)
    register_button = create_button(win, Point(130, 380), Point(270, 420), "Register",  "#2E8B57","white")
    error_message = create_label (win,"",Point(200, 480),12,"#FF6347")
    
    drawFootballField(win)
    
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