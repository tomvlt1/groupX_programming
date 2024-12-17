
from graphics import *

def screen():
    screen_width = 900  
    screen_height = 500  
    screen_widthHome = 800  
    screen_heightHome = 500  
    return screen_width, screen_height, screen_widthHome, screen_heightHome

def color():
    colorblueBac=color_rgb(31, 27, 58)
    colorvlueButtons=color_rgb(44, 40, 85)
    colorvlueButtons1=color_rgb(84, 80, 125)
    colorgreen="#F8F9FA"
    colorcream=color_rgb(242, 237, 228)
    return colorblueBac, colorvlueButtons, colorvlueButtons1, colorgreen, colorcream
    
session = {}

def setIDUser(IdUser):
    session['IdUser']= IdUser
def getIDUser():
    return session.get('IdUser', None)   
def setCurrentWindow(Win):
    session['CurrentWindow']= Win
def getCurrentWindow():
    return session.get('CurrentWindow', None)  
def setFilters(vfilter):
    session['Filters']= vfilter
def getFilters():
    return session.get('Filters', [])    
def setDataset(IdFileLoad):
    session['IdFileLoad']=IdFileLoad
def getDataset():
    return session.get('IdFileLoad',"") 
  

  
def is_click_in_rectangle(click_point, rectangle):
    
    if click_point and rectangle:
        x1, y1 = rectangle.getP1().getX(), rectangle.getP1().getY()  
        x2, y2 = rectangle.getP2().getX(), rectangle.getP2().getY()  
        
        
        return x1 <= click_point.getX() <= x2 and y1 <= click_point.getY() <= y2
    return False

def is_click_in_text_area(click_point, text_object):
  
    if click_point and text_object:
        x1, y1 = text_object.getAnchor().getX(), text_object.getAnchor().getY()
        
        text_width = len(text_object.getText()) * 12  
        text_height = 40  
        
        x2, y2 = x1 + text_width, y1 + text_height

        return x1 <= click_point.getX() <= x2 and y1 <= click_point.getY() <= y2
    return False


def create_button(win,p1, p2, label, fill_color, text_color,vout="grey",size=14):
    button = Rectangle(p1,p2)
    button.setFill(fill_color)
    button.setWidth(2)
    
    button.draw(win)

    button_text = Text(button.getCenter(), label)
    button_text.setSize(size)
    button_text.setTextColor(text_color)
    button_text.draw(win)
    
    return button,button_text 
def create_image_button(win, p1, p2, image_path, size=(50, 50), vout="grey"):
    button = Rectangle(p1, p2)
    button.setFill(vout)
    button.setWidth(0)
    button.draw(win)
    
    image = Image(button.getCenter(), image_path)
    
    image_width, image_height = size
    image.width = image_width
    image.height = image_height
    image.draw(win)
    
    return button, image
def create_label(win, text, p1, size=12, vcolor="black",style="normal"):
    label = Text(p1, text)
    
    label.setSize(size)
    label.setTextColor(vcolor)
    label.setStyle(style)
   
    label.draw(win)
    
    return label
def create_entry(win, p1, vwidth,size=12, style="normal", vcolor="black",vfill="white",voutl="grey"):   

    entry = Entry(p1, vwidth)  

    entry.setSize(size)
    entry.setStyle(style)   
    entry.setFill(vfill)   
  
    entry.draw(win)

    return entry

def messages(valortext):            
        win_message = GraphWin("Mensaje", 300, 200)        
        words = valortext.split()  
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            if len(current_line) == 4:  
                lines.append(" ".join(current_line))  
                current_line = []  
        if current_line:  
            lines.append(" ".join(current_line)) 
        message = Text(Point(150,60), "\n".join(lines))
        message .setSize(11)  
        message .setTextColor("#2E8B57")  
        message .setStyle("normal")  
        ok_button = Rectangle(Point(110, 130), Point(170, 170))
        ok_button.setFill("#2E8B57")   
        ok_text = Text(Point(140, 150), "OK")
        ok_text.setSize(11)
        ok_text.setTextColor("white")        
        message.draw(win_message)
        ok_button.draw(win_message)
        ok_text.draw(win_message)        
        while True:
            click_point = win_message.getMouse()
            if is_click_in_rectangle(click_point, ok_button):
                win_message.close()
                break  
        
        
