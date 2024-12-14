from graphics import *
from Globals import *
from DataFunctions import validate_user

def LoginGUI(controller):
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
    subtitle = create_label(win, "Login into your FootViz Account", Point(200, 80), 12, "#6C757D")
    
    username_label = create_label(win, "Username", Point(130, 180), 12, "#6C757D")
    username_field = create_entry(win, Point(200, 210), 25, vcolor="#F0F8FF")
    
    password_label = create_label(win, "Password", Point(130, 260), 12, "#6C757D")
    password_field = create_entry(win, Point(200, 290), 25, vcolor="#F0F8FF")
    password_field.setText("")  # Asegúrate de ocultar el texto si es necesario
    
    login_button, _ = create_button(win, Point(130, 330), Point(270, 370), "Login Now", "#2E8B57", "white")
    register_button, _ = create_button(win, Point(130, 380), Point(270, 420), "Register", "#2E8B57", "white")
    
    error_message = create_label(win, "", Point(200, 480), 12, "#FF6347")
    
    # drawFootballField debe estar en graphics_helpers.py o en otro módulo adecuado
    # from graphics_helpers import drawFootballField
    # drawFootballField(win, Point(400, 0), Point(800, 500))
    
    while True:
        click_point = win.checkMouse()
        if is_click_in_rectangle(click_point, login_button):
            username = username_field.getText()
            password = password_field.getText()
            result, vmessage, username, user_id = validate_user(username, password)
            if result:
                setIDUser(user_id)
                controller.navigate_to_dashboard()
                break
            else:
                messages(vmessage)
        elif is_click_in_rectangle(click_point, register_button):
            controller.navigate_to_register()
            break
