from graphics import *
from Globals import *
from DataFunctions import get_headers,get_operators_for_column,get_unique_values,filter_data_from_db
import pandas as pd

(screen_width, screen_height, screen_widthHome, screen_heightHome)=screen()
(colorblueBac, colorvlueButtons, colorvlueButtons1, colorgreen, colorcream)=color()

def build_filters_page(win):
    from Dashboard import create_dashboard  #imported here to avoid circular references
    
    back_button, vim = create_image_button(win, Point(0, 0), Point(80, 50), "images/back3.png",size=(20, 20), vout=colorblueBac)    
    title = create_label(win, "Add Filters (Football Theme)",Point(450, 40), 16, colorcream, "bold")
    vtestinstruction="Add as many filters as you want, then click Next Step.\nThis will get you to the column selection page."
    instructions =create_label(win, vtestinstruction,Point(450, 70), 12, colorcream, "normal")

    available_columns = get_headers()
    applied_filters = []
    #We recover if we had something saved and we come from another window
    
    vfilter=getFilters()
    if not vfilter:
         filters_str="No filters yet."
    else:
        applied_filters=vfilter
        filters_str = [f"{c} {o} '{v}'" for (c, o, v) in applied_filters]
        filters_display_text=" AND\n".join(filters_str)
        
    filters_display  =create_label(win,  filters_str,Point(450, 280), 12, colorcream, "normal")
    

    col_label =create_label(win,"Column:",Point(290, 120), 12, colorcream, "normal")
    op_label =create_label(win,"Operator:",Point(290, 160), 12, colorcream, "normal")
    val_label =create_label(win,"Value:",Point(290, 200), 12, colorcream, "normal")
    
    col_box, col_text = create_button(win, Point(340, 105), Point(520, 135), "Select column", "white", "black",10)   
    op_box , op_text = create_button(win, Point(340, 145), Point(520, 175), "Select operator", "white", "black",10)   
    val_box , val_text = create_button(win,Point(340, 185), Point(520, 215), "Select value", "white", "black",10)   

    selected_col = None
    selected_op  = None
    selected_val = None

    add_filter_btn, add_filter_txt = create_button(
        win, Point(540, 105), Point(640, 135), "Add Filter",
        fill_color=color_rgb(28,195,170), text_color="white", vout="grey", size=12
    )
    next_step_btn, next_step_txt = create_button(
        win, Point(540, 145), Point(640, 175), "Next Step",
        fill_color=color_rgb(0,128,255), text_color="white", vout="grey", size=12
    )
    clear_filters_btn, clear_filters_txt = create_button(
        win, Point(540, 185), Point(640, 215), "Clear All",
        fill_color=color_rgb(200, 128, 0), text_color="white", vout="grey", size=12
    )

    while True:
        click = win.getMouse()
        if click is None:
            continue

        x, y = click.getX(), click.getY()

        if is_click_in_rectangle(click, col_box):
            selected_col = create_scrollable_dropdown(win, "", available_columns, Point(430,120))
            col_text.setText(selected_col if selected_col else "Select column")
            selected_op = None
            selected_val = None
            op_text.setText("Select operator")
            val_text.setText("Select value")

        if is_click_in_rectangle(click, op_box):
            operators = get_operators_for_column(selected_col)
            selected_op = create_scrollable_dropdown(win, "", operators, Point(430,160))
            op_text.setText(selected_op if selected_op else "Select operator")
            selected_val = None
            val_text.setText("Select value")

        if is_click_in_rectangle(click, val_box) and selected_col and selected_op:
            unique_vals = get_unique_values(selected_col)
            selected_val = create_scrollable_dropdown(win, "", unique_vals, Point(430,200))
            val_text.setText(str(selected_val) if selected_val else "Select value")

        if  is_click_in_rectangle(click, add_filter_btn):
            
            if selected_col and selected_op and selected_val is not None:
                
                applied_filters.append((selected_col, selected_op, selected_val))
                filters_str = [f"{c} {o} '{v}'" for (c, o, v) in applied_filters]
                filters_display_text=" AND\n".join(filters_str)
                filters_display.undraw()                
                filters_display  =create_label(win, filters_display_text,Point(450, 280), 12, colorcream, "normal")
                setFilters(applied_filters)
                selected_col = None
                selected_op = None
                selected_val = None
                col_text.setText("Select column")
                op_text.setText("Select operator")
                val_text.setText("Select value")

        elif is_click_in_rectangle(click, next_step_btn):
            return applied_filters

        elif  is_click_in_rectangle(click, clear_filters_btn):
            applied_filters.clear()
            setFilters(None)
            filters_display.setText("No filters yet.")
            selected_col = None
            selected_op = None
            selected_val = None
            col_text.setText("Select column")
            op_text.setText("Select operator")
            val_text.setText("Select value")
            
        elif is_click_in_rectangle(click, back_button):
            create_dashboard()  #bo back to the dashboard
       