def show_import_message(window, vpoint):
    origin_x = vpoint.getX()-210  
    origin_y = vpoint.getY() +30  
    rectangle1 = Rectangle(Point(origin_x , origin_y - 10), Point(origin_x + 230, origin_y + 160))
    rectangle1.setFill("lightgray")
    rectangle1.setWidth(1)
    rectangle1.draw(window)   
    message = Text(Point(origin_x + 120, origin_y + 30), "The file 'file_to_import.csv' ")
    message1 = Text(Point(origin_x + 120, origin_y + 50), " will be imported ")
    message2 = Text(Point(origin_x + 120, origin_y + 70), "from the 'files' folder")
    message.setSize(12)
    message.setTextColor("black")
    message1.setSize(12)
    message1.setTextColor("black")
    message2.setSize(12)
    message2.setTextColor("black")
    message.draw(window)
    message1.draw(window)
    message2.draw(window)
    ok_button = Rectangle(Point(origin_x +30, origin_y + 100), Point(origin_x + 100, origin_y + 140))
    ok_button.setFill("blue")
    ok_button.draw(window)
    cancel_button = Rectangle(Point(origin_x + 110, origin_y + 100), Point(origin_x + 190, origin_y + 140))
    cancel_button.setFill("blue")
    cancel_button.draw(window)
    ok_text = Text(Point(origin_x + 65, origin_y + 120), "OK")
    ok_text.setSize(12)
    ok_text.setTextColor("white")
    ok_text.draw(window)
    cancel_text = Text(Point(origin_x + 150, origin_y + 120), "Cancel")
    cancel_text.setSize(12)
    cancel_text.setTextColor("white")
    cancel_text.draw(window)
    vector_objects=(rectangle1,message,message1,message2,ok_button,cancel_button,ok_text,cancel_text) 
    return vector_objects


def drawFootballField(win, p1, p2):
    field_width = p2.getX() - p1.getX()
    field_height = p2.getY() - p1.getY()

    field = Rectangle(p1, p2)
    field.setFill("#2E8B57")
    field.setOutline("#FFFFFF")
    field.setWidth(2)
    field.draw(win)

    outer_boundary = Rectangle(Point(p1.getX() + 0.05 * field_width, p1.getY() + 0.04 * field_height),
                               Point(p1.getX() + 0.95 * field_width, p1.getY() + 0.96 * field_height))
    outer_boundary.setOutline("white")
    outer_boundary.setWidth(2)
    outer_boundary.draw(win)

    center_line = Line(Point(p1.getX() + 0.5 * field_width, p1.getY()),
                       Point(p1.getX() + 0.5 * field_width, p2.getY()))
    center_line.setOutline("white")
    center_line.setWidth(2)
    center_line.draw(win)

    center_circle_radius = 0.1 * field_height  
    center_circle = Circle(Point(p1.getX() + 0.5 * field_width, p1.getY() + 0.5 * field_height), center_circle_radius)
    center_circle.setOutline("white")
    center_circle.setWidth(2)
    center_circle.draw(win)

    center_dot_radius = 0.01 * field_height 
    center_dot = Circle(Point(p1.getX() + 0.5 * field_width, p1.getY() + 0.5 * field_height), center_dot_radius)
    center_dot.setFill("white")
    center_dot.draw(win)

    top_penalty_area = Rectangle(Point(p1.getX() + 0.15 * field_width, p1.getY() + 0.04 * field_height),
                                 Point(p1.getX() + 0.85 * field_width, p1.getY() + 0.24 * field_height))
    top_penalty_area.setOutline("white")
    top_penalty_area.setWidth(2)
    top_penalty_area.draw(win)

    bottom_penalty_area = Rectangle(Point(p1.getX() + 0.15 * field_width, p1.getY() + 0.76 * field_height),
                                    Point(p1.getX() + 0.85 * field_width, p1.getY() + 0.96 * field_height))
    bottom_penalty_area.setOutline("white")
    bottom_penalty_area.setWidth(2)
    bottom_penalty_area.draw(win)

    top_goal_area = Rectangle(Point(p1.getX() + 0.18 * field_width, p1.getY() + 0.04 * field_height),
                              Point(p1.getX() + 0.82 * field_width, p1.getY() + 0.08 * field_height))
    top_goal_area.setOutline("white")
    top_goal_area.setWidth(2)
    top_goal_area.draw(win)

    bottom_goal_area = Rectangle(Point(p1.getX() + 0.18 * field_width, p1.getY() + 0.92 * field_height),
                                 Point(p1.getX() + 0.82 * field_width, p1.getY() + 0.96 * field_height))
    bottom_goal_area.setOutline("white")
    bottom_goal_area.setWidth(2)
    bottom_goal_area.draw(win)

    top_goal_dot_radius = 0.01 * field_height  
    top_goal_dot = Circle(Point(p1.getX() + 0.5 * field_width, p1.getY() + 0.08 * field_height), top_goal_dot_radius)
    top_goal_dot.setFill("white")
    top_goal_dot.draw(win)

    bottom_goal_dot_radius = 0.01 * field_height  
    bottom_goal_dot = Circle(Point(p1.getX() + 0.5 * field_width, p1.getY() + 0.92 * field_height), bottom_goal_dot_radius)
    bottom_goal_dot.setFill("white")
    bottom_goal_dot.draw(win)

