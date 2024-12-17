# FileSelect.py

from Globals import (
    create_button,
    create_label,
    is_click_in_rectangle,screen)
import os
from graphics import GraphWin, Point

(screen_width, screen_height, screen_widthHome, screen_heightHome)=screen()
def list_files(directory, extensions=(".txt", ".csv")):
    return [f for f in os.listdir(directory) if f.endswith(extensions)]

def clear_window(win):
    for item in win.items[:]:
        item.undraw()
    win.update()

def draw_file_selector(win, files):
    
    
    clear_window(win)
    create_label(win, "Select a File", Point(win.getWidth() / 2, 20), size=16, style="bold")
    
    y_offset = 100
    x_center = win.getWidth() / 2
    buttons = []
    for i, file in enumerate(files):
        y_position = y_offset + i * 50
        rect, file_text = create_button(
            win,
            Point(x_center - 200, y_position - 20),
            Point(x_center + 200, y_position + 20),
            file,
            fill_color="lightgray",
            text_color="black",
            size=12,
        )
        buttons.append((rect, file_text, file))
    return buttons

def file_selector(folder_name, win_width=screen_width, win_height=screen_height):
    """
    Opens a separate window to let the user select a file from `folder_name`.
    Returns the full path to the selected file, or raises FileNotFoundError if folder/files are missing.
    """
    
    
    win = GraphWin("File Selector", win_width, win_height)
    win.setBackground("#2c2855")
    
    target_dir = os.path.join(os.getcwd(), folder_name)
    if not os.path.exists(target_dir):
        raise FileNotFoundError(f"Folder '{folder_name}' does not exist.")
    
    files = list_files(target_dir)
    if not files:
        raise FileNotFoundError(f"No files found in folder '{folder_name}'.")

    while True:
        buttons = draw_file_selector(win, files)
        click = win.getMouse()
        for rect, _, file in buttons:
            if is_click_in_rectangle(click, rect):
                win.close()
                return os.path.join(target_dir, file),file