def build_columns_page(win, filters):
    
    for item in win.items[:]:
        item.undraw()
    win.items.clear()

    sidebar_color = color_rgb(31, 27, 58)
    sidebar = Rectangle(Point(0,0), Point(200,500))
    sidebar.setFill(sidebar_color)
    sidebar.setOutline(sidebar_color)
    sidebar.draw(win)
    
    title = create_label(win, "Select Columns to Display",Point(450, 40), 16, colorcream, "bold")
    vtestinstruction="Add columns, then click Submit. "
    vtestinstruction1="If you select no columns, all columns will be displayed."
    instructions =create_label(win, vtestinstruction,Point(450, 70), 12, colorcream, "normal")
    instructions1 =create_label(win, vtestinstruction1,Point(450, 100), 12, colorcream, "normal")

    back_button, vim = create_image_button(win, Point(0, 0), Point(80, 50), "images/back3.png",size=(20, 20), vout=colorblueBac)    

    submit_btn, submit_txt = create_button(
        win, Point(20,80), Point(180,120), "Submit",
        fill_color=color_rgb(28,195,170), text_color="white", vout="grey", size=12
    )

    available_columns = get_headers()
    selected_columns = []
    columns_display =create_label(win, "No columns selected.",Point(450, 280), 12, colorcream, "normal")
    col_label = create_label(win, "Display Column:",Point(290, 140), 12, colorcream, "normal")

    disp_box, disp_text = create_button(win,Point(340,125), Point(520,155), "Select column", "white", "black",10)   
   

    add_col_btn, add_col_txt = create_button(
        win, Point(540,125), Point(640,155), "Add Column",
        fill_color=color_rgb(28,195,170), text_color="white", vout="grey", size=12
    )

    # --- Order By UI ---
    order_by_label = create_label(win, "Order By:", Point(750, 140), size=12, vcolor="white")
    order_box,order_text=create_button(win,Point(700,125), Point(880,155), "Select column", "white", "black",10)   
    
    direction_label = create_label(win, "Direction:", Point(750, 200), size=12, vcolor="white")
    direction_box,direction_text=create_button(win,Point(700,185), Point(880,215), "ASC / DESC", "white", "black",10)   
   
    order_btn, order_btn_txt = create_button(
        win, Point(700,230), Point(880,260), "Apply Sort",
        fill_color=color_rgb(28,195,170), text_color="white", vout="grey", size=12
    )

    # --- Unique Feature ---
    unique_label = create_label(win, "Select Unique Column:", Point(450, 330), size=12, vcolor="white")
    
    unique_box,unique_text=create_button(win,Point(340,350), Point(520,380), "Select column", "white", "black",10)   
   
    unique_btn, unique_btn_txt = create_button(
        win, Point(540,350), Point(640,380), "Unique OFF",
        fill_color=color_rgb(100, 100, 100), text_color="white", vout="grey", size=12
    )
    unique_column = None
    is_unique = False

    order_by_col = None
    order_by_dir = None
    selected_col = None


    while True:
        click = win.getMouse()
        if click is None:
            continue        
        
        if is_click_in_rectangle(click, back_button):
            build_2_page_ui()  
    
        elif is_click_in_rectangle(click, submit_btn):  
            df = filter_data_from_db(
                filters=filters,
                columns=selected_columns if selected_columns else None,
                order_by_column=order_by_col,
                order_by_direction=order_by_dir,
                unique_column=unique_column if is_unique else None
            )
            return df
            
       
        elif is_click_in_rectangle(click, disp_box): 
            selected_col = create_scrollable_dropdown(win, "", available_columns, Point(430,140))
            disp_text.setText(selected_col if selected_col else "Select column")
       
        elif is_click_in_rectangle(click, add_col_btn):  
            if not selected_columns:
                selected_columns.append(selected_col)
                columns_display.undraw()
                columns_display =create_label(win, selected_col,Point(450, 280), 12, colorcream, "normal")
            else:
                selected_columns.append(selected_col)
                columns_display.undraw()
                columns_display_text=", ".join(selected_columns)
                columns_display =create_label(win, columns_display_text,Point(450, 280), 12, colorcream, "normal")
           
            selected_col = None
            disp_text.setText("Select column")
            
        
        if is_click_in_rectangle(click, order_box):
            order_by_col = create_scrollable_dropdown(win, "", available_columns, Point(790,140))
            order_text.setText(order_by_col if order_by_col else "Select column")

       
        if is_click_in_rectangle(click, direction_box):
            direction_options = ["ASC", "DESC"]
            order_by_dir = create_scrollable_dropdown(win, "", direction_options, Point(790,200))
            direction_text.setText(order_by_dir if order_by_dir else "ASC / DESC")

       
        if is_click_in_rectangle(click, order_btn):
            if order_by_col and order_by_dir:
                order_btn.setFill(color_rgb(0, 200, 0))
                order_btn_txt.setText("Sort Applied")
                win.update()
                time.sleep(1)
                order_btn.setFill(color_rgb(28,195,170))
                order_btn_txt.setText("Apply Sort")

      
        if is_click_in_rectangle(click, unique_box):
            unique_column = create_scrollable_dropdown(win, "", available_columns, Point(430,365))
            unique_text.setText(unique_column if unique_column else "Select column")

       
        if is_click_in_rectangle(click, unique_btn):
            if unique_column:
                is_unique = not is_unique
                if is_unique:
                    unique_btn_txt.setText(f"Unique ON ({unique_column})")
                    unique_btn.setFill(color_rgb(28,195,170))
                else:
                    unique_btn_txt.setText("Unique OFF")
                    unique_btn.setFill(color_rgb(100,100,100))
            else:
                alert_text = create_label(win, "Select a column for uniqueness!", Point(450, 430), size=10, vcolor="red")
                win.update()
                time.sleep(2)
                alert_text.undraw()


