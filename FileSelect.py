from Globals import (
    create_button,
    create_label,
    is_click_in_rectangle,
    screen_width,
    screen_height,
)
import os
from graphics import GraphWin, Point

# Simplified file selector
def list_files(directory, extensions=(".txt", ".csv")):
    """List files in a directory with specific extensions."""
    return [f for f in os.listdir(directory) if f.endswith(extensions)]

def clear_window(win):
    """Clears all elements from the window."""
    for item in win.items[:]:
        item.undraw()
    win.update()

def draw_file_selector(win, files):
    """Draws the file selector interface in the window."""
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
    """Creates a file selection interface."""
    win = GraphWin("File Selector", win_width, win_height)
    win.setBackground("dark green")
    
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
                return os.path.join(target_dir, file)

# Main function
def main():
    try:
        selected_file = file_selector("target_folder")
        print(f"Selected file: {selected_file}")
    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    main()
