from graphics import *
from Createtable import (Create_Table, Connect_to_Mysql)

def on_submit(userport, filepath, win):
    try:
        port = int(userport.getText())
        file = filepath.getText()

        mydb = Connect_to_Mysql(port)
        Create_Table(file, mydb)

        msg = Text(Point(win.getWidth()/2, win.getHeight()-30), "¡Tabla creada exitosamente!")
        msg.setSize(12)
        msg.setFill("white")
        msg.draw(win)

    except Exception as e:
        error_msg = Text(Point(win.getWidth()/2, win.getHeight()-30), f"Error: {str(e)}")
        error_msg.setSize(12)
        error_msg.setFill("red")
        error_msg.draw(win)

# Crear la ventana
win_width = 400
win_height = 300
win = GraphWin("Interfaz de Fútbol", win_width, win_height)
win.setBackground("dark green")

# Título
title = Text(Point(win_width/2, 30), "Cargar Datos de Fútbol")
title.setSize(20)
title.setStyle('bold')
title.setTextColor("white")
title.draw(win)

# Entrada para el número de puerto
port_label = Text(Point(100, 100), "Número de Puerto:")
port_label.setSize(12)
port_label.setTextColor("white")
port_label.draw(win)

port_entry = Entry(Point(250, 100), 10)
port_entry.draw(win)

# Entrada para la ruta del archivo
file_label = Text(Point(100, 150), "Ruta del Archivo:")
file_label.setSize(12)
file_label.setTextColor("white")
file_label.draw(win)

file_entry = Entry(Point(250, 150), 25)
file_entry.draw(win)

# Botón de Submit
submit_button = Rectangle(Point(150, 200), Point(250, 240))
submit_button.setFill("white")
submit_button.draw(win)

submit_text = Text(submit_button.getCenter(), "Submit")
submit_text.setFill("dark green")
submit_text.draw(win)

# Esperar a que el usuario haga clic
while True:
    click = win.getMouse()
    if submit_button.getP1().getX() <= click.getX() <= submit_button.getP2().getX() and \
       submit_button.getP1().getY() <= click.getY() <= submit_button.getP2().getY():
        on_submit(port_entry, file_entry, win)
        break

# Instrucción para cerrar la ventana
close_msg = Text(Point(win_width/2, win_height - 10), "Haga clic para cerrar.")
close_msg.setSize(10)
close_msg.setFill("white")
close_msg.draw(win)

win.getMouse()
win.close()