
from graphics import *

session = {}

def setIDUser(IdUser):
    session['IdUser']= IdUser
def getIDUser():
    return session.get('IdUser', None)   
def setCurrentWindow(Win):
    session['CurrentWindow']= Win
def getCurrentWindow():
    return session.get('CurrentWindow', None)   

#controlar si he criclado en un rectangle      
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

def create_button(win,p1, p2, label, fill_color, text_color,vout="grey"):
    button = Rectangle(p1,p2)
    button.setFill(fill_color)
    button.setWidth(2)
    
    button.draw(win)

    button_text = Text(button.getCenter(), label)
    button_text.setSize(14)
    button_text.setTextColor(text_color)
    button_text.draw(win)
    
    return button    
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
        # Create a window of 400x400 pixels
        win = GraphWin("Mensaje", 300, 300)        
               # Split the input text into lines of 4 words each
        words = valortext.split()  # Split the text into words
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            if len(current_line) == 6:  # If the current line has 4 words
                lines.append(" ".join(current_line))  # Join the words into a string and add it to lines
                current_line = []  # Start a new line
        if current_line:  # If there are remaining words that didn't form a full line
            lines.append(" ".join(current_line))  # Add the last line
        # Create a text object with the message to display      
        message = Text(Point(100,30), "\n".join(lines))
        message .setSize(11)  # Set font size
        message .setTextColor("#2E8B57")  # Set text color
        message .setStyle("normal")  # Set font style
         # Create the OK button
        ok_button = Rectangle(Point(50, 120), Point(150, 160))
        ok_button.setFill("#2E8B57")   
        # Create the button text
        ok_text = Text(Point(100, 140), "OK")
        ok_text.setSize(11)
        ok_text.setTextColor("white")        
        # Draw 
        message.draw(win)
        ok_button.draw(win)
        ok_text.draw(win)        
        # Wait for the user to click the OK button
        while True:
            click_point = win.getMouse()
            if is_click_in_rectangle(click_point, ok_button):
                break  # Exit the loop when the OK button is clicked
        # Close the window
        win.close()   