def build_2_page_ui():
    
    oldwin = getCurrentWindow()
    if oldwin:
        oldwin.close()

    win = GraphWin("Football Data Filtering",  screen_width, screen_height)
    setCurrentWindow(win)
   
    bg_color = color_rgb(44, 40, 85)
    win.setBackground(bg_color)

    sidebar_color = color_rgb(31, 27, 58)
    sidebar = Rectangle(Point(0,0), Point(200,500))
    sidebar.setFill(sidebar_color)
    sidebar.setOutline(sidebar_color)
    sidebar.draw(win)
    
    back_button, vim = create_image_button(win, Point(0, 0), Point(80, 50), "images/back3.png",size=(20, 20), vout=colorblueBac)    

   
   
    filters = build_filters_page(win)
    if filters is None:
        #win.close()
        return pd.DataFrame()

   
    while True:
        
        df = build_columns_page(win, filters)
        if df is None:
            # user clicked back => re-draw filter page
            for item in win.items[:]:
                item.undraw()
            win.items.clear()
            sidebar = Rectangle(Point(0,0), Point(200,500))
            sidebar.setFill(sidebar_color)
            sidebar.setOutline(sidebar_color)
            sidebar.draw(win)
            filters = build_filters_page(win)
 
        else:
            # We got final dataframe or user closed
            win.close()
            df.to_csv("temp_data.csv", index=False)
            return "temp_data.csv"


def main():
    final_df = build_2_page_ui()
    from PostFilter import GraphOptions   
    selected_option = GraphOptions()       # This will open the "Variable to Graph" / "Graph to Variable" window

    return "Data returned to main()", selected_option
if __name__ == "__main__":
    final_df, selected_option = main()
    print("\nData returned to main():")
    print(final_df)
    print(f"Post-Filter Option: {selected_option}")