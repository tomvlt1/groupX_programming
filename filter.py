from graphics import *
from Globals import is_click_in_rectangle, create_label, create_button, create_scrollable_dropdown
from DataFunctions import openconnection
import pandas as pd

def get_headers():
    conn = None
    cursor = None
    try:
        conn = openconnection()
        cursor = conn.cursor()
        cursor.execute("SHOW COLUMNS FROM `DataDetail`")
        headers = [row[0] for row in cursor.fetchall()]
        return headers[1:]  # Exclude first column if you don't need it
    except Exception as e:
        print(f"Error fetching headers: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_column_datatype(column_name):
    conn = None
    cursor = None
    try:
        conn = openconnection()
        cursor = conn.cursor()
        query = f"SELECT `{column_name}` FROM `DataDetail` WHERE `{column_name}` IS NOT NULL LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            if isinstance(result[0], (int, float)):
                return "numerical"
            else:
                return "text"
    except Exception as e:
        print(f"Error determining datatype for column {column_name}: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return "text"

def get_unique_values(column_name):
    conn = None
    cursor = None
    try:
        conn = openconnection()
        cursor = conn.cursor()
        query = f"SELECT DISTINCT `{column_name}` FROM `DataDetail`"
        cursor.execute(query)
        results = cursor.fetchall()
        return [row[0] for row in results if row[0] is not None]
    except Exception as e:
        print(f"Error fetching unique values: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_operators_for_column(column_name):
    """
    Removed 'LIKE' operator as requested. Only basic operators remain.
    """
    datatype = get_column_datatype(column_name)
    if datatype == "numerical":
        return ["=", ">", "<", ">=", "<="]
    else:
        return ["="]  # For text columns, only '='

def filter_data_from_db(filters=None, columns=None, order_by_column=None, order_by_direction=None, is_unique=False):
    conn = None
    cursor = None
    try:
        conn = openconnection()
        cursor = conn.cursor()

        # If no columns selected, select all columns
        if not columns or len(columns) == 0:
            column_str = "*"
        else:
            column_str = ", ".join(f"`{col}`" for col in columns)

        # If user wants unique rows, use DISTINCT
        select_clause = "DISTINCT" if is_unique else ""

        query = f"SELECT {select_clause} {column_str} FROM `DataDetail`"
        if filters:
            conditions = []
            for (col, op, val) in filters:
                conditions.append(f"`{col}` {op} '{val}'")
            query += " WHERE " + " AND ".join(conditions)

        # Add ORDER BY if user selected a column and direction
        if order_by_column and order_by_direction:
            query += f" ORDER BY `{order_by_column}` {order_by_direction}"

        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        return pd.DataFrame(results, columns=column_names)

    except Exception as e:
        print(f"Error occurred: {e}")
        return pd.DataFrame()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def build_filters_page(win):
    title = Text(Point(450, 40), "Add Filters (Football Theme)")
    title.setSize(16)
    title.setTextColor("white")
    title.setStyle("bold")
    title.draw(win)

    instructions = Text(Point(450, 70), "Add as many filters as you want, then click Next Step.\nThis will get you to the column selection page.")
    instructions.setSize(12)
    instructions.setTextColor("white")
    instructions.draw(win)

    available_columns = get_headers()
    applied_filters = []

    filters_display = Text(Point(450, 280), "No filters yet.")
    filters_display.setSize(12)
    filters_display.setTextColor("white")
    filters_display.draw(win)

    col_label = Text(Point(290, 120), "Column:")
    op_label  = Text(Point(290, 160), "Operator:")
    val_label = Text(Point(290, 200), "Value:")
    for lbl in (col_label, op_label, val_label):
        lbl.setSize(12)
        lbl.setTextColor("white")
        lbl.draw(win)

    col_box = Rectangle(Point(340, 105), Point(520, 135))
    op_box  = Rectangle(Point(340, 145), Point(520, 175))
    val_box = Rectangle(Point(340, 185), Point(520, 215))
    for box in (col_box, op_box, val_box):
        box.setFill("white")
        box.setOutline("white")
        box.draw(win)

    col_text = Text(Point(430, 120), "Select column")
    col_text.setSize(10)
    col_text.setTextColor("black")
    col_text.draw(win)

    op_text = Text(Point(430, 160), "Select operator")
    op_text.setSize(10)
    op_text.setTextColor("black")
    op_text.draw(win)

    val_text = Text(Point(430, 200), "Select value")
    val_text.setSize(10)
    val_text.setTextColor("black")
    val_text.draw(win)

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

        # Column Box
        if 340 <= x <= 520 and 105 <= y <= 135:
            selected_col = create_scrollable_dropdown(win, "", available_columns, Point(430,120))
            col_text.setText(selected_col if selected_col else "Select column")
            selected_op = None
            selected_val = None
            op_text.setText("Select operator")
            val_text.setText("Select value")

        # Operator Box
        if 340 <= x <= 520 and 145 <= y <= 175 and selected_col:
            operators = get_operators_for_column(selected_col)
            selected_op = create_scrollable_dropdown(win, "", operators, Point(430,160))
            op_text.setText(selected_op if selected_op else "Select operator")
            selected_val = None
            val_text.setText("Select value")

        # Value Box
        if 340 <= x <= 520 and 185 <= y <= 215 and selected_col and selected_op:
            unique_vals = get_unique_values(selected_col)
            selected_val = create_scrollable_dropdown(win, "", unique_vals, Point(430,200))
            val_text.setText(str(selected_val) if selected_val else "Select value")

        # Add Filter
        if 540 <= x <= 640 and 105 <= y <= 135:
            if selected_col and selected_op and selected_val is not None:
                applied_filters.append((selected_col, selected_op, selected_val))
                filters_str = [f"{c} {o} '{v}'" for (c, o, v) in applied_filters]
                filters_display.setText(" AND\n".join(filters_str))
                selected_col = None
                selected_op = None
                selected_val = None
                col_text.setText("Select column")
                op_text.setText("Select operator")
                val_text.setText("Select value")

        # Next Step
        if 540 <= x <= 640 and 145 <= y <= 175:
            return applied_filters

        # Clear All
        if 540 <= x <= 640 and 185 <= y <= 215:
            applied_filters.clear()
            filters_display.setText("No filters yet.")
            selected_col = None
            selected_op = None
            selected_val = None
            col_text.setText("Select column")
            op_text.setText("Select operator")
            val_text.setText("Select value")

def build_columns_page(win, filters):
    for item in win.items[:]:
        item.undraw()
    win.items.clear()

    sidebar_color = color_rgb(31, 27, 58)
    sidebar = Rectangle(Point(0,0), Point(200,500))
    sidebar.setFill(sidebar_color)
    sidebar.setOutline(sidebar_color)
    sidebar.draw(win)

    title = Text(Point(450, 40), "Select Columns to Display")
    title.setSize(16)
    title.setTextColor("white")
    title.setStyle("bold")
    title.draw(win)

    instructions = Text(Point(450, 70), "Add columns, then click Submit.\nIf none selected, all columns will be displayed.")
    instructions.setSize(12)
    instructions.setTextColor("white")
    instructions.draw(win)

    back_btn, back_txt = create_button(
        win, Point(20,20), Point(180,60), "Back",
        fill_color=color_rgb(28,195,170), text_color="white", vout="grey", size=12
    )
    submit_btn, submit_txt = create_button(
        win, Point(20,80), Point(180,120), "Submit",
        fill_color=color_rgb(28,195,170), text_color="white", vout="grey", size=12
    )

    available_columns = get_headers()
    selected_columns = []
    columns_display = Text(Point(450, 280), "No columns selected.")
    columns_display.setSize(12)
    columns_display.setTextColor("white")
    columns_display.draw(win)

    col_label = Text(Point(290, 140), "Display Column:")
    col_label.setSize(12)
    col_label.setTextColor("white")
    col_label.draw(win)

    disp_box = Rectangle(Point(340,125), Point(520,155))
    disp_box.setFill("white")
    disp_box.setOutline("white")
    disp_box.draw(win)

    disp_text = Text(Point(430,140), "Select column")
    disp_text.setSize(10)
    disp_text.setTextColor("black")
    disp_text.draw(win)

    add_col_btn, add_col_txt = create_button(
        win, Point(540,125), Point(640,155), "Add Column",
        fill_color=color_rgb(28,195,170), text_color="white", vout="grey", size=12
    )

    # --- New UI for Order By (column dropdown + direction dropdown + button) ---
    order_by_label = Text(Point(750, 140), "Order By:")
    order_by_label.setSize(12)
    order_by_label.setTextColor("white")
    order_by_label.draw(win)

    order_box = Rectangle(Point(700,125), Point(880,155))
    order_box.setFill("white")
    order_box.setOutline("white")
    order_box.draw(win)

    order_text = Text(Point(790,140), "Select column")
    order_text.setSize(10)
    order_text.setTextColor("black")
    order_text.draw(win)

    direction_label = Text(Point(750, 200), "Direction:")
    direction_label.setSize(12)
    direction_label.setTextColor("white")
    direction_label.draw(win)

    direction_box = Rectangle(Point(700,185), Point(880,215))
    direction_box.setFill("white")
    direction_box.setOutline("white")
    direction_box.draw(win)

    direction_text = Text(Point(790,200), "ASC / DESC")
    direction_text.setSize(10)
    direction_text.setTextColor("black")
    direction_text.draw(win)

    order_btn, order_btn_txt = create_button(
        win, Point(700,230), Point(880,260), "Apply Sort",
        fill_color=color_rgb(28,195,170), text_color="white", vout="grey", size=12
    )
    # ---------------------------------------------------------------------------

    # --- New unique feature (checkbox-like toggle) ---
    unique_label = Text(Point(450, 330), "Toggle Unique Rows:")
    unique_label.setSize(12)
    unique_label.setTextColor("white")
    unique_label.draw(win)

    # Simple toggle button
    unique_btn, unique_btn_txt = create_button(
        win, Point(390,350), Point(510,380), "Unique OFF",
        fill_color=color_rgb(100, 100, 100), text_color="white", vout="grey", size=12
    )
    is_unique = False
    # -------------------------------------------------

    selected_col = None
    order_by_col = None
    order_by_dir = None

    while True:
        click = win.getMouse()
        if click is None:
            continue
        x, y = click.getX(), click.getY()

        # Back to filters
        if 20 <= x <= 180 and 20 <= y <= 60:
            return None

        # Submit
        if 20 <= x <= 180 and 80 <= y <= 120:
            df = filter_data_from_db(
                filters=filters,
                columns=selected_columns if selected_columns else None,
                order_by_column=order_by_col,
                order_by_direction=order_by_dir,
                is_unique=is_unique
            )
            return df

        # Display column box
        if 340 <= x <= 520 and 125 <= y <= 155:
            selected_col = create_scrollable_dropdown(win, "", available_columns, Point(430,140))
            disp_text.setText(selected_col if selected_col else "Select column")

        # Add Column
        if 540 <= x <= 640 and 125 <= y <= 155 and selected_col:
            if selected_col not in selected_columns:
                selected_columns.append(selected_col)
                columns_display.setText(", ".join(selected_columns))
            selected_col = None
            disp_text.setText("Select column")

        # Order By column box
        if 700 <= x <= 880 and 125 <= y <= 155:
            order_by_col = create_scrollable_dropdown(win, "", available_columns, Point(790,140))
            order_text.setText(order_by_col if order_by_col else "Select column")

        # Direction box
        if 700 <= x <= 880 and 185 <= y <= 215:
            direction_options = ["ASC", "DESC"]
            order_by_dir = create_scrollable_dropdown(win, "", direction_options, Point(790,200))
            direction_text.setText(order_by_dir if order_by_dir else "ASC / DESC")

        # Apply Sort button
        if 700 <= x <= 880 and 230 <= y <= 260:
            if order_by_col and order_by_dir:
                # Change button color and text
                order_btn.setFill(color_rgb(0, 200, 0))  # Change to green
                order_btn_txt.setText("Sort Applied")

                # Pause briefly to show the effect
                win.update()  # Force immediate redraw
                time.sleep(1)

                # Reset button to original state
                order_btn.setFill(color_rgb(28, 195, 170))  # Original color
                order_btn_txt.setText("Apply Sort")

        # Toggle Unique Rows button
        if 390 <= x <= 510 and 350 <= y <= 380:
            is_unique = not is_unique
            if is_unique:
                unique_btn_txt.setText("Unique ON")
                unique_btn.setFill(color_rgb(28,195,170))
            else:
                unique_btn_txt.setText("Unique OFF")
                unique_btn.setFill(color_rgb(100,100,100))

def build_2_page_ui():
    win = GraphWin("Football Data Filtering", 900, 500)
    bg_color = color_rgb(44, 40, 85)
    win.setBackground(bg_color)

    sidebar_color = color_rgb(31, 27, 58)
    sidebar = Rectangle(Point(0,0), Point(200,500))
    sidebar.setFill(sidebar_color)
    sidebar.setOutline(sidebar_color)
    sidebar.draw(win)

    # Page 1: Filters
    filters = build_filters_page(win)
    if filters is None:
        return pd.DataFrame()

    # Page 2: Columns
    while True:
        df = build_columns_page(win, filters)
        if df is None:
            # User clicked back => re-draw filter page
            for item in win.items[:]:
                item.undraw()
            win.items.clear()
            sidebar = Rectangle(Point(0,0), Point(200,500))
            sidebar.setFill(sidebar_color)
            sidebar.setOutline(sidebar_color)
            sidebar.draw(win)
            filters = build_filters_page(win)
        else:
            win.close()
            df.to_csv("temp_data.csv", index=False)
            return "temp_data.csv"

def main():
    final_df = build_2_page_ui()
    # Once the user finishes the 2-page filter UI, we then call PostFilter.py

    from PostFilter import GraphOptions
    selected_option = GraphOptions()
    return "Data returned to main()", selected_option

if __name__ == "__main__":
    final_df, selected_option = main()
    print("\nData returned to main():")
    print(final_df)
    print(f"Post-Filter Option: {selected_option}")