def create_scrollable_dropdown(win, label, options, position, width=15, visible_count=10):
    dropdown_label_color = "white"
    label_position = Point(position.getX() - (width * 7), position.getY())
    create_label(win, label, label_position, size=12)

    dropdown_bg_color = color_rgb(255, 255, 255) 
    dropdown_outline_color = "black"

    dropdown = Rectangle(
        Point(position.getX() - width*5, position.getY() - 10),
        Point(position.getX() + width*5, position.getY() + 10)
    )
    dropdown.setOutline(dropdown_outline_color)
    dropdown.setFill(dropdown_bg_color)
    dropdown.draw(win)

    selected_text = Text(dropdown.getCenter(), "Select...")
    selected_text.setSize(10)
    selected_text.setTextColor("black")
    selected_text.draw(win)

    while True:
        click = win.getMouse()
        if is_click_in_rectangle(click, dropdown):
            dropdown_options = []
            visible_options = options[:visible_count]

            for i, option in enumerate(visible_options):
                option_rect = Rectangle(
                    Point(dropdown.getP1().getX(), dropdown.getP2().getY() + i * 20),
                    Point(dropdown.getP2().getX(), dropdown.getP2().getY() + (i+1)*20)
                )
                option_rect.setFill("white")
                option_rect.setOutline("black")
                option_rect.draw(win)

                option_text = Text(option_rect.getCenter(), str(option))
                option_text.setSize(10)
                option_text.setTextColor("black")
                option_text.draw(win)

                dropdown_options.append((option_rect, option_text, option))

            up_button = down_button = up_text = down_text = None
            if len(options) > visible_count:
                up_button = Rectangle(
                    Point(dropdown.getP1().getX(), dropdown.getP2().getY() - 20),
                    Point(dropdown.getP2().getX(), dropdown.getP2().getY())
                )
                up_button.setFill("#D3D3D3")
                up_button.setOutline("black")
                up_button.draw(win)
                up_text = Text(up_button.getCenter(), "▲")
                up_text.setSize(10)
                up_text.setTextColor("black")
                up_text.draw(win)

                down_button = Rectangle(
                    Point(dropdown.getP1().getX(), dropdown.getP2().getY() + visible_count*20),
                    Point(dropdown.getP2().getX(), dropdown.getP2().getY() + (visible_count+1)*20)
                )
                down_button.setFill("#D3D3D3")
                down_button.setOutline("black")
                down_button.draw(win)
                down_text = Text(down_button.getCenter(), "▼")
                down_text.setSize(10)
                down_text.setTextColor("black")
                down_text.draw(win)

            start_index = 0
            while True:
                option_click = win.getMouse()
                if up_button and is_click_in_rectangle(option_click, up_button) and start_index > 0:
                    start_index -= visible_count
                elif down_button and is_click_in_rectangle(option_click, down_button) and start_index + visible_count < len(options):
                    start_index += visible_count

                for rect, t, _ in dropdown_options:
                    rect.undraw()
                    t.undraw()
                dropdown_options.clear()

                visible_options = options[start_index:start_index+visible_count]
                for i, opt in enumerate(visible_options):
                    option_rect = Rectangle(
                        Point(dropdown.getP1().getX(), dropdown.getP2().getY() + i * 20),
                        Point(dropdown.getP2().getX(), dropdown.getP2().getY() + (i+1)*20)
                    )
                    option_rect.setFill("white")
                    option_rect.setOutline("black")
                    option_rect.draw(win)

                    option_text = Text(option_rect.getCenter(), str(opt))
                    option_text.setSize(10)
                    option_text.setTextColor("black")
                    option_text.draw(win)

                    dropdown_options.append((option_rect, option_text, opt))

                for rect, text_obj, val_opt in dropdown_options:
                    if is_click_in_rectangle(option_click, rect):
                        for r, t, _ in dropdown_options:
                            r.undraw()
                            t.undraw()
                        if up_button:
                            up_button.undraw()
                            up_text.undraw()
                        if down_button:
                            down_button.undraw()
                            down_text.undraw()
                        selected_text.setText(str(val_opt))
                        return val_opt
                    
