from graphics import *
from Globals import *
from DataFunctions import *
from tkinter import messagebox #to messages user
from tkinter.filedialog import askopenfilename #to import files

# Screen dimensions
screen_width = 1280  # Width
screen_height = 720  # Height

# Function to handle user login
def login_user(input1,input2):
    username = input1.getText()  # Get the username from the input field
    password = input2.getText()  # Get the password directly from the input field
    
    result, vmessage,username, user_id = validate_user(username, password)
    if result:
        # Display the message on the screen
        messagebox.showinfo(getCurrentWindow(),vmessage)
        show_user_screen(username, user_id)
    else:
        messagebox.showerror(getCurrentWindow(),vmessage)


# Function to open to the login screen
def open_login_screen():
    # Reset session or user-related data
    setIDUser(None)  
    # Close the current window (if applicable)
    win=getCurrentWindow()
    if win is not None:
        win.close() 
    
    # Reinitialize the login screen
    login_window = GraphWin("Login", screen_width, screen_height)
    login_window.setBackground("white")
    setCurrentWindow(login_window)
    # Title
    title = Text(Point(screen_width / 2, 80), "Welcome to LaLiga")
    title.setSize(26)
    title.setStyle("bold")
    title.setTextColor("darkblue")
    title.draw(login_window)

    # Subtitle
    subtitle = Text(Point(screen_width / 2, 120), "Please enter your credentials below")
    subtitle.setSize(16)
    subtitle.setTextColor("gray")
    subtitle.draw(login_window)

    # Username field
    username_label = Text(Point(screen_width / 2 - 200, screen_height / 2 - 150), "Username:")
    username_label.setSize(18)
    username_label.setTextColor("black")
    username_label.draw(login_window)
    username_input = Entry(Point(screen_width / 2 + 50, screen_height / 2 - 150), 30)
    username_input.setFill("lightgray")
    username_input.draw(login_window)

    # Password field
    password_label = Text(Point(screen_width / 2 - 200, screen_height / 2 - 100), "Password:")
    password_label.setSize(18)
    password_label.setTextColor("black")
    password_label.draw(login_window)
    password_input = Entry(Point(screen_width / 2 + 50, screen_height / 2 - 100), 30)
    password_input.setFill("lightgray")
    password_input.draw(login_window)

    # Login button
    login_button = Rectangle(Point(screen_width / 2 - 150, screen_height / 2 + 50), Point(screen_width / 2 + 150, screen_height / 2 + 100))
    login_button.setFill("lightblue")
    login_button.setOutline("darkblue")
    login_button.setWidth(2)
    login_button.draw(login_window)
    login_button_text = Text(Point(screen_width / 2, screen_height / 2 + 75), "Login")
    login_button_text.setSize(18)
    login_button_text.setStyle("bold")
    login_button_text.setTextColor("black")
    login_button_text.draw(login_window)

    # Link to "Create New User"
    create_user_link = Text(Point(screen_width / 2, screen_height / 2 + 150), "Don't have an account? Create a new user")
    create_user_link.setSize(14)
    create_user_link.setTextColor("blue")
    create_user_link.setStyle("italic")
    create_user_link.draw(login_window)


    # Event loop for login interaction
    while True:
        click_point = login_window.checkMouse()  # Detect mouse clicks

        # Check if the login button is clicked
        if click_point and (screen_width / 2 - 150 <= click_point.getX() <= screen_width / 2 + 150 and
                            screen_height / 2 + 50 <= click_point.getY() <= screen_height / 2 + 100):
            login_user(username_input,password_input)
            
           

        # Check if the "Create New User" link is clicked
        if click_point and (screen_width / 2 - 200 <= click_point.getX() <= screen_width / 2 + 200 and
                            screen_height / 2 + 140 <= click_point.getY() <= screen_height / 2 + 160):
            open_user_creation_screen()  # Go to user creation screen
           
    
