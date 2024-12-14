from graphics import *
from Globals import *
from DataFunctions import *
from graph_1 import *
from FootGameHome import FootGameHomeMain
from Graphsuggest import *
import time
from login import LoginGUI


#********FUNCTIONS********
 





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
