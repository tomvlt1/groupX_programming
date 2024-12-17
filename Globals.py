
from graphics import *

# Screen dimensions
def screen():
    screen_width = 900  # Width
    screen_height = 500  # Height
    screen_widthHome = 800  # Width
    screen_heightHome = 500  # Height
    return screen_width, screen_height, screen_widthHome, screen_heightHome

def color():
    colorblueBac=color_rgb(31, 27, 58)
    colorvlueButtons=color_rgb(44, 40, 85)
    colorvlueButtons1=color_rgb(84, 80, 125)
    colorgreen="#F8F9FA"
    colorcream=color_rgb(242, 237, 228)
    return colorblueBac, colorvlueButtons, colorvlueButtons1, colorgreen, colorcream
    
class SessionManager:
    def __init__(self):
        self.session = {}

    def setIDUser(self, IdUser):
        self.session['IdUser'] = IdUser

    def getIDUser(self):
        return self.session.get('IdUser', None)

    def setCurrentWindow(self, Win):
        self.session['CurrentWindow'] = Win

    def getCurrentWindow(self):
        return self.session.get('CurrentWindow', None)

    def setFilters(self, vfilter):
        self.session['Filters'] = vfilter

    def getFilters(self):
        return self.session.get('Filters', [])

    def setDataset(self, IdFileLoad):
        self.session['IdFileLoad'] = IdFileLoad

    def getDataset(self):
        return self.session.get('IdFileLoad', "")
  

  
def is_click_in_rectangle(click_point, rectangle):
    
    if click_point and rectangle:
        # Obtener las coordenadas de las esquinas del rectángulo
        x1, y1 = rectangle.getP1().getX(), rectangle.getP1().getY()  # Esquina superior izquierda
        x2, y2 = rectangle.getP2().getX(), rectangle.getP2().getY()  # Esquina inferior derecha
        
        # Verificar si el clic está dentro del rectángulo
        return x1 <= click_point.getX() <= x2 and y1 <= click_point.getY() <= y2
    return False

def is_click_in_text_area(click_point, text_object):
  
    if click_point and text_object:
        # Obtener las coordenadas del ancla del texto (punto superior izquierdo)
        x1, y1 = text_object.getAnchor().getX(), text_object.getAnchor().getY()
        
        # Estimación de las dimensiones del texto 
        text_width = len(text_object.getText()) * 12  # Estimación de ancho basado en caracteres
        text_height = 40  # Estimación de altura por línea (ajustar según la fuente)
        
        # Calcular las esquinas basadas en el punto de anclaje y las dimensiones
        x2, y2 = x1 + text_width, y1 + text_height

        # Verificar si el clic está dentro del área estimada
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
    # Create the button as a rectangle
    button = Rectangle(p1, p2)
    button.setFill(vout)
    button.setWidth(0)
    button.draw(win)
    
    # Load the image
    image = Image(button.getCenter(), image_path)
    
    # Resize the image if a size is provided
    image_width, image_height = size
    image.width = image_width
    image.height = image_height
    image.draw(win)
    
    return button, image
def create_label(win, text, p1, size=12, vcolor="black",style="normal"):
    # Crear el objeto de texto
    label = Text(p1, text)
    
    # Personalizar el texto
    label.setSize(size)
    label.setTextColor(vcolor)
    label.setStyle(style)
   
    # Dibujar el texto en la ventana
    label.draw(win)
    
    # Retornar el label para futuras modificaciones
    return label
def create_entry(win, p1, vwidth,size=12, style="normal", vcolor="black",vfill="white",voutl="grey"):   

    # Crear el campo de entrada (Entry)
    entry = Entry(p1, vwidth)  # El ancho es la diferencia entre x2 y x1

    # Personalizar el campo de entrada
    entry.setSize(size)
    entry.setStyle(style)   
    entry.setFill(vfill)   # Color de fondo
  
    # Dibujar el campo de entrada en la ventana
    entry.draw(win)

    # Retornar el objeto Entry para futuras manipulaciones
    return entry

def messages(valortext):            
        # Create a window of pixels
        win_message = GraphWin("Mensaje", 300, 200)        
               # Split the input text into lines of 4 words each
        words = valortext.split()  # Split the text into words
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            if len(current_line) == 4:  # If the current line has 4 words
                lines.append(" ".join(current_line))  # Join the words into a string and add it to lines
                current_line = []  # Start a new line
        if current_line:  # If there are remaining words that didn't form a full line
            lines.append(" ".join(current_line))  # Add the last line
        # Create a text object with the message to display      
        message = Text(Point(150,60), "\n".join(lines))
        message .setSize(11)  # Set font size
        message .setTextColor("#2E8B57")  # Set text color
        message .setStyle("normal")  # Set font style
         # Create the OK button
        ok_button = Rectangle(Point(110, 130), Point(170, 170))
        ok_button.setFill("#2E8B57")   
        # Create the button text
        ok_text = Text(Point(140, 150), "OK")
        ok_text.setSize(11)
        ok_text.setTextColor("white")        
        # Draw 
        message.draw(win_message)
        ok_button.draw(win_message)
        ok_text.draw(win_message)        
        # Wait for the user to click the OK button
        while True:
            click_point = win_message.getMouse()
            if is_click_in_rectangle(click_point, ok_button):
                win_message.close()
                break  # Exit the loop when the OK button is clicked
        
        
