from graphics import *
from Globals import is_click_in_rectangle, create_label, create_button, create_scrollable_dropdown
from DataFunctions import openconnection
import pandas as pd
import time

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

def filter_data_from_db(filters=None, columns=None,
                        order_by_column=None, order_by_direction=None,
                        unique_column=None):
    """
    Modifies the query to apply DISTINCT on the specified unique_column, if any.
    """
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

        # If a unique column is specified, use DISTINCT on that column.
        if unique_column:
            select_clause = f"DISTINCT `{unique_column}`"
            if column_str != "*":
                select_clause += f", {column_str}"
        else:
            select_clause = column_str

        if select_clause.strip().startswith(","):
            select_clause = select_clause.lstrip(",")

        query = f"SELECT {select_clause} FROM `DataDetail`"

        if filters:
            conditions = []
            for (col, op, val) in filters:
                conditions.append(f"`{col}` {op} '{val}'")
            query += " WHERE " + " AND ".join(conditions)

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
    # Use create_label with vcolor param
    title = create_label(win, "Add Filters (Football Theme)", Point(450, 40), size=16, vcolor="white", style="bold")
    instructions = create_label(
        win,
        "Add as many filters as you want, then click Next Step.\nThis will get you to the column selection page.",
        Point(450, 70),
        size=12,
        vcolor="white"
    )

    available_columns = get_headers()
    applied_filters = []

    filters_display = create_label(win, "No filters yet.", Point(450, 280), size=12, vcolor="white")

    col_label = create_label(win, "Column:", Point(290, 120), size=12, vcolor="white")
    op_label  = create_label(win, "Operator:", Point(290, 160), size=12, vcolor="white")
    val_label = create_label(win, "Value:", Point(290, 200), size=12, vcolor="white")

    col_box = Rectangle(Point(340, 105), Point(520, 135))
    op_box  = Rectangle(Point(340, 145), Point(520, 175))
    val_box = Rectangle(Point(340, 185), Point(520, 215))
    for box in (col_box, op_box, val_box):
        box.setFill("white")
        box.setOutline("white")
        box.draw(win)

    col_text = create_label(win, "Select column", Point(430, 120), size=10, vcolor="black")
    op_text = create_label(win, "Select operator", Point(430, 160), size=10, vcolor="black")
    val_text = create_label(win, "Select value", Point(430, 200), size=10, vcolor="black")

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

        # Column Box
        if is_click_in_rectangle(click, Rectangle(Point(340,105), Point(520,135))):
            selected_col = create_scrollable_dropdown(win, "", available_columns, Point(430,120))
            col_text.setText(selected_col if selected_col else "Select column")
            selected_op = None
            selected_val = None
            op_text.setText("Select operator")
            val_text.setText("Select value")

        # Operator Box
        if is_click_in_rectangle(click, Rectangle(Point(340,145), Point(520,175))) and selected_col:
            operators = get_operators_for_column(selected_col)
            selected_op = create_scrollable_dropdown(win, "", operators, Point(430,160))
            op_text.setText(selected_op if selected_op else "Select operator")
            selected_val = None
            val_text.setText("Select value")

        # Value Box
        if is_click_in_rectangle(click, Rectangle(Point(340,185), Point(520,215))) and selected_col and selected_op:
            unique_vals = get_unique_values(selected_col)
            selected_val = create_scrollable_dropdown(win, "", unique_vals, Point(430,200))
            val_text.setText(str(selected_val) if selected_val else "Select value")

        # Add Filter
        if is_click_in_rectangle(click, Rectangle(Point(540,105), Point(640,135))):
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
        if is_click_in_rectangle(click, Rectangle(Point(540,145), Point(640,175))):
            return applied_filters

        # Clear All
        if is_click_in_rectangle(click, Rectangle(Point(540,185), Point(640,215))):
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

    title = create_label(win, "Select Columns to Display", Point(450, 40), size=16, vcolor="white", style="bold")
    instructions = create_label(
        win, "Add columns, then click Submit.\nIf none selected, all columns will be displayed.",
        Point(450, 70), size=12, vcolor="white"
    )

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
    columns_display = create_label(win, "No columns selected.", Point(450, 280), size=12, vcolor="white")

    col_label = create_label(win, "Display Column:", Point(290, 140), size=12, vcolor="white")

    disp_box = Rectangle(Point(340,125), Point(520,155))
    disp_box.setFill("white")
    disp_box.setOutline("white")
    disp_box.draw(win)

    disp_text = create_label(win, "Select column", Point(430,140), size=10, vcolor="black")

    add_col_btn, add_col_txt = create_button(
        win, Point(540,125), Point(640,155), "Add Column",
        fill_color=color_rgb(28,195,170), text_color="white", vout="grey", size=12
    )

    # --- Order By UI ---
    order_by_label = create_label(win, "Order By:", Point(750, 140), size=12, vcolor="white")

    order_box = Rectangle(Point(700,125), Point(880,155))
    order_box.setFill("white")
    order_box.setOutline("white")
    order_box.draw(win)

    order_text = create_label(win, "Select column", Point(790,140), size=10, vcolor="black")

    direction_label = create_label(win, "Direction:", Point(750, 200), size=12, vcolor="white")

    direction_box = Rectangle(Point(700,185), Point(880,215))
    direction_box.setFill("white")
    direction_box.setOutline("white")
    direction_box.draw(win)

    direction_text = create_label(win, "ASC / DESC", Point(790,200), size=10, vcolor="black")

    order_btn, order_btn_txt = create_button(
        win, Point(700,230), Point(880,260), "Apply Sort",
        fill_color=color_rgb(28,195,170), text_color="white", vout="grey", size=12
    )

    # --- Unique Feature ---
    unique_label = create_label(win, "Select Unique Column:", Point(450, 330), size=12, vcolor="white")

    unique_box = Rectangle(Point(340,350), Point(520,380))
    unique_box.setFill("white")
    unique_box.setOutline("white")
    unique_box.draw(win)

    unique_text = create_label(win, "Select column", Point(430,365), size=10, vcolor="black")

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

        # Back to filters
        if is_click_in_rectangle(click, Rectangle(Point(20,20), Point(180,60))):
            return None

        # Submit
        if is_click_in_rectangle(click, Rectangle(Point(20,80), Point(180,120))):
            df = filter_data_from_db(
                filters=filters,
                columns=selected_columns if selected_columns else None,
                order_by_column=order_by_col,
                order_by_direction=order_by_dir,
                unique_column=unique_column if is_unique else None
            )
            return df

        # Display column box
        if is_click_in_rectangle(click, Rectangle(Point(340,125), Point(520,155))):
            selected_col = create_scrollable_dropdown(win, "", available_columns, Point(430,140))
            disp_text.setText(selected_col if selected_col else "Select column")

        # Add Column
        if is_click_in_rectangle(click, Rectangle(Point(540,125), Point(640,155))):
            if selected_col and (selected_col not in selected_columns):
                selected_columns.append(selected_col)
                columns_display.setText(", ".join(selected_columns))
            selected_col = None
            disp_text.setText("Select column")

        # Order By column box
        if is_click_in_rectangle(click, Rectangle(Point(700,125), Point(880,155))):
            order_by_col = create_scrollable_dropdown(win, "", available_columns, Point(790,140))
            order_text.setText(order_by_col if order_by_col else "Select column")

        # Direction box
        if is_click_in_rectangle(click, Rectangle(Point(700,185), Point(880,215))):
            direction_options = ["ASC", "DESC"]
            order_by_dir = create_scrollable_dropdown(win, "", direction_options, Point(790,200))
            direction_text.setText(order_by_dir if order_by_dir else "ASC / DESC")

        # Apply Sort button
        if is_click_in_rectangle(click, Rectangle(Point(700,230), Point(880,260))):
            if order_by_col and order_by_dir:
                order_btn.setFill(color_rgb(0, 200, 0))
                order_btn_txt.setText("Sort Applied")
                win.update()
                time.sleep(1)
                order_btn.setFill(color_rgb(28,195,170))
                order_btn_txt.setText("Apply Sort")

        # Unique Column dropdown
        if is_click_in_rectangle(click, Rectangle(Point(340,350), Point(520,380))):
            unique_column = create_scrollable_dropdown(win, "", available_columns, Point(430,365))
            unique_text.setText(unique_column if unique_column else "Select column")

        # Unique On/Off button
        if is_click_in_rectangle(click, Rectangle(Point(540,350), Point(640,380))):
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
    from PostFilter import GraphOptions
    selected_option = GraphOptions()
    return "Data returned to main()", selected_option

if __name__ == "__main__":
    final_df, selected_option = main()
    print("\nData returned to main():")
    print(final_df)
    print(f"Post-Filter Option: {selected_option}")
