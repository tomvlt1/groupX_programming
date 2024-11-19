from graphics import *
import os


def ClearWindow(win):
    for item in win.items[:]:
        item.undraw()
    win.update()


# we first need to find a way to find all the files that are in the current directory or a directory of our choice
# (which will help make user experience better) so the users just have to drop the file in the directory.
# we will be using the os module, the input will be a directory, and the output will be a list of files in the directory.
# we also only want to keep the files that are relevant to the user.
# We will only keep the files that end with .sql, .txt or .csv as these are the only files that work in my SQL server.
def ListFiles(directory):
    all_files = os.listdir(directory)
    return [f for f in all_files if f.endswith(('.sql', '.txt', '.csv'))]


# Once the files are found, we will display them in the window.
# We will create a function that will draw the files in the window, as for any other graphics we need to take the win
# as an argument but we also need to pass the file as an argument so we can display it.
# We need a title to indicate to the user what we are displaying.
# Under this, we will display the files in the directory.
# We will create a box for each file and a text object that will display the name of the file.
# We offset the box with a for loop that increments the direction of the y-axis.
#we are placing these boxses, just like the title, in the center of the window
# we also want to place
def DrawFileSelector(win, files):
    ClearWindow(win)
    title = Text(Point(win.getWidth() / 2, 20), "Select a File")
    title.setSize(16)
    title.setStyle("bold")
    title.draw(win)

    y_offset = 100  
    x_center = win.getWidth() / 2  
    for i, file in enumerate(files):
        y_position = y_offset + i * 50  
        rect = Rectangle(Point(x_center - 200, y_position - 20), 
                         Point(x_center + 200, y_position + 20))
        rect.setFill("lightgray")
        rect.draw(win)

        file_text = Text(Point(x_center, y_position), file)  # Center text within the rectangle
        file_text.setSize(12)
        file_text.draw(win)

#we set the windows size to be x and y, we set the background to green to reflect the color of football
# we first start within the current directory and from there we will navigate to the target directory. We assume it has a fixed name for all use cases
# we need to check if the folder AND  the files exist, it is best for us to catch this error now to prevent it further down the line
# we create an infinite loop in which we will display the files in the directory, and ask for a user input (click in our case)
# once the user clicks, we check with an if statement to see if the click is within the box of any of the files
# once done we return the path of the file (perhaps subject to change later down the line as we may just want it as a database)

def FileSelector(folder_name, x, y):
    win = GraphWin("File Selector", x, y)
    win.setBackground("dark green")

    current_dir = os.getcwd()
    target_dir = os.path.join(current_dir, folder_name)

    if not os.path.exists(target_dir):
        win.close()
        raise FileNotFoundError(f"Folder '{folder_name}' does not exist in the current directory.")

    files = ListFiles(target_dir)
    if not files:
        win.close()
        raise FileNotFoundError(f"No files found in folder '{folder_name}'.")

    while True:
        DrawFileSelector(win, files)

        click = win.getMouse()

        y_offset = 100  
        for i, file in enumerate(files):
            y_position = y_offset + i * 50  
            if (win.getWidth() / 2 - 200) <= click.x <= (win.getWidth() / 2 + 200) and \
               (y_position - 20) <= click.y <= (y_position + 20):
                win.close()
                return os.path.join(target_dir, file)
            
# we establish the x and y values for the window and the folder name as we need them to be consistent accross pages
# we have a hardcoded folder name as we are assuming that the user will always be selecting from the same folder
# we have a try and except block to catch any errors that may occur and smoothen the user experience

def main():
    x = 1300
    y = 800
    folder_name = "target_folder"
    try:
        selected_file = FileSelector(folder_name, x, y)
        print(f"Selected file: {selected_file}")
    except FileNotFoundError as e:
        print(e)


main()