def show_import_message(window, vpoint):
      # Define the origin point for the message and buttons
    origin_x = vpoint.getX()-210  # Move a bit more to the left
    origin_y = vpoint.getY() +30  # Move a bit higher from the bottom
    # Create the background rectangle for the message, covering the buttons
    rectangle1 = Rectangle(Point(origin_x , origin_y - 10), Point(origin_x + 230, origin_y + 160))
    rectangle1.setFill("lightgray")
    rectangle1.setWidth(1)
    rectangle1.draw(window)   
    # Create the informational message text
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
    # Create the OK button
    ok_button = Rectangle(Point(origin_x +30, origin_y + 100), Point(origin_x + 100, origin_y + 140))
    ok_button.setFill("blue")
    ok_button.draw(window)
    # Create the Cancel button
    cancel_button = Rectangle(Point(origin_x + 110, origin_y + 100), Point(origin_x + 190, origin_y + 140))
    cancel_button.setFill("blue")
    cancel_button.draw(window)
    # Create the OK button text
    ok_text = Text(Point(origin_x + 65, origin_y + 120), "OK")
    ok_text.setSize(12)
    ok_text.setTextColor("white")
    ok_text.draw(window)
    # Create the Cancel button text
    cancel_text = Text(Point(origin_x + 150, origin_y + 120), "Cancel")
    cancel_text.setSize(12)
    cancel_text.setTextColor("white")
    cancel_text.draw(window)
    vector_objects=(rectangle1,message,message1,message2,ok_button,cancel_button,ok_text,cancel_text) 
    return vector_objects


def drawFootballField(win, p1, p2):
    # Calculate width and height based on the points
    field_width = p2.getX() - p1.getX()
    field_height = p2.getY() - p1.getY()

    # Draw the football field as a rectangle
    field = Rectangle(p1, p2)
    field.setFill("#2E8B57")
    field.setOutline("#FFFFFF")
    field.setWidth(2)
    field.draw(win)

    # Outer boundary
    outer_boundary = Rectangle(Point(p1.getX() + 0.05 * field_width, p1.getY() + 0.04 * field_height),
                               Point(p1.getX() + 0.95 * field_width, p1.getY() + 0.96 * field_height))
    outer_boundary.setOutline("white")
    outer_boundary.setWidth(2)
    outer_boundary.draw(win)

    # Center line
    center_line = Line(Point(p1.getX() + 0.5 * field_width, p1.getY()),
                       Point(p1.getX() + 0.5 * field_width, p2.getY()))
    center_line.setOutline("white")
    center_line.setWidth(2)
    center_line.draw(win)

    # Center circle (resizable)
    center_circle_radius = 0.1 * field_height  # Radius proportional to the height
    center_circle = Circle(Point(p1.getX() + 0.5 * field_width, p1.getY() + 0.5 * field_height), center_circle_radius)
    center_circle.setOutline("white")
    center_circle.setWidth(2)
    center_circle.draw(win)

    # Center dot (resizable)
    center_dot_radius = 0.01 * field_height  # Radius proportional to the height
    center_dot = Circle(Point(p1.getX() + 0.5 * field_width, p1.getY() + 0.5 * field_height), center_dot_radius)
    center_dot.setFill("white")
    center_dot.draw(win)

    # Top penalty area
    top_penalty_area = Rectangle(Point(p1.getX() + 0.15 * field_width, p1.getY() + 0.04 * field_height),
                                 Point(p1.getX() + 0.85 * field_width, p1.getY() + 0.24 * field_height))
    top_penalty_area.setOutline("white")
    top_penalty_area.setWidth(2)
    top_penalty_area.draw(win)

    # Bottom penalty area
    bottom_penalty_area = Rectangle(Point(p1.getX() + 0.15 * field_width, p1.getY() + 0.76 * field_height),
                                    Point(p1.getX() + 0.85 * field_width, p1.getY() + 0.96 * field_height))
    bottom_penalty_area.setOutline("white")
    bottom_penalty_area.setWidth(2)
    bottom_penalty_area.draw(win)

    # Top goal area
    top_goal_area = Rectangle(Point(p1.getX() + 0.18 * field_width, p1.getY() + 0.04 * field_height),
                              Point(p1.getX() + 0.82 * field_width, p1.getY() + 0.08 * field_height))
    top_goal_area.setOutline("white")
    top_goal_area.setWidth(2)
    top_goal_area.draw(win)

    # Bottom goal area
    bottom_goal_area = Rectangle(Point(p1.getX() + 0.18 * field_width, p1.getY() + 0.92 * field_height),
                                 Point(p1.getX() + 0.82 * field_width, p1.getY() + 0.96 * field_height))
    bottom_goal_area.setOutline("white")
    bottom_goal_area.setWidth(2)
    bottom_goal_area.draw(win)

    # Top goal dot (resizable)
    top_goal_dot_radius = 0.01 * field_height  # Radius proportional to the height
    top_goal_dot = Circle(Point(p1.getX() + 0.5 * field_width, p1.getY() + 0.08 * field_height), top_goal_dot_radius)
    top_goal_dot.setFill("white")
    top_goal_dot.draw(win)

    # Bottom goal dot (resizable)
    bottom_goal_dot_radius = 0.01 * field_height  # Radius proportional to the height
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
                # Scroll Up
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

                # Scroll Down
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

                # Undraw old options
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
                    
