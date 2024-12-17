# ChooseDataset.py
from Globals import (
    create_button,
    create_label,
    is_click_in_rectangle,create_image_button,
    screen_width,
    screen_height,
    getIDUser,setDataset,colorcream,
)
from graphics import GraphWin, Point
from DataFunctions import Select_Load_Files


def clear_window(win):
    for item in win.items[:]:
        item.undraw()
    win.update()

def draw_dataset(win):
    
    clear_window(win)
    
    create_label(win, "Select file", Point(win.getWidth() / 2, 40), 16, colorcream,style="bold")
   
    back_button, vim = create_image_button(win, Point(0, 0), Point(80, 50), "images/back3.png",size=(20, 20), vout= "#2c2855")
    
    y_offset = 100
    x_center = win.getWidth() / 2
    
    iduser= getIDUser()
    if  iduser:   
        vfiles = Select_Load_Files()
        if vfiles:
            # Label for selecting year            
            buttons = []
            idx=1
        
            for i in range(len(vfiles)):
                idload,vfile, vdata = vfiles[i]
                btn, txt13 = create_button(win, Point(10, 60 + (idx * 40)), Point(300, 100 + (idx * 40)), str(vfile + '    ' + str(vdata)), "#4682B4", "white",size=9)
                idx+=1
                buttons.append((idload, btn, txt13))            
           
        return buttons, back_button

def dataset_selector( win_width=screen_width, win_height=screen_height):
    from Dashboard import create_dashboard
    """
    Opens a separate window to let the user select a file from `folder_name`.
    Returns the full path to the selected file, or raises FileNotFoundError if folder/files are missing.
    """
    
    
    win = GraphWin("Dataset Selector", win_width, win_height)
    win.setBackground("#2c2855")
    
    while True:        
        buttons, back_button= draw_dataset(win)
        click = win.getMouse()
         
        if is_click_in_rectangle(click, back_button):
            create_dashboard()  # Go back to the dashboard            
        else:            
            for idload, btn, txt13 in buttons:            
                if is_click_in_rectangle(click, btn):  
                    setDataset(idload)              
                    win.close()
                    return idload,txt13.getText()