# Function to open the user creation screen
def open_user_creation_screen():
    win=getCurrentWindow()
    if win is not None:
        win.close()  
    
    # Create the user creation window
    create_user_window = GraphWin("Create User", screen_width, screen_height)  
    create_user_window.setBackground("white")  # Keep the same background color as Login
    setCurrentWindow(create_user_window)
    # Title
    title = Text(Point(screen_width / 2, 80), "Create New User")
    title.setSize(26)
    title.setStyle("bold")
    title.setTextColor("darkblue")
    title.draw(create_user_window)

    # Subtitle
    subtitle = Text(Point(screen_width / 2, 120), "Fill in the details below to create a new account")
    subtitle.setSize(16)
    subtitle.setTextColor("gray")
    subtitle.draw(create_user_window)

    # Username field
    username_label = Text(Point(screen_width / 2 - 200, screen_height / 2 - 150), "New Username:")
    username_label.setSize(18)
    username_label.setTextColor("black")
    username_label.draw(create_user_window)
    username_input = Entry(Point(screen_width / 2 + 50, screen_height / 2 - 150), 30)
    username_input.setFill("lightgray")
    username_input.draw(create_user_window)

    # Password field
    password_label = Text(Point(screen_width / 2 - 200, screen_height / 2 - 100), "New Password:")
    password_label.setSize(18)
    password_label.setTextColor("black")
    password_label.draw(create_user_window)
    password_input = Entry(Point(screen_width / 2 + 50, screen_height / 2 - 100), 30)
    password_input.setFill("lightgray")
    password_input.draw(create_user_window)

    # Confirm Password field
    confirm_password_label = Text(Point(screen_width / 2 - 200, screen_height / 2 - 50), "Confirm Password:")
    confirm_password_label.setSize(18)
    confirm_password_label.setTextColor("black")
    confirm_password_label.draw(create_user_window)
    confirm_password_input = Entry(Point(screen_width / 2 + 50, screen_height / 2 - 50), 30)
    confirm_password_input.setFill("lightgray")
    confirm_password_input.draw(create_user_window)

    # Submit button
    submit_button = Rectangle(Point(screen_width / 2 - 150, screen_height / 2 + 50), Point(screen_width / 2 + 150, screen_height / 2 + 100))
    submit_button.setFill("lightblue")
    submit_button.setOutline("darkblue")
    submit_button.setWidth(2)
    submit_button.draw(create_user_window)
    submit_button_text = Text(Point(screen_width / 2, screen_height / 2 + 75), "Create Account")
    submit_button_text.setSize(18)
    submit_button_text.setStyle("bold")
    submit_button_text.setTextColor("black")
    submit_button_text.draw(create_user_window)

    # Back to login link
    back_to_login_link = Text(Point(screen_width / 2, screen_height / 2 + 150), "Back to Login")
    back_to_login_link.setSize(14)
    back_to_login_link.setTextColor("blue")
    back_to_login_link.setStyle("italic")
    back_to_login_link.draw(create_user_window)

    # Event loop for interaction
    while True:
        click_point = create_user_window.checkMouse()  # Detect mouse clicks

        # Check if the submit button is clicked
        if click_point and (screen_width / 2 - 150 <= click_point.getX() <= screen_width / 2 + 150 and
                            screen_height / 2 + 50 <= click_point.getY() <= screen_height / 2 + 100):
            create_user(username_input.getText(), password_input.getText())
            create_user_window.close()
            open_login_screen()  # Go back to the login screen

        # Check if the back to login link is clicked
        if click_point and (screen_width / 2 - 100 <= click_point.getX() <= screen_width / 2 + 100 and
                            screen_height / 2 + 140 <= click_point.getY() <= screen_height / 2 + 160):
            create_user_window.close()
            open_login_screen()  # Go back to the login screen
        

# Función para eliminar la última carga del usuario
def delete_last_load(user_id):
    try:
        delete_last_insert_for_user(user_id)
        messagebox.showinfo("Success", "Last load has been deleted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while deleting the last load: {e}")

# Función para mostrar la pantalla principal
def show_user_screen(username, user_id):
    try:
        win = getCurrentWindow()  # Obtén la ventana actual
        if win is not None:  # Verifica si la ventana existe
            win.close()  # Intenta cerrar la ventana
    except Exception as e:  # Captura cualquier error al cerrar
        pass
    
    # Crear ventana
    user_screen_Main = GraphWin("User Screen", 800, 600)
    user_screen_Main.setBackground("white")
    setCurrentWindow(user_screen_Main)
    win = user_screen_Main
    
    # Saludo al usuario
    greeting = Text(Point(400, 100), f"Hello, {username}! Welcome to your dashboard.")
    greeting.setSize(18)
    greeting.setStyle("bold")
    greeting.setTextColor("darkblue")
    greeting.draw(win)

    # Botón para importar CSV
    import_button = Rectangle(Point(300, 200), Point(500, 250))
    import_button.setFill("lightblue")
    import_button.draw(win)
    import_text = Text(Point(400, 225), "Import CSV")
    import_text.setSize(16)
    import_text.setTextColor("black")
    import_text.draw(win)

    # Botón para eliminar la última carga
    delete_button = Rectangle(Point(300, 300), Point(500, 350))
    delete_button.setFill("lightcoral")
    delete_button.draw(win)
    delete_text = Text(Point(400, 325), "Delete Last Load")
    delete_text.setSize(16)
    delete_text.setTextColor("black")
    delete_text.draw(win)

    # Loop para manejar eventos
    while True:
        click_point = win.getMouse()
        if (300 <= click_point.getX() <= 500 and 200 <= click_point.getY() <= 250):
            # Seleccionar archivo CSV
            file_path = askopenfilename(filetypes=[("CSV Files", "*.csv")])
            
            if file_path:
                # Crear registro en LoadFiles y obtener el idLoad
                result, last_insert_id ,vmessage = create_load_record(user_id, file_path)
                if result:
                    # Importar datos desde el archivo CSV
                    import_csv_to_database(file_path, int(user_id), int(last_insert_id))
                    messagebox.showinfo(getCurrentWindow(), vmessage)
                else:
                    messagebox.showerror(getCurrentWindow(), vmessage)
                
                break  # Sale del ciclo después de procesar el CSV

        elif (300 <= click_point.getX() <= 500 and 300 <= click_point.getY() <= 350):
            # Eliminar la última carga
            delete_last_load(user_id)
           

#init app     
open_login_screen